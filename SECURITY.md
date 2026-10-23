# Security Policy

## Reporting a Vulnerability

Please **do not** open a public issue for security problems — for example a plugin that gets
around NtfyBar's permission sandbox, leaks message data, or a way to install files that don't
match their published checksums.

Use GitHub's private vulnerability reporting instead (**Security → Report a vulnerability** on
this repository, or on [NtfyBar](https://github.com/roypadina/NtfyBar) for problems in the app's
plugin runtime).

You'll get an acknowledgement within a few days. Once a fix is available it will be released
and the report disclosed, with credit unless you prefer otherwise.

## Scope

This repository holds plugin code (`plugins/`), the marketplace index (`marketplace.json`) and its
checks. The sandbox itself — the JavaScript runtime, permission enforcement, checksum verification
and installer — lives in the NtfyBar app.
