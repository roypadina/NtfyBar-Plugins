# Permissions

Every plugin can read the message that triggered it (see `ctx` in [authoring.md](authoring.md)).
Anything more needs a permission. Permissions are:

- **declared** in `plugin.json`, each with a reason (`permissionReasons`);
- **shown** to the user before the plugin is enabled, and again when an update adds one;
- **enforced**: a method on the `ntfy` object only exists while its permission is granted, and
  every call checks the grant again. The user can switch single permissions off at any time.

Grants belong to one copy of a plugin: a local folder with the same id as an installed plugin
does not inherit its permissions.

| Permission | What the user sees | API |
|---|---|---|
| *(always)* | Read each message that triggers it — title, text, tags, links — and that topic's label. Never topic names, server addresses or your settings. | `ctx` |
| `history.read` | Read earlier messages of the topic that triggered it. | `ntfy.history(options)` |
| `topics.read` | See the labels of all your topics (and, with history access, their messages). | `ntfy.topics()` |
| `publish` | Send messages to your topics — at most 10 a minute, capped by quiet hours. | `ntfy.publish(message)` |
| `clipboard.write` | Put text on your clipboard. | `ntfy.copy(text)` |
| `openURL` | Open web links (http/https) in your browser — a link can carry message text to that site. | `ntfy.openURL(url)` |
| `storage` | Keep up to 1 MB of its own data on this Mac. | `ntfy.storage.get/set/remove` |
| `ui` | Show its own popups with buttons. | return `{popup: …}` |

## API

### `ntfy.history({topicId?, before?, after?, limit?})` — `history.read`

Returns messages (newest first) in the same shape as `ctx.message`.

- `topicId` omitted → the topic that triggered the call. Another topic also needs `topics.read`.
- `before` / `after`: unix seconds (exclusive).
- `limit`: default 50, at most 200.

### `ntfy.topics()` — `topics.read`

Returns `[{id, label}]` for every topic the user subscribes to.

### `ntfy.publish({topicId, message, title?, priority?, tags?, click?})` — `publish`

Sends a message to one of the user's topics (by `topicId`) and returns `true` when it was queued.
`message` is required (≤4096 characters); `priority` 1–5 (default 3), lowered during the user's
quiet hours; `tags` up to 10; `click` only if http/https. At most 10 publishes a minute per
plugin. Messages NtfyBar publishes come back on the stream like any other; NtfyBar recognises
its own and runs no rules on them.

### `ntfy.copy(text)` — `clipboard.write`

Replaces the clipboard with `text` (≤1 MB).

### `ntfy.openURL(url)` — `openURL`

Opens an http or https URL in the default browser — at most 10 a minute, and not while
notifications are paused. Anything else (`file:`, app schemes) fails. Note for users: a URL can
carry message text to the site it opens, so grant this only to plugins you trust.

### `ntfy.storage` — `storage`

- `ntfy.storage.get(key)` → the stored JSON value or `undefined`
- `ntfy.storage.set(key, value)` → `true`; fails when the plugin's data would exceed 1 MB
- `ntfy.storage.remove(key)` → `true`

Keys are strings of up to 200 characters; values are anything JSON can hold. Each plugin has its
own file; plugins can't read each other's data.

### Popups — `ui`

An action (or `onPopupAction`) may return `{popup: spec}`; see [popup-spec.md](popup-spec.md).
Without `ui` that return value is an error.

## What plugins can never do

There is no API, with any permission, to: run commands or Shortcuts, use the network, read the
clipboard or files, read or change settings and rules, subscribe or unsubscribe topics, or see
topic names, server addresses or credentials.

A failed call (permission missing or switched off, bad arguments) throws a JavaScript error.

## Limits of the sandbox

- **Redaction is best-effort.** NtfyBar replaces every topic name and server address it finds in
  the text it hands to a plugin. It can't recognise them if the sender encoded or split them, and a
  plugin with both `publish` and `history.read` could test guesses. Keep secrets out of message text.
- **Time:** 1 s per call and at most 5 s of JavaScript time per minute; beyond that the plugin is
  disabled until you reload plugins.
- **Memory:** JavaScriptCore has no per-plugin memory limit; a plugin can briefly use a lot of
  memory. Only install plugins you trust.
