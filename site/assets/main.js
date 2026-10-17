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

// Home hero slider: rotates every 6s on its own; only the Pause button stops it.
(function () {
  var root = document.querySelector(".hero-slider");
  if (!root) return;
  var slides = root.querySelectorAll(".slide");
  var dots = root.querySelectorAll(".slider-dots button");
  var pauseBtn = root.querySelector(".slider-pause");
  var MS = 6000, i = 0, timer = null;
  var userPaused = false;
  root.style.setProperty("--slide-ms", MS + "ms");

  function show(n) {
    i = (n + slides.length) % slides.length;
    slides.forEach(function (s, k) {
      var on = k === i;
      s.classList.toggle("is-active", on);
      if (on) { s.removeAttribute("aria-hidden"); s.removeAttribute("inert"); }
      else { s.setAttribute("aria-hidden", "true"); s.setAttribute("inert", ""); }
    });
    // clear, force a reflow, then set: restarts the progress bar animation
    dots.forEach(function (d) { d.removeAttribute("aria-current"); });
    void root.offsetWidth;
    dots[i].setAttribute("aria-current", "true");
    restart();
  }
  function stop() { clearTimeout(timer); timer = null; }
  function restart() { stop(); if (!userPaused) timer = setTimeout(function () { show(i + 1); }, MS); }
  function setPaused(p) {
    userPaused = p;
    root.classList.toggle("paused", p);
    pauseBtn.textContent = p ? "Play" : "Pause";
    pauseBtn.setAttribute("aria-label", p ? "Resume rotation" : "Pause rotation");
    restart();
  }
  root.querySelectorAll(".slider-arrow").forEach(function (b) {
    b.addEventListener("click", function () { show(i + Number(b.dataset.dir)); });
  });
  dots.forEach(function (d, k) { d.addEventListener("click", function () { show(k); }); });
  pauseBtn.addEventListener("click", function () { setPaused(!userPaused); });

  // swipe on phones
  var x0 = null;
  root.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  root.addEventListener("touchend", function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 50) show(i + (dx < 0 ? 1 : -1));
  });

  setPaused(userPaused);
})();
