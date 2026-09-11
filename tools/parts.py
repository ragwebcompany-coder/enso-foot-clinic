# -*- coding: utf-8 -*-
"""Shared markup: head, header, drawer, footer, overlays, icons, foot diagram."""
import json, sys, os, hashlib, html as _html
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content"))
from data import SITE, CONDITIONS, TREATMENTS, PRACTITIONER

I = {
 "search": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="1.8"/><path d="M16.5 16.5L21 21" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
 "chev": '<svg class="nav__chev" width="11" height="11" viewBox="0 0 12 12" fill="none" aria-hidden="true"><path d="M2.5 4.5L6 8l3.5-3.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "phone": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 3h3.5l1.7 4.2-2.1 1.5a12.5 12.5 0 006.2 6.2l1.5-2.1L20 14.5V18a2 2 0 01-2.2 2A16.8 16.8 0 013 6.2 2 2 0 015 3z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>',
 "mail": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2.5" stroke="currentColor" stroke-width="1.7"/><path d="M4 7l8 5.5L20 7" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>',
 "pin": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 21s7-5.6 7-11a7 7 0 10-14 0c0 5.4 7 11 7 11z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><circle cx="12" cy="10" r="2.6" stroke="currentColor" stroke-width="1.7"/></svg>',
 "clock": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="8.5" stroke="currentColor" stroke-width="1.7"/><path d="M12 7.5V12l3 2" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "lock": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="4" y="10" width="16" height="11" rx="2.5" stroke="currentColor" stroke-width="1.8"/><path d="M8 10V7a4 4 0 018 0v3" stroke="currentColor" stroke-width="1.8"/></svg>',
 "play": '<svg width="46" height="46" viewBox="0 0 46 46" fill="none" aria-hidden="true"><circle cx="23" cy="23" r="21" stroke="currentColor" stroke-width="1.6" opacity=".8"/><path d="M19 15.5l12 7.5-12 7.5z" fill="currentColor"/></svg>',
 "pdf": '<svg width="30" height="30" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M14 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V8l-5-5z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M14 3v5h5" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>',
 "up": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 19V6M6 11l6-6 6 6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "close": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
 "left": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M14.5 5L8 12l6.5 7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "right": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9.5 5L16 12l-6.5 7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "fb": '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-8h2.7l.4-3.1h-3.1V7.9c0-.9.25-1.5 1.55-1.5h1.65V3.6c-.29-.04-1.27-.12-2.41-.12-2.39 0-4.02 1.46-4.02 4.13v2.3H7.5V13h2.77v8h3.23z"/></svg>',
 "tiktok": '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.6 5.82A4.28 4.28 0 0115.54 3h-3.1v12.4a2.59 2.59 0 01-2.59 2.5 2.59 2.59 0 01-2.6-2.58 2.59 2.59 0 013.1-2.54v-3.1a5.66 5.66 0 00-.5-.03A5.68 5.68 0 004.17 15.4a5.68 5.68 0 005.68 5.68 5.68 5.68 0 005.69-5.68V9.4a7.35 7.35 0 004.29 1.37V7.7a4.28 4.28 0 01-3.23-1.88z"/></svg>',
 "down": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 5v13M6 13l6 6 6-6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 # Three line marks for the phone cover's pillars: the foot in plan, the sole in
 # profile with its loaded zones, and a nail on its bed.
 "pil_foot": '<svg width="34" height="40" viewBox="0 0 34 40" fill="none" aria-hidden="true"><path d="M7 16c0-5 3.5-8 8-8s9 3 9 8c0 4-2 6-2.5 9.5C21 29 22 33 18.5 35c-3 1.6-7 .4-8-3-.8-3 .5-5 .5-8C11 21 7 20 7 16z" stroke="currentColor" stroke-width="1.4"/><circle cx="10" cy="7" r="2.6" stroke="currentColor" stroke-width="1.3"/><circle cx="16" cy="4.4" r="2.1" stroke="currentColor" stroke-width="1.3"/><circle cx="21" cy="4.6" r="1.9" stroke="currentColor" stroke-width="1.3"/><circle cx="25.4" cy="6.6" r="1.7" stroke="currentColor" stroke-width="1.3"/></svg>',
 "pil_tool": '<svg width="40" height="40" viewBox="0 0 40 40" fill="none" aria-hidden="true"><path d="M7.5 31.5L19 20" stroke="currentColor" stroke-width="3.4" stroke-linecap="round"/><path d="M19.5 20.5L29 11c2-2 5.2-.6 5.2 2.1 0 1.1-.5 2.2-1.3 2.9L23.5 24.5z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/><path d="M6 35h28" stroke="currentColor" stroke-width="1.3" opacity=".4" stroke-linecap="round"/></svg>',
 "pil_nail": '<svg width="34" height="40" viewBox="0 0 34 40" fill="none" aria-hidden="true"><path d="M17 4c7 0 11 6 11 13v11c0 4-4 7-11 7S6 32 6 28V17C6 10 10 4 17 4z" stroke="currentColor" stroke-width="1.4"/><path d="M17 9.5c4 0 6.2 3.4 6.2 7.8v9.4H10.8v-9.4c0-4.4 2.2-7.8 6.2-7.8z" stroke="currentColor" stroke-width="1.3"/><path d="M13.2 14.2c2-1.7 5.6-1.7 7.6 0" stroke="currentColor" stroke-width="1.1" opacity=".65"/></svg>',
 "shield": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 3l7.5 3v5.5c0 4.6-3.1 8.5-7.5 9.5-4.4-1-7.5-4.9-7.5-9.5V6L12 3z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>',
}


