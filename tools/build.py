# -*- coding: utf-8 -*-
"""Builds the Ensō Foot Clinic static site into enso-new/site/.

    python3 enso-new/tools/build.py

Set ENSO_OUT to write somewhere else (e.g. the repo root: ENSO_OUT=.).

Content comes from content/pagecopy.py (page bodies) and content/data.py
(structure, contact details, the «Ποιοι είμαστε» text). No database, no build
tool beyond Python 3.

The site is four sections, as the clinic asked (Oct 2026):
  /              Ποιοι είμαστε — entry screen, the practitioner's text, contact
  /ypiresies/    Υπηρεσίες — the six services, nothing under the cards but the note
  /seminaria/    Σεμινάρια
  /epikoinonia/  Επικοινωνία — addresses, phones, maps, company details
plus /oroi-chrisis/ (legal), /stoicheia-epicheirisis/ (company details, linked
only from the foot of the page) and a 404.
"""
import os, re, sys, json, html, datetime, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "content"))
sys.path.insert(0, HERE)

from data import (SITE, PRACTITIONER, TREATMENTS, KIND_LABELS, MATRIX_COLS,
                  BIO_BRIEF, BIO_FULL, BIO_FULL_PROFILE, SERVICES_DISCLAIMER,
                  SEMINARS, SEMINAR_STATUS, SEMINAR_MODES, SEMINAR_NOTIFY, PAYMENT)
from pagecopy import COPY
import parts
from parts import I, rel, head, header, footer, overlays, asset

OUT = os.path.abspath(os.environ.get("ENSO_OUT") or os.path.join(ROOT, "site"))
# parts.asset() hashes files from here.
parts.ASSET_ROOT = OUT
TODAY = datetime.date.today().isoformat()

TREATS = {t["slug"]: t for t in TREATMENTS}

# ── URL map ──────────────────────────────────────────────────────────────────
# Every page of the site, keyed by its copy slug. Used by the sitemap.
URLMAP = {
    "home": "", "epikoinonia": "epikoinonia/", "oroi-chrisis": "oroi-chrisis/",
    "stoicheia-epicheirisis": "stoicheia-epicheirisis/",
    "ypiresies": "ypiresies/", "seminaria": "seminaria/",
    "egrafi": "seminaria/egrafi/",
}
for _s in SEMINARS:
    URLMAP[_s["slug"]] = f"seminaria/{_s['slug']}/"
for t in TREATMENTS:
    URLMAP[t["slug"]] = f"ypiresies/{t['slug']}/"


def rewrite_links(markup, depth):
    """Turns the `@/some/path/` sentinel used in the copy into a relative URL, and
    marks outbound links as external. tel:, mailto: and #anchors are left alone."""
    def repl(m):
        href = m.group(1)
        if href.startswith("@/"):
            return f'href="{rel(depth)}{href[2:].lstrip("/")}"'
        if href.startswith(("tel:", "mailto:", "#")):
            return m.group(0)
        if href.startswith(("http://", "https://")):
            return f'href="{href}" rel="noopener" target="_blank"'
        return m.group(0)
    return re.sub(r'href="([^"]*)"', repl, markup)


FAQ_HEAD = re.compile(r"<h2>([^<]*(?:Συχνές ερωτήσεις|Συχνές Ερωτήσεις|FAQ)[^<]*)</h2>", re.I)


def split_faq(markup):
    """Pulls a trailing FAQ section out of the copy so it can become an accordion."""
    m = FAQ_HEAD.search(markup)
    if not m:
        return markup, None, []
    before, rest = markup[:m.start()], markup[m.end():]
    pairs = []
    for h in re.finditer(r"<h3>(.*?)</h3>", rest, re.S):
        q = re.sub(r"<[^>]+>", "", h.group(1)).strip()
        nxt = re.search(r"<h3>", rest[h.end():], re.S)
        body = rest[h.end(): h.end() + (nxt.start() if nxt else len(rest))]
        if q and body.strip():
            pairs.append((q, body.strip()))
    if not pairs:
        return markup, None, []
    return before, m.group(1).strip(), pairs


def faq_block(title, pairs, idx_prefix="faq"):
    if not pairs:
        return "", None
    items = "".join(f"""<div class="faq__item" id="{idx_prefix}-{i+1}">
      <button class="faq__q" type="button" aria-expanded="false" aria-controls="{idx_prefix}-{i+1}-a">
        <span>{html.escape(q)}</span><span class="faq__sign" aria-hidden="true"></span></button>
      <div class="faq__a" id="{idx_prefix}-{i+1}-a" aria-hidden="true"><div>{a}</div></div>
    </div>""" for i, (q, a) in enumerate(pairs))
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", a)).strip()}}
        for q, a in pairs]}
    return f"""<section class="section section--tight section--mist">
  <div class="wrap wrap--narrow">
    <div class="sec-head"><p class="eyebrow">Ερωτήσεις</p><h2>{html.escape(title or "Συχνές ερωτήσεις")}</h2></div>
    <div class="faq">{items}</div>
  </div>
</section>""", ld


def prose(slug, depth, drop_faq=True):
    rec = COPY.get(slug)
    if not rec:
        return "", None, []
    body = rewrite_links(rec["html"], depth)
    faq_title, pairs = None, []
    if drop_faq:
        body, faq_title, pairs = split_faq(body)
    return body.strip(), faq_title, pairs


def plain(slug, limit=None):
    rec = COPY.get(slug)
    if not rec:
        return ""
    t = html.unescape(re.sub(r"<[^>]+>", " ", rec["html"]))
    t = re.sub(r"\s+", " ", t).strip()
    return t[:limit] if limit else t


def smart_desc(text, limit=155):
    """Builds a description from whole sentences instead of a hard character cut."""
    text = re.sub(r"\s+", " ", html.unescape(text)).strip()
    chunks = [p for p in re.split(r"(?<=[.;!?])\s+", text) if p]
    out = ""
    for part in chunks:
        if len(out) + len(part) + 1 <= limit:
            out = (out + " " + part).strip()
            continue
        if len(out) < limit * 0.55:
            room = limit - len(out) - 2
            tail = part[:room].rsplit(" ", 1)[0].rstrip(" ,·—-")
            if tail:
                out = (out + " " + tail).strip() + "…"
        break
    if not out:
        out = text[:limit].rsplit(" ", 1)[0].rstrip(" ,·—-") + "…"
    return out


def meta_desc(slug, fallback=""):
    d = (COPY.get(slug) or {}).get("description", "").strip()
    if not d:
        d = smart_desc(plain(slug, 600)) or fallback
    return html.escape(d[:158], quote=True)


def local_desc(text, tail=" Ensō Foot Clinic, Περαία — Θεσσαλονίκη."):
    """Appends the locality to a meta description when there is room for it."""
    text = text.rstrip()
    if "Περαία" in text or "Θεσσαλον" in text or len(text) + len(tail) > 158:
        return text
    return text + tail


def write(path, markup):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(markup)


def write_root(path, markup):
    """Repo-level config, not site output. Vercel only reads vercel.json from the
    root of the repository — a copy inside site/ is never seen."""
    open(os.path.join(ROOT, path), "w", encoding="utf-8").write(markup)


def page(*, path, title, desc, depth, body, active="", jsonld=None,
         og_image="assets/img/og-enso.png", body_class=""):
    markup = (head(title, desc, depth, path or "", jsonld=jsonld, og_image=og_image,
                   rooted=(path == "404.html"))
              + f'\n<body{" class=" + chr(34) + body_class + chr(34) if body_class else ""}>'
              + f'\n<div class="progress" aria-hidden="true"></div>\n'
              + header(depth, active)
              + f'\n<main id="main">\n{body}\n</main>\n'
              + footer(depth) + "\n" + overlays(depth)
              + f'\n<script src="{asset(depth, "assets/js/enso.js")}" defer></script>\n</body>\n</html>\n')
    write(path + "index.html" if path.endswith("/") or path == "" else path, markup)
    return markup


# ── Structured data ─────────────────────────────────────────────────────────
CLINIC_ID = SITE["domain"] + "/#clinic"
PODOLOGIST_ID = SITE["domain"] + "/#" + PRACTITIONER["slug"]


def _address():
    return {"@type": "PostalAddress",
            "streetAddress": "Ρωμανού 11, 3ος όροφος",
            "addressLocality": SITE["locality"],
            "addressRegion": SITE["region"],
            "postalCode": SITE["postcode"],
            "addressCountry": "GR"}


def _address_athens():
    return {"@type": "PostalAddress",
            "streetAddress": "Ελ. Βενιζέλου 180, 1ος όροφος",
            "addressLocality": "Καλλιθέα",
            "addressRegion": "Αττική",
            "postalCode": SITE["postcode_athens"],
            "addressCountry": "GR"}


