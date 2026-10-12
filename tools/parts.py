# -*- coding: utf-8 -*-
"""Shared markup: head, header, drawer, footer, overlays, icons."""
import json, sys, os, hashlib, html as _html
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content"))
from data import SITE, TREATMENTS, PRACTITIONER

I = {
 "chev": '<svg class="nav__chev" width="11" height="11" viewBox="0 0 12 12" fill="none" aria-hidden="true"><path d="M2.5 4.5L6 8l3.5-3.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "phone": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 3h3.5l1.7 4.2-2.1 1.5a12.5 12.5 0 006.2 6.2l1.5-2.1L20 14.5V18a2 2 0 01-2.2 2A16.8 16.8 0 013 6.2 2 2 0 015 3z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>',
 "mail": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2.5" stroke="currentColor" stroke-width="1.7"/><path d="M4 7l8 5.5L20 7" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>',
 "pin": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 21s7-5.6 7-11a7 7 0 10-14 0c0 5.4 7 11 7 11z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><circle cx="12" cy="10" r="2.6" stroke="currentColor" stroke-width="1.7"/></svg>',
 "clock": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="8.5" stroke="currentColor" stroke-width="1.7"/><path d="M12 7.5V12l3 2" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "stairs": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M3 20h5v-5h5v-5h5V5h3" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "doc": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M14 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V8l-5-5z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M14 3v5h5M8.5 13h7M8.5 17h7" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "up": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 19V6M6 11l6-6 6 6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "right": '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9.5 5L16 12l-6.5 7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "fb": '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-8h2.7l.4-3.1h-3.1V7.9c0-.9.25-1.5 1.55-1.5h1.65V3.6c-.29-.04-1.27-.12-2.41-.12-2.39 0-4.02 1.46-4.02 4.13v2.3H7.5V13h2.77v8h3.23z"/></svg>',
 "tiktok": '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.6 5.82A4.28 4.28 0 0115.54 3h-3.1v12.4a2.59 2.59 0 01-2.59 2.5 2.59 2.59 0 01-2.6-2.58 2.59 2.59 0 013.1-2.54v-3.1a5.66 5.66 0 00-.5-.03A5.68 5.68 0 004.17 15.4a5.68 5.68 0 005.68 5.68 5.68 5.68 0 005.69-5.68V9.4a7.35 7.35 0 004.29 1.37V7.7a4.28 4.28 0 01-3.23-1.88z"/></svg>',
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


# The whole site menu: exactly the four entries the clinic asked for (Oct 2026).
# (key, path, label) — `key` is what a page passes as `active=`.
# «Ποιοι είμαστε» links to the section anchor so that, from any page, it
# lands on her text and not on the entry screen (gate) again.
NAV = [("about", "#poioi-eimaste", "Ποιοι είμαστε"),
       ("treatments", "ypiresies/", "Υπηρεσίες"),
       ("seminars", "seminaria/", "Σεμινάρια"),
       ("contact", "epikoinonia/", "Επικοινωνία")]

# UI strings.
T = dict(
    skip="Μετάβαση στο περιεχόμενο", nav_label="Κύρια πλοήγηση",
    treatments="Υπηρεσίες", contact="Επικοινωνία", site="Ο ιστότοπος",
    book="Ραντεβού", menu="Μενού",
    hours="Ωράριο", terms="Όροι χρήσης & απόρρητο",
    tagline="Ποδολογικό κέντρο σε Θεσσαλονίκη και Αθήνα, από το 2002. "
            "Θεραπεία και φροντίδα του άκρου ποδός.",
    top="Επιστροφή στην κορυφή", close="Κλείσιμο",
    ck_title="Cookies",
    ck_body="Κρατάμε μόνο ό,τι χρειάζεται για να λειτουργεί ο ιστότοπος. Τα υπόλοιπα τα αποφασίζετε εσείς.",
    ck_need="Απαραίτητα", ck_stats="Στατιστικά χρήσης", ck_always="Πάντα ενεργά",
    ck_save="Αποθήκευση επιλογών", ck_min="Μόνο τα απαραίτητα",
    madeby="Made by",
)


def head(title, desc, depth, canonical, *, jsonld=None, og_image="assets/img/og-enso.png",
         rooted=False):
    """`rooted`: the page is served at arbitrary URLs (the 404), so every
    relative link must resolve from the site root — <base href="/"> and no
    indexing."""
    b = rel(depth)
    ld = "".join('<script type="application/ld+json">%s</script>'
                 % json.dumps(x, ensure_ascii=False, separators=(",", ":")) for x in (jsonld or []))
    return f"""<!doctype html>
<html lang="el" data-base="{b or './'}">
<head>
<meta charset="utf-8">
{'<base href="/">\n<meta name="robots" content="noindex">\n' if rooted else ""}<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE['domain']}/{canonical.lstrip('/')}">
<meta name="theme-color" content="#0c3f7c">
<meta name="geo.region" content="{SITE['region_iso']}">
<meta name="geo.placename" content="{SITE['locality']}, {SITE['region']}">
<meta name="geo.position" content="{SITE['lat']};{SITE['lng']}">
<meta name="ICBM" content="{SITE['lat']}, {SITE['lng']}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:locale" content="el_GR">
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


def drawer(depth):
    b = rel(depth)
    links = "".join(
        f'<div class="drawer__group"><a class="drawer__top" href="{b}{path}">{label}</a></div>'
        for _k, path, label in NAV)
    return f"""<div class="drawer" id="drawer">
  {links}
  <div class="drawer__cta">
    <a class="btn btn--block" href="tel:{SITE['phone_href']}">{I['phone']} Θεσσαλονίκη · {SITE['phone']}</a>
    <a class="btn btn--ghost btn--block" href="tel:{SITE['phone_alt_href']}">{I['phone']} Αθήνα · {SITE['phone_alt']}</a>
    <a class="btn btn--ghost btn--block" href="mailto:{SITE['email']}">{I['mail']} {SITE['email']}</a>
  </div>
</div>"""


def header(depth, active=""):
    b = rel(depth)
    items = "".join(
        f'<div class="nav__item"><a class="nav__link" href="{b}{path}"'
        f'{" aria-current=" + chr(34) + "page" + chr(34) if active == key else ""}>{label}</a></div>'
        for key, path, label in NAV)
    return f"""<a class="skip" href="#main">{T['skip']}</a>
<header class="header">
  <div class="wrap header__bar">
    <a class="brand" href="{b or './'}"><img src="{asset(depth, "assets/img/logo.svg")}" alt="{SITE["name"]}" width="174" height="42"></a>
    <nav class="nav" aria-label="{T['nav_label']}">{items}</nav>
    <div class="header__tools">
      <a class="btn btn--sm" href="tel:{SITE['phone_href']}">{I['phone']} {T['book']}</a>
      <button class="icon-btn burger" aria-label="{T['menu']}" aria-expanded="false" aria-controls="drawer">
        <span></span><span></span><span></span></button>
    </div>
  </div>
</header>
{drawer(depth)}"""


def footer(depth):
    b = rel(depth)
    hours = "".join(f"<div><span>{a}</span><span>{c}</span></div>" for a, c in SITE["hours"])
    col_site = "".join(f'<li><a href="{b}{path}">{label}</a></li>' for _k, path, label in NAV)
    col_site += f'<li><a href="{b}oroi-chrisis/">{T["terms"]}</a></li>'
    col_treats = "".join(f'<li><a href="{b}ypiresies/{x["slug"]}/">{x["title"]}</a></li>' for x in TREATMENTS)
    return f"""<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__brand">
        <img src="{asset(depth, "assets/img/logo-light.svg")}" alt="{SITE['name']}" width="196" height="61" loading="lazy">
        <p class="small" style="margin-top:1.1rem;max-width:34ch;color:#9dc0de">{T['tagline']}</p>
        <div class="socials" style="margin-top:1.5rem">
          <a href="{SITE['social']['facebook']}" rel="noopener" target="_blank" aria-label="Facebook">{I['fb']}</a>
          <a href="{SITE['social']['tiktok']}" rel="noopener" target="_blank" aria-label="TikTok">{I['tiktok']}</a>
        </div>
      </div>
      <div><h4>{T['site']}</h4><ul>{col_site}</ul></div>
      <div><h4>{T['treatments']}</h4><ul>{col_treats}</ul></div>
      <div>
        <h4>{T['contact']}</h4>
        <ul style="margin-bottom:1.6rem">
          <li class="footer__place"><b>Θεσσαλονίκη</b>
            <a href="{SITE['map']}" rel="noopener" target="_blank">{SITE['address']}, {SITE['postcode']}</a>
            <a href="tel:{SITE['phone_href']}">{SITE['phone']}</a></li>
          <li class="footer__place"><b>Αθήνα</b>
            <a href="{SITE['map_athens']}" rel="noopener" target="_blank">{SITE['address_athens']}, {SITE['postcode_athens']}</a>
            <span><a href="tel:{SITE['phone_alt_href']}">{SITE['phone_alt']}</a> · <a href="tel:{SITE['phone_mob_href']}">{SITE['phone_mob']}</a></span></li>
          <li><a href="mailto:{SITE['email']}">{SITE['email']}</a></li>
        </ul>
        <h4>{T['hours']}</h4>
        <div class="footer__hours">{hours}</div>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© {SITE['founded']}–2026 {SITE['name']} · {PRACTITIONER['name']} · {SITE['locality']}, {SITE['region']}</span>
      <span style="display:flex;gap:1.25rem;flex-wrap:wrap;align-items:center">
        <a href="{b}oroi-chrisis/">{T['terms']}</a>
        <a class="credit" href="{_html.escape(SITE['credit']['url'], quote=True)}" target="_blank" rel="noopener noreferrer">
          {T['madeby']} <b>{SITE['credit']['name']}</b></a>
      </span>
    </div>
  </div>
</footer>"""


def overlays(depth=0):
    return f"""<div class="cookies" role="region" aria-label="{T['ck_title']}">
  <div>
    <h4 style="margin-bottom:.4rem;text-transform:none;letter-spacing:0;font-size:1rem">{T['ck_title']}</h4>
    <p class="small muted">{T['ck_body']}</p>
  </div>
  <div style="display:grid;gap:.65rem">
    <div class="cookies__toggle"><span>{T['ck_need']}</span>
      <label class="switch"><input type="checkbox" checked disabled><i></i><span class="vh">{T['ck_always']}</span></label></div>
    <div class="cookies__toggle"><span>{T['ck_stats']}</span>
      <label class="switch"><input type="checkbox" id="cookie-analytics"><i></i><span class="vh">{T['ck_stats']}</span></label></div>
  </div>
  <div class="cookies__row">
    <button class="btn btn--sm" data-cookie-accept>{T['ck_save']}</button>
    <button class="btn btn--ghost btn--sm" data-cookie-reject>{T['ck_min']}</button>
  </div>
</div>

<button class="totop" aria-label="{T['top']}">{I['up']}</button>

<div class="actionbar">
  <a class="btn btn--sm btn--block" href="tel:{SITE['phone_href']}">{I['phone']} Θεσσαλονίκη</a>
  <a class="btn btn--sm btn--block" href="tel:{SITE['phone_alt_href']}">{I['phone']} Αθήνα</a>
</div>"""