def rel(depth):
    return "../" * depth if depth else ""


# Asset filenames are stable (enso.css, logo.svg…), so a long cache on them means
# a returning browser renders NEW html against OLD css — the page arrives with
# markup its stylesheet has never heard of. Appending a content hash makes every
# change a new URL, which is what lets the far-future cache be correct instead of
# dangerous. build.py points ASSET_ROOT at the output directory before rendering.
ASSET_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")
_VER = {}


def ver(path):
    if path not in _VER:
        try:
            with open(os.path.join(ASSET_ROOT, path), "rb") as f:
                _VER[path] = hashlib.sha256(f.read()).hexdigest()[:10]
        except OSError:
            _VER[path] = ""
    return _VER[path]


def asset(depth, path):
    """Relative URL for an asset, carrying its content hash."""
    v = ver(path)
    return rel(depth) + path + (f"?v={v}" if v else "")


# UI strings. The clinical copy stays in Greek; the shell speaks the page's language.
T = {
    "el": dict(
        skip="Μετάβαση στο περιεχόμενο", nav_label="Κύρια πλοήγηση",
        clinic="Το κέντρο", conditions="Παθήσεις", treatments="Υπηρεσίες",
        both="Παθήσεις & υπηρεσίες", guide="Οδηγός συμπτωμάτων",
        tracker="Φροντίδα ποδιών", seminars="Σεμινάρια",
        articles="Άρθρα", gallery="Εικονογραφήσεις", contact="Επικοινωνία",
        book="Ραντεβού", search="Αναζήτηση (Ctrl+K)", menu="Μενού", other_lang="EN",
        all_conditions="Όλες οι παθήσεις", compare="Σύγκριση υπηρεσιών",
        search_ph="Πάθηση, υπηρεσία ή άρθρο…", search_hint="Γράψτε τουλάχιστον 2 χαρακτήρες.",
        hours="Ωράριο", terms="Όροι χρήσης & απόρρητο", other_lang_full="English",
        tagline="Ποδολογικό κέντρο σε Θεσσαλονίκη και Αθήνα, από το 2002. "
                "Θεραπεία και φροντίδα του άκρου ποδός.",
        call="Κλήση", top="Επιστροφή στην κορυφή", close="Κλείσιμο",
        prev="Προηγούμενο", next="Επόμενο", view="Προβολή",
        ck_title="Cookies",
        ck_body="Κρατάμε μόνο ό,τι χρειάζεται για να λειτουργεί ο ιστότοπος. Τα υπόλοιπα τα αποφασίζετε εσείς.",
        ck_need="Απαραίτητα", ck_stats="Στατιστικά χρήσης", ck_always="Πάντα ενεργά",
        ck_save="Αποθήκευση επιλογών", ck_min="Μόνο τα απαραίτητα",
        madeby="Made by",
    ),
    "en": dict(
        skip="Skip to content", nav_label="Main navigation",
        clinic="The clinic", conditions="Conditions", treatments="Services",
        both="Conditions & services", guide="Symptom guide",
        tracker="Foot care", seminars="Seminars",
        articles="Articles", gallery="Illustrations", contact="Contact",
        book="Book", search="Search (Ctrl+K)", menu="Menu", other_lang="ΕΛ",
        all_conditions="All conditions", compare="Compare services",
        search_ph="Condition, service or article…", search_hint="Type at least 2 characters.",
        hours="Opening hours", terms="Terms & privacy", other_lang_full="Ελληνικά",
        tagline="Podology centre in Thessaloniki and Athens, practising since 2002.",
        call="Call", top="Back to top", close="Close",
        prev="Previous", next="Next", view="View",
        ck_title="Cookies",
        ck_body="We keep only what the site needs to work. The rest is up to you.",
        ck_need="Essential", ck_stats="Usage statistics", ck_always="Always on",
        ck_save="Save choices", ck_min="Essential only",
        madeby="Made by",
    ),
}