def _geo():
    return {"@type": "GeoCoordinates", "latitude": SITE["lat"], "longitude": SITE["lng"]}


def _area_served():
    return ([{"@type": "City", "name": a} for a in SITE["areas"]]
            + [{"@type": "AdministrativeArea", "name": "Κεντρική Μακεδονία"},
               {"@type": "Country", "name": "Ελλάδα"}])


def _legal_value(key):
    for k, v in SITE["legal_rows"]:
        if k == key:
            return v
    return None


def clinic_ld():
    """Podiatric practice, not a hospital: `Podiatric` medicalSpecialty on a
    MedicalBusiness, with the practitioner as founder and employee."""
    d = {
        "@context": "https://schema.org",
        "@type": ["MedicalBusiness", "LocalBusiness"],
        "@id": CLINIC_ID,
        "name": SITE["name"],
        "legalName": SITE["legal"],
        "alternateName": ["Ensō Foot Clinic", "Ενσο Ποδολογικό Κέντρο"],
        "description": "Ποδολογικό κέντρο σε Περαία Θεσσαλονίκης και Καλλιθέα Αθήνας, "
                       "από το 2002. Κλινική συμβουλευτική και εμβιομηχανική αξιολόγηση, "
                       "κλινική ποδολογική φροντίδα, έλεγχος διαβητικού ποδιού, αφαίρεση "
                       "κάλων, θεραπεία ξηροδερμίας, ορθονυχία.",
        "url": SITE["domain"] + "/",
        "logo": SITE["domain"] + "/assets/img/logo.svg",
        "image": [SITE["domain"] + "/assets/img/og-enso.png"],
        "telephone": SITE["phone_href"],
        "contactPoint": [
            {"@type": "ContactPoint", "telephone": SITE["phone_href"],
             "contactType": "reservations", "areaServed": "GR",
             "availableLanguage": ["el", "en"], "name": "Περαία, Θεσσαλονίκη"},
            {"@type": "ContactPoint", "telephone": SITE["phone_alt_href"],
             "contactType": "reservations", "areaServed": "GR",
             "availableLanguage": ["el", "en"], "name": "Αθήνα"},
        ],
        "email": SITE["email"],
        "foundingDate": SITE["founded"],
        "priceRange": "€€",
        "currenciesAccepted": "EUR",
        "paymentAccepted": "Μετρητά, Κάρτα",
        "knowsLanguage": ["el", "en"],
        "address": _address(),
        "geo": _geo(),
        "hasMap": SITE["map_full"],
        "location": {"@type": "Place", "name": "Ensō Foot Clinic — Αθήνα",
                     "address": _address_athens(), "hasMap": SITE["map_athens"],
                     "geo": {"@type": "GeoCoordinates", "latitude": SITE["lat_athens"],
                             "longitude": SITE["lng_athens"]},
                     "telephone": SITE["phone_alt_href"]},
        "areaServed": _area_served(),
        "medicalSpecialty": "Podiatric",
        "founder": {"@id": PODOLOGIST_ID},
        "employee": {"@id": PODOLOGIST_ID},
        "availableService": [
            {"@type": "MedicalTherapy", "name": t["title"],
             "alternateName": t["short"], "description": t["lead"],
             "url": f"{SITE['domain']}/ypiresies/{t['slug']}/"} for t in TREATMENTS],
        # No openingHoursSpecification: the clinic works by appointment and has
        # never published fixed hours. Inventing them would be worse than omitting.
        "sameAs": list(SITE["social"].values()),
    }
    if _legal_value("ΑΦΜ"):
        d["vatID"] = "EL" + _legal_value("ΑΦΜ")
        d["taxID"] = _legal_value("ΑΦΜ")
    return d


def podologist_ld():
    return {
        "@context": "https://schema.org",
        "@type": ["Person", "MedicalBusiness"],
        "@id": PODOLOGIST_ID,
        "name": PRACTITIONER["name"],
        "alternateName": PRACTITIONER["name_en"],
        "jobTitle": "Ποδολόγος",
        "description": PRACTITIONER["blurb"],
        "url": SITE["domain"] + "/",
        "medicalSpecialty": "Podiatric",
        "worksFor": {"@id": CLINIC_ID},
        "workLocation": {"@type": "Place", "name": SITE["name"],
                         "address": _address(), "geo": _geo()},
        "address": _address(),
        "telephone": SITE["phone_href"],
        "email": SITE["email"],
        "areaServed": _area_served(),
        "knowsLanguage": ["el", "en"],
        "knowsAbout": [t["title"] for t in TREATMENTS],
        "sameAs": list(SITE["social"].values()),
    }


def org_graph():
    """Clinic + podologist in one graph — the @id references resolve on every page."""
    c, d = clinic_ld(), podologist_ld()
    c.pop("@context", None); d.pop("@context", None)
    return {"@context": "https://schema.org", "@graph": [c, d]}


def seo_title(text, suffix=" | Ensō Foot Clinic", cap=70):
    """Keeps the brand suffix only while the title still fits a search result."""
    return text if len(text) + len(suffix) > cap else text + suffix


def img(name, alt, w, h, depth, *, cls="", loading="lazy", priority=False):
    extra = ' fetchpriority="high"' if priority else ""
    load = "" if priority else f' loading="{loading}" decoding="async"'
    klass = f' class="{cls}"' if cls else ""
    return (f'<img src="{asset(depth, "assets/img/" + name)}" alt="{alt}" width="{w}" height="{h}"'
            f'{load}{extra}{klass}>')


def crumbs(items, depth):
    """items: [(label, url_or_None)] — last one is the current page."""
    lis = [f'<li><a href="{rel(depth)}#poioi-eimaste">Ποιοι είμαστε</a></li>']
    for label, url in items:
        lis.append(f'<li><a href="{url}">{label}</a></li>' if url else f"<li>{label}</li>")
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Αρχική", "item": SITE["domain"] + "/"}]}
    for n, (label, _url) in enumerate(items, start=2):
        ld["itemListElement"].append({"@type": "ListItem", "position": n, "name": label})
    return f'<ol class="crumbs">{"".join(lis)}</ol>', ld


# ── Reusable blocks ─────────────────────────────────────────────────────────
def motto_band(depth):
    """The clinic's own words on the deep ground. This is what replaced the old
    «Επόμενο βήμα» call-to-action band at the foot of every page (Oct 2026)."""
    lead, body = SITE["motto"]
    return f"""<section class="section section--deep motto">
  <div class="wrap wrap--narrow">
    <span class="motto__rule" aria-hidden="true"></span>
    <p class="motto__lead">{lead}</p>
    <p class="motto__body">{body}</p>
  </div>
</section>"""


def contact_cards(depth, *, link=True):
    """The two centres, side by side: address with floor, postcode, phones, map."""
    b = rel(depth)
    more = (f'<p style="margin-top:2rem"><a class="link-more" href="{b}epikoinonia/">'
            f'Όλα τα στοιχεία επικοινωνίας και χάρτες</a></p>') if link else ""
    return f"""<div class="grid grid--2">
      <div class="card place">
        <p class="card__kicker">Θεσσαλονίκη</p>
        <h3>Ποδολογικό κέντρο Περαίας</h3>
        <ul class="info-list">
          <li>{I['pin']}<div><b>Διεύθυνση</b>
            <a href="{SITE['map']}" target="_blank" rel="noopener">{SITE['street']}, {SITE['postcode']} {SITE['locality']} {SITE['region']}</a></div></li>
          <li>{I['stairs']}<div><b>Όροφος</b><span>{SITE['floor']}</span></div></li>
          <li>{I['phone']}<div><b>Τηλέφωνο</b><a href="tel:{SITE['phone_href']}">{SITE['phone']}</a></div></li>
          <li>{I['mail']}<div><b>Email</b><a href="mailto:{SITE['email']}">{SITE['email']}</a></div></li>
        </ul>
      </div>
      <div class="card place">
        <p class="card__kicker">Αθήνα</p>
        <h3>Ποδολογικό κέντρο Καλλιθέας</h3>
        <ul class="info-list">
          <li>{I['pin']}<div><b>Διεύθυνση</b>
            <a href="{SITE['map_athens']}" target="_blank" rel="noopener">{SITE['street_athens']}, {SITE['postcode_athens']} Καλλιθέα Αθήνα</a></div></li>
          <li>{I['stairs']}<div><b>Όροφος</b><span>{SITE['floor_athens']}</span></div></li>
          <li>{I['phone']}<div><b>Τηλέφωνα</b>
            <a href="tel:{SITE['phone_alt_href']}">{SITE['phone_alt']}</a> ·
            <a href="tel:{SITE['phone_mob_href']}">{SITE['phone_mob']}</a></div></li>
          <li>{I['mail']}<div><b>Email</b><a href="mailto:{SITE['email']}">{SITE['email']}</a></div></li>
        </ul>
      </div>
    </div>{more}"""


