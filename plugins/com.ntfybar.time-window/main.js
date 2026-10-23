// Time Window: a zero-permission example. Uses only the message time (local clock of this Mac).

function minutes(hhmm) {
  var m = /^(\d{1,2}):(\d{2})$/.exec(String(hhmm || "").trim());
  if (!m || Number(m[1]) > 23 || Number(m[2]) > 59) return null;
  return Number(m[1]) * 60 + Number(m[2]);
}

var DAYS = {
  "every-day": [0, 1, 2, 3, 4, 5, 6],
  "mon-fri": [1, 2, 3, 4, 5],
  "sun-thu": [0, 1, 2, 3, 4],
  "weekend-sat-sun": [6, 0],
  "weekend-fri-sat": [5, 6]
};

function within(ctx, params) {
  var from = minutes(params.from || "09:00");
  var to = minutes(params.to || "18:00");
  if (from === null || to === null || from === to) return false;
  var d = new Date(ctx.message.time * 1000);
  var t = d.getHours() * 60 + d.getMinutes();
  var days = DAYS[params.days || "every-day"] || DAYS["every-day"];
  // A window that crosses midnight belongs to the day it started on.
  var startDay = from > to && t < to ? (d.getDay() + 6) % 7 : d.getDay();
  if (days.indexOf(startDay) < 0) return false;
  return from < to ? t >= from && t < to : t >= from || t < to;
}