def head(title, desc, depth, canonical, *, lang="el", alt=None, jsonld=None,
         og_image="assets/img/og-enso.png"):
    b = rel(depth)
    ld = "".join('<script type="application/ld+json">%s</script>'
                 % json.dumps(x, ensure_ascii=False, separators=(",", ":")) for x in (jsonld or []))
    alt_links = ""
    if alt:
        alt_links = '<link rel="alternate" hreflang="%s" href="%s/%s">' % (
            alt[0], SITE["domain"], alt[1].lstrip("/"))
    return f"""<!doctype html>
<html lang="{lang}" data-base="{b or './'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE['domain']}/{canonical.lstrip('/')}">
<link rel="alternate" hreflang="{lang}" href="{SITE['domain']}/{canonical.lstrip('/')}">{alt_links}
<meta name="theme-color" content="#0c3f7c">
<meta name="geo.region" content="{SITE['region_iso']}">
<meta name="geo.placename" content="{SITE['locality']}, {SITE['region']}">
<meta name="geo.position" content="{SITE['lat']};{SITE['lng']}">
<meta name="ICBM" content="{SITE['lat']}, {SITE['lng']}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:locale" content="{'el_GR' if lang == 'el' else 'en_GB'}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE['domain']}/{canonical.lstrip('/')}">
<meta property="og:image" content="{SITE['domain']}/{og_image}">
<meta property="og:image:alt" content="{SITE['name']} — ποδολογικό κέντρο, Περαία Θεσσαλονίκης">
<meta property="place:location:latitude" content="{SITE['lat']}">
<meta property="place:location:longitude" content="{SITE['lng']}">
<meta property="business:contact_data:locality" content="{SITE['locality']}">
<meta property="business:contact_data:region" content="{SITE['region']}">
<meta property="business:contact_data:postal_code" content="{SITE['postcode']}">
<meta property="business:contact_data:country_name" content="Greece">
<meta property="business:contact_data:phone_number" content="{SITE['phone_href']}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{asset(depth, "assets/img/favicon.svg")}" type="image/svg+xml">
<link rel="icon" href="{asset(depth, "assets/img/favicon-144.png")}" sizes="144x144">
<link rel="apple-touch-icon" href="{asset(depth, "assets/img/favicon-144.png")}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@300;400;500;700&amp;display=swap">
<link rel="stylesheet" href="{asset(depth, "assets/css/enso.css")}">
<script>document.documentElement.className+=" js";</script>
{ld}</head>"""


def search_overlay(lang="el"):
    t = T[lang]
    return f"""<div class="search" role="dialog" aria-modal="true" aria-label="{t['search']}" aria-hidden="true">
  <div class="search__panel">
    <div class="search__field">{I['search']}
      <label class="vh" for="search-input">{t['search']}</label>
      <input id="search-input" type="search" placeholder="{t['search_ph']}" autocomplete="off">
      <button class="search__kbd" data-search-close>ESC</button>
    </div>
    <div class="search__results" id="search-results">
      <p class="search__empty">{t['search_hint']}</p>
    </div>
  </div>
</div>"""