def compare_section(depth, *, heading=True):
    rows = ""
    for t in TREATMENTS:
        m = t["matrix"]
        cells = "".join(f"<td>{m[key]}</td>" for key, _label in MATRIX_COLS)
        rows += f"""<tr data-invasive="{t['kind']}">
      <td><a href="{rel(depth)}ypiresies/{t['slug']}/">{t['title']}</a>
        <div class="tiny muted" style="margin-top:.2rem">{t['short']}</div>
        <div style="margin-top:.5rem"><span class="tag tag--{t['kind']}">{KIND_LABELS[t['kind']]}</span></div></td>
      {cells}</tr>"""
    heads = "".join(f'<th scope="col">{label}</th>' for _key, label in MATRIX_COLS)
    filters = "".join(
        f'<button class="filter" data-filter="{k}" aria-pressed="false">{v}</button>'
        for k, v in KIND_LABELS.items())
    head_html = ""
    if heading:
        head_html = """<div class="sec-head sec-head--split">
      <div class="stack"><p class="eyebrow">Σύγκριση</p><h2>Τι σημαίνει η κάθε υπηρεσία στην πράξη.</h2></div>
      <p class="lede">Πόσο κρατάει, τι θα νιώσετε, πόσο συχνά χρειάζεται και τι γίνεται μόλις
        σηκωθείτε από την πολυθρόνα.</p>
    </div>"""
    return f"""<section class="section" id="compare">
  <div class="wrap">
    {head_html}
    <div class="compare">
      <div class="compare__filters" role="group" aria-label="Φίλτρα υπηρεσιών">
        <button class="filter" data-filter="all" aria-pressed="true">Όλες</button>
        {filters}
        <span class="tiny muted" data-compare-count style="align-self:center;margin-left:.5rem">{len(TREATMENTS)} υπηρεσίες</span>
      </div>
      <div class="compare__scroll">
        <table>
          <caption class="vh">Σύγκριση υπηρεσιών</caption>
          <thead><tr><th scope="col">Υπηρεσία</th>{heads}</tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
      <p class="tiny muted" style="margin-top:1rem">Κάθε πόδι είναι διαφορετικό.
        Το τελικό πλάνο ορίζεται μετά από κλινική εξέταση.</p>
    </div>
  </div>
</section>"""


# ── Home: entry screen → «Ποιοι είμαστε» → motto → contact ──────────────────
def bio_block():
    """The short, dated CV under «Ποιοι είμαστε», with a «Λεπτομέρειες» button
    that opens the complete CV (data.py → BIO_FULL)."""
    def rows(items):
        return "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in items)

    def entry(e):
        when = f'<span class="cv__when">{e["when"]}</span>' if e.get("when") else ""
        sub_ = f'<p class="cv__sub">{e["sub"]}</p>' if e.get("sub") else ""
        text = e["text"]
        body = (("<ul class=\"cv__bullets\">" + "".join(f"<li>{x}</li>" for x in text) + "</ul>")
                if isinstance(text, list) else f"<p>{text}</p>")
        return f"""<li class="cv__entry">
            <div class="cv__head"><h4>{e["title"]}</h4>{when}</div>
            {sub_}{body}
          </li>"""

    sections = "".join(f"""<section class="cv__section">
          <h3>{heading}</h3>
          <ul class="cv__list">{"".join(entry(e) for e in entries)}</ul>
        </section>""" for heading, entries in BIO_FULL)

    return f"""<div class="about__bio" id="viografiko">
      <p class="eyebrow">Βιογραφικό</p>
      <h2 class="about__bio-title">Εν συντομία</h2>
      <ul class="timeline">{rows(BIO_BRIEF)}</ul>
      <details class="more" id="viografiko-plires">
        <summary><span class="more__open">Λεπτομέρειες</span><span class="more__shut">Λιγότερα</span>
          {I['chev']}</summary>
        <div class="cv">
          <p class="cv__profile">{BIO_FULL_PROFILE}</p>
          {sections}
        </div>
      </details>
    </div>"""


def build_home():
    d = 0
    p = PRACTITIONER
    paras = [html.escape(x) for x in p["about"]]
    paras[0] = '<span class="qm">«</span>' + paras[0]
    paras[-1] = paras[-1] + '<span class="qm">»</span>'
    about_html = "".join(f"<p>{x}</p>" for x in paras)

    # The entry screen (Oct 2026, second round of her notes): the ensō ring
    # nearly filling the screen, «ENSŌ / FOOT CLINIC» centred inside it with a
    # round ENTER button under the name. No hairline grid, no lines under the
    # ring. The whole screen is one button; a tap anywhere (or Enter) fades it
    # out and the page starts straight on «Ποιοι είμαστε». It is skipped when
    # the page is opened on an anchor (the menu links to /#poioi-eimaste) or
    # has already been passed once in this browser session — see gate() in
    # enso.js.
    body = f"""<button class="gate" type="button" aria-label="Είσοδος στον ιστότοπο του Ensō Foot Clinic">
  <span class="hero__aurora" aria-hidden="true"><i></i><i></i><i></i></span>
  <span class="gate__glow" aria-hidden="true"></span>
  <span class="gate__inner">
    <span class="gate__ring">
      {img("enso-badge-light.svg", "", 400, 400, 0, cls="gate__mark", priority=True)}
      <span class="gate__core">
        <span class="gate__lockup">
          <span class="gate__word">Ensō</span>
          <span class="gate__word2">Foot Clinic</span>
        </span>
        <span class="gate__enter">Enter</span>
      </span>
    </span>
  </span>
</button>

<section class="section about" id="poioi-eimaste">
  <div class="wrap">
    <div class="about__grid">
      <div class="about__who">
        <p class="eyebrow">Ποιοι είμαστε</p>
        <h1>{p['name']}</h1>
        <p class="about__role">{html.escape(p['role'])}</p>
        {img("enso-badge.svg", "Το σήμα ensō του Ensō Foot Clinic", 400, 400, 0, cls="about__mark")}
      </div>
      <div class="about__text">{about_html}</div>
    </div>
    {bio_block()}
  </div>
</section>

{motto_band(d)}

<section class="section section--mist" id="epikoinonia">
  <div class="wrap">
    <div class="sec-head sec-head--split">
      <div class="stack"><p class="eyebrow">Επικοινωνία</p>
        <h2>Περαία Θεσσαλονίκης και Καλλιθέα Αθήνας.</h2></div>
      <p class="lede">Τα ραντεβού κλείνονται τηλεφωνικά. Καλέστε στο κέντρο που σας
        εξυπηρετεί και θα βρούμε ώρα μαζί.</p>
    </div>
    {contact_cards(d)}
  </div>
</section>"""

    ld = [org_graph(),
          {"@context": "https://schema.org", "@type": "WebSite", "name": SITE["name"],
           "url": SITE["domain"] + "/", "inLanguage": "el",
           "publisher": {"@id": CLINIC_ID}},
          {"@context": "https://schema.org", "@type": "AboutPage",
           "name": "Ποιοι είμαστε — Ensō Foot Clinic", "inLanguage": "el",
           "url": SITE["domain"] + "/", "mainEntity": {"@id": PODOLOGIST_ID}}]

    page(path="", title="Ensō Foot Clinic — Ποδολόγος σε Περαία Θεσσαλονίκης & Αθήνα",
         desc="Ελπινίκη Χριστοδούλου, εξειδικευμένη ποδολόγος, ιδρύτρια του Ensō Foot "
              "Clinic. Ποδολογικά κέντρα στην Περαία Θεσσαλονίκης και στην Καλλιθέα Αθήνας.",
         depth=d, body=body, jsonld=ld, active="about", body_class="page--home")


# ── Services ────────────────────────────────────────────────────────────────
def doc_layout(depth, body_html, aside_html=""):
    return f"""<section class="section section--tight">
  <div class="wrap">
    <div class="doc">
      <article class="prose">{body_html}</article>
      <aside class="doc__aside" data-toc-wrap>
        <div>
          <p class="eyebrow" style="margin-bottom:.9rem">Σε αυτή τη σελίδα</p>
          <nav class="toc" aria-label="Περιεχόμενα"></nav>
        </div>
        {aside_html}
      </aside>
    </div>
  </div>
</section>"""


def aside_cta(depth):
    return f"""<div class="card" style="background:var(--mist-2);border-color:transparent">
  <h3 style="font-size:1.05rem">Έχετε ερώτηση;</h3>
  <p class="small">Δεν χρειάζεται να ξέρετε τι να ρωτήσετε. Πείτε μας τι νιώθετε.</p>
  <a class="btn btn--sm btn--block" href="tel:{SITE['phone_href']}">{I['phone']} {SITE['phone']}</a>
  <a class="btn btn--ghost btn--sm btn--block" href="tel:{SITE['phone_alt_href']}">Αθήνα · {SITE['phone_alt']}</a>
</div>"""


