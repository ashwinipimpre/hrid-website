// Mobile menu
(function () {
  var btn = document.querySelector(".menu-btn");
  var nav = document.getElementById("site-nav");
  if (!btn || !nav) return;
  btn.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    btn.textContent = open ? "Close" : "Menu";
  });
})();

// Forms: sent to Netlify Forms on the live site (they arrive in the Netlify dashboard and by email).
(function () {
  var live = /(^|\.)hriddigitalgroup\.com$|\.netlify\.app$/.test(location.hostname);
  document.querySelectorAll("form.site-form").forEach(function (form) {
    var status = form.querySelector(".form-status");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var btn = form.querySelector("button[type=submit]");
      var say = function (msg, ok) {
        status.textContent = msg;
        status.className = "form-status " + (ok ? "ok" : "err");
      };
      if (!live) {
        say("Preview only: this form starts sending once the site is live on hriddigitalgroup.com.", true);
        return;
      }
      btn.disabled = true;
      var data = new URLSearchParams(new FormData(form)).toString();
      fetch("/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: data })
        .then(function (r) {
          if (!r.ok) throw new Error(r.status);
          form.reset();
          say(form.dataset.success || "Thanks! We will get back to you within one working day.", true);
        })
        .catch(function () {
          say("Your message could not be sent. Please email info@hriddigitalgroup.com or WhatsApp +91 94041 26138.", false);
        })
        .finally(function () { btn.disabled = false; });
    });
  });
})();
