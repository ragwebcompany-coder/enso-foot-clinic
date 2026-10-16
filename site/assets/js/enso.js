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
    // Behind the entry screen nothing should play yet: the page builds itself
    // once the gate is opened, as the logo lands.
    if ($(".gate")) {
      document.addEventListener("enso:reveal", function () { start(items); }, { once: true });
      return;
    }
    start(items);
  }
  function start(items) {
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
      var flew = !reduced && fly(g);
      setTimeout(function () { document.dispatchEvent(new Event("enso:reveal")); }, flew ? 450 : 0);
      g.classList.add("is-leaving");
      root.classList.remove("gate-open");
      var done = function () {
        g.remove();
        document.dispatchEvent(new Event("enso:gate"));
      };
      if (reduced) done(); else setTimeout(done, flew ? 1150 : 750);
    }
    g.addEventListener("click", open);
    lean(g);
  }

  /* ENTER: the ring lifts off the entry screen and lands on the mark of the
     header logo, top left, spinning once on the way. A clone flies on top of
     everything; the gate fades behind it; the header logo is held invisible
     until the clone touches down, then the two cross-fade, so there is never a
     second copy of the mark on screen. The geometry is the two marks' own
     squares: the badge carries the mark inset 22/400 on every side, the header
     logo carries it at x 10–106 of a 396×96 viewBox. */
  function fly(g) {
    var src = $(".gate__mark", g), brand = $(".header .brand img");
    if (!src || !brand || !src.animate) return false;
    var a = src.getBoundingClientRect(), b = brand.getBoundingClientRect();
    if (!a.width || !b.width) return false;
    var inset = 22 / 400, markA = a.width * (1 - 2 * inset);
    var markB = b.height, bx = b.left + b.width * (10 / 396), by = b.top;
    var k = markB / markA;
    var dx = (bx + markB / 2) - (a.left + a.width / 2);
    var dy = (by + markB / 2) - (a.top + a.height / 2);

    var clone = src.cloneNode(true);
    clone.className = "gate-fly";
    clone.removeAttribute("fetchpriority");
    clone.style.cssText = "left:" + a.left + "px;top:" + a.top + "px;width:" + a.width +
      "px;height:" + a.height + "px";
    document.body.appendChild(clone);
    src.style.visibility = "hidden";
    document.documentElement.classList.add("brand-landing");

    var anim = clone.animate([
      { transform: "translate(0,0) scale(1) rotate(0deg)", opacity: 1, filter: "drop-shadow(0 0 0 rgba(69,179,232,0))" },
      { transform: "translate(" + dx * .55 + "px," + dy * .35 + "px) scale(" + (1 + (k - 1) * .5) + ") rotate(200deg)",
        opacity: 1, filter: "drop-shadow(0 0 28px rgba(69,179,232,.75))", offset: .55 },
      { transform: "translate(" + dx + "px," + dy + "px) scale(" + k + ") rotate(360deg)", opacity: 1,
        filter: "drop-shadow(0 0 6px rgba(69,179,232,.5))" }
    ], { duration: 1100, easing: "cubic-bezier(.65,0,.25,1)", fill: "forwards" });

    var landed = false;
    function land() {
      if (landed) return;
      landed = true;
      document.documentElement.classList.remove("brand-landing");
      document.documentElement.classList.add("brand-landed");
      clone.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 380, fill: "forwards" })
        .onfinish = function () { clone.remove(); };
      setTimeout(function () { document.documentElement.classList.remove("brand-landed"); }, 1400);
    }
    anim.onfinish = land;
    setTimeout(land, 1150);   // in case the finish event never arrives
    return true;
  }

  /* The ring leans towards the pointer, and a wash of the logo's aqua follows
     it. Only where there is a real pointer to follow: a touch screen has none,
     and the CSS gives it a slow float instead. Everything is written as custom
     properties on the gate, so if this never runs the ring simply sits still. */
  function lean(g) {
    if (reduced) return;
    if (!window.matchMedia("(hover: hover) and (pointer: fine)").matches) return;
    var VARS = ["--tilt-x", "--tilt-y", "--shift-x", "--shift-y"];
    g.addEventListener("pointermove", function (e) {
      if (e.pointerType === "touch") return;
      var nx = (e.clientX / window.innerWidth) * 2 - 1;
      var ny = (e.clientY / window.innerHeight) * 2 - 1;
      var st = g.style;
      st.setProperty("--tilt-y", (nx * 5).toFixed(2) + "deg");
      st.setProperty("--tilt-x", (-ny * 3.5).toFixed(2) + "deg");
      st.setProperty("--shift-x", (nx * 16).toFixed(1) + "px");
      st.setProperty("--shift-y", (ny * 11).toFixed(1) + "px");
      st.setProperty("--glow-x", (nx * 50 + 50).toFixed(1) + "%");
      st.setProperty("--glow-y", (ny * 50 + 50).toFixed(1) + "%");
      g.classList.add("is-pointing");
    }, { passive: true });
    g.addEventListener("pointerleave", function () {
      g.classList.remove("is-pointing");
      VARS.forEach(function (k) { g.style.removeProperty(k); });
    });
  }

  /* ── Futuristic layer ──────────────────────────────────────────────── */
  /* Everything here is decoration over a page that is complete without it:
     staggered blur-in reveals for every block, a light that follows the
     pointer around card edges, the motto set word by word, and a scroll
     velocity skew on the big headings. Off for reduced motion. */
  function futurist() {
    if (reduced) return;
    var SEL = [".sec-head", ".page-head .crumbs", ".page-head h1", ".page-head .lede",
      ".card", ".place", ".sem-card", ".mapcard", ".legal > div",
      ".faq__item", ".info-list > li", ".about__who > *", ".about__text > p",
      ".about__bio > *", ".prose > *", ".creds__list li", ".timeline li",
      ".disclaimer", ".motto__rule", ".footer__grid > *",
      ".checkout .fieldset", ".checkout .order"].join(",");
    $$(SEL).forEach(function (el) {
      // Legal text inside the checkout's scroll panels is read, not staged.
      if (el.hasAttribute("data-reveal") || el.closest(".gate") || el.closest(".fold")) return;
      var sib = 0, p = el.previousElementSibling;
      while (p && sib < 6) { if (p.matches(SEL)) sib++; p = p.previousElementSibling; }
      el.setAttribute("data-reveal", String(sib * 80));
      el.classList.add("fx-rise");
    });

    // The motto arrives word by word.
    $$(".motto__lead").forEach(function (h) {
      var words = h.textContent.trim().split(/\s+/);
      h.innerHTML = words.map(function (w, i) {
        return '<span class="fx-word" style="--i:' + i + '">' + w + "</span>";
      }).join(" ");
      h.setAttribute("data-reveal", "0");
    });

    // A light that follows the pointer along the edges of every card.
    if (window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
      $$(".card, .place, .sem-card, .mapcard, .legal, .faq__item, .btn")
        .forEach(function (el) {
          el.classList.add("fx-glow");
          el.addEventListener("pointermove", function (e) {
            var r = el.getBoundingClientRect();
            el.style.setProperty("--mx", (e.clientX - r.left) + "px");
            el.style.setProperty("--my", (e.clientY - r.top) + "px");
          }, { passive: true });
        });
    }

    // Big headings lean a touch into fast scrolling, then settle.
    var heads = $$("h1, .sec-head h2, .motto__lead"), last = scrollY, raf = 0, skew = 0;
    function tick() {
      var v = scrollY - last; last = scrollY;
      skew += (Math.max(-6, Math.min(6, v * .12)) - skew) * .18;
      document.documentElement.style.setProperty("--fx-skew", skew.toFixed(2) + "deg");
      raf = Math.abs(skew) > .02 ? requestAnimationFrame(tick) : 0;
    }
    addEventListener("scroll", function () { if (!raf) raf = requestAnimationFrame(tick); }, { passive: true });
    heads.forEach(function (h) { h.classList.add("fx-skew"); });
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

  /* ── Seminar checkout ───────────────────────────────────────────────── */
  // Pay button unlocks only after the consent box is ticked and a seminar
  // is chosen. While PAYMENT.action is unset (data-pending) a submit shows
  // the note instead of posting anywhere.
  function checkout() {
    var form = $(".checkout");
    if (!form) return;
    var agree = $("#agree", form), sel = $("#seminar", form), btn = $("[type=submit]", form);
    var amount = $("#amount", form), note = $("[data-pending-note]", form);
    var out = function (key) { return $('[data-order="' + key + '"]', form); };

    function summary() {
      if (!sel || !sel.options.length) return;
      var o = sel.options[sel.selectedIndex];
      if (!o || !o.value) return;
      out("title").textContent = o.getAttribute("data-title");
      out("when").textContent = o.getAttribute("data-when") + " · " + o.getAttribute("data-mode");
      out("price").textContent = o.getAttribute("data-price");
      out("total").textContent = o.getAttribute("data-price");
      if (amount) amount.value = o.getAttribute("data-price");
    }
    function sync() {
      btn.disabled = !(agree.checked && sel && !sel.disabled && sel.value);
    }
    var wanted = new URLSearchParams(location.search).get("s");
    if (wanted && sel && !sel.disabled) {
      for (var i = 0; i < sel.options.length; i++)
        if (sel.options[i].value === wanted) { sel.selectedIndex = i; break; }
    }
    if (sel) sel.addEventListener("change", function () { summary(); sync(); });
    agree.addEventListener("change", sync);

    var inv = $("#invoice", form), invFields = $(".invoice-fields", form);
    if (inv && invFields) {
      var toggle = function () {
        invFields.hidden = !inv.checked;
        $$("input", invFields).forEach(function (el) { el.required = inv.checked && el.id !== "tax-office"; });
      };
      inv.addEventListener("change", toggle); toggle();
    }

    form.addEventListener("submit", function (e) {
      if (!form.checkValidity()) {
        e.preventDefault();
        var bad = $(":invalid", form);
        if (bad) { bad.focus(); if (bad.reportValidity) bad.reportValidity(); }
        return;
      }
      if (form.hasAttribute("data-pending")) {
        e.preventDefault();
        if (note) { note.hidden = false; note.scrollIntoView({ block: "nearest", behavior: "smooth" }); }
      }
    });
    summary(); sync();
  }

  function init() {
    gate(); header(); futurist(); reveal(); compare(); faq(); doc(); chrome(); cookies(); checkout();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