def build_treatment(t):
    d, slug = 2, t["slug"]
    body, faq_title, pairs = prose(slug, d)
    faq_html, faq_ld = faq_block(faq_title, pairs, f"faq-{slug}")
    crumb_html, crumb_ld = crumbs([("Υπηρεσίες", rel(d) + "ypiresies/"), (t["title"], None)], d)
    m = t["matrix"]
    facts = [(label, m[key]) for key, label in MATRIX_COLS] + [("Πόνος", m["pain"])]
    facts_html = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in facts)
    treats_html = "".join(f'<span class="chip">{x}</span>' for x in t["treats"])
    head_block = f"""<section class="page-head">
  <div class="wrap">
    {crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack">
        <p class="eyebrow">{t['short']}</p>
        <h1>{t['title']}</h1>
      </div>
      <div class="stack">
        <p class="lede" style="font-size:1.06rem">{t['lead']}</p>
        <div class="pill-row">{treats_html}</div>
      </div>
    </div>
  </div>
</section>

<section class="creds">
  <div class="wrap"><ul class="creds__list creds__list--facts">{facts_html}</ul></div>
</section>"""
    ld = [crumb_ld, org_graph(),
          {"@context": "https://schema.org", "@type": "MedicalTherapy",
           "name": t["title"], "alternateName": t["short"], "description": t["lead"],
           "url": f"{SITE['domain']}/ypiresies/{slug}/",
           "bodyLocation": "Άκρο πόδι",
           "howPerformed": m["setting"],
           "preparation": m["sensation"],
           "followup": m["after"],
           "relevantSpecialty": "Podiatric",
           "provider": {"@id": CLINIC_ID},
           "performer": {"@id": PODOLOGIST_ID},
           "indication": [{"@type": "MedicalIndication", "name": x} for x in t["treats"]]}]
    if faq_ld:
        ld.append(faq_ld)
    if t["kind"] == "prevention" and slug == TREATMENTS[0]["slug"]:
        body += f'<p class="disclaimer disclaimer--inline">{SERVICES_DISCLAIMER}</p>'
    page(path=f"ypiresies/{slug}/",
         title=seo_title(f"{t['title']} — {t['short']}"),
         desc=local_desc(t.get("meta") or meta_desc(slug, t["lead"])), depth=d,
         body=head_block + doc_layout(d, body, aside_cta(d)) + faq_html + motto_band(d),
         jsonld=ld, active="treatments")


def build_treatments_hub():
    d = 1
    cards = "".join(f"""<a class="card" href="{rel(d)}ypiresies/{t['slug']}/" data-reveal="{i*50}">
      <p class="card__kicker">{t['short']}</p><h3>{t['title']}</h3><p>{t['lead']}</p>
      <p class="card__foot"><span class="link-more">Αναλυτικά</span></p></a>"""
      for i, t in enumerate(TREATMENTS))
    crumb_html, crumb_ld = crumbs([("Υπηρεσίες", None)], d)
    body = f"""<section class="page-head">
  <div class="wrap">
    {crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack"><p class="eyebrow">Υπηρεσίες</p>
        <h1>Ανώδυνα, αναίμακτα, με αποστειρωμένα εργαλεία.</h1></div>
      <p class="lede">Έξι υπηρεσίες που καλύπτουν την αξιολόγηση, την πρόληψη και τη
        θεραπεία. Ανοίξτε την καθεμία για να δείτε τι περιλαμβάνει.</p>
    </div>
  </div>
</section>
<section class="section section--tight">
  <div class="wrap">
    <div class="grid grid--3">{cards}</div>
    <p class="disclaimer">{SERVICES_DISCLAIMER}</p>
  </div>
</section>"""
    ld = [crumb_ld, org_graph(),
          {"@context": "https://schema.org", "@type": "ItemList",
           "name": "Υπηρεσίες — Ensō Foot Clinic",
           "itemListElement": [
               {"@type": "ListItem", "position": i,
                "url": f"{SITE['domain']}/ypiresies/{t['slug']}/", "name": t["title"]}
               for i, t in enumerate(TREATMENTS, start=1)]}]
    page(path="ypiresies/", title="Υπηρεσίες ποδολογίας — Περαία & Αθήνα | Ensō Foot Clinic",
         desc="Κλινική συμβουλευτική και εμβιομηχανική αξιολόγηση, κλινική ποδολογική "
              "φροντίδα, αφαίρεση κάλων, θεραπεία ξηροδερμίας, ορθονυχία, έλεγχος "
              "διαβητικού ποδιού. Περαία Θεσσαλονίκης και Αθήνα.",
         depth=d, body=body, jsonld=ld, active="treatments")


# ── Seminars ─────────────────────────────────────────────────────────────────
# There is no booking platform yet, so registration composes an email — swap
# `register` in data.py for ("url", href) and every open seminar hands off to the
# platform instead, with no template change here.
def _seminar_meta(sem):
    rows = [("Ημερομηνία", sem["human"]),
            ("Μορφή", SEMINAR_MODES[sem["mode"]]),
            ("Πού", sem["venue"]),
            ("Διάρκεια", sem["duration"]),
            ("Επίπεδο", sem["level"])]
    if sem.get("seats"):
        rows.append(("Θέσεις", f"{sem['seats']} συμμετέχοντες"))
    if sem.get("price"):
        rows.append(("Συμμετοχή", sem["price"]))
    return rows


def _seminar_cta(sem, *, block=False):
    kind, value = sem["register"]
    cls = "btn btn--block" if block else "btn"
    if kind == "url":
        return (f'<a class="{cls}" href="{value}" target="_blank" rel="noopener">'
                f'Εγγραφή στο σεμινάριο</a>')
    if kind == "pay":
        return (f'<a class="{cls}" href="{rel(2)}seminaria/egrafi/?s={sem["slug"]}">'
                f'Εγγραφή &amp; πληρωμή</a>')
    if kind == "email":
        subject = urllib.parse.quote(f"Εγγραφή — {sem['title']}")
        body = urllib.parse.quote(
            f"Θα ήθελα να δηλώσω συμμετοχή στο σεμινάριο «{sem['title']}»"
            f" ({sem['human']}).\n\nΟνοματεπώνυμο:\nΙδιότητα:\nΤηλέφωνο:")
        return f'<a class="{cls}" href="mailto:{value}?subject={subject}&amp;body={body}">Δήλωση συμμετοχής</a>'
    return (f'<a class="{cls} btn--ghost" href="{SEMINAR_NOTIFY}">'
            f'Ενημερώστε με για το επόμενο</a>')


def _seminar_card(sem, depth):
    label, tone = SEMINAR_STATUS[sem["status"]]
    facts = "".join(f"<li><b>{a}</b><span>{b}</span></li>"
                    for a, b in _seminar_meta(sem)[:3])
    return f"""<article class="sem-card">
      <div class="sem-card__head">
        <span class="tag tag--{tone}">{label}</span>
        <p class="card__kicker" style="margin:0">{sem['kicker']}</p>
      </div>
      <h3><a href="{rel(depth)}seminaria/{sem['slug']}/">{sem['title']}</a></h3>
      <p>{sem['lead']}</p>
      <ul class="sem-card__facts">{facts}</ul>
      <p class="card__foot"><a class="link-more" href="{rel(depth)}seminaria/{sem['slug']}/">Αναλυτικά</a></p>
    </article>"""


def _seminar_ld(sem):
    """EducationEvent so it can surface as an event, Course so the syllabus reads."""
    kind, value = sem["register"]
    offer = {"@type": "Offer",
             "availability": ("https://schema.org/InStock" if sem["status"] == "open"
                              else "https://schema.org/SoldOut" if sem["status"] == "past"
                              else "https://schema.org/PreOrder"),
             "url": value if kind == "url"
                    else f"{SITE['domain']}/seminaria/{sem['slug']}/"}
    # price and priceCurrency travel together or not at all — a currency on its
    # own makes Google drop the whole offer.
    if sem.get("price_eur") is not None:
        offer["price"] = sem["price_eur"]
        offer["priceCurrency"] = "EUR"
    location = ({"@type": "VirtualLocation", "url": SITE["domain"] + "/seminaria/"}
                if sem["mode"] == "online"
                else {"@type": "Place", "name": sem["venue"],
                      "address": _address(), "geo": _geo()})
    return {
        "@context": "https://schema.org", "@type": "EducationEvent",
        "name": sem["title"], "description": sem["lead"],
        "startDate": sem["start"], "endDate": sem["end"],
        "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": {
            "online": "https://schema.org/OnlineEventAttendanceMode",
            "onsite": "https://schema.org/OfflineEventAttendanceMode",
            "hybrid": "https://schema.org/MixedEventAttendanceMode"}[sem["mode"]],
        "location": location,
        "inLanguage": "el",
        "url": f"{SITE['domain']}/seminaria/{sem['slug']}/",
        "organizer": {"@id": CLINIC_ID},
        "performer": {"@id": PODOLOGIST_ID},
        "offers": offer,
        "about": {"@type": "Course", "name": sem["title"],
                  "description": sem["lead"],
                  "provider": {"@id": CLINIC_ID},
                  "teaches": sem.get("topics", []),
                  "educationalLevel": sem["level"],
                  "inLanguage": "el",
                  "hasCourseInstance": {
                      "@type": "CourseInstance",
                      "courseMode": SEMINAR_MODES[sem["mode"]],
                      "startDate": sem["start"], "endDate": sem["end"],
                      "location": location}},
    }