EN_NAV = [("the-clinic", "The Clinic"), ("diabetic-foot-care", "Diabetic Foot Care"),
          ("calluses-and-corns", "Calluses & Corns"), ("dry-cracked-heels", "Dry & Cracked Heels"),
          ("ingrown-toenail", "Ingrown Toenail"), ("medical-pedicure", "Medical Pedicure")]


def drawer(depth, lang="el"):
    b, t = rel(depth), T[lang]
    if lang == "en":
        links = "".join(f'<div class="drawer__group"><a class="drawer__top" href="{b}en/{s}/">{n}</a></div>'
                        for s, n in EN_NAV)
        return f"""<div class="drawer" id="drawer">
  <div class="drawer__group"><a class="drawer__top" href="{b}en/">{SITE['name']}</a></div>
  {links}
  <div class="drawer__group"><a class="drawer__top" href="{b}">{t['other_lang_full']}</a></div>
  <div class="drawer__cta">
    <a class="btn btn--block" href="tel:{SITE['phone_href']}">{I['phone']} {SITE['phone']}</a>
    <a class="btn btn--ghost btn--block" href="mailto:{SITE['email']}">{I['mail']} {SITE['email']}</a>
  </div>
</div>"""
    conds = "".join(f'<a href="{b}pathiseis/{c["slug"]}/">{c["title"]}</a>' for c in CONDITIONS)
    treats = "".join(f'<a href="{b}ypiresies/{x["slug"]}/">{x["title"]}</a>' for x in TREATMENTS)
    return f"""<div class="drawer" id="drawer">
  <div class="drawer__group"><a class="drawer__top" href="{b}to-iatreio/">{t['clinic']}</a></div>
  <div class="drawer__group">
    <button class="drawer__top" aria-expanded="false">{t['conditions']} {I['chev']}</button>
    <div class="drawer__panel"><a href="{b}pathiseis/">{t['all_conditions']}</a>{conds}</div>
  </div>
  <div class="drawer__group">
    <button class="drawer__top" aria-expanded="false">{t['treatments']} {I['chev']}</button>
    <div class="drawer__panel"><a href="{b}ypiresies/">{t['compare']}</a>{treats}</div>
  </div>
  <div class="drawer__group"><a class="drawer__top" href="{b}odigos-symptomaton/">{t['guide']}</a></div>
  <div class="drawer__group"><a class="drawer__top" href="{b}frontida-podion/">{t['tracker']}</a></div>
  <div class="drawer__group"><a class="drawer__top" href="{b}seminaria/">{t['seminars']}</a></div>
  <div class="drawer__group"><a class="drawer__top" href="{b}arthra/">{t['articles']}</a></div>
  <div class="drawer__group"><a class="drawer__top" href="{b}gallery/">{t['gallery']}</a></div>
  <div class="drawer__group"><a class="drawer__top" href="{b}epikoinonia/">{t['contact']}</a></div>
  <div class="drawer__group"><a class="drawer__top" href="{b}en/">{t['other_lang_full']}</a></div>
  <div class="drawer__cta">
    <a class="btn btn--block" href="tel:{SITE['phone_href']}">{I['phone']} {SITE['phone']}</a>
    <a class="btn btn--ghost btn--block" href="mailto:{SITE['email']}">{I['mail']} {SITE['email']}</a>
  </div>
</div>"""


