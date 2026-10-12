/* Ensō Foot Clinic — interface behaviour. No dependencies. */
(function () {
  "use strict";

  var $  = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function store(key, val) {
    try {
      if (val === undefined) return localStorage.getItem(key);
      localStorage.setItem(key, val);
    } catch (e) { return null; }
  }

  /* ── Header & drawer ───────────────────────────────────────────────── */
  function header() {
    var el = $(".header");
    if (!el) return;
    var onScroll = function () { el.classList.toggle("is-stuck", window.scrollY > 8); };
    onScroll();
    addEventListener("scroll", onScroll, { passive: true });

    var burger = $(".burger");
    var close = function () {
      document.body.classList.remove("nav-open");
      if (burger) burger.setAttribute("aria-expanded", "false");
    };
    if (burger) {
      burger.addEventListener("click", function () {
        var open = document.body.classList.toggle("nav-open");
        burger.setAttribute("aria-expanded", open);
      });
    }
    $$(".drawer a").forEach(function (a) { a.addEventListener("click", close); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("nav-open")) close();
    });
  }

  /* ── Reveal on scroll ──────────────────────────────────────────────── */
  function reveal() {
    var items = $$("[data-reveal]");
    if (!items.length) return;
    if (reduced || !("IntersectionObserver" in window)) {
      items.forEach(function (i) { i.classList.add("is-in"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var delay = +(en.target.getAttribute("data-reveal") || 0);
        setTimeout(function () { en.target.classList.add("is-in"); }, delay);
        io.unobserve(en.target);
      });
    }, { rootMargin: "0px 0px -12% 0px", threshold: 0.08 });
    items.forEach(function (i) { io.observe(i); });
    // Safety net: nothing stays hidden if the observer never fires for it.
    setTimeout(function () {
      items.forEach(function (i) {
        var r = i.getBoundingClientRect();
        if (r.top < innerHeight * 1.2) i.classList.add("is-in");
      });
    }, 1500);
  }

  /* ── Service comparison ────────────────────────────────────────────── */
  function compare() {
    var root = $("#compare");
    if (!root) return;
    $$(".filter", root).forEach(function (f) {
      f.addEventListener("click", function () {
        var val = f.getAttribute("data-filter");
        $$(".filter", root).forEach(function (o) { o.setAttribute("aria-pressed", o === f); });
        var shown = 0;
        $$("tbody tr", root).forEach(function (tr) {
          var ok = val === "all" || tr.getAttribute("data-invasive") === val;
          tr.hidden = !ok;
          if (ok) shown++;
        });
        var live = $("[data-compare-count]", root);
        if (live) live.textContent = shown + (shown === 1 ? " υπηρεσία" : " υπηρεσίες");
      });
    });
  }

  /* ── FAQ ───────────────────────────────────────────────────────────── */
  function faq() {
    $$(".faq__item").forEach(function (item) {
      var btn = $(".faq__q", item);
      var panel = $(".faq__a", item);
      btn.addEventListener("click", function () {
        var open = item.classList.toggle("is-open");
        btn.setAttribute("aria-expanded", open);
        panel.setAttribute("aria-hidden", !open);
        if (open && item.id) history.replaceState(null, "", "#" + item.id);
      });
    });
    if (location.hash) {
      var target = document.getElementById(location.hash.slice(1));
      if (target && target.classList.contains("faq__item")) {
        target.classList.add("is-open");
        $(".faq__q", target).setAttribute("aria-expanded", "true");
      }
    }
  }

  /* ── Long pages: TOC, scroll spy, reading progress ─────────────────── */
  function doc() {
    var bar = $(".progress");
    if (bar) {
      var onScroll = function () {
        var h = document.documentElement.scrollHeight - innerHeight;
        bar.style.transform = "scaleX(" + (h > 0 ? Math.min(1, scrollY / h) : 0) + ")";
      };
      onScroll();
      addEventListener("scroll", onScroll, { passive: true });
    }
    var toc = $(".toc");
    var prose = $(".prose");
    if (!toc || !prose) return;
    var heads = $$("h2, h3", prose).filter(function (h) { return h.textContent.trim().length > 2; });
    if (heads.length < 3) { var w = toc.closest("[data-toc-wrap]"); if (w) w.hidden = true; return; }
    heads.forEach(function (h, i) {
      if (!h.id) h.id = "s-" + (i + 1);
      var a = document.createElement("a");
      a.href = "#" + h.id;
      a.textContent = h.textContent;
      a.setAttribute("data-depth", h.tagName === "H3" ? "3" : "2");
      toc.appendChild(a);
    });
    if (!("IntersectionObserver" in window)) return;
    var links = $$("a", toc);
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (l) {
          l.classList.toggle("is-active", l.getAttribute("href") === "#" + en.target.id);
        });
      });
    }, { rootMargin: "-15% 0px -70% 0px" });
    heads.forEach(function (h) { spy.observe(h); });
  }

  /* ── Chrome: to-top, action bar ────────────────────────────────────── */
  function chrome() {
    var top = $(".totop"), bar = $(".actionbar");
    var onScroll = function () {
      top && top.classList.toggle("is-shown", scrollY > 600);
      bar && bar.classList.toggle("is-shown", scrollY > 320);
    };
    onScroll();
    addEventListener("scroll", onScroll, { passive: true });
    top && top.addEventListener("click", function () {
      scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" });
    });
  }

  /* ── Entry screen ──────────────────────────────────────────────────── */
  /* The homepage opens on the ring and ENTER. One tap anywhere (or Enter —
     the gate is a button and takes focus) fades it out. It is NOT shown again
     when the page is opened on an anchor (the menu's «Ποιοι είμαστε» points to
     /#poioi-eimaste) or when it has already been passed once in this browser
     session — otherwise the menu would loop back to the entry screen. */
  function gate() {
    var g = $(".gate");
    var root = document.documentElement;
    var seen = function (val) {
      try {
        if (val === undefined) return sessionStorage.getItem("enso-gate");
        sessionStorage.setItem("enso-gate", val);
      } catch (e) { return null; }
    };
    // Any other page counts as having entered the site: the logo or a
    // breadcrumb back to the homepage must not open on the entry screen.
    if (!g) { seen("1"); return; }
    if (location.hash || seen()) {
      g.remove();
      document.dispatchEvent(new Event("enso:gate"));
      return;
    }
    root.classList.add("gate-open");
    try { g.focus({ preventScroll: true }); } catch (e) {}
    var opened = false;
    function open() {
      if (opened) return;
      opened = true;
      seen("1");
      g.classList.add("is-leaving");
      root.classList.remove("gate-open");
      var done = function () {
        g.remove();
        document.dispatchEvent(new Event("enso:gate"));
      };
      if (reduced) done(); else setTimeout(done, 750);
    }
    g.addEventListener("click", open);
  }

  /* ── Cookie notice ─────────────────────────────────────────────────── */
  function cookies() {
    var box = $(".cookies");
    if (!box) return;
    if (store("enso-consent")) return;
    var show = function () { setTimeout(function () { box.classList.add("is-shown"); }, 900); };
    // Not on top of the entry screen: wait until it has been opened.
    if ($(".gate")) document.addEventListener("enso:gate", show, { once: true });
    else show();
    function save(value) {
      store("enso-consent", value);
      box.classList.remove("is-shown");
    }
    $("[data-cookie-accept]", box).addEventListener("click", function () {
      save($("#cookie-analytics", box).checked ? "all" : "necessary");
    });
    $("[data-cookie-reject]", box).addEventListener("click", function () { save("necessary"); });
  }

  function init() {
    gate(); header(); reveal(); compare(); faq(); doc(); chrome(); cookies();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