def build_seminar(sem):
    d, slug = 2, sem["slug"]
    body, faq_title, pairs = prose(slug, d)
    faq_html, faq_ld = faq_block(faq_title, pairs, f"faq-{slug}")
    crumb_html, crumb_ld = crumbs([("Σεμινάρια", rel(d) + "seminaria/"), (sem["title"], None)], d)
    label, tone = SEMINAR_STATUS[sem["status"]]
    facts = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in _seminar_meta(sem))
    topics = "".join(f"<li>{t}</li>" for t in sem.get("topics", []))
    aside = f"""<div class="card" style="background:var(--mist-2);border-color:transparent">
  <h3 style="font-size:1.05rem">{'Συμμετοχή' if sem['status'] != 'past' else 'Επόμενο σεμινάριο'}</h3>
  <p class="small">{'Οι θέσεις είναι περιορισμένες.' if sem.get('seats') else 'Θα σας απαντήσουμε την ίδια ή την επόμενη εργάσιμη.'}</p>
  {_seminar_cta(sem, block=True)}
</div>"""
    head_block = f"""<section class="page-head">
  <div class="wrap">
    {crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack">
        <div class="pill-row"><span class="tag tag--{tone}">{label}</span></div>
        <p class="eyebrow">{sem['kicker']}</p>
        <h1>{sem['title']}</h1>
      </div>
      <div class="stack">
        <p class="lede" style="font-size:1.05rem">{sem['lead']}</p>
        {_seminar_cta(sem)}
      </div>
    </div>
  </div>
</section>

<section class="creds">
  <div class="wrap"><ul class="creds__list creds__list--facts">{facts}</ul></div>
</section>"""
    topics_html = f"""<section class="section section--tight">
  <div class="wrap wrap--narrow">
    <div class="sec-head"><p class="eyebrow">Περιεχόμενο</p><h2>Τι καλύπτει.</h2></div>
    <ul class="bullets">{topics}</ul>
  </div>
</section>""" if topics else ""
    ld = [crumb_ld, org_graph(), _seminar_ld(sem)]
    if faq_ld:
        ld.append(faq_ld)
    page(path=f"seminaria/{slug}/", title=seo_title(sem["title"]),
         desc=meta_desc(slug, sem["lead"]), depth=d,
         body=head_block + doc_layout(d, body, aside) + topics_html + faq_html + motto_band(d),
         jsonld=ld, active="seminars")


def build_seminars_hub():
    d = 1
    upcoming = [x for x in SEMINARS if x["status"] in ("open", "announced")]
    past = [x for x in SEMINARS if x["status"] == "past"]
    body_html, faq_title, pairs = prose("seminaria", d)
    faq_html, faq_ld = faq_block(faq_title, pairs, "faq-seminaria")

    if upcoming:
        next_block = f"""<div class="grid grid--{min(len(upcoming), 2)}">
      {"".join(_seminar_card(x, d) for x in upcoming)}</div>"""
    else:
        # An empty programme is the honest state today, so it is designed rather
        # than left to look broken.
        next_block = f"""<div class="sem-empty">
      <div class="stack">
        <p class="eyebrow">Καμία προγραμματισμένη ημερομηνία</p>
        <h3>Το επόμενο σεμινάριο δεν έχει ανακοινωθεί ακόμη.</h3>
        <p class="lede" style="font-size:1rem">Αφήστε μας τα στοιχεία σας και θα είστε
          από τους πρώτους που θα ενημερωθούν όταν ανοίξουν οι εγγραφές.</p>
      </div>
      <a class="btn" href="{SEMINAR_NOTIFY}">Δηλώστε ενδιαφέρον</a>
    </div>"""

    past_block = f"""<section class="section section--tight">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Αρχείο</p><h2>Έχουν γίνει.</h2></div>
    <div class="grid grid--{min(len(past), 2)}">{"".join(_seminar_card(x, d) for x in past)}</div>
  </div>
</section>""" if past else ""

    crumb_html, crumb_ld = crumbs([("Σεμινάρια", None)], d)
    body = f"""<section class="page-head">
  <div class="wrap">{crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack"><p class="eyebrow">Εκπαίδευση</p>
        <h1>Σεμινάρια, workshops &amp; masterclasses.</h1></div>
      <p class="lede">Η ίδια δουλειά, από την άλλη πλευρά του τραπεζιού: εκπαίδευση
        επαγγελματιών από το 2002, με σεμινάρια, διδασκαλία σε Ι.ΙΕΚ και χρόνια ως
        Academy Instructor.</p>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Επόμενο</p></div>
    {next_block}
    <p class="small muted" style="margin-top:1.25rem">Εγγραφές και πληρωμή με κάρτα γίνονται από τη σελίδα
      <a href="{rel(d)}seminaria/egrafi/">Εγγραφή &amp; πληρωμή</a>. Διαβάστε την
      <a href="{rel(d)}oroi-chrisis/#politiki-akyrosis">πολιτική ακύρωσης</a> πριν δηλώσετε συμμετοχή.</p>
  </div>
</section>

{past_block}
{doc_layout(d, body_html, aside_cta(d))}
{faq_html}
{motto_band(d)}"""

    ld = [crumb_ld, org_graph(),
          {"@context": "https://schema.org", "@type": "ItemList",
           "name": "Σεμινάρια — Ensō Foot Clinic",
           "itemListElement": [
               {"@type": "ListItem", "position": i,
                "url": f"{SITE['domain']}/seminaria/{x['slug']}/", "name": x["title"]}
               for i, x in enumerate(SEMINARS, start=1)]}]
    if faq_ld:
        ld.append(faq_ld)
    page(path="seminaria/", title="Σεμινάρια ποδολογίας | Ensō Foot Clinic",
         desc="Σεμινάρια, workshops και masterclasses ποδολογίας από την Ελπινίκη "
              "Χριστοδούλου. Δηλώστε ενδιαφέρον για το επόμενο.",
         depth=d, body=body, jsonld=ld, active="seminars")


# ── Contact, terms, 404 ─────────────────────────────────────────────────────
def legal_table():
    """The company details, from data.py. A missing value is shown as pending
    rather than invented, and main() prints a reminder for each one."""
    rows = ""
    for k, v in SITE["legal_rows"]:
        val = (f"<span>{html.escape(v)}</span>" if v
               else '<span class="pending">θα συμπληρωθεί</span>')
        rows += f"<div><b>{k}</b>{val}</div>"
    return f'<div class="legal">{rows}</div>'