def header(depth, active="", lang="el", over_dark=False):
    b, t = rel(depth), T[lang]
    cur = lambda k: ' aria-current="page"' if active == k else ""
    if lang == "en":
        items = "".join(
            f'<div class="nav__item"><a class="nav__link" href="{b}en/{s}/"{cur(s)}>{n}</a></div>'
            for s, n in EN_NAV[:4])
        nav = f"""<nav class="nav" aria-label="{t['nav_label']}">
        <div class="nav__item"><a class="nav__link" href="{b}en/"{cur('home')}>{SITE['name']}</a></div>
        {items}
      </nav>"""
        lang_link = f'<a class="lang" href="{b}" hreflang="el">{t["other_lang"]}</a>'
    else:
        conds = "".join(
            f'<a class="mega__link" href="{b}pathiseis/{c["slug"]}/"><b>{c["title"]}</b>'
            f'<span>{c["plain"]}</span></a>' for c in CONDITIONS)
        treats = "".join(
            f'<a class="mega__link" href="{b}ypiresies/{x["slug"]}/"><b>{x["title"]}</b>'
            f'<span>{x["short"]}</span></a>' for x in TREATMENTS)
        nav = f"""<nav class="nav" aria-label="{t['nav_label']}">
        <div class="nav__item"><a class="nav__link" href="{b}to-iatreio/"{cur('clinic')}>{t['clinic']}</a></div>
        <div class="nav__item" data-mega>
          <button class="nav__link" aria-expanded="false">{t['both']} {I['chev']}</button>
          <div class="mega">
            <div class="mega__col"><p class="mega__title">{t['conditions']}</p>{conds}</div>
            <div class="mega__col"><p class="mega__title">{t['treatments']}</p>{treats}</div>
          </div>
        </div>
        <div class="nav__item"><a class="nav__link" href="{b}odigos-symptomaton/"{cur('guide')}>{t['guide']}</a></div>
        <div class="nav__item"><a class="nav__link" href="{b}seminaria/"{cur('seminars')}>{t['seminars']}</a></div>
        <div class="nav__item nav__item--optional"><a class="nav__link" href="{b}arthra/"{cur('articles')}>{t['articles']}</a></div>
        <div class="nav__item"><a class="nav__link" href="{b}epikoinonia/"{cur('contact')}>{t['contact']}</a></div>
      </nav>"""
        lang_link = f'<a class="lang" href="{b}en/" hreflang="en">{t["other_lang"]}</a>'

    # Over a deep hero the header floats transparent, so it carries the light
    # lockup as well and CSS swaps them as the page scrolls into the solid bar.
    brand_img = f'<img class="brand__dark" src="{asset(depth, "assets/img/logo.svg")}" alt="{SITE["name"]}" width="174" height="42">'
    if over_dark:
        brand_img += (f'<img class="brand__light" src="{asset(depth, "assets/img/logo-light.svg")}" '
                      f'alt="" aria-hidden="true" width="174" height="42">')
    return f"""<a class="skip" href="#main">{t['skip']}</a>
<header class="header">
  <div class="wrap header__bar">
    <a class="brand" href="{(b + 'en/') if lang == 'en' else (b or './')}">{brand_img}</a>
    {nav}
    <div class="header__tools">
      <button class="icon-btn" data-search-open aria-label="{t['search']}">{I['search']}</button>
      {lang_link}
      <a class="btn btn--sm" href="tel:{SITE['phone_href']}">{t['book']}</a>
      <button class="icon-btn burger" aria-label="{t['menu']}" aria-expanded="false" aria-controls="drawer">
        <span></span><span></span><span></span></button>
    </div>
  </div>
</header>
{drawer(depth, lang)}
{search_overlay(lang)}"""


