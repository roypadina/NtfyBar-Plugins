# Popup spec

With the `ui` permission, an action can return `{popup: spec}`. NtfyBar draws it with its own
native popup — the same floating panel as built-in alerts — and labels it with the topic and the
plugin's name. Plugins never get a web view.

```js
return {
  popup: {
    title: "Deploy finished",          // required, ≤200 characters
    icon: "checkmark.seal",            // optional SF Symbol name
    accent: "success",                 // info (default) | success | warning | critical
    timeoutSec: 30,                    // optional, 0–600; 0 or missing = stays until dismissed
    blocks: [
      { text: "Build **#482** is live." },          // markdown, ≤4096 characters
      { kv: [["Branch", "main"], ["Took", "3 m 12 s"]] },  // table, ≤50 rows
      { progress: 0.75, label: "Rollout 75 %" },    // 0–1
      { badge: "Production" }                       // ≤40 characters
    ],
    buttons: [                         // up to 3
      { id: "ok", label: "Got it", style: "prominent" },   // default | prominent | destructive
      { id: "rollback", label: "Roll back", style: "destructive" }
    ],
    state: { build: 482 }              // any JSON ≤64 KB, handed back to onPopupAction
  }
};
```

Rules:

- Unknown keys are ignored, so newer specs still load in older NtfyBar versions.
- Wrong types, out-of-range values or too many blocks/buttons make the whole popup an error
  (logged; nothing is shown).
- At most 20 blocks. A block with no known key is skipped.
- Button `id`: letters, digits, `_` and `-`, ≤40 characters, unique within the popup. Labels ≤40.
- NtfyBar always adds a **Dismiss** button. **Return** presses your `prominent` button; if you
  marked none, Return presses Dismiss — a popup that just appeared never fires one of your
  buttons by accident.
- Markdown links in text blocks open only if they are http/https.

## Buttons

When the user presses one of your buttons, NtfyBar calls:

```js
function onPopupAction(ctx, buttonId, state) {
  // ctx: the message that triggered the popup; state: what you returned in the spec
  if (buttonId === "ok") return { close: true };
  return { popup: { title: "Are you sure?", buttons: [{ id: "yes", label: "Yes" }], state: state } };
}
```

Return `undefined` or `{close: true}` to close the popup, or `{popup: spec}` to replace its
content in place. Without an `onPopupAction` function, every button just closes the popup.

## Example

[`plugins/com.ntfybar.ack-button`](../plugins/com.ntfybar.ack-button) shows a popup with an ACK
button and publishes a reply when it is pressed.