def build_contact():
    d = 1
    hours = "".join(f'<div style="display:flex;justify-content:space-between;gap:1rem;'
                    f'border-bottom:1px solid var(--line-soft);padding:.55rem 0">'
                    f'<span>{a}</span><b style="font-weight:560">{b}</b></div>'
                    for a, b in SITE["hours"])

    local_faq = [
        ("Πού ακριβώς βρίσκεται το ποδολογικό κέντρο;",
         f"<p>Στη Θεσσαλονίκη, στη Ρωμανού 11 στην Περαία, στον <b>3ο όροφο</b>. Στην Αθήνα, "
         f"στη <b>Λεωφ. Ελ. Βενιζέλου 180</b> στην Καλλιθέα, στον <b>1ο όροφο</b>. Οι χάρτες σε αυτή τη σελίδα "
         "ανοίγουν απευθείας οδηγίες πλοήγησης σε Google Maps, Waze ή Moovit.</p>"),
        ("Δέχεστε ραντεβού και στην Αθήνα;",
         f"<p>Ναι, στο ποδολογικό κέντρο της Καλλιθέας, Ελ. Βενιζέλου 180. Καλέστε στο "
         f"<a href=\"tel:{SITE['phone_alt_href']}\">{SITE['phone_alt']}</a> "
         f"ή στο <a href=\"tel:{SITE['phone_mob_href']}\">{SITE['phone_mob']}</a> για "
         "διαθεσιμότητα.</p>"),
        ("Χρειάζομαι ραντεβού ή μπορώ να περάσω;",
         f"<p>Χρειάζεται ραντεβού — το ποδολογικό κέντρο λειτουργεί κατόπιν συνεννόησης. Καλέστε στο "
         f"{SITE['phone']} για τη Θεσσαλονίκη ή στο {SITE['phone_alt']} για την Αθήνα. "
         "Τα ραντεβού κλείνονται μόνο τηλεφωνικά — έτσι ξέρετε αμέσως τι ώρα υπάρχει, "
         "χωρίς αναμονή για απάντηση.</p>"),
        ("Τι να φέρω μαζί μου στο πρώτο ραντεβού;",
         "<p>Τα <b>παπούτσια που φοράτε καθημερινά</b> — όχι τα «καλά». Είναι η πιο χρήσιμη "
         "πληροφορία που μπορείτε να δώσετε. Επίσης τη λίστα των φαρμάκων σας, και αν έχετε "
         "διαβήτη, τις τελευταίες εξετάσεις σακχάρου και HbA1c.</p>"),
    ]
    faq_html, faq_ld = faq_block("Συχνές ερωτήσεις για την επίσκεψη", local_faq, "faq-visit")

    crumb_html, crumb_ld = crumbs([("Επικοινωνία", None)], d)
    body = f"""<section class="page-head">
  <div class="wrap">{crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack"><p class="eyebrow">Επικοινωνία · Θεσσαλονίκη &amp; Αθήνα</p>
        <h1>Περαία Θεσσαλονίκης και Καλλιθέα Αθήνας.</h1></div>
      <p class="lede">Δύο ποδολογικά κέντρα, ένα τηλέφωνο για το καθένα. Τα ραντεβού
        κλείνονται τηλεφωνικά — καλέστε μας και θα βρούμε ώρα μαζί.</p>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="contact-grid">
      <div class="stack" style="justify-items:stretch">
        <ul class="info-list">
          <li>{I['pin']}<div><b>Θεσσαλονίκη</b>
            <a href="{SITE['map']}" target="_blank" rel="noopener">{SITE['street']}, {SITE['postcode']} {SITE['locality']} {SITE['region']}</a></div></li>
          <li>{I['stairs']}<div><b>Όροφος</b><span>{SITE['floor']}</span></div></li>
          <li>{I['phone']}<div><b>Τηλέφωνο Θεσσαλονίκης</b><a href="tel:{SITE['phone_href']}">{SITE['phone']}</a></div></li>
          <li>{I['pin']}<div><b>Αθήνα</b>
            <a href="{SITE['map_athens']}" target="_blank" rel="noopener">{SITE['street_athens']}, {SITE['postcode_athens']} Καλλιθέα</a></div></li>
          <li>{I['stairs']}<div><b>Όροφος</b><span>{SITE['floor_athens']}</span></div></li>
          <li>{I['phone']}<div><b>Τηλέφωνα Αθήνας</b>
            <a href="tel:{SITE['phone_alt_href']}">{SITE['phone_alt']}</a> ·
            <a href="tel:{SITE['phone_mob_href']}">{SITE['phone_mob']}</a></div></li>
          <li>{I['mail']}<div><b>Email</b><a href="mailto:{SITE['email']}">{SITE['email']}</a></div></li>
          <li>{I['clock']}<div style="width:100%"><b>Ωράριο</b><div style="margin-top:.35rem">{hours}</div></div></li>
        </ul>
        <a class="btn btn--block" href="tel:{SITE['phone_href']}">{I['phone']} Θεσσαλονίκη · {SITE['phone']}</a>
        <a class="btn btn--ghost btn--block" href="tel:{SITE['phone_alt_href']}">{I['phone']} Αθήνα · {SITE['phone_alt']}</a>
      </div>
      <div class="stack" style="justify-items:stretch">
        <figure class="mapcard">
          <iframe class="map" loading="lazy" title="Χάρτης — Ensō Foot Clinic, Ρωμανού 11, Περαία Θεσσαλονίκης"
            referrerpolicy="no-referrer-when-downgrade" src="{SITE['embed'].replace('&', '&amp;')}"></iframe>
          <figcaption>
            <div><b>Θεσσαλονίκη</b><span>{SITE['street']}, {SITE['postcode']} {SITE['locality']} · {SITE['floor']}</span></div>
            <div class="pill-row">
              <a class="chip" href="{SITE['map_full']}" target="_blank" rel="noopener">{I['pin']} Google Maps</a>
              <a class="chip" href="{SITE['waze']}" target="_blank" rel="noopener">Waze</a>
              <a class="chip" href="{SITE['moovit']}" target="_blank" rel="noopener">Moovit</a>
            </div>
          </figcaption>
        </figure>
        <figure class="mapcard">
          <iframe class="map" loading="lazy" title="Χάρτης — Ensō Foot Clinic, Λεωφ. Ελ. Βενιζέλου 180, Καλλιθέα Αθήνας"
            referrerpolicy="no-referrer-when-downgrade" src="{SITE['embed_athens'].replace('&', '&amp;')}"></iframe>
          <figcaption>
            <div><b>Αθήνα</b><span>{SITE['street_athens']}, {SITE['postcode_athens']} Καλλιθέα · {SITE['floor_athens']}</span></div>
            <div class="pill-row">
              <a class="chip" href="{SITE['map_athens_full']}" target="_blank" rel="noopener">{I['pin']} Google Maps</a>
            </div>
          </figcaption>
        </figure>
      </div>
    </div>
  </div>
</section>
{faq_html}
{motto_band(d)}"""

    place_ld = {
        "@context": "https://schema.org", "@type": "ContactPage",
        "name": "Επικοινωνία — Ensō Foot Clinic",
        "url": f"{SITE['domain']}/epikoinonia/",
        "inLanguage": "el", "about": {"@id": CLINIC_ID},
        "mainEntity": {"@id": CLINIC_ID},
    }
    ld = [crumb_ld, org_graph(), place_ld]
    if faq_ld:
        ld.append(faq_ld)
    page(path="epikoinonia/",
         title="Επικοινωνία & ραντεβού — Περαία, Αθήνα | Ensō Foot Clinic",
         desc=f"Ensō Foot Clinic — {SITE['address']}, {SITE['postcode']} Περαία. "
              f"Θεσσαλονίκη {SITE['phone']} · Αθήνα {SITE['phone_alt']}. Κατόπιν ραντεβού.",
         depth=d, body=body, jsonld=ld, active="contact")


def build_company():
    """The company details (ΓΕΜΗ, ΑΦΜ…) on their own page, linked only from the
    foot of every page — she asked for them out of the contact page, where
    «μόνο αν πατήσει κάποιος θα μπει μέσα να το δει» (Oct 2026)."""
    d = 1
    crumb_html, crumb_ld = crumbs([("Στοιχεία επιχείρησης", None)], d)
    body = f"""<section class="page-head">
  <div class="wrap wrap--narrow">{crumb_html}
    <p class="eyebrow">Στοιχεία επιχείρησης</p>
    <h1 style="font-size:clamp(1.9rem,1.3rem+2.2vw,2.8rem)">Ταυτότητα της επιχείρησης</h1>
    <p class="lede" style="margin-top:.9rem">Τα νόμιμα στοιχεία του ποδολογικού κέντρου,
      όπως αναγράφονται στα παραστατικά του.</p>
  </div>
</section>
<section class="section section--tight"><div class="wrap wrap--narrow">
  {legal_table()}
  <p class="small muted" style="margin-top:1.5rem">Για ραντεβού και οδηγίες πρόσβασης, δείτε την
    <a href="{rel(d)}epikoinonia/">Επικοινωνία</a>.</p>
</div></section>"""
    page(path="stoicheia-epicheirisis/", title="Στοιχεία επιχείρησης | Ensō Foot Clinic",
         desc="Επωνυμία, ΑΦΜ, ΔΟΥ και αριθμός ΓΕΜΗ της ENSO FOOT CLINIC ΜΟΝΟΠΡΟΣΩΠΗ Ι.Κ.Ε.",
         depth=d, body=body, jsonld=[crumb_ld])


def build_terms():
    d = 1
    body_html, _, _ = prose("oroi-chrisis", d)
    cancel_html, _, _ = prose("politiki-akyrosis", d)
    body_html = (body_html.replace("<!--LEGAL-->", legal_table())
                          .replace("<!--CANCELLATION-->", cancel_html))
    crumb_html, crumb_ld = crumbs([("Όροι χρήσης & απόρρητο", None)], d)
    body = f"""<section class="page-head">
  <div class="wrap wrap--narrow">{crumb_html}
    <h1 style="font-size:clamp(1.9rem,1.3rem+2.2vw,2.8rem)">Όροι χρήσης &amp; πολιτική απορρήτου</h1>
    <p class="lede" style="margin-top:.9rem">Τελευταία ενημέρωση: {TODAY}</p>
  </div>
</section>
<section class="section section--tight"><div class="wrap wrap--narrow">
  <article class="prose">{body_html}</article></div></section>"""
    page(path="oroi-chrisis/", title="Όροι χρήσης & πολιτική απορρήτου | Ensō Foot Clinic",
         desc="Όροι χρήσης, πολιτική απορρήτου και διαχείριση προσωπικών δεδομένων "
              "για τον ιστότοπο του Ensō Foot Clinic.",
         depth=d, body=body, jsonld=[crumb_ld])


