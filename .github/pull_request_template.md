## Plugin

<!-- Name, id, and what it does in one or two sentences. -->

## Permissions

<!-- Each permission and why it is needed. -->

## Checklist

- [ ] Folder is `plugins/<id>/`, and every file is listed in `plugin.json` `files`
- [ ] `python3 scripts/validate.py --update-hashes` then `python3 scripts/validate.py` pass
- [ ] Tried in NtfyBar from a local folder (Settings › Plugins › Sources)
- [ ] Fewest permissions needed; honest `permissionReasons`
- [ ] Readable JavaScript: nothing minified or obfuscated
