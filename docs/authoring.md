# Writing an NtfyBar plugin

A plugin adds **conditions** (true/false checks) and **actions** (things to do) to NtfyBar's
rules. It is a folder with a `plugin.json` manifest and one JavaScript file. It runs in a
sandbox: it only sees the message that triggered it, and it can only do what its permissions
allow and the user agreed to.

## Folder layout

```
com.example.my-plugin/      ← folder name = plugin id
├── plugin.json
└── main.js
```

Files sit directly in the folder (no subfolders). Every file must be listed in `files`.

## plugin.json

```json
{
  "id": "com.example.my-plugin",
  "name": "My Plugin",
  "version": "1.0.0",
  "description": "One line, up to 120 characters.",
  "author": { "name": "Your Name", "url": "https://github.com/you" },
  "apiVersion": 1,
  "minAppVersion": "1.0.0",
  "entry": "main.js",
  "files": ["plugin.json", "main.js"],
  "permissions": ["ui"],
  "permissionReasons": { "ui": "Shows the build result in a popup." },
  "providers": [
    {
      "id": "com.example.my-plugin.failed-build",
      "kind": "condition",
      "name": "Build failed",
      "description": "The message reports a failed build.",
      "function": "isFailedBuild",
      "params": [{ "key": "branch", "label": "Branch", "kind": "text", "placeholder": "main" }]
    }
  ],
  "popup": { "engine": "declarative" }
}
```

| Field | Rules |
|---|---|
| `id` | Lowercase reverse-DNS (`com.example.name`), ≤100 characters. Equals the folder name. `com.ntfybar.*` is reserved for official plugins. |
| `name` | ≤60 characters. |
| `version` | Your version string, e.g. `1.2.0`. |
| `description` | Required, ≤120 characters. |
| `author` | Optional `{name, url}`. The name "NtfyBar" is reserved for official plugins. |
| `apiVersion` | `1`. |
| `minAppVersion` | Optional. Oldest NtfyBar version that can run the plugin. |
| `entry` | The JavaScript file NtfyBar runs. Must be listed in `files`. |
| `files` | Every file in the package, `plugin.json` included. Names: letters, digits, `_ . -`; no leading dot. |
| `permissions` | What the plugin may do beyond reading the triggering message. See [permissions.md](permissions.md). |
| `permissionReasons` | **Required** for every listed permission, ≤120 characters each. Shown to the user next to NtfyBar's own description. |
| `providers` | At least one. See below. |
| `popup` | Optional. `{"engine": "declarative"}` is the only engine today. |

Each provider:

| Field | Rules |
|---|---|
| `id` | Must start with your plugin id plus a dot. |
| `kind` | `condition` or `action`. |
| `name`, `description` | Shown in the rule editor. Description ≤120 characters. |
| `function` | Name of a global JavaScript function in `entry`. |
| `params` | Optional fields the user fills in per rule: `{key, label, kind, placeholder}`, `kind` = `text`, `number`, `bool`, `topic`, or (NtfyBar 1.1+) `choice` with `"choices": ["a", "b"]` (2–20 values of letters, digits, `_` or `-`; the rule gets the chosen value). |

A package with an invalid manifest is not loaded. A provider with a problem (bad id, missing
function, unknown param kind) is skipped on its own; the rest of the package still works. The
Plugins settings tab lists every problem.

## JavaScript

```js
// condition: return true or false
function isFailedBuild(ctx, params) {
  return /failed/i.test(ctx.message.title || "") && (!params.branch || ctx.message.message.indexOf(params.branch) >= 0);
}

// action: return undefined, or {popup: …} (needs the "ui" permission)
function showResult(ctx, params) {
  return { popup: { title: ctx.message.title, accent: "critical", blocks: [{ text: ctx.message.message }] } };
}

// optional: called when a button on one of your popups is pressed
function onPopupAction(ctx, buttonId, state) {
  return { close: true }; // or undefined (also closes), or {popup: …} to replace the popup
}
```

Any other return type is an error, logged as a provider error. A thrown exception is logged the
same way; NtfyBar and the rule's other steps keep running.

### `ctx`

```js
{
  message: {
    id, time,            // ntfy message id, unix seconds
    title, message,      // strings (title may be missing)
    priority,            // 1 (min) … 5 (urgent)
    tags,                // array of strings
    click, icon,         // URLs when present
    actions, attachment, // as ntfy sends them
    contentType,         // "text/markdown" for markdown messages
    isCatchUp            // true if it arrived while NtfyBar was offline
  },
  topic: { id, label }   // NtfyBar's id for the topic, and the user's label
}
```

Topic names and server addresses are hidden from plugins (best-effort): wherever one appears in a message (links,
action URLs, headers, bodies), it is replaced by `[topic]` or `[server]`.

### `params`

The values the user entered in the rule editor, keyed by `key`: strings, numbers, booleans;
`topic` params hold a topic id.

### The `ntfy` object

Each method exists **only while its permission is granted**. The user can switch single
permissions off at any time, so check before you call:

```js
if (ntfy.publish) ntfy.publish({ topicId: ctx.topic.id, message: "seen" });
```

The methods are described in [permissions.md](permissions.md).

### Environment

- Plain JavaScript (JavaScriptCore). Nothing else is defined: no `fetch`, `XMLHttpRequest`,
  `require`, timers, `process` or DOM.
- Every call into your plugin may run for **1 second**. A call that takes longer is stopped;
  after three stops the plugin is disabled until the user reloads plugins.
- Calls happen on NtfyBar's main thread — keep them short.
- Call `ntfy` methods inside your functions, not at the top level of the script.

## Try it locally

1. NtfyBar → **Settings › Plugins › Sources › Add Folder…** and pick your plugin folder (or a
   folder that contains several).
2. **Installed** → your plugin → **Review and Enable…**.
3. **Settings › Rules** → add a rule that uses your condition or action.
4. After editing files, press **Reload Plugins**.

Local plugins are marked **Unverified source**. Errors (bad manifest, skipped providers) show in
the Plugins tab; runtime errors from your functions are in the log:

```sh
/usr/bin/log show --last 10m --predicate 'subsystem == "com.padina.ntfybar" AND category == "plugins"'
```

## Limits

| What | Limit |
|---|---|
| One file | 2 MB |
| Whole package | 10 MB |
| One call | 1 s (3 timeouts → disabled until reload) |
| JavaScript time | 5 s per minute in total (more → disabled until reload) |
| `ntfy.openURL` | 10 per minute; nothing opens while notifications are paused |
| `ntfy.history` | 200 messages per call |
| `ntfy.publish` | 10 per minute per plugin; quiet hours cap the priority |
| `ntfy.storage` | 1 MB per plugin |
| `ntfy.copy` | 1 MB of text |
| Popup | 20 blocks, 3 buttons, text block 4 KB, 50 table rows, state 64 KB |

See also: [permissions.md](permissions.md) · [popup-spec.md](popup-spec.md) · [publishing.md](publishing.md)