# ── Seminar checkout ─────────────────────────────────────────────────────────
# One page for every paid seminar: /seminaria/egrafi/?s=<slug>. Built to the
# Visa/MasterCard rules Worldline quoted for the ePOS application (Oct 2026):
# a consent checkbox with the exact English wording, and the Terms and the
# Cancellation Policy opening inline, expand/collapse and scrollable, directly
# under the checkbox — never a redirect to another page.
CONSENT_WORDING = "I have read and agree to Terms and Conditions &amp; Cancellation Policy"


def _legal_fold(key, label_en, label_el, inner_html):
    return f"""<details class="fold" id="fold-{key}">
  <summary><span><b>{label_en}</b> · {label_el}</span>{I['chev']}</summary>
  <div class="fold__scroll prose prose--compact" tabindex="0" aria-label="{label_el}">{inner_html}</div>
</details>"""


def build_checkout():
    d = 2
    payable = [s for s in SEMINARS if s["status"] in ("open", "announced")
               and (s.get("price_eur") or 0) > 0]
    crumb_html, crumb_ld = crumbs([("Σεμινάρια", rel(d) + "seminaria/"),
                                   ("Εγγραφή & πληρωμή", None)], d)
    terms_html, _, _ = prose("oroi-chrisis", d)
    cancel_html, _, _ = prose("politiki-akyrosis", d)
    terms_html = (terms_html.replace("<!--LEGAL-->", legal_table())
                            .replace("<!--CANCELLATION-->", cancel_html))

    if payable:
        options = "".join(
            f'<option value="{s["slug"]}" data-title="{html.escape(s["title"], quote=True)}" '
            f'data-when="{html.escape(s["human"], quote=True)}" data-price="{s["price_eur"]}" '
            f'data-mode="{SEMINAR_MODES[s["mode"]]}">{s["title"]} — {s["human"]}</option>'
            for s in payable)
        select = f'<select id="seminar" name="seminar" required>{options}</select>'
        empty_note = ""
    else:
        select = ('<select id="seminar" name="seminar" required disabled>'
                  '<option value="">— Δεν υπάρχει σεμινάριο με ανοιχτές εγγραφές —</option></select>')
        empty_note = (f'<p class="form-note" role="status">Δεν υπάρχει αυτή τη στιγμή σεμινάριο με '
                      f'ανοιχτές εγγραφές. <a href="{SEMINAR_NOTIFY}">Δηλώστε ενδιαφέρον</a> και '
                      f'θα ενημερωθείτε πρώτοι.</p>')

    action = PAYMENT["action"] or ""
    pending = "" if PAYMENT["action"] else ' data-pending="1"'
    body = f"""<section class="page-head">
  <div class="wrap">{crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack"><p class="eyebrow">Σεμινάρια</p>
        <h1>Εγγραφή &amp; πληρωμή.</h1></div>
      <p class="lede">Συμπληρώστε τα στοιχεία σας, διαβάστε και αποδεχθείτε τους όρους και
        ολοκληρώστε την πληρωμή με κάρτα στο ασφαλές περιβάλλον της {PAYMENT['provider']}.</p>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <form class="checkout" method="post" action="{action}"{pending} novalidate="">
      <input type="hidden" name="currency" value="{PAYMENT['currency']}">
      <input type="hidden" name="amount" id="amount" value="">
      <div class="checkout__main">
        <fieldset class="fieldset">
          <legend>1. Σεμινάριο</legend>
          <div class="field">
            <label for="seminar">Επιλέξτε σεμινάριο</label>
            {select}
          </div>
          {empty_note}
        </fieldset>

        <fieldset class="fieldset">
          <legend>2. Στοιχεία συμμετέχοντα</legend>
          <div class="field-grid">
            <div class="field field--full">
              <label for="name">Ονοματεπώνυμο</label>
              <input id="name" name="name" type="text" autocomplete="name" required>
            </div>
            <div class="field">
              <label for="email">Email</label>
              <input id="email" name="email" type="email" autocomplete="email" required>
              <small>Εδώ θα σταλεί η επιβεβαίωση και ο σύνδεσμος παρακολούθησης.</small>
            </div>
            <div class="field">
              <label for="phone">Τηλέφωνο</label>
              <input id="phone" name="phone" type="tel" autocomplete="tel" required>
            </div>
            <div class="field field--full">
              <label for="role">Ιδιότητα</label>
              <select id="role" name="role" required>
                <option value="podologos">Ποδολόγος</option>
                <option value="spoudastis">Σπουδαστής/-τρια ποδολογίας</option>
                <option value="ygeia">Άλλος επαγγελματίας υγείας</option>
                <option value="allo">Άλλο</option>
              </select>
            </div>
          </div>
          <label class="check">
            <input type="checkbox" id="invoice" name="invoice" value="1">
            <span>Θέλω τιμολόγιο (αντί για απόδειξη)</span>
          </label>
          <div class="field-grid invoice-fields" hidden>
            <div class="field field--full">
              <label for="company">Επωνυμία</label>
              <input id="company" name="company" type="text" autocomplete="organization">
            </div>
            <div class="field">
              <label for="vat">ΑΦΜ</label>
              <input id="vat" name="vat" type="text" inputmode="numeric" pattern="[0-9]{{9}}">
            </div>
            <div class="field">
              <label for="tax-office">ΔΟΥ</label>
              <input id="tax-office" name="tax_office" type="text">
            </div>
          </div>
        </fieldset>

        <fieldset class="fieldset">
          <legend>3. Όροι &amp; πληρωμή</legend>
          <label class="check check--consent">
            <input type="checkbox" id="agree" name="agree" value="1" required>
            <span>{CONSENT_WORDING}<small>Έχω διαβάσει και αποδέχομαι τους Όρους &amp; Προϋποθέσεις
              και την Πολιτική Ακύρωσης.</small></span>
          </label>
          <div class="folds">
            {_legal_fold("terms", "Terms and Conditions", "Όροι &amp; Προϋποθέσεις", terms_html)}
            {_legal_fold("cancellation", "Cancellation Policy", "Πολιτική Ακύρωσης", cancel_html)}
          </div>
        </fieldset>
      </div>

      <aside class="checkout__aside">
        <div class="order">
          <p class="eyebrow" style="margin-bottom:.6rem">Η εγγραφή σας</p>
          <h3 class="order__title" data-order="title">{payable[0]['title'] if payable else 'Σεμινάριο'}</h3>
          <p class="small muted" data-order="when">{payable[0]['human'] if payable else '—'}</p>
          <dl class="order__rows">
            <div><dt>Συμμετοχή</dt><dd><span data-order="price">{payable[0]['price_eur'] if payable else '—'}</span> €</dd></div>
            <div class="order__total"><dt>Σύνολο</dt><dd><span data-order="total">{payable[0]['price_eur'] if payable else '—'}</span> €</dd></div>
          </dl>
          <p class="small muted">Τελική τιμή. Εκδίδεται νόμιμο παραστατικό από την {SITE['legal']}.</p>
          <button class="btn btn--block" type="submit" disabled>Συνέχεια στην ασφαλή πληρωμή</button>
          <p class="form-note" data-pending-note hidden>{PAYMENT['pending_note']}</p>
          <p class="order__secure small">Η πληρωμή γίνεται στο περιβάλλον της {PAYMENT['provider']}
            (Visa, Mastercard). Τα στοιχεία της κάρτας σας δεν περνούν από τον ιστότοπό μας.</p>
          <p class="small"><a href="{rel(d)}oroi-chrisis/">Όροι χρήσης &amp; απόρρητο</a> ·
            <a href="{rel(d)}oroi-chrisis/#politiki-akyrosis">Πολιτική ακύρωσης</a></p>
        </div>
      </aside>
    </form>
  </div>
</section>"""
    page(path="seminaria/egrafi/", title="Εγγραφή & πληρωμή σεμιναρίου | Ensō Foot Clinic",
         desc="Δηλώστε συμμετοχή σε σεμινάριο ποδολογίας του Ensō Foot Clinic και πληρώστε "
              "με κάρτα στο ασφαλές περιβάλλον της Worldline.",
         depth=d, body=body, jsonld=[crumb_ld, org_graph()], active="seminars")


