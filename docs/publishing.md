# Publishing a plugin

Plugins in this repository show up in every NtfyBar under **Settings › Plugins › Available**.

1. Fork this repository.
2. Add your plugin as `plugins/<your plugin id>/` (folder name = `id` in `plugin.json`).
3. Add an entry to `marketplace.json`:

   ```json
   {
     "id": "com.example.my-plugin",
     "name": "My Plugin",
     "version": "1.0.0",
     "description": "Same text as in plugin.json.",
     "permissions": ["ui"],
     "source": {
       "type": "github",
       "repo": "roypadina/NtfyBar-Plugins",
       "ref": "main",
       "path": "plugins/com.example.my-plugin"
     },
     "files": {}
   }
   ```

4. Fill in the checksums and check everything:

   ```sh
   python3 scripts/validate.py --update-hashes
   python3 scripts/validate.py
   ```

5. Try it in NtfyBar from a local folder (see [authoring.md](authoring.md#try-it-locally)).
6. Open a pull request. CI runs `scripts/validate.py`; a maintainer reviews the code.

## How installs are verified

NtfyBar downloads exactly the files listed in your entry from this repository, checks each one
against its SHA-256 from `marketplace.json`, checks that the manifest matches the entry (same
id, files and permissions), and only then asks the user for consent and writes the plugin. If
any file differs, nothing is installed and an existing version stays as it was.

## Review rules

A plugin is accepted when:

- it asks for the fewest permissions it needs, and each reason says honestly why;
- the code is readable: no minified or obfuscated JavaScript, no encoded payloads;
- it doesn't try to get around the sandbox or to impersonate NtfyBar's own popups or settings;
- it does what its name and description say, and nothing else.

Updates: bump `version` in `plugin.json` and `marketplace.json`, re-run
`scripts/validate.py --update-hashes`. An update that adds a permission makes every user
confirm it again.

## Your own marketplace

A marketplace is any `marketplace.json` reachable over https in this format (with your own
`repo`). Users add it under **Settings › Plugins › Sources › Marketplaces**; its plugins are
marked **Unverified source**.
