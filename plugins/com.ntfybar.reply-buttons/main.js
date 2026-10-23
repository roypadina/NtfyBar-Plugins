// Reply Buttons: turn a message into a question. Each button "Label=reply" publishes its reply text
// to the topic picked in the rule — e.g. a Home Assistant automation listening on that topic.

function parseButtons(params) {
  var out = [];
  ["button1", "button2", "button3"].forEach(function (key, i) {
    var raw = String(params[key] || "");
    var eq = raw.indexOf("=");
    if (eq <= 0 || eq === raw.length - 1) return;
    out.push({ id: "b" + (i + 1), label: raw.slice(0, eq).trim().slice(0, 40), reply: raw.slice(eq + 1).trim().slice(0, 1000) });
  });
  return out;
}

function showButtons(ctx, params) {
  var buttons = parseButtons(params);
  if (!buttons.length || !params.topic) return undefined;
  var m = ctx.message;
  return {
    popup: {
      title: m.title || ctx.topic.label,
      icon: "arrowshape.turn.up.left.2",
      accent: m.priority >= 4 ? "warning" : "info",
      blocks: m.message ? [{ text: m.message }] : [],
      buttons: buttons.map(function (b) { return { id: b.id, label: b.label }; }),
      state: { topic: params.topic, replies: buttons.reduce(function (o, b) { o[b.id] = b.reply; return o; }, {}) }
    }
  };
}

function onPopupAction(ctx, buttonId, state) {
  var reply = state && state.replies && state.replies[buttonId];
  if (reply && ntfy.publish) {
    ntfy.publish({ topicId: state.topic, title: "Reply: " + (ctx.message.title || ctx.topic.label), message: reply, priority: 3 });
  }
  return { close: true };
}
