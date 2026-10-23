#!/usr/bin/env python3
"""Checks marketplace.json against plugins/: every entry's folder, file list, permissions and
per-file SHA-256 must match. NtfyBar validates manifests itself on install; this catches
mismatches before a PR is merged.

Usage:
  scripts/validate.py                  check (CI)
  scripts/validate.py --update-hashes  rewrite the sha256 values in marketplace.json from plugins/
"""
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ID = re.compile(r"^[a-z0-9-]+(\.[a-z0-9-]+)+$")
SAFE_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")
PERMISSIONS = {"history.read", "topics.read", "publish", "clipboard.write", "openURL", "storage", "ui"}
MAX_FILE = 2 * 1024 * 1024
MAX_PACKAGE = 10 * 1024 * 1024


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    update = "--update-hashes" in sys.argv[1:]
    index_path = os.path.join(ROOT, "marketplace.json")
    index = json.load(open(index_path, encoding="utf-8"))
    errors = []
    seen = set()
    for entry in index.get("plugins", []):
        pid = entry.get("id", "")
        where = f"{pid or '<no id>'}:"
        if not ID.match(pid):
            errors.append(f"{where} id must be reverse-DNS, lowercase")
            continue
        if pid in seen:
            errors.append(f"{where} listed twice")
        seen.add(pid)
        src = entry.get("source", {})
        if src.get("type") != "github" or src.get("repo") != "roypadina/NtfyBar-Plugins" or src.get("ref") != "main" \
                or src.get("path") != f"plugins/{pid}":
            errors.append(f"{where} source must be github roypadina/NtfyBar-Plugins, ref main, path plugins/{pid}")
        folder = os.path.join(ROOT, "plugins", pid)
        manifest_path = os.path.join(folder, "plugin.json")
        if not os.path.isfile(manifest_path):
            errors.append(f"{where} plugins/{pid}/plugin.json is missing")
            continue
        try:
            manifest = json.load(open(manifest_path, encoding="utf-8"))
        except ValueError as e:
            errors.append(f"{where} plugin.json is not valid JSON: {e}")
            continue
        if manifest.get("id") != pid:
            errors.append(f"{where} plugin.json id differs from the folder / entry")
        if not 0 < len(str(manifest.get("description", ""))) <= 120:
            errors.append(f"{where} description is required, up to 120 characters")
        for prov in manifest.get("providers", []):
            if not str(prov.get("id", "")).startswith(pid + "."):
                errors.append(f"{where} provider id {prov.get('id')} must start with {pid}.")
            if not 0 < len(str(prov.get("description", ""))) <= 120:
                errors.append(f"{where} provider {prov.get('id')} description is required, up to 120 characters")
        for key in ("name", "version", "description"):
            if entry.get(key) != manifest.get(key):
                errors.append(f"{where} {key} differs between marketplace.json and plugin.json")
        perms = manifest.get("permissions", [])
        unknown = set(perms) - PERMISSIONS
        if unknown:
            errors.append(f"{where} unknown permissions {sorted(unknown)}")
        if set(entry.get("permissions", [])) != set(perms):
            errors.append(f"{where} permissions differ between marketplace.json and plugin.json")
        reasons = manifest.get("permissionReasons", {})
        for p in perms:
            if not str(reasons.get(p, "")).strip():
                errors.append(f"{where} permissionReasons needs a reason for {p}")
        listed = manifest.get("files", [])
        on_disk = sorted(n for n in os.listdir(folder) if not n.startswith("."))
        if sorted(listed) != on_disk:
            errors.append(f"{where} plugin.json files {sorted(listed)} != folder contents {on_disk}")
        for name in listed:
            if not SAFE_NAME.match(name) or name.startswith("."):
                errors.append(f"{where} unsafe file name {name}")
        total = sum(os.path.getsize(os.path.join(folder, n)) for n in listed if os.path.isfile(os.path.join(folder, n)))
        if total > MAX_PACKAGE:
            errors.append(f"{where} package is larger than 10 MB")
        if update:
            entry["files"] = {n: sha256(os.path.join(folder, n)) for n in sorted(listed) if os.path.isfile(os.path.join(folder, n))}
            continue
        hashes = entry.get("files", {})
        if sorted(hashes) != sorted(listed):
            errors.append(f"{where} marketplace files {sorted(hashes)} != plugin.json files {sorted(listed)}")
        for name, expected in hashes.items():
            path = os.path.join(folder, name)
            if not os.path.isfile(path):
                continue
            if os.path.getsize(path) > MAX_FILE:
                errors.append(f"{where} {name} is larger than 2 MB")
            if sha256(path) != str(expected).lower():
                errors.append(f"{where} {name} sha256 mismatch (run scripts/validate.py --update-hashes)")
    folders = {n for n in os.listdir(os.path.join(ROOT, "plugins")) if not n.startswith(".")}
    for extra in sorted(folders - seen):
        errors.append(f"plugins/{extra} is not listed in marketplace.json")
    if update:
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print("hashes updated")
        return 0
    for e in errors:
        print("error:", e)
    print(f"{len(index.get('plugins', []))} plugin(s) checked, {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
