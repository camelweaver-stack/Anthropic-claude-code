/* West FW Living — chat concierge widget (vanilla JS, no dependencies).
   Floating button bottom-right; opens a chat panel that talks to
   /.netlify/functions/concierge. When a visitor shares an email address, the
   contact info is also submitted to the existing FormSubmit lead endpoint. */
(function () {
  "use strict";
  if (window.__wflConcierge) return;
  window.__wflConcierge = true;

  var GREEN = "#2F6B4F", WHEAT = "#D9A441", INK = "#182019", BG = "#F7F5EF";
  var ENDPOINT = "/.netlify/functions/concierge";
  var FORM_ENDPOINT = "https://formsubmit.co/ajax/leads@anastasiaweaver.com";
  var EMAIL_RE = /[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}/;
  var USER_CAP = 25;

  var messages = [];       // {role, content} sent to the function
  var userCount = 0;
  var leadSent = false;
  var busy = false;

  // ---- styles ----
  var css =
    "#wfl-cc-btn{position:fixed;right:20px;bottom:20px;z-index:2147483000;background:" + GREEN +
      ";color:#fff;border:none;border-radius:999px;padding:13px 20px;font:600 15px 'Instrument Sans',system-ui,sans-serif;" +
      "box-shadow:0 6px 20px rgba(24,32,25,.28);cursor:pointer;display:flex;align-items:center;gap:8px}" +
    "#wfl-cc-btn:hover{background:#234C39}" +
    "#wfl-cc-btn .dot{width:9px;height:9px;border-radius:50%;background:" + WHEAT + "}" +
    "#wfl-cc-panel{position:fixed;right:20px;bottom:78px;z-index:2147483000;width:360px;max-width:calc(100vw - 32px);" +
      "height:520px;max-height:calc(100vh - 110px);background:" + BG + ";border:1.5px solid " + GREEN +
      ";border-radius:14px;box-shadow:0 12px 40px rgba(24,32,25,.32);display:none;flex-direction:column;overflow:hidden;" +
      "font-family:'Instrument Sans',system-ui,sans-serif;color:" + INK + "}" +
    "#wfl-cc-panel.open{display:flex}" +
    "#wfl-cc-head{background:" + GREEN + ";color:#fff;padding:13px 16px;display:flex;align-items:center;justify-content:space-between}" +
    "#wfl-cc-head b{font-family:'Fraunces',serif;font-weight:700;font-size:1.02rem}" +
    "#wfl-cc-head small{display:block;font-size:.66rem;letter-spacing:.1em;text-transform:uppercase;opacity:.85}" +
    "#wfl-cc-close{background:none;border:none;color:#fff;font-size:22px;line-height:1;cursor:pointer;padding:0 4px}" +
    "#wfl-cc-log{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10px}" +
    ".wfl-cc-msg{max-width:84%;padding:9px 13px;border-radius:13px;font-size:14.5px;line-height:1.5;white-space:pre-wrap;word-wrap:break-word}" +
    ".wfl-cc-bot{align-self:flex-start;background:#fff;border:1px solid #E1E5DD}" +
    ".wfl-cc-me{align-self:flex-end;background:" + GREEN + ";color:#fff}" +
    ".wfl-cc-typing{align-self:flex-start;color:#4C564E;font-size:14px;font-style:italic}" +
    "#wfl-cc-form{display:flex;gap:8px;padding:11px;border-top:1.5px solid #E1E5DD;background:" + BG + "}" +
    "#wfl-cc-input{flex:1;border:1.5px solid #C9CFC6;border-radius:9px;padding:9px 11px;font:15px 'Instrument Sans',system-ui,sans-serif;background:#fff;color:" + INK + "}" +
    "#wfl-cc-input:focus{outline:3px solid " + WHEAT + ";outline-offset:1px}" +
    "#wfl-cc-send{background:" + GREEN + ";color:#fff;border:none;border-radius:9px;padding:0 15px;font:600 15px 'Instrument Sans',system-ui,sans-serif;cursor:pointer}" +
    "#wfl-cc-send:disabled{opacity:.55;cursor:default}" +
    "@media(max-width:480px){#wfl-cc-panel{right:0;left:0;bottom:0;width:100%;max-width:100%;height:80vh;border-radius:14px 14px 0 0}}";
  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  // ---- elements ----
  var btn = document.createElement("button");
  btn.id = "wfl-cc-btn";
  btn.type = "button";
  btn.setAttribute("aria-label", "Ask about the area");
  btn.innerHTML = '<span class="dot"></span>Ask about the area';

  var panel = document.createElement("div");
  panel.id = "wfl-cc-panel";
  panel.setAttribute("role", "dialog");
  panel.setAttribute("aria-label", "West FW Living guide");
  panel.innerHTML =
    '<div id="wfl-cc-head"><span><b>West FW Living guide</b><small>Ask about the area</small></span>' +
    '<button id="wfl-cc-close" type="button" aria-label="Close">&times;</button></div>' +
    '<div id="wfl-cc-log"></div>' +
    '<form id="wfl-cc-form" autocomplete="off">' +
    '<input id="wfl-cc-input" type="text" placeholder="Ask about renting, buying, schools…" aria-label="Your message" maxlength="600">' +
    '<button id="wfl-cc-send" type="submit">Send</button></form>';

  document.body.appendChild(btn);
  document.body.appendChild(panel);

  var log = panel.querySelector("#wfl-cc-log");
  var form = panel.querySelector("#wfl-cc-form");
  var input = panel.querySelector("#wfl-cc-input");
  var sendBtn = panel.querySelector("#wfl-cc-send");
  var greeted = false;

  function addMsg(role, text) {
    var el = document.createElement("div");
    el.className = "wfl-cc-msg " + (role === "me" ? "wfl-cc-me" : "wfl-cc-bot");
    el.textContent = text; // escape: textContent, never innerHTML
    log.appendChild(el);
    log.scrollTop = log.scrollHeight;
    return el;
  }

  function openPanel() {
    panel.classList.add("open");
    if (!greeted) {
      greeted = true;
      addMsg("bot", "Hi! I'm the West FW Living guide. Ask me anything about renting, buying, or living in west Fort Worth.");
    }
    setTimeout(function () { input.focus(); }, 60);
  }
  function closePanel() { panel.classList.remove("open"); }

  btn.addEventListener("click", function () {
    panel.classList.contains("open") ? closePanel() : openPanel();
  });
  panel.querySelector("#wfl-cc-close").addEventListener("click", closePanel);

  function transcriptText() {
    return messages.slice(-10).map(function (m) {
      return (m.role === "assistant" ? "Guide" : "Visitor") + ": " + m.content;
    }).join("\n");
  }

  // Submit contact info to the existing FormSubmit lead pipe (source=concierge).
  function submitLead(email) {
    if (leadSent) return;
    leadSent = true;
    // Look back through the visitor's turns for a name and a phone number.
    var joined = messages.filter(function (m) { return m.role === "user"; })
      .map(function (m) { return m.content; }).join(" ");
    var phoneMatch = joined.match(/(\+?1[\s.\-]?)?\(?\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}/);
    var payload = {
      name: "Concierge lead",
      email: email,
      phone: phoneMatch ? phoneMatch[0] : "",
      source: "concierge",
      message: transcriptText(),
      _subject: "Website lead — West FW Living (Concierge)",
    };
    fetch(FORM_ENDPOINT, {
      method: "POST",
      headers: { "content-type": "application/json", accept: "application/json" },
      body: JSON.stringify(payload),
    }).catch(function () { /* non-blocking: stay in chat */ });
  }

  function typing() {
    var t = document.createElement("div");
    t.className = "wfl-cc-typing";
    t.textContent = "typing…";
    log.appendChild(t);
    log.scrollTop = log.scrollHeight;
    return t;
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (busy) return;
    var text = input.value.trim();
    if (!text) return;

    input.value = "";
    addMsg("me", text);
    messages.push({ role: "user", content: text });
    userCount++;

    // Fire the lead capture as soon as the visitor shares an email.
    var em = text.match(EMAIL_RE);
    if (em) submitLead(em[0]);

    if (userCount > USER_CAP) {
      addMsg("bot", "Best next step — grab the guide that fits you on the site, or leave your email and we'll follow up.");
      messages.push({ role: "assistant", content: "Best next step — grab the guide that fits you on the site, or leave your email and we'll follow up." });
      return;
    }

    busy = true;
    sendBtn.disabled = true;
    var t = typing();

    fetch(ENDPOINT, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ messages: messages }),
    })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        t.remove();
        var reply = (data && data.reply) ? data.reply : "Sorry — I hit a snag. Try again?";
        addMsg("bot", reply);
        messages.push({ role: "assistant", content: reply });
      })
      .catch(function () {
        t.remove();
        addMsg("bot", "Sorry — I hit a snag. Try again in a moment?");
      })
      .then(function () {
        busy = false;
        sendBtn.disabled = false;
        input.focus();
      });
  });
})();