def footer(depth, lang="el"):
    b, t = rel(depth), T[lang]
    rows = SITE["hours_en"] if lang == "en" else SITE["hours"]
    hours = "".join(f"<div><span>{a}</span><span>{c}</span></div>" for a, c in rows)
    if lang == "en":
        col1 = "".join(f'<li><a href="{b}en/{s}/">{n}</a></li>' for s, n in EN_NAV[1:4])
        col2 = "".join(f'<li><a href="{b}en/{s}/">{n}</a></li>' for s, n in EN_NAV[4:])
        addr, addr2 = SITE["address_en"], SITE["address_athens_en"]
        city1, city2 = "Thessaloniki", "Athens"
    else:
        col1 = "".join(f'<li><a href="{b}pathiseis/{c["slug"]}/">{c["title"]}</a></li>' for c in CONDITIONS)
        col2 = "".join(f'<li><a href="{b}ypiresies/{x["slug"]}/">{x["title"]}</a></li>' for x in TREATMENTS)
        addr, addr2 = SITE["address"], SITE["address_athens"]
        city1, city2 = "Θεσσαλονίκη", "Αθήνα"
    h1, h2 = t["conditions"], t["treatments"]
    return f"""<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__brand">
        <img src="{asset(depth, "assets/img/logo-light.svg")}" alt="{SITE['name']}" width="196" height="61" loading="lazy">
        <p class="small" style="margin-top:1.1rem;max-width:34ch;color:#9dc0de">{t['tagline']}</p>
        <div class="socials" style="margin-top:1.5rem">
          <a href="{SITE['social']['facebook']}" rel="noopener" target="_blank" aria-label="Facebook">{I['fb']}</a>
          <a href="{SITE['social']['tiktok']}" rel="noopener" target="_blank" aria-label="TikTok">{I['tiktok']}</a>
        </div>
      </div>
      <div><h4>{h1}</h4><ul>{col1}</ul></div>
      <div><h4>{h2}</h4><ul>{col2}</ul></div>
      <div>
        <h4>{t['contact']}</h4>
        <ul style="margin-bottom:1.6rem">
          <li class="footer__place"><b>{city1}</b>
            <a href="{SITE['map']}" rel="noopener" target="_blank">{addr}, {SITE['postcode']}</a>
            <a href="tel:{SITE['phone_href']}">{SITE['phone']}</a></li>
          <li class="footer__place"><b>{city2}</b>
            <a href="{SITE['map_athens']}" rel="noopener" target="_blank">{addr2}, {SITE['postcode_athens']}</a>
            <span><a href="tel:{SITE['phone_alt_href']}">{SITE['phone_alt']}</a> · <a href="tel:{SITE['phone_mob_href']}">{SITE['phone_mob']}</a></span></li>
          <li><a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
        </ul>
        <h4>{t['hours']}</h4>
        <div class="footer__hours">{hours}</div>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© {SITE['founded']}–2026 {SITE['name']} · {SITE['locality']}, {SITE['region']}</span>
      <span style="display:flex;gap:1.25rem;flex-wrap:wrap;align-items:center">
        <a href="{b}seminaria/">{t['seminars']}</a>
        <a href="{b}oroi-chrisis/">{t['terms']}</a>
        <a href="{(b + 'en/') if lang == 'el' else b}">{t['other_lang_full']}</a>
        <a class="credit" href="{_html.escape(SITE['credit']['url'], quote=True)}" target="_blank" rel="noopener noreferrer">
          {t['madeby']} <b>{SITE['credit']['name']}</b></a>
      </span>
    </div>
  </div>
</footer>"""


def overlays(depth=0, lang="el"):
    t = T[lang]
    return f"""<div class="lightbox" role="dialog" aria-modal="true" aria-label="{t['view']}" aria-hidden="true">
  <div class="lightbox__stage-wrap" style="width:min(1100px,100%)">
    <div class="lightbox__bar">
      <span class="small" data-lb-caption></span>
      <span style="display:flex;gap:.5rem">
        <span class="lightbox__nav">
          <button type="button" data-lb-prev aria-label="{t['prev']}">{I['left']}</button>
          <button type="button" data-lb-next aria-label="{t['next']}">{I['right']}</button>
        </span>
        <button type="button" class="lightbox__close" aria-label="{t['close']}">{I['close']}</button>
      </span>
    </div>
    <div class="lightbox__stage"></div>
  </div>
</div>

<div class="cookies" role="region" aria-label="{t['ck_title']}">
  <div>
    <h4 style="margin-bottom:.4rem;text-transform:none;letter-spacing:0;font-size:1rem">{t['ck_title']}</h4>
    <p class="small muted">{t['ck_body']}</p>
  </div>
  <div style="display:grid;gap:.65rem">
    <div class="cookies__toggle"><span>{t['ck_need']}</span>
      <label class="switch"><input type="checkbox" checked disabled><i></i><span class="vh">{t['ck_always']}</span></label></div>
    <div class="cookies__toggle"><span>{t['ck_stats']}</span>
      <label class="switch"><input type="checkbox" id="cookie-analytics"><i></i><span class="vh">{t['ck_stats']}</span></label></div>
  </div>
  <div class="cookies__row">
    <button class="btn btn--sm" data-cookie-accept>{t['ck_save']}</button>
    <button class="btn btn--ghost btn--sm" data-cookie-reject>{t['ck_min']}</button>
  </div>
</div>

<button class="totop" aria-label="{t['top']}">{I['up']}</button>

<div class="actionbar">
  <a class="btn btn--sm btn--block" href="tel:{SITE['phone_href']}">{I['phone']} {t['book']} · {SITE['phone']}</a>
</div>"""