def build_404():
    d = 0
    body = f"""<section class="section" style="min-height:56vh;display:grid;place-items:center">
  <div class="wrap wrap--narrow" style="text-align:center">
    <p class="eyebrow eyebrow--plain" style="justify-content:center">404</p>
    <h1 style="margin-block:.8rem 1.2rem">Αυτή η σελίδα δεν υπάρχει.</h1>
    <p class="lede" style="margin-inline:auto">Ο ιστότοπος ανανεώθηκε και κάποιοι σύνδεσμοι άλλαξαν.
      Ξεκινήστε από την αρχική ή δείτε τις υπηρεσίες μας.</p>
    <div class="pill-row" style="justify-content:center;margin-top:1.75rem">
      <a class="btn" href="/">Ποιοι είμαστε</a>
      <a class="btn btn--ghost" href="/ypiresies/">Υπηρεσίες</a>
      <a class="btn btn--ghost" href="/epikoinonia/">Επικοινωνία</a>
    </div>
  </div>
</section>"""
    page(path="404.html", title="Η σελίδα δεν βρέθηκε | Ensō Foot Clinic",
         desc="Η σελίδα που ζητήσατε δεν υπάρχει. Ο ιστότοπος του Ensō Foot Clinic "
              "ανανεώθηκε — ξεκινήστε από την αρχική.",
         depth=d, body=body)


# ── Sitemap, robots ─────────────────────────────────────────────────────────
def build_index_files():
    urls = [("", "1.0"), ("ypiresies/", "0.8"), ("seminaria/", "0.8"),
            ("seminaria/egrafi/", "0.5"),
            ("epikoinonia/", "0.8"), ("oroi-chrisis/", "0.3"),
            ("stoicheia-epicheirisis/", "0.3")]
    urls += [(f"ypiresies/{t['slug']}/", "0.7") for t in TREATMENTS]
    urls += [(f"seminaria/{x['slug']}/", "0.5") for x in SEMINARS]
    body = "".join(
        f"<url><loc>{SITE['domain']}/{u}</loc><lastmod>{TODAY}</lastmod>"
        f"<changefreq>monthly</changefreq><priority>{p}</priority></url>" for u, p in urls)
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + body + "</urlset>")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE['domain']}/sitemap.xml\n")
    return len(urls)


# ── Legacy URL redirects ────────────────────────────────────────────────────
# The URLs the current ensofootclinic.gr serves, so nothing that ranks today 404s,
# plus the sections of the previous draft of this site that were dropped in
# Oct 2026. The two Greek paths appear percent-encoded in the current site's
# markup, but Apache, Netlify and Vercel all match against the *decoded* path —
# so both spellings are emitted for each.
LEGACY_URLS = [
    ("/about", "/"),
    ("/services", "/ypiresies/"),
    ("/services/ΔΙΑΒΗΤΙΚΟ-ΠΟΔΙ", "/ypiresies/elenchos-diavitikou-podiou/"),
    ("/services/%CE%94%CE%99%CE%91%CE%92%CE%97%CE%A4%CE%99%CE%9A%CE%9F-%CE%A0%CE%9F%CE%94%CE%99",
     "/ypiresies/elenchos-diavitikou-podiou/"),
    ("/contact", "/epikoinonia/"),
    ("/seminars", "/seminaria/"),
    ("/seminars/freeseminar", "/seminaria/1o-seminario-podologias/"),
    ("/terms", "/oroi-chrisis/"),
    ("/privacy", "/oroi-chrisis/"),
    ("/Διαδικτυακά-Μαθήματα", "/"),
    ("/%CE%94%CE%B9%CE%B1%CE%B4%CE%B9%CE%BA%CF%84%CF%85%CE%B1%CE%BA%CE%AC-%CE%9C%CE%B1%CE%B8%CE%AE%CE%BC%CE%B1%CF%84%CE%B1", "/"),
    # Sections removed from this site in Oct 2026.
    ("/to-iatreio", "/"),
    ("/elpiniki-christodoulou", "/"),
    ("/pathiseis", "/ypiresies/"),
    ("/pathiseis/diavitiko-podi", "/ypiresies/elenchos-diavitikou-podiou/"),
    ("/pathiseis/skliryseis-kaloi-tyloi", "/ypiresies/afairesi-kalon-tylon/"),
    ("/pathiseis/ksirodermia-pelmaton", "/ypiresies/therapeia-ksirodermias/"),
    ("/pathiseis/eisfriksi-nychiou", "/ypiresies/orthonychia-narthikes/"),
    ("/odigos-symptomaton", "/ypiresies/"),
    ("/frontida-podion", "/ypiresies/"),
    ("/arthra", "/"),
    ("/gallery", "/"),
    ("/en", "/"),
    # Renamed in Oct 2026: «Ιατρική ποδολογία» → «Κλινική ποδολογική φροντίδα».
    ("/ypiresies/iatriki-podologia", "/ypiresies/kliniki-podologiki-frontida/"),
]


def build_redirects():
    rules = list(LEGACY_URLS)

    write("_redirects", "".join(f"{a}  {b}  301\n" for a, b in rules))

    # GitHub Pages has no server-side redirects, so each legacy path gets a
    # tiny page that forwards instantly (meta refresh 0 + canonical, which
    # Google treats as a permanent redirect). Percent-encoded duplicates
    # collapse onto the decoded path, since Pages decodes the request first.
    seen = set()
    for a, b in rules:
        path = urllib.parse.unquote(a).strip("/")
        if not path or path in seen:
            continue
        seen.add(path)
        dest = b   # root-relative, so it works on github.io before the domain moves
        write(path + "/index.html", f"""<!doctype html>
<html lang="el"><head><meta charset="utf-8">
<title>Ανακατεύθυνση…</title>
<meta http-equiv="refresh" content="0; url={dest}">
<link rel="canonical" href="{dest}">
<meta name="robots" content="noindex">
</head><body><p>Η σελίδα μεταφέρθηκε: <a href="{dest}">{dest}</a></p></body></html>
""")
    # Pages must serve the folder verbatim (no Jekyll, which would drop
    # _redirects) and know the custom domain.
    write(".nojekyll", "")
    write("CNAME", urllib.parse.urlparse(SITE["domain"]).netloc + "\n")
    ht = ["RewriteEngine On"]
    ht += [f"RewriteRule ^{a.strip('/')}/?$ {b} [R=301,L,NE]" for a, b in rules]
    ht.append("ErrorDocument 404 /404.html")
    write(".htaccess", "\n".join(ht) + "\n")

    # Vercel reads this from the repository root, and the site lives one level
    # down, so `outputDirectory` is what stops the deployment 404-ing at /. The
    # no-op build command keeps that setting unambiguous for the zero-config
    # static pipeline.
    write_root("vercel.json", json.dumps({
        "$schema": "https://openapi.vercel.sh/vercel.json",
        "buildCommand": "echo 'static site — nothing to build'",
        "outputDirectory": "site",
        "trailingSlash": True,
        "cleanUrls": False,
        # trailingSlash normalises the path before redirects are matched, so the
        # source must carry the slash too.
        "redirects": [{"source": a if a.endswith("/") else a + "/",
                       "destination": b, "permanent": True} for a, b in rules],
        "headers": [
            # Every asset URL carries a ?v=<content hash>, so a changed file is a
            # new URL and this cache can never serve stale CSS against new HTML.
            {"source": "/assets/(.*)",
             "headers": [{"key": "Cache-Control",
                          "value": "public, max-age=31536000, immutable"}]},
            # HTML must always be revalidated, or the versioned URLs never arrive.
            {"source": "/((?!assets/).*)",
             "headers": [{"key": "Cache-Control",
                          "value": "public, max-age=0, must-revalidate"}]},
            {"source": "/(.*)", "headers": [
                {"key": "X-Content-Type-Options", "value": "nosniff"},
                {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
                {"key": "Permissions-Policy", "value": "geolocation=(), microphone=(), camera=()"},
            ]},
        ],
    }, ensure_ascii=False, indent=2) + "\n")

    return len(rules)


def main():
    build_home()
    for t in TREATMENTS:
        build_treatment(t)
    build_treatments_hub()
    build_seminars_hub()
    for _s in SEMINARS:
        build_seminar(_s)
    build_checkout()
    build_contact(); build_company(); build_terms(); build_404()
    indexed = build_index_files()
    n = build_redirects()
    pages = sum(len([f for f in fs if f.endswith(".html")]) for _, _, fs in os.walk(OUT))
    print(f"built {pages} pages · {indexed} in sitemap · {n} redirects · {OUT}")
    missing = [k for k, v in SITE["legal_rows"] if not v]
    if missing:
        print("  ! στοιχεία επιχείρησης προς συμπλήρωση στο content/data.py → SITE['legal_rows']: "
              + ", ".join(missing))


if __name__ == "__main__":
    main()
