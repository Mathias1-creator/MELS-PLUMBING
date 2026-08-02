/* ==========================================================================
   MELS PLUMBING — main.js
   Vanilla JS only. No libraries, no build step.
   Modules: mobile nav · scroll reveal · stat counters · FAQ accordion · lightbox
   Every motion path checks prefers-reduced-motion before animating.
   ========================================================================== */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ------------------------------------------------------------------
     Mobile navigation
     ------------------------------------------------------------------ */
  (function mobileNav() {
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.getElementById("primary-nav");
    if (!toggle || !nav) return;

    function close() {
      nav.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    }

    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      nav.classList.toggle("is-open", !open);
      toggle.setAttribute("aria-expanded", open ? "false" : "true");
    });

    // Close when a link is chosen
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) close();
    });

    // Close on Escape, and return focus to the button
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        close();
        toggle.focus();
      }
    });

    // Reset state when leaving the mobile breakpoint
    var mq = window.matchMedia("(min-width: 901px)");
    var onChange = function (e) { if (e.matches) close(); };
    if (mq.addEventListener) mq.addEventListener("change", onChange);
    else if (mq.addListener) mq.addListener(onChange);
  })();

  /* ------------------------------------------------------------------
     Scroll reveal — fade + 20px rise on section entry
     ------------------------------------------------------------------ */
  (function scrollReveal() {
    var items = document.querySelectorAll(".reveal");
    if (!items.length) return;

    if (reduceMotion || !("IntersectionObserver" in window)) {
      Array.prototype.forEach.call(items, function (el) { el.classList.add("is-visible"); });
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -10% 0px", threshold: 0.12 });

    Array.prototype.forEach.call(items, function (el) { observer.observe(el); });
  })();

  /* ------------------------------------------------------------------
     Stat counters — animate once when the band scrolls into view
     ------------------------------------------------------------------ */
  (function statCounters() {
    var counters = document.querySelectorAll("[data-count-to]");
    if (!counters.length) return;

    function render(el, value) {
      var prefix = el.getAttribute("data-prefix") || "";
      var suffix = el.getAttribute("data-suffix") || "";
      el.textContent = prefix + value + suffix;
    }

    function run(el) {
      var target = parseInt(el.getAttribute("data-count-to"), 10);
      if (isNaN(target)) return;

      if (reduceMotion) { render(el, target); return; }

      var duration = 1500;
      var start = null;

      function step(timestamp) {
        if (start === null) start = timestamp;
        var progress = Math.min((timestamp - start) / duration, 1);
        // easeOutCubic — fast start, gentle landing
        var eased = 1 - Math.pow(1 - progress, 3);
        render(el, Math.round(target * eased));
        if (progress < 1) window.requestAnimationFrame(step);
        else render(el, target);
      }

      window.requestAnimationFrame(step);
    }

    if (!("IntersectionObserver" in window)) {
      Array.prototype.forEach.call(counters, function (el) {
        render(el, parseInt(el.getAttribute("data-count-to"), 10));
      });
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          run(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    Array.prototype.forEach.call(counters, function (el) {
      render(el, 0);
      observer.observe(el);
    });
  })();

  /* ------------------------------------------------------------------
     FAQ accordion — one panel open at a time, animated height, ARIA kept in sync
     ------------------------------------------------------------------ */
  (function accordion() {
    var triggers = document.querySelectorAll(".faq__trigger");
    if (!triggers.length) return;

    function collapse(trigger) {
      var panel = document.getElementById(trigger.getAttribute("aria-controls"));
      if (!panel) return;
      trigger.setAttribute("aria-expanded", "false");
      // Lock the current pixel height first so the transition has somewhere to go from
      panel.style.height = panel.scrollHeight + "px";
      // Force reflow before dropping to 0
      void panel.offsetHeight;
      panel.style.height = "0px";
    }

    function expand(trigger) {
      var panel = document.getElementById(trigger.getAttribute("aria-controls"));
      if (!panel) return;
      trigger.setAttribute("aria-expanded", "true");
      panel.style.height = panel.scrollHeight + "px";
      // After the transition, release to auto so the panel reflows on resize
      var done = function (e) {
        if (e.propertyName !== "height") return;
        panel.style.height = "auto";
        panel.removeEventListener("transitionend", done);
      };
      if (reduceMotion) panel.style.height = "auto";
      else panel.addEventListener("transitionend", done);
    }

    Array.prototype.forEach.call(triggers, function (trigger) {
      trigger.addEventListener("click", function () {
        var isOpen = trigger.getAttribute("aria-expanded") === "true";

        // Close whichever one is open
        Array.prototype.forEach.call(triggers, function (other) {
          if (other.getAttribute("aria-expanded") === "true") collapse(other);
        });

        if (!isOpen) expand(trigger);
      });
    });
  })();

  /* ------------------------------------------------------------------
     Gallery lightbox — click to open, prev/next, ESC / overlay click to close.
     Focus is trapped while open and restored to the trigger on close.
     ------------------------------------------------------------------ */
  (function lightbox() {
    var box = document.getElementById("lightbox");
    var triggers = document.querySelectorAll("[data-lightbox]");
    if (!box || !triggers.length) return;

    var img = box.querySelector(".lightbox__img");
    var caption = box.querySelector(".lightbox__caption");
    var btnClose = box.querySelector(".lightbox__close");
    var btnPrev = box.querySelector(".lightbox__prev");
    var btnNext = box.querySelector(".lightbox__next");
    var slides = Array.prototype.map.call(triggers, function (t) {
      var thumb = t.querySelector("img");
      return {
        src: t.getAttribute("data-lightbox"),
        alt: thumb ? thumb.getAttribute("alt") : "",
      };
    });

    var index = 0;
    var lastFocused = null;

    function show(i) {
      index = (i + slides.length) % slides.length;
      var slide = slides[index];
      img.setAttribute("src", slide.src);
      img.setAttribute("alt", slide.alt);
      caption.textContent = "Image " + (index + 1) + " of " + slides.length + " — " + slide.alt;
    }

    function open(i, trigger) {
      lastFocused = trigger || document.activeElement;
      show(i);
      box.classList.add("is-open");
      box.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
      btnClose.focus();
      document.addEventListener("keydown", onKeydown);
    }

    function close() {
      box.classList.remove("is-open");
      box.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
      document.removeEventListener("keydown", onKeydown);
      if (lastFocused && lastFocused.focus) lastFocused.focus();
    }

    function onKeydown(e) {
      if (e.key === "Escape") { close(); return; }
      if (e.key === "ArrowLeft") { show(index - 1); return; }
      if (e.key === "ArrowRight") { show(index + 1); return; }
      if (e.key !== "Tab") return;

      // Keep Tab inside the dialog
      var focusables = [btnClose, btnPrev, btnNext];
      var first = focusables[0];
      var last = focusables[focusables.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }

    Array.prototype.forEach.call(triggers, function (trigger, i) {
      trigger.addEventListener("click", function () { open(i, trigger); });
    });

    btnClose.addEventListener("click", close);
    btnPrev.addEventListener("click", function () { show(index - 1); });
    btnNext.addEventListener("click", function () { show(index + 1); });

    // Click on the backdrop (but not the image itself) closes
    box.addEventListener("click", function (e) {
      if (e.target === box || e.target.classList.contains("lightbox__figure")) close();
    });
  })();

  /* ------------------------------------------------------------------
     Current year in the footer
     ------------------------------------------------------------------ */
  (function currentYear() {
    var slots = document.querySelectorAll("[data-year]");
    var year = new Date().getFullYear();
    Array.prototype.forEach.call(slots, function (el) { el.textContent = year; });
  })();
})();