# ── Foot diagram ─────────────────────────────────────────────────────────────
# A schematic lateral view of the right foot, drawn for this site. The toes are
# on the left, the heel on the right, the leg cut off above the ankle. The
# forefoot pad and the heel pad meet the ground; the arch lifts between them.
#
# Each zone is a focusable hotspot. The «Με πρόβλημα» toggle fades in what each
# of the four conditions actually looks like — a keratin plaque with a core
# under the forefoot, fissures across the heel pad, a nail edge curling into the
# fold, and the pressure points a neuropathic foot no longer feels.
FOOT_SVG = """<svg class="anatomy__svg" viewBox="0 0 680 560" role="img"
  aria-label="Σχηματική πλάγια τομή του άκρου ποδός: νύχι μεγάλου δακτύλου, πρόσθιο πέλμα, πτέρνα, δέρμα με τα νεύρα και τα αγγεία του">
  <defs>
    <linearGradient id="tissue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#e8f2fb"/><stop offset="1" stop-color="#c5dcf0"/>
    </linearGradient>
    <linearGradient id="skinGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#fdf1e8"/><stop offset="1" stop-color="#f6e0d1"/>
    </linearGradient>
  </defs>

  <!-- Leg above the ankle, cut off, sitting behind the foot. -->
  <path d="M404 168h88v168h-88z" fill="#eef5fc"/>
  <path d="M404 168v150M492 168v152" fill="none" stroke="#dae7f3" stroke-width="2"/>

  <!-- The foot itself: dorsum from the toe up to the ankle, down the achilles,
       round the heel, then along the sole with the arch lifting in the middle. -->
  <path id="foot-skin"
        d="M150 384C176 376 244 350 300 314C346 284 382 246 396 200
           C400 186 400 178 400 170H496C496 196 498 262 502 306
           C506 348 508 380 504 402C500 424 486 434 466 434
           L400 434C356 434 336 396 296 392C256 388 238 424 200 432
           L132 432C108 432 92 418 94 400C96 384 118 376 150 384Z"
        fill="url(#skinGrad)" stroke="#e0c6b3" stroke-width="2"/>

  <!-- Ground and skeletal hints. -->
  <path d="M62 440h556" stroke="#d2e4f2" stroke-width="4" stroke-linecap="round"/>
  <g stroke="#e6eef7" stroke-width="9" stroke-linecap="round" fill="none">
    <path d="M196 408l108-58"/><path d="M214 416l104-50"/><path d="M238 420l96-42"/>
  </g>
  <ellipse cx="452" cy="392" rx="46" ry="34" fill="#f2e2d4" opacity=".7"/>

  <!-- Nail of the great toe. -->
  <g class="hot" id="g-nail" data-zone="nail" tabindex="0" role="button"
     aria-label="Νύχι μεγάλου δακτύλου — είσφρηση όνυχος">
    <g class="organ">
      <ellipse class="hot__shape" cx="118" cy="392" rx="22" ry="12"
               transform="rotate(-24 118 392)" fill="url(#tissue)"
               stroke="#8fb0d0" stroke-width="1.8"/>
    </g>
    <g class="flaw">
      <path d="M132 400c8 6 12 13 12 20" fill="none" stroke="#c2544f"
            stroke-width="4.5" stroke-linecap="round"/>
      <ellipse cx="140" cy="414" rx="16" ry="11" fill="#c2544f" opacity=".26"/>
    </g>
    <path class="hot__lead" d="M108 376V118h44" fill="none"/>
    <text class="hot__label" x="160" y="122">Νύχι μεγάλου δακτύλου</text>
    <rect class="hot__hit" x="84" y="362" width="84" height="72"/>
  </g>

  <!-- Forefoot pad: the metatarsal heads, where calluses and corns build up. -->
  <g class="hot" id="g-forefoot" data-zone="forefoot" tabindex="0" role="button"
     aria-label="Πρόσθιο πέλμα — σκληρύνσεις, κάλοι και τύλοι">
    <g class="organ">
      <path class="hot__shape" d="M142 424h74" fill="none"
            stroke="url(#tissue)" stroke-width="17" stroke-linecap="round"/>
    </g>
    <g class="flaw">
      <path d="M150 424h60" fill="none" stroke="#d9a066" stroke-width="15" stroke-linecap="round"/>
      <path d="M182 418l-7-32h14z" fill="#b57433"/>
      <circle cx="182" cy="382" r="6" fill="#c2544f" opacity=".55"/>
    </g>
    <path class="hot__lead" d="M182 446v42h56" fill="none"/>
    <text class="hot__label" x="246" y="493">Πρόσθιο πέλμα</text>
    <rect class="hot__hit" x="128" y="400" width="106" height="48"/>
  </g>

  <!-- Heel pad: where dryness and fissures happen. -->
  <g class="hot" id="g-heel" data-zone="heel" tabindex="0" role="button"
     aria-label="Πτέρνα — ξηροδερμία πελμάτων και ραγάδες">
    <g class="organ">
      <path class="hot__shape" d="M404 426h62" fill="none"
            stroke="url(#tissue)" stroke-width="19" stroke-linecap="round"/>
    </g>
    <g class="flaw">
      <path d="M404 424h62" fill="none" stroke="#d9a066" stroke-width="15" stroke-linecap="round"/>
      <path d="M412 410v26M428 406v30M444 408v28M460 412v22" fill="none"
            stroke="#a53c33" stroke-width="3.6" stroke-linecap="round"/>
    </g>
    <path class="hot__lead" d="M508 420h54" fill="none"/>
    <text class="hot__label" x="570" y="425">Πτέρνα</text>
    <rect class="hot__hit" x="392" y="398" width="112" height="50"/>
  </g>

  <!-- Skin, nerves and vessels: the diabetic foot lives here. -->
  <g class="hot" id="g-circulation" data-zone="circulation" tabindex="0" role="button"
     aria-label="Δέρμα, νεύρα και αγγεία — διαβητικό πόδι">
    <g class="organ">
      <path class="hot__shape" d="M448 186c-6 62-30 112-70 150-40 38-96 62-166 74"
            fill="none" stroke="url(#tissue)" stroke-width="8" stroke-linecap="round"/>
      <path d="M448 186c-6 62-30 112-70 150-40 38-96 62-166 74"
            fill="none" stroke="#8fb0d0" stroke-width="1.4" opacity=".6" stroke-dasharray="5 7"/>
    </g>
    <g class="flaw">
      <path d="M330 356c-36 30-76 48-118 54" fill="none" stroke="#c2544f"
            stroke-width="9" stroke-linecap="round" opacity=".32"/>
      <g fill="none" stroke="#c2544f" stroke-width="3">
        <circle cx="182" cy="424" r="14"/><circle cx="434" cy="424" r="14"/>
        <circle cx="122" cy="392" r="14"/>
      </g>
    </g>
    <path class="hot__lead" d="M436 250h126" fill="none"/>
    <text class="hot__label" x="570" y="255">Νεύρα &amp; αγγεία</text>
    <rect class="hot__hit" x="300" y="188" width="164" height="150"/>
  </g>

  <text class="hot__label" x="618" y="462" text-anchor="end" fill="#6f8d96">Έδαφος</text>
</svg>"""


def anatomy_block(depth):
    return f"""<div class="anatomy" id="anatomy" data-default="nail">
  <div class="anatomy__stage">
    <div class="anatomy__toggle" role="group" aria-label="Κατάσταση διαγράμματος">
      <button type="button" data-state="normal" aria-pressed="true">Φυσιολογικό</button>
      <button type="button" data-state="affected" aria-pressed="false">Με πρόβλημα</button>
    </div>
    {FOOT_SVG}
  </div>
  <div class="anatomy__panel" aria-live="polite"></div>
</div>"""
