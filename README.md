<div align="center">

<img src="https://raw.githubusercontent.com/roypadina/NtfyBar/main/docs/AppIcon-1024.png" width="128" alt="NtfyBar icon">

# NtfyBar Plugins

**The official plugin marketplace for [NtfyBar](https://github.com/roypadina/NtfyBar) — sandboxed JavaScript conditions, actions and popups for your ntfy notifications.**

[![Validate](https://github.com/roypadina/NtfyBar-Plugins/actions/workflows/validate.yml/badge.svg)](https://github.com/roypadina/NtfyBar-Plugins/actions/workflows/validate.yml)
[![Website](https://img.shields.io/badge/website-apps.roypadina-2F62E6)](https://apps.roypadina.synology.me/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-support-F16061?logo=ko-fi&logoColor=white)](https://ko-fi.com/roypadina)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](CONTRIBUTING.md)

</div>

NtfyBar is a macOS menu-bar client for [ntfy](https://ntfy.sh). Its rules can use conditions and
actions from plugins. Plugins run in a sandbox: they see only the message that triggered them, with
your topic names and server addresses hidden (best-effort — see [Limits of the sandbox](docs/permissions.md#limits-of-the-sandbox)), and they can only do what their declared permissions allow —
after you agreed.

## Requirements

- NtfyBar 1.0.0 or later (macOS 14 Sonoma or later, Apple Silicon and Intel).

## Install a plugin

In NtfyBar: **Settings › Plugins › Available › Refresh**, then **Install…** on a plugin. NtfyBar
downloads its files, checks every one against the SHA-256 in [`marketplace.json`](marketplace.json),
shows what the plugin will be able to do, and installs it only if you allow it. Then use it in a
rule under **Settings › Rules**.

## Plugins

| Plugin | What it does | Permissions |
|---|---|---|
| [Alert Card](plugins/com.ntfybar.alert-card) ⭐ | Big alert card with Acknowledge and Snooze, optional auto-dismiss, position choice and a times-today count. | ui, publish, storage |
| [Repeat & Burst](plugins/com.ntfybar.history-conditions) ⭐ | Conditions: "not seen recently" (calm flapping alerts) and "burst" (≥ N messages in M minutes). | history.read |
| [Extract](plugins/com.ntfybar.extract) ⭐ | Copy a regex match (codes, IPs) or open it in a link template (PR numbers). | clipboard.write, openURL |
| [JSON Fields](plugins/com.ntfybar.json-fields) ⭐ | Match JSON messages by a field's value or a change in it; show a JSON message as a table. | ui, history.read |
| [ACK Button](plugins/com.ntfybar.ack-button) ⭐ | Popup with an ACK button that replies to the topic the alert came from. | ui, publish, storage |
| [Time Window](plugins/com.ntfybar.time-window) | Condition: arrived between two times of day on chosen days. A zero-permission example. | — |
| [Reply Buttons](plugins/com.ntfybar.reply-buttons) | Popup with up to three buttons; each sends its own reply to a topic you pick (two-way home automation). | ui, publish |

⭐ = also ships inside NtfyBar (off until you enable it). Those update together with the app.

## Permissions at a glance

| Permission | Allows |
|---|---|
| *(always)* | Reading the message that triggered it, and that topic's label |
| `history.read` | Earlier messages of that topic |
| `topics.read` | Labels of all your topics |
| `publish` | Sending to your topics (10/min, quiet hours apply) |
| `clipboard.write` | Putting text on the clipboard |
| `openURL` | Opening http/https links |
| `storage` | Up to 1 MB of its own data |
| `ui` | Its own popups with buttons |

Never possible, with any permission: running commands, network access, reading the clipboard or
files, changing settings, subscribing to topics. Details: [docs/permissions.md](docs/permissions.md).

## Write your own

- [Authoring guide](docs/authoring.md) — manifest, JavaScript contract, trying it locally
- [Permissions](docs/permissions.md) — every API and what it may do
- [Popup spec](docs/popup-spec.md) — declarative popups and buttons
- [Publishing](docs/publishing.md) — getting a plugin into this marketplace

## Contributing

Pull requests with new plugins are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). Report security
problems privately: [SECURITY.md](SECURITY.md).

## More Mac apps by Roy

Free, open-source Mac menu-bar apps and terminal tools, all on one site: **[apps.roypadina.synology.me](https://apps.roypadina.synology.me/)**.

- [NtfyBar](https://apps.roypadina.synology.me/apps/ntfybar/) — ntfy notifications on your Mac: popups that stay, rules, commands, plugins.
- [MaccyPlus](https://apps.roypadina.synology.me/apps/maccyplus/) — Maccy, plus automation: rules, hotkeys, plugins and a CLI for AI agents.
- [MeetAlert](https://apps.roypadina.synology.me/apps/meetalert/) — Meeting alerts you can't miss: a popup that stays, a phone push that escalates.
- [LanGuard](https://apps.roypadina.synology.me/apps/languard/) — Wi-Fi off when you're wired. Back on when you're not.

## Support

NtfyBar and these plugins are free and open source. If they save you time, a coffee keeps the next one coming:

[![Support me on Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/roypadina)

## License

[MIT](LICENSE) © Roy Padina. Not affiliated with ntfy.
