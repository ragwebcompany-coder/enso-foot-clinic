# -*- coding: utf-8 -*-
"""Builds the Ensō Foot Clinic static site into enso-new/site/.

    python3 enso-new/tools/build.py

Set ENSO_OUT to write somewhere else (e.g. the repo root: ENSO_OUT=.).

Content comes from content/pagecopy.py (page bodies) and content/data.py (structure,
contact details, menus). No database, no build tool beyond Python 3.
"""
import os, re, sys, json, html, datetime, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "content"))
sys.path.insert(0, HERE)

from data import (SITE, PRACTITIONER, CONDITIONS, TREATMENTS, ARTICLES, GUIDE_STEPS,
                  RED_FLAGS, TRACKER, EN_PAGES, MONTHS, KIND_LABELS, MATRIX_COLS,
                  GALLERY, GALLERY_CATS, SEMINARS, SEMINAR_STATUS, SEMINAR_MODES,
                  SEMINAR_NOTIFY)
from pagecopy import COPY
import parts
from parts import (I, rel, head, header, footer, overlays,
                   anatomy_block, asset)

OUT = os.path.abspath(os.environ.get("ENSO_OUT") or os.path.join(ROOT, "site"))
# parts.asset() hashes files from here.
parts.ASSET_ROOT = OUT
TODAY = datetime.date.today().isoformat()

CONDS = {c["slug"]: c for c in CONDITIONS}
TREATS = {t["slug"]: t for t in TREATMENTS}

# ── URL map ──────────────────────────────────────────────────────────────────
# Every page of the site, keyed by its copy slug. Used by the `@/` link rewriter,
# the search index and the sitemap.
URLMAP = {
    "home": "", "to-iatreio": "to-iatreio/",
    PRACTITIONER["slug"]: PRACTITIONER["slug"] + "/",
    "epikoinonia": "epikoinonia/", "oroi-chrisis": "oroi-chrisis/",
    "arthra": "arthra/", "gallery": "gallery/",
    "odigos-symptomaton": "odigos-symptomaton/", "frontida-podion": "frontida-podion/",
    "pathiseis": "pathiseis/", "ypiresies": "ypiresies/", "seminaria": "seminaria/",
}
for _s in SEMINARS:
    URLMAP[_s["slug"]] = f"seminaria/{_s['slug']}/"
for c in CONDITIONS:
    URLMAP[c["slug"]] = f"pathiseis/{c['slug']}/"
for t in TREATMENTS:
    URLMAP[t["slug"]] = f"ypiresies/{t['slug']}/"
for slug, _tag in ARTICLES:
    URLMAP.setdefault(slug, f"arthra/{slug}/")
for new, legacy, _t in EN_PAGES:
    URLMAP[legacy] = f"en/{new}/"
URLMAP["en"] = "en/"


def rewrite_links(markup, depth):
    """Turns the `@/some/path/` sentinel used in copy.py into a relative URL, and
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


def faq_block(title, pairs, idx_prefix="faq", lang="el"):
    if not pairs:
        return "", None
    eyebrow = "Ερωτήσεις" if lang == "el" else "Questions"
    fallback = "Συχνές ερωτήσεις" if lang == "el" else "Frequently asked questions"
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
    <div class="sec-head"><p class="eyebrow">{eyebrow}</p><h2>{html.escape(title or fallback)}</h2></div>
    <div class="faq">{items}</div>
  </div>
</section>""", ld


def prose(slug, depth, drop_faq=True):
    rec = COPY.get(slug)
    if not rec:
        return "", None, []
    # Rewrite before splitting: the FAQ answers carry internal links too, and
    # they leave here as their own fragment that never passes through again.
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


def page(*, path, title, desc, depth, body, active="", jsonld=None, lang="el",
         alt=None, og_image="assets/img/og-enso.png", extra_js="", body_class="",
         over_dark=False):
    markup = (head(title, desc, depth, path or "", lang=lang, alt=alt,
                   jsonld=jsonld, og_image=og_image)
              + f'\n<body{" class=" + chr(34) + body_class + chr(34) if body_class else ""}>'
              + f'\n<div class="progress" aria-hidden="true"></div>\n'
              + header(depth, active, lang, over_dark=over_dark)
              + f'\n<main id="main">\n{body}\n</main>\n'
              + footer(depth, lang) + "\n" + overlays(depth, lang)
              + (f'\n<script>{extra_js}</script>' if extra_js else "")
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


def _geo():
    return {"@type": "GeoCoordinates", "latitude": SITE["lat"], "longitude": SITE["lng"]}


def _area_served():
    """The areas the clinic actually draws patients from, plus the region.
    Declared here rather than as near-duplicate landing pages."""
    return ([{"@type": "City", "name": a} for a in SITE["areas"]]
            + [{"@type": "AdministrativeArea", "name": "Κεντρική Μακεδονία"},
               {"@type": "Country", "name": "Ελλάδα"}])


def clinic_ld():
    """Podiatric practice, not a hospital: `Podiatric` medicalSpecialty on a
    MedicalBusiness, with the practitioner as founder and employee."""
    return {
        "@context": "https://schema.org",
        "@type": ["MedicalBusiness", "LocalBusiness"],
        "@id": CLINIC_ID,
        "name": SITE["name"],
        "legalName": SITE["legal"],
        "alternateName": ["Ensō Foot Clinic", "Ενσο Ποδολογικό Ιατρείο",
                          "Trellis Podology & Nails"],
        "description": "Ποδολογικό ιατρείο στην Περαία Θεσσαλονίκης, από το 2002. "
                       "Διαβητικό πόδι, σκληρύνσεις, κάλοι και τύλοι, ξηροδερμία "
                       "πελμάτων και ραγάδες, είσφρηση όνυχος και ορθονυχία.",
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
        "sameAs": [SITE["social"]["facebook"], SITE["social"]["tiktok"]],
    }


def podologist_ld():
    return {
        "@context": "https://schema.org",
        "@type": ["Person", "MedicalBusiness"],
        "@id": PODOLOGIST_ID,
        "name": PRACTITIONER["name"],
        "alternateName": PRACTITIONER["name_en"],
        "jobTitle": "Ποδολόγος",
        "description": re.sub(r"<[^>]+>", "", PRACTITIONER["blurb"]),
        "url": f"{SITE['domain']}/{PRACTITIONER['slug']}/",
        "medicalSpecialty": "Podiatric",
        "worksFor": {"@id": CLINIC_ID},
        "workLocation": {"@type": "Place", "name": SITE["name"],
                         "address": _address(), "geo": _geo()},
        "address": _address(),
        "telephone": SITE["phone_href"],
        "email": SITE["email"],
        "areaServed": _area_served(),
        "knowsLanguage": ["el", "en"],
        "knowsAbout": [c["title"] for c in CONDITIONS] + [t["title"] for t in TREATMENTS],
        "sameAs": [SITE["social"]["facebook"], SITE["social"]["tiktok"]],
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
    """SVG is served as-is; raster art gets a WebP source with the original as fallback."""
    stem, ext = name.rsplit(".", 1)
    extra = ' fetchpriority="high"' if priority else ""
    load = "" if priority else f' loading="{loading}" decoding="async"'
    klass = f' class="{cls}"' if cls else ""
    src = asset(depth, "assets/img/" + name)
    if ext.lower() == "svg":
        return (f'<img src="{src}" alt="{alt}" width="{w}" height="{h}"'
                f'{load}{extra}{klass}>')
    webp = asset(depth, f"assets/img/{stem}.webp")
    return (f'<picture><source srcset="{webp}" type="image/webp">'
            f'<img src="{src}" alt="{alt}" width="{w}" height="{h}"'
            f'{load}{extra}{klass}></picture>')


def crumbs(items, depth, lang="el"):
    """items: [(label, url_or_None)] — last one is the current page."""
    root = "Αρχική" if lang == "el" else "Home"
    lis = [f'<li><a href="{rel(depth)}{"en/" if lang == "en" else ""}">{root}</a></li>']
    for label, url in items:
        lis.append(f'<li><a href="{url}">{label}</a></li>' if url else f"<li>{label}</li>")
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": root,
         "item": SITE["domain"] + ("/en/" if lang == "en" else "/")}]}
    for n, (label, _url) in enumerate(items, start=2):
        ld["itemListElement"].append({"@type": "ListItem", "position": n, "name": label})
    return f'<ol class="crumbs">{"".join(lis)}</ol>', ld


# ── Reusable blocks ─────────────────────────────────────────────────────────
def cta_band(depth):
    return f"""<section class="section section--deep">
  <div class="wrap">
    <div class="split" style="align-items:center">
      <div class="stack">
        <p class="eyebrow">Επόμενο βήμα</p>
        <h2>Δείξτε μας το πόδι σας πριν το λύσετε μόνοι σας.</h2>
        <p class="lede">Θα το εξετάσουμε, θα σας πούμε τι βλέπουμε και τι το προκαλεί, και θα
          φύγετε με γραπτό πλάνο — συμπεριλαμβανομένης της περίπτωσης που δεν χρειάζεται να
          κάνετε τίποτα. Τα ραντεβού κλείνονται τηλεφωνικά.</p>
      </div>
      <div class="stack" style="justify-items:stretch">
        <a class="btn btn--light btn--block" href="tel:{SITE['phone_href']}">{I['phone']} Θεσσαλονίκη · {SITE['phone']}</a>
        <a class="btn btn--outline-light btn--block" href="tel:{SITE['phone_alt_href']}">{I['phone']} Αθήνα · {SITE['phone_alt']}</a>
        <p class="tiny" style="color:#8fb8c3">{SITE['address']}, {SITE['postcode']}
          {SITE['locality']}, {SITE['region']}</p>
      </div>
    </div>
  </div>
</section>"""


def guide_section(depth, *, heading=True):
    steps = json.dumps({
        "phone": SITE["phone"], "phoneHref": SITE["phone_href"],
        "steps": [{"id": s["id"], "type": s["type"], "q": s["q"], "help": s["help"],
                   "options": [[o[0], o[1], o[2]] for o in s["options"]]} for s in GUIDE_STEPS],
        "conditions": {c["slug"]: {
            "title": c["title"], "lead": c["lead"], "url": rel(depth) + f"pathiseis/{c['slug']}/",
            "treatments": [{"title": TREATS[t]["title"], "url": rel(depth) + f"ypiresies/{t}/"}
                           for t in c["treatments"]]} for c in CONDITIONS},
    }, ensure_ascii=False, separators=(",", ":"))
    head_html = ""
    if heading:
        head_html = """<div class="sec-head sec-head--split">
      <div class="stack">
        <p class="eyebrow">Οδηγός συμπτωμάτων</p>
        <h2>Πώς λέγεται αυτό που νιώθετε;</h2>
      </div>
      <p class="lede">Τέσσερις ερωτήσεις σε καθημερινή γλώσσα. Στο τέλος θα ξέρετε ποιον όρο
        να αναζητήσετε και τι κάνουμε συνήθως σε τέτοιες περιπτώσεις.</p>
    </div>"""
    return f"""<section class="section section--mist" id="odigos">
  <div class="wrap">
    {head_html}
    <div class="guide" id="guide" data-reveal>
      <div class="guide__head">
        <div style="display:flex;align-items:center;gap:.65rem">
          {I['shield']}<span class="small" style="font-weight:560;color:var(--deep)">Ιδιωτικός οδηγός</span>
        </div>
        <div class="guide__steps guide__dots" aria-hidden="true"></div>
      </div>
      <div class="guide__body"><p class="muted">Φόρτωση…</p></div>
    </div>
    <p class="tiny muted" style="margin-top:1rem;max-width:60ch">
      Ο οδηγός δεν αντικαθιστά την κλινική εξέταση και δεν στέλνει τις απαντήσεις σας πουθενά.
      Αν έχετε {" ή ".join("<b>" + f.lower() + "</b>" for f in RED_FLAGS[:2])},
      μη χρησιμοποιήσετε τον οδηγό — καλέστε μας ή απευθυνθείτε σε γιατρό.</p>
  </div>
  <script>window.ENSO_GUIDE={steps};</script>
</section>"""


ZONE_LABELS = {"nail": "Νύχι μεγάλου δακτύλου", "forefoot": "Πρόσθιο πέλμα",
               "heel": "Πτέρνα", "circulation": "Δέρμα, νεύρα & αγγεία"}


def anatomy_section(depth):
    by_zone = {}
    for c in CONDITIONS:
        by_zone.setdefault(c["zone"], []).append(c)
    info = {zone: {"zone": ZONE_LABELS[zone], "conditions": [
        {"title": c["title"], "plain": c["plain"], "lead": c["lead"],
         "url": rel(depth) + f"pathiseis/{c['slug']}/",
         "treatments": [{"title": TREATS[t]["title"], "url": rel(depth) + f"ypiresies/{t}/"}
                        for t in c["treatments"]]} for c in cs]}
            for zone, cs in by_zone.items()}
    return f"""<section class="section">
  <div class="wrap">
    <div class="sec-head sec-head--split">
      <div class="stack">
        <p class="eyebrow">Η ανατομία, χωρίς μυστήρια</p>
        <h2>Τέσσερις ζώνες, ένα πόδι που τις μοιράζεται.</h2>
      </div>
      <p class="lede">Το νύχι, το πρόσθιο πέλμα, η πτέρνα και το δέρμα με τα νεύρα του
        φορτίζονται μαζί σε κάθε βήμα. Δείτε πού εμφανίζεται τι — και γιατί.</p>
    </div>
    {anatomy_block(depth)}
    <p class="anatomy__hint" style="margin-top:1.25rem">
      Επιλέξτε μια ζώνη στο διάγραμμα. Το «Με πρόβλημα» δείχνει σχηματικά πώς εμφανίζεται
      η κάθε πάθηση.</p>
  </div>
  <script>window.ENSO_ANATOMY={json.dumps(info, ensure_ascii=False, separators=(",", ":"))};</script>
</section>"""


def tracker_section(depth):
    """Daily foot-care checklist. Same widget mechanics as the rest of the system:
    a progress ring, a routine switcher, two counters and localStorage."""
    data = json.dumps(TRACKER, ensure_ascii=False, separators=(",", ":"))
    buttons = "".join(
        f"""<button type="button" class="prog-btn" data-prog="{k['id']}" aria-pressed="{str(i == 0).lower()}">
      <span style="display:grid"><b>{k['name']}</b><span>{k['desc']}</span></span>
      <i>{k['meta']}</i></button>""" for i, k in enumerate(TRACKER))
    return f"""<div class="tracker" id="tracker">
  <div>
    <div class="tracker__stage">
      <svg class="tracker__ring" viewBox="0 0 100 100" aria-hidden="true">
        <circle class="tracker__track" cx="50" cy="50" r="46"/>
        <circle class="tracker__prog" cx="50" cy="50" r="46"/>
      </svg>
      <div class="tracker__orb">
        <div style="display:grid;gap:.3rem;text-align:center">
          <span class="tracker__count" aria-live="off">0/5</span>
          <span class="tracker__phase" aria-live="polite">Ξεκινήστε</span>
        </div>
      </div>
    </div>
  </div>
  <div class="stack" style="justify-items:stretch">
    <div class="tracker__progs">{buttons}</div>
    <ul class="checks" data-tracker-list></ul>
    <div class="tracker__meta">
      <div><b data-tracker-done>0/5</b><span class="tiny muted">βήματα σήμερα</span></div>
      <div><b data-tracker-streak>0</b><span class="tiny muted">σερί ημερών</span></div>
    </div>
    <button class="btn btn--ghost btn--sm" data-tracker-reset>Μηδενισμός ημέρας</button>
    <p class="tiny muted">Η πρόοδος μένει στη συσκευή σας και δεν στέλνεται πουθενά. Ο tracker
      οργανώνει τη ρουτίνα φροντίδας — δεν αντικαθιστά την κλινική εξέταση ούτε τη θεραπεία.</p>
  </div>
  <script>window.ENSO_TRACKER={data};</script>
</div>"""


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


# ── Home ─────────────────────────────────────────────────────────────────────
def build_home():
    d = 0
    conds = "".join(f"""<a class="card" href="pathiseis/{c['slug']}/" data-reveal="{i*60}">
      <p class="card__kicker">{c['stat'][0]} · {c['stat'][1]}</p>
      <h3>{c['title']}</h3>
      <p>{c['lead']}</p>
      <p class="cond-card__voice">«{c['plain']}»</p>
    </a>""" for i, c in enumerate(CONDITIONS))

    treats = "".join(f"""<a class="card" href="ypiresies/{t['slug']}/" data-reveal="{i*50}">
      <p class="card__kicker">{t['short']}</p>
      <h3>{t['title']}</h3>
      <p>{t['lead']}</p>
      <p class="card__foot"><span class="link-more">Αναλυτικά</span></p>
    </a>""" for i, t in enumerate(TREATMENTS[:3]))

    art = "".join(f"""<a class="card" href="arthra/{slug}/" data-reveal="{i*60}">
      <p class="card__kicker">{tag}</p>
      <h3>{html.escape(article_title(slug))}</h3>
      <p>{html.escape(plain(slug, 120))}…</p>
    </a>""" for i, (slug, tag) in enumerate(ARTICLES[:3]))

    # `count` drives the tick-up on reveal; the rest of the label is preserved.
    creds = [(PRACTITIONER["since"], "Στον κλάδο του άκρου ποδός, αδιάλειπτα"),
             (PRACTITIONER["years"], "Χρόνια κλινικής εμπειρίας"),
             ("96%", "Επιτυχία στην ορθονυχία με νάρθηκα"),
             ("Κλάση B", "Αποστείρωση εργαλείων σε αυτόκαυστο")]
    creds_html = "".join(
        f'<li><b data-count="{a}">{a}</b><span>{b}</span></li>' for a, b in creds)

    # The phone cover: rendered at every width, shown only under 720px. Three
    # pillars stand in for the nav, each pointing at a real condition page.
    PILLARS = [("pathiseis/diavitiko-podi/", "Διαβητικό<br>πόδι", "foot"),
               ("ypiresies/iatriki-podologia/", "Ιατρική<br>ποδολογία", "tool"),
               ("ypiresies/orthonychia-narthikes/", "Ορθονυχία<br>&amp; νύχια", "nail")]
    pillars = "".join(
        f'<a href="{href}">{I["pil_" + icon]}<span>{label}</span></a>'
        for href, label, icon in PILLARS)

    body = f"""<section class="hero hero--deep">
  <div class="hero__aurora" aria-hidden="true"><i></i><i></i><i></i></div>
  <div class="hero__mesh" aria-hidden="true"></div>
  <div class="wrap hero__grid">
    <div class="hero__copy">
      <p class="eyebrow">Ποδολογικό ιατρείο · Περαία, Θεσσαλονίκη</p>
      <div class="hero__cover">
        {img("enso-badge.svg", "Το σήμα ensō του Ensō Foot Clinic", 400, 400, 0,
             cls="hero__badge-mark")}
        <p class="hero__wordmark">Ensō <span>Foot Clinic</span></p>
        <p class="hero__rule"><span>Ποδολογία · Ποδιατρική</span></p>
        <div class="hero__pillars">{pillars}</div>
        <p class="hero__pitch"><span class="qm">«</span>Η βαρύτητα μπορεί να γίνει ο
          <em>καλύτερός σου σύμμαχος</em> αφού πρώτα κάνεις τον ποδίατρο
          <em>καλύτερό σου φίλο</em>.<span class="qm">»</span></p>
        <p class="hero__sign">{PRACTITIONER['name']}</p>
        <div class="hero__cover-cta">
          <a class="btn" href="tel:{SITE['phone_href']}">Κλείστε ραντεβού</a>
          <a class="btn btn--ghost" href="ypiresies/">Οι υπηρεσίες μας</a>
        </div>
        <a class="hero__scroll" href="#odigos" aria-label="Δείτε περισσότερα">
          <span class="hero__scroll-mouse"></span>{I['down']}</a>
      </div>
      <h1 class="slogan"><span class="qm">«</span>{PRACTITIONER['quote']}<span class="qm">»</span></h1>
      <p class="slogan__by">{PRACTITIONER['name']}</p>
      <p class="lede">Κάλοι, ραγάδες, νύχια που εισφρύουν, διαβητικό πόδι. Αν δεν ξέρετε
        πώς να περιγράψετε αυτό που νιώθετε, ξεκινήστε από τον οδηγό.</p>
      <div class="hero__actions">
        <a class="btn btn--light hero__act--desk" href="#odigos">Ξεκινήστε τον οδηγό</a>
        <a class="btn btn--light hero__act--phone" href="tel:{SITE['phone_href']}">Ζητήστε ραντεβού</a>
        <a class="btn btn--outline-light" href="tel:{SITE['phone_href']}">{I['phone']} {SITE['phone']}</a>
      </div>
      <p class="hero__note">{I['lock']} Οι απαντήσεις σας μένουν στη συσκευή σας.</p>
    </div>
    <div class="hero__figure" data-reveal="120">
      <div class="hero__pane">
        {img("hero-enso-dark.svg", "Το σήμα ensō του ιατρείου", 500, 620, 0, priority=True)}
      </div>
      <div class="hero__badge">
        <b>{SITE['founded']}</b>
        <span>Από τότε δουλεύουμε πάνω στο ίδιο πράγμα: γιατί πονάει αυτό το πόδι</span>
      </div>
    </div>
  </div>

  <div class="wrap">
    <ul class="creds__list creds__list--deep">{creds_html}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head sec-head--split">
      <div class="stack">
        <p class="eyebrow">Παθήσεις</p>
        <h2>Τέσσερα προβλήματα που φέρνουν σχεδόν όλους εδώ.</h2>
      </div>
      <p class="lede">Διαβάστε τι είναι, γιατί εμφανίζεται και τι γίνεται γι' αυτό —
        γραμμένο ώστε να το καταλάβετε πριν μπείτε στο ιατρείο.</p>
    </div>
    <div class="grid grid--2">{conds}</div>
    <p style="margin-top:2rem"><a class="link-more" href="pathiseis/">Όλες οι παθήσεις</a></p>
  </div>
</section>

{anatomy_section(d)}

{guide_section(d)}

<section class="section">
  <div class="wrap">
    <div class="sec-head sec-head--split">
      <div class="stack"><p class="eyebrow">Υπηρεσίες</p>
        <h2>Πρώτα φεύγει ο πόνος. Μετά φεύγει η αιτία.</h2></div>
      <p class="lede">Η ανακούφιση είναι εύκολη και άμεση. Το δύσκολο — και το ουσιαστικό —
        είναι να μη ξαναγυρίσει το πρόβλημα στο ίδιο σημείο.</p>
    </div>
    <div class="grid grid--3">{treats}</div>
    <p style="margin-top:2rem"><a class="link-more" href="ypiresies/">Συγκρίνετε όλες τις υπηρεσίες</a></p>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap">
    <div class="split split--wide-left">
      <div class="frame" data-reveal>
        {img("elpiniki-christodoulou.svg", "Ensō Foot Clinic — Ελπινίκη Χριστοδούλου, Ποδολόγος", 900, 900, 0)}
      </div>
      <div class="stack">
        <p class="eyebrow">Το ιατρείο · Περαία, Θεσσαλονίκη</p>
        <h2>Μία ποδολόγος, ένα πόδι τη φορά, από το 2002.</h2>
        <p class="lede">Η Ελπινίκη Χριστοδούλου έχει πάνω από 19 χρόνια στη θεραπεία του
          άκρου ποδός. Εδώ δεν θα σας δει «η ομάδα» — θα σας δει η ίδια, κάθε φορά.</p>
        <ul class="info-list" style="margin-block:.5rem">
          <li>{I['pin']}<div><b>Πού θα μας βρείτε</b>
            <a href="epikoinonia/">{SITE['address']}, {SITE['postcode']}</a></div></li>
          <li>{I['clock']}<div><b>Ραντεβού</b>
            <span class="muted">Κατόπιν συνεννόησης · Περαία και Αθήνα</span></div></li>
        </ul>
        <div class="pill-row">
          <a class="chip" href="{PRACTITIONER['slug']}/">Βιογραφικό</a>
          <a class="chip" href="to-iatreio/">Το ιατρείο</a>
          <a class="chip" href="gallery/">Εικονογραφήσεις</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head sec-head--split">
      <div class="stack"><p class="eyebrow">Φροντίδα ποδιών</p>
        <h2>Ξεκινήστε από κάτι που μπορείτε να κάνετε απόψε.</h2></div>
      <p class="lede">Ο ημερήσιος έλεγχος παίρνει δύο λεπτά και προλαμβάνει τα περισσότερα
        από όσα βλέπουμε στο ιατρείο. Ο tracker κρατά το σερί σας — δωρεάν, χωρίς εγγραφή.</p>
    </div>
    {tracker_section(d)}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="panel panel--deep">
      <div class="stack">
        <p class="eyebrow">Εκπαίδευση</p>
        <h2>Σεμινάρια για επαγγελματίες.</h2>
        <p class="lede">Η ίδια δουλειά από την άλλη πλευρά του τραπεζιού: σεμινάρια,
          workshops και masterclasses ποδολογίας, διδασκαλία σε Ι.ΙΕΚ και χρόνια ως
          Academy Instructor.</p>
      </div>
      <div class="stack" style="justify-items:stretch">
        <a class="btn btn--light btn--block" href="seminaria/">Δείτε τα σεμινάρια</a>
        <p class="tiny" style="color:#8fb8c3">Το επόμενο δεν έχει ανακοινωθεί ακόμη —
          δηλώστε ενδιαφέρον και θα ενημερωθείτε πρώτοι.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap">
    <div class="sec-head sec-head--split">
      <div class="stack"><p class="eyebrow">Άρθρα</p><h2>Από το ιατρείο, γραπτώς.</h2></div>
      <p class="lede">Ό,τι εξηγούμε συχνότερα, γραμμένο μία φορά καλά.</p>
    </div>
    <div class="grid grid--3">{art}</div>
    <p style="margin-top:2rem"><a class="link-more" href="arthra/">Όλα τα άρθρα</a></p>
  </div>
</section>

{cta_band(d)}"""

    ld = [org_graph(),
          {"@context": "https://schema.org", "@type": "WebSite", "name": SITE["name"],
           "url": SITE["domain"] + "/", "inLanguage": "el",
           "publisher": {"@id": CLINIC_ID}}]

    page(path="", title="Ποδολόγος στην Περαία Θεσσαλονίκης | Ensō Foot Clinic",
         desc="Ποδολογικό ιατρείο στην Περαία, από το 2002. Διαβητικό πόδι, κάλοι και "
              "τύλοι, ραγάδες πτέρνας, είσφρηση όνυχος με ανώδυνη ορθονυχία.",
         depth=0, body=body, jsonld=ld, alt=("en", "en/"),
         body_class="page--home", over_dark=True)


def article_title(slug):
    rec = COPY.get(slug) or {}
    return html.unescape((rec.get("h1") or rec.get("title") or slug).split(" | ")[0]).strip()


def article_date(slug):
    rec = COPY.get(slug) or {}
    d = rec.get("date")
    if not d:
        return "2026-01-01", "2026"
    mon, day, year = d
    return f"{year}-{MONTHS.get(mon, '01')}-{int(day):02d}", f"{day} {mon} {year}"


# ── Condition & service pages ───────────────────────────────────────────────
def related_strip(depth, treat_slugs, title="Σχετικές υπηρεσίες"):
    if not treat_slugs:
        return ""
    cards = "".join(f"""<a class="card" href="{rel(depth)}ypiresies/{s}/">
      <p class="card__kicker">{TREATS[s]['short']}</p><h3>{TREATS[s]['title']}</h3>
      <p>{TREATS[s]['lead']}</p></a>""" for s in treat_slugs if s in TREATS)
    return f"""<section class="section section--tight">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">{title}</p></div>
    <div class="grid grid--{min(len(treat_slugs), 3)}">{cards}</div>
  </div>
</section>"""


def doc_layout(depth, body_html, aside_html="", lang="el"):
    label = "Σε αυτή τη σελίδα" if lang == "el" else "On this page"
    nav_label = "Περιεχόμενα" if lang == "el" else "Contents"
    return f"""<section class="section section--tight">
  <div class="wrap">
    <div class="doc">
      <article class="prose">{body_html}</article>
      <aside class="doc__aside" data-toc-wrap>
        <div>
          <p class="eyebrow" style="margin-bottom:.9rem">{label}</p>
          <nav class="toc" aria-label="{nav_label}"></nav>
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


def build_condition(c):
    d, slug = 2, c["slug"]
    body, faq_title, pairs = prose(slug, d)
    faq_html, faq_ld = faq_block(faq_title, pairs, f"faq-{slug}")
    crumb_html, crumb_ld = crumbs([("Παθήσεις", rel(d) + "pathiseis/"), (c["title"], None)], d)
    head_block = f"""<section class="page-head">
  <div class="wrap">
    {crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack">
        <p class="eyebrow">{c['stat'][0]} · {c['stat'][1]}</p>
        <h1>{c['title']}</h1>
      </div>
      <div class="stack">
        <p class="voice">{c['plain']}</p>
        <p class="lede" style="font-size:1rem">{c['lead']}</p>
      </div>
    </div>
  </div>
</section>"""
    ld = [crumb_ld, org_graph(),
          {"@context": "https://schema.org", "@type": "MedicalWebPage",
           "name": c["title"], "inLanguage": "el",
           "url": f"{SITE['domain']}/pathiseis/{slug}/",
           "specialty": "Podiatric",
           "lastReviewed": TODAY,
           "reviewedBy": {"@id": PODOLOGIST_ID},
           "about": {
               "@type": "MedicalCondition",
               "name": c["title"],
               "description": c["lead"],
               "possibleTreatment": [
                   {"@type": "MedicalTherapy", "name": TREATS[t]["title"],
                    "url": f"{SITE['domain']}/ypiresies/{t}/"}
                   for t in c["treatments"] if t in TREATS]},
           "publisher": {"@id": CLINIC_ID},
           "provider": {"@id": CLINIC_ID}}]
    if faq_ld:
        ld.append(faq_ld)
    page(path=f"pathiseis/{slug}/",
         title=seo_title(f"{c['title']} — αίτια & θεραπεία"),
         desc=local_desc(c.get("meta") or meta_desc(slug, c["lead"])), depth=d,
         body=head_block + doc_layout(d, body, aside_cta(d)) + faq_html
              + related_strip(d, c["treatments"]) + cta_band(d),
         jsonld=ld)


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
    page(path=f"ypiresies/{slug}/",
         title=seo_title(f"{t['title']} — {t['short']}"),
         desc=local_desc(t.get("meta") or meta_desc(slug, t["lead"])), depth=d,
         body=head_block + doc_layout(d, body, aside_cta(d)) + faq_html + cta_band(d),
         jsonld=ld, active="treatments")


def build_article(slug, tag):
    d = 2
    title = article_title(slug)
    iso, human = article_date(slug)
    body, faq_title, pairs = prose(slug, d)
    faq_html, faq_ld = faq_block(faq_title, pairs, f"faq-{slug}")
    crumb_html, crumb_ld = crumbs([("Άρθρα", rel(d) + "arthra/"), (title, None)], d)
    others = [(s, tg) for s, tg in ARTICLES if s != slug and tg == tag][:2] \
             or [(s, tg) for s, tg in ARTICLES if s != slug][:2]
    more = "".join(f"""<a class="card" href="{rel(d)}arthra/{s}/">
      <p class="card__kicker">{tg}</p><h3>{html.escape(article_title(s))}</h3></a>""" for s, tg in others)
    head_block = f"""<section class="page-head">
  <div class="wrap wrap--narrow">
    {crumb_html}
    <p class="eyebrow">{tag} · <time datetime="{iso}">{human}</time></p>
    <h1 style="font-size:clamp(1.9rem,1.3rem+2.4vw,3rem);margin-top:.75rem">{html.escape(title)}</h1>
  </div>
</section>"""
    ld = [crumb_ld, {"@context": "https://schema.org", "@type": "Article",
                     "headline": title, "datePublished": iso, "dateModified": iso,
                     "inLanguage": "el", "articleSection": tag,
                     "author": {"@id": PODOLOGIST_ID},
                     "publisher": {"@id": CLINIC_ID},
                     "mainEntityOfPage": f"{SITE['domain']}/arthra/{slug}/"},
          org_graph()]
    if faq_ld:
        ld.append(faq_ld)
    page(path=f"arthra/{slug}/", title=seo_title(title),
         desc=meta_desc(slug, title), depth=d,
         body=head_block + doc_layout(d, body, aside_cta(d)) + faq_html + f"""
<section class="section section--tight section--mist">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Διαβάστε επίσης</p></div>
    <div class="grid grid--2">{more}</div>
  </div>
</section>""" + cta_band(d), jsonld=ld, active="articles")


# ── Seminars ─────────────────────────────────────────────────────────────────
# The teaching side of the practice. There is no booking platform yet, so
# registration composes an email — swap `register` in data.py for ("url", href)
# and every open seminar hands off to the platform instead, with no template
# change here.
def _seminar_meta(sem):
    """The facts strip shared by the card and the detail page."""
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
    """Whatever «register» means today."""
    kind, value = sem["register"]
    cls = "btn btn--block" if block else "btn"
    if kind == "url":
        return (f'<a class="{cls}" href="{value}" target="_blank" rel="noopener">'
                f'Εγγραφή στο σεμινάριο</a>')
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
        # schema.org has no "finished" status: an event that ran as planned stays
        # EventScheduled, and the past date is what marks it as over.
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
         body=head_block + doc_layout(d, body, aside) + topics_html + faq_html + cta_band(d),
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
  </div>
</section>

{past_block}
{doc_layout(d, body_html, aside_cta(d))}
{faq_html}
{cta_band(d)}"""

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


# ── Hubs ─────────────────────────────────────────────────────────────────────
def build_conditions_hub():
    d = 1
    cards = "".join(f"""<a class="card" href="{rel(d)}pathiseis/{c['slug']}/" data-reveal="{i*50}">
      <p class="card__kicker">{c['stat'][0]} · {c['stat'][1]}</p>
      <h3>{c['title']}</h3><p>{c['lead']}</p>
      <p class="cond-card__voice">«{c['plain']}»</p></a>""" for i, c in enumerate(CONDITIONS))
    crumb_html, crumb_ld = crumbs([("Παθήσεις", None)], d)
    body = f"""<section class="page-head">
  <div class="wrap">
    {crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack"><p class="eyebrow">Παθήσεις</p>
        <h1>Τέσσερις καταστάσεις που μοιράζονται ένα πόδι.</h1></div>
      <p class="lede">Σπάνια έρχονται μόνες τους: το λάθος παπούτσι φτιάχνει και τον κάλο
        και την ονυχοκρύπτωση. Γι' αυτό εξετάζουμε ολόκληρο το πόδι, όχι μόνο το σημείο
        που πονάει.</p>
    </div>
  </div>
</section>
<section class="section section--tight"><div class="wrap"><div class="grid grid--2">{cards}</div></div></section>
{anatomy_section(d)}
{guide_section(d)}
{cta_band(d)}"""
    page(path="pathiseis/", title="Παθήσεις άκρου ποδός | Ensō Foot Clinic",
         desc="Διαβητικό πόδι, σκληρύνσεις, κάλοι και τύλοι, ξηροδερμία πελμάτων και "
              "ραγάδες, είσφρηση όνυχος. Τι είναι και πώς αντιμετωπίζονται.",
         depth=d, body=body, jsonld=[crumb_ld])


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
      <p class="lede">Πέντε υπηρεσίες που καλύπτουν και την πρόληψη και τη θεραπεία.
        Δείτε τι σημαίνει η καθεμία σε χρόνο, αίσθηση και συχνότητα.</p>
    </div>
  </div>
</section>
<section class="section section--tight"><div class="wrap"><div class="grid grid--3">{cards}</div></div></section>
{compare_section(d)}
{cta_band(d)}"""
    page(path="ypiresies/", title="Υπηρεσίες ποδολογίας — Περαία | Ensō Foot Clinic",
         desc="Ιατρική ποδολογία, αφαίρεση κάλων και τύλων, θεραπεία ξηροδερμίας, "
              "ορθονυχία με νάρθηκα, έλεγχος διαβητικού ποδιού. Περαία, Θεσσαλονίκη.",
         depth=d, body=body, jsonld=[crumb_ld], active="treatments")


def build_articles_hub():
    d = 1
    tags = []
    for _s, t in ARTICLES:
        if t not in tags:
            tags.append(t)
    filters = '<button class="filter" data-tag-filter="all" aria-pressed="true">Όλα</button>' + "".join(
        f'<button class="filter" data-tag-filter="{t}" aria-pressed="false">{t}</button>' for t in tags)
    rows = ""
    for slug, tag in ARTICLES:
        title = article_title(slug)
        iso, human = article_date(slug)
        excerpt = html.escape(plain(slug, 150))
        needle = html.escape((title + " " + tag + " " + plain(slug, 400)).lower(), quote=True)
        rows += f"""<a class="article-row" href="{rel(d)}arthra/{slug}/" data-tag="{tag}" data-search="{needle}">
      <time datetime="{iso}">{human}</time>
      <div><h3>{html.escape(title)}</h3><p>{excerpt}…</p></div>
      <span class="chip">{tag}</span></a>"""
    crumb_html, crumb_ld = crumbs([("Άρθρα", None)], d)
    body = f"""<section class="page-head">
  <div class="wrap">
    {crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack"><p class="eyebrow">Άρθρα</p><h1>Από το ιατρείο, γραπτώς.</h1></div>
      <p class="lede">{len(ARTICLES)} κείμενα για ό,τι εξηγούμε συχνότερα. Χωρίς ορολογία
        εκεί που δεν χρειάζεται.</p>
    </div>
  </div>
</section>
<section class="section section--tight" id="articles">
  <div class="wrap">
    <div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:center;justify-content:space-between;margin-bottom:2rem">
      <div class="compare__filters" style="margin:0">{filters}</div>
      <label class="searchbar">{I['search']}
        <span class="vh">Αναζήτηση στα άρθρα</span>
        <input type="search" placeholder="Αναζήτηση στα άρθρα…" data-article-search autocomplete="off"></label>
    </div>
    <div class="article-list">{rows}</div>
    <p class="empty" data-article-empty hidden>Δεν βρέθηκε άρθρο με αυτά τα κριτήρια.</p>
  </div>
</section>
{cta_band(d)}"""
    page(path="arthra/", title="Άρθρα ποδολογίας | Ensō Foot Clinic",
         desc="Άρθρα για το διαβητικό πόδι, τους κάλους, τις ραγάδες πτέρνας, τα νύχια "
              "και τη σωστή φροντίδα των ποδιών, από το Ensō Foot Clinic.",
         depth=d, body=body, jsonld=[crumb_ld], active="articles")


# ── Clinic, practitioner, guide, tracker, gallery, contact, terms ───────────
def build_clinic():
    d = 1
    body_html, faq_title, pairs = prose("to-iatreio", d)
    faq_html, faq_ld = faq_block(faq_title, pairs, "faq-clinic")
    crumb_html, crumb_ld = crumbs([("Το ιατρείο", None)], d)
    body = f"""<section class="page-head">
  <div class="wrap">{crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack"><p class="eyebrow">Το ιατρείο</p>
        <h1>Ένας κύκλος που κλείνει με μία κίνηση.</h1></div>
      <p class="lede">Ποδολογικό ιατρείο στην Περαία Θεσσαλονίκης. Αποστειρωμένα εργαλεία,
        στεγνή τεχνική, μηδενικός πόνος — και ένα γραπτό πλάνο που φεύγει μαζί σας.</p>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="frame" data-reveal>
      {img("clinic-enso.svg", "Το σήμα ensō του ιατρείου σε πλήρες πλάτος", 1600, 700, d)}
    </div>
  </div>
</section>

{doc_layout(d, body_html, aside_cta(d))}
{faq_html}

<section class="section section--mist">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Ποιος θα σας δει</p><h2>Μία ποδολόγος, κάθε φορά.</h2></div>
    <div class="split split--wide-left">
      <div class="frame" style="max-width:420px">
        {img(PRACTITIONER['photo'], PRACTITIONER['name'] + " — Ποδολόγος", 900, 900, d)}
      </div>
      <div class="stack">
        <p class="eyebrow">{PRACTITIONER['role']}</p>
        <h3 style="font-family:var(--display);font-size:1.7rem">{PRACTITIONER['name']}</h3>
        <p class="lede">{PRACTITIONER['blurb']}</p>
        <ul class="timeline">
          {"".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in PRACTITIONER['credentials'][:4])}
        </ul>
        <p><a class="link-more" href="{rel(d)}{PRACTITIONER['slug']}/">Πλήρες βιογραφικό</a></p>
      </div>
    </div>
  </div>
</section>
{cta_band(d)}"""
    ld = [crumb_ld, org_graph()]
    if faq_ld:
        ld.append(faq_ld)
    page(path="to-iatreio/", title="Το ιατρείο — Περαία, Θεσσαλονίκη | Ensō Foot Clinic",
         desc="Ποδολογικό ιατρείο στην Περαία Θεσσαλονίκης, από το 2002. Αποστείρωση "
              "κλάσης B, στεγνή τεχνική, γραπτό πλάνο φροντίδας.",
         depth=d, body=body, jsonld=ld, active="clinic")


def build_practitioner():
    d = 1
    p = PRACTITIONER
    body_html, _, _ = prose(p["slug"], d)
    crumb_html, crumb_ld = crumbs([(p["name"], None)], d)
    creds = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in p["credentials"])
    body = f"""<section class="page-head">
  <div class="wrap">{crumb_html}
    <div class="split split--wide-left" style="align-items:end">
      <div class="stack"><p class="eyebrow">{p['role']}</p><h1>{p['name']}</h1>
        <p class="slogan" style="font-size:clamp(1.2rem,1rem+.9vw,1.72rem)">
          <span class="qm">«</span>{p['quote']}<span class="qm">»</span></p>
        <p class="lede">{p['blurb']}</p></div>
      <div class="frame" style="max-width:360px">{img(p['photo'], p['name'] + " — Ποδολόγος", 900, 900, d)}</div>
    </div>
  </div>
</section>

<section class="section section--tight section--mist">
  <div class="wrap">
    <div class="sec-head"><p class="eyebrow">Επαγγελματική εμπειρία</p></div>
    <ul class="timeline">{creds}</ul>
  </div>
</section>

{doc_layout(d, body_html, aside_cta(d))}
{cta_band(d)}"""
    ld = [crumb_ld, org_graph(),
          {"@context": "https://schema.org", "@type": "ProfilePage",
           "inLanguage": "el", "url": f"{SITE['domain']}/{p['slug']}/",
           "mainEntity": {"@id": PODOLOGIST_ID}}]
    page(path=f"{p['slug']}/", title=seo_title(f"{p['name']} — Ποδολόγος, Θεσσαλονίκη"),
         desc=local_desc(meta_desc(p["slug"], p["blurb"])), depth=d, body=body, jsonld=ld)


def build_guide_page():
    d = 1
    crumb_html, crumb_ld = crumbs([("Οδηγός συμπτωμάτων", None)], d)
    flags = "".join(f"<li>{f}</li>" for f in RED_FLAGS)
    body = f"""<section class="page-head">
  <div class="wrap">{crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack"><p class="eyebrow">Οδηγός συμπτωμάτων</p>
        <h1>Δεν χρειάζεται να ξέρετε πώς λέγεται.</h1></div>
      <p class="lede">Τέσσερις ερωτήσεις, γραμμένες όπως θα το λέγατε σε φίλο. Στο τέλος
        θα ξέρετε ποιον όρο να αναζητήσετε και ποιες είναι οι επιλογές σας.</p>
    </div>
  </div>
</section>
{guide_section(d, heading=False)}
<section class="section section--tight">
  <div class="wrap">
    <div class="split">
      <div class="stack">
        <p class="eyebrow">Πότε να μην περιμένετε</p>
        <h2>Κάποια σημάδια θέλουν γιατρό σήμερα.</h2>
        <p class="lede">Ο οδηγός δεν είναι κατάλληλος αν έχετε:</p>
        <ul class="bullets">{flags}</ul>
        <a class="btn" href="tel:{SITE['phone_href']}">{I['phone']} Καλέστε μας</a>
      </div>
      <div class="stack">
        <p class="eyebrow">Πώς λειτουργεί</p>
        <ul class="timeline">
          <li><b>01</b><span>Επιλέγετε όσα σας ταιριάζουν, με καθημερινά λόγια.</span></li>
          <li><b>02</b><span>Ο οδηγός σταθμίζει τις απαντήσεις και δείχνει τις πιθανές αντιστοιχίες.</span></li>
          <li><b>03</b><span>Παίρνετε συνδέσμους στις σχετικές σελίδες και μπορείτε να ζητήσετε ραντεβού.</span></li>
        </ul>
        <p class="tiny muted">Τίποτα δεν φεύγει από τη συσκευή σας: ο υπολογισμός γίνεται
          τοπικά στον browser και δεν αποθηκεύεται πουθενά.</p>
      </div>
    </div>
  </div>
</section>
{cta_band(d)}"""
    page(path="odigos-symptomaton/", title="Οδηγός συμπτωμάτων ποδιού | Ensō Foot Clinic",
         desc="Τέσσερις ερωτήσεις σε καθημερινή γλώσσα για να καταλάβετε τι μπορεί να "
              "συμβαίνει στα πόδια σας. Ιδιωτικό, χωρίς εγγραφή.",
         depth=d, body=body, jsonld=[crumb_ld], active="guide")


def build_tracker_page():
    d = 1
    crumb_html, crumb_ld = crumbs([("Φροντίδα ποδιών", None)], d)
    body = f"""<section class="page-head">
  <div class="wrap">{crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack"><p class="eyebrow">Καθημερινή φροντίδα</p>
        <h1>Ημερήσιος tracker φροντίδας ποδιών.</h1></div>
      <p class="lede">Τρεις έτοιμες ρουτίνες — καθημερινή φροντίδα, διαβητικό πόδι, και τις
        πρώτες ημέρες μετά από συνεδρία. Τσεκάρετε τα βήματα, κρατήστε το σερί σας. Όλα
        μένουν στη συσκευή σας.</p>
    </div>
  </div>
</section>
<section class="section section--tight"><div class="wrap">{tracker_section(d)}</div></section>
<section class="section section--mist">
  <div class="wrap">
    <div class="split">
      <div class="stack">
        <p class="eyebrow">Πώς γίνεται σωστά</p>
        <h2>Δύο λεπτά, κάθε βράδυ, με σειρά.</h2>
        <ul class="bullets">
          <li>Ελέγχετε ολόκληρο το πέλμα — και κάτω από τα δάχτυλα, με καθρέφτη αν χρειάζεται.</li>
          <li>Στεγνώνετε προσεκτικά ανάμεσα στα δάχτυλα. Εκεί ξεκινούν οι μύκητες.</li>
          <li>Ενυδατώνετε πέλμα και πτέρνα — ποτέ ανάμεσα στα δάχτυλα.</li>
          <li>Κόβετε τα νύχια ίσια, χωρίς να στρογγυλεύετε τις γωνίες.</li>
          <li>Ελέγχετε το εσωτερικό του παπουτσιού με το χέρι πριν το φορέσετε.</li>
          <li>Εναλλάσσετε παπούτσια: ένα ζευγάρι θέλει πάνω από 24 ώρες για να στεγνώσει.</li>
        </ul>
      </div>
      <div class="stack">
        <p class="eyebrow">Πότε δεν αρκεί</p>
        <h2>Η ρουτίνα προλαμβάνει. Δεν θεραπεύει.</h2>
        <p class="lede">Ένας κάλος με πυρήνα, μια βαθιά ραγάδα ή ένα νύχι που εισφρύει δεν
          λύνονται με κρέμα και υπομονή. Χρειάζονται ποδολογική πράξη — και όσο νωρίτερα,
          τόσο πιο απλή.</p>
        <div class="pill-row">
          <a class="chip" href="{rel(d)}pathiseis/diavitiko-podi/">Διαβητικό πόδι</a>
          <a class="chip" href="{rel(d)}pathiseis/skliryseis-kaloi-tyloi/">Κάλοι & τύλοι</a>
          <a class="chip" href="{rel(d)}odigos-symptomaton/">Οδηγός συμπτωμάτων</a>
        </div>
      </div>
    </div>
  </div>
</section>
{cta_band(d)}"""
    page(path="frontida-podion/", title="Ημερήσιος Tracker Φροντίδας Ποδιών | Ensō Foot Clinic",
         desc="Δωρεάν ημερήσιος tracker φροντίδας ποδιών με τρεις ρουτίνες και σερί ημερών — "
              "για διαβητικό πόδι, καθημερινή φροντίδα και μετά τη συνεδρία.",
         depth=d, body=body, jsonld=[crumb_ld])


def build_gallery():
    d = 1
    cats = dict(GALLERY_CATS)
    items = "".join(f"""<button class="gal__item" data-item data-kind="{cat}"
      data-full="{rel(d)}assets/img/{stem}.svg" data-alt="{html.escape(cap, quote=True)}">
      {img(stem + ".svg", html.escape(cap, quote=True), 800, 500, d)}
      <span class="gal__cap">{html.escape(cap)}</span></button>""" for stem, cat, cap in GALLERY)
    filters = "".join(
        f'<button class="filter" data-gal-filter="{k}" aria-pressed="false">{v}</button>'
        for k, v in GALLERY_CATS)
    crumb_html, crumb_ld = crumbs([("Εικονογραφήσεις", None)], d)
    body = f"""<section class="page-head">
  <div class="wrap">{crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack"><p class="eyebrow">Εικονογραφήσεις</p>
        <h1>Δείτε τι συμβαίνει κάτω από το δέρμα.</h1></div>
      <p class="lede">{len(GALLERY)} σχηματικές εικονογραφήσεις της ανατομίας, των τεσσάρων
        παθήσεων, των θεραπειών και της σωστής φροντίδας. Σχεδιάστηκαν ειδικά για αυτόν τον
        ιστότοπο.</p>
    </div>
  </div>
</section>
<section class="section section--tight">
  <div class="wrap">
    <div class="compare__filters" role="group" aria-label="Φίλτρα εικονογραφήσεων">
      <button class="filter" data-gal-filter="all" aria-pressed="true">Όλα</button>
      {filters}
    </div>
    <div class="gal" data-gallery>{items}</div>
    <p class="tiny muted" style="margin-top:1.5rem;max-width:62ch">
      Οι εικόνες είναι σχηματικές και εκπαιδευτικές. Δεν απεικονίζουν πραγματικά περιστατικά
      ασθενών και δεν αποτελούν υπόσχεση αποτελέσματος — κάθε πόδι είναι διαφορετικό.</p>
  </div>
</section>
{cta_band(d)}"""
    page(path="gallery/", title="Εικονογραφήσεις ποδολογίας | Ensō Foot Clinic",
         desc="Σχηματικές εικονογραφήσεις για την ανατομία του άκρου ποδός, τις παθήσεις, "
              "τις θεραπείες και τη σωστή καθημερινή φροντίδα.",
         depth=d, body=body, jsonld=[crumb_ld], active="gallery")


def build_contact():
    d = 1
    hours = "".join(f'<div style="display:flex;justify-content:space-between;gap:1rem;'
                    f'border-bottom:1px solid var(--line-soft);padding:.55rem 0">'
                    f'<span>{a}</span><b style="font-weight:560">{b}</b></div>'
                    for a, b in SITE["hours"])
    venues = "".join(f"""<div class="card">
      <p class="card__kicker">{n}</p>
      <h3 style="font-size:1.05rem">{a}</h3>
      <p>{w}</p></div>""" for n, a, w in SITE["venues"])
    areas = "".join(f'<span class="chip">{a}</span>' for a in SITE["areas"])

    local_faq = [
        ("Πού ακριβώς βρίσκεται το ιατρείο;",
         f"<p>Στη Ρωμανού 11 στην Περαία, στον <b>3ο όροφο</b>. Ο χάρτης σε αυτή τη σελίδα "
         "ανοίγει απευθείας οδηγίες πλοήγησης σε Google Maps, Waze ή Moovit.</p>"),
        ("Από ποιες περιοχές έρχονται οι ασθενείς σας;",
         "<p>Κυρίως από την Περαία, τους Νέους Επιβάτες, την Αγία Τριάδα, τη Νέα Μηχανιώνα, "
         "την Επανομή, το Πλαγιάρι και τη Θέρμη, αλλά και από τη Θεσσαλονίκη και την "
         "Καλαμαριά. Το καλοκαίρι έρχονται και επισκέπτες από τη Χαλκιδική.</p>"),
        ("Δέχεστε ραντεβού και στην Αθήνα;",
         f"<p>Ναι. Καλέστε στο <a href=\"tel:{SITE['phone_alt_href']}\">{SITE['phone_alt']}</a> "
         f"ή στο <a href=\"tel:{SITE['phone_mob_href']}\">{SITE['phone_mob']}</a> για "
         "διαθεσιμότητα και τόπο συνάντησης.</p>"),
        ("Χρειάζομαι ραντεβού ή μπορώ να περάσω;",
         f"<p>Χρειάζεται ραντεβού — το ιατρείο λειτουργεί κατόπιν συνεννόησης. Καλέστε στο "
         f"{SITE['phone']}. Τα ραντεβού κλείνονται μόνο τηλεφωνικά — έτσι ξέρετε "
         "αμέσως τι ώρα υπάρχει, χωρίς αναμονή για απάντηση.</p>"),
        ("Τι να φέρω μαζί μου στο πρώτο ραντεβού;",
         "<p>Τα <b>παπούτσια που φοράτε καθημερινά</b> — όχι τα «καλά». Είναι η πιο χρήσιμη "
         "πληροφορία που μπορείτε να δώσετε. Επίσης τη λίστα των φαρμάκων σας, και αν έχετε "
         "διαβήτη, τις τελευταίες εξετάσεις σακχάρου και HbA1c.</p>"),
        ("Μιλάτε αγγλικά;",
         f"<p>Ναι. Η εξέταση και η ενημέρωση μπορούν να γίνουν στα αγγλικά — δείτε και την "
         f"<a href=\"{rel(d)}en/\">αγγλική έκδοση</a> του ιστότοπου.</p>"),
    ]
    faq_html, faq_ld = faq_block("Συχνές ερωτήσεις για την επίσκεψη", local_faq, "faq-visit")

    crumb_html, crumb_ld = crumbs([("Επικοινωνία", None)], d)
    body = f"""<section class="page-head">
  <div class="wrap">{crumb_html}
    <div class="sec-head sec-head--split" style="margin-bottom:0">
      <div class="stack"><p class="eyebrow">Επικοινωνία · Περαία, Θεσσαλονίκη</p>
        <h1>Ρωμανού 11, Περαία — 3ος όροφος.</h1></div>
      <p class="lede">Τα ραντεβού κλείνονται τηλεφωνικά. Καλέστε μας και θα βρούμε
        ώρα μαζί — υπάρχουν ραντεβού και στην Αθήνα.</p>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="contact-grid">
      <div class="stack" style="justify-items:stretch">
        <ul class="info-list">
          <li>{I['pin']}<div><b>Διεύθυνση</b>
            <a href="{SITE['map']}" target="_blank" rel="noopener">{SITE['address']}, {SITE['postcode']} {SITE['locality']}</a></div></li>
          <li>{I['phone']}<div><b>Θεσσαλονίκη</b><a href="tel:{SITE['phone_href']}">{SITE['phone']}</a></div></li>
          <li>{I['phone']}<div><b>Αθήνα</b>
            <a href="tel:{SITE['phone_alt_href']}">{SITE['phone_alt']}</a> ·
            <a href="tel:{SITE['phone_mob_href']}">{SITE['phone_mob']}</a></div></li>
          <li>{I['mail']}<div><b>Email</b><a href="mailto:{SITE['email']}">{SITE['email']}</a></div></li>
          <li>{I['clock']}<div style="width:100%"><b>Ωράριο</b><div style="margin-top:.35rem">{hours}</div></div></li>
        </ul>
        <a class="btn btn--block" href="tel:{SITE['phone_href']}">{I['phone']} Καλέστε για ραντεβού</a>
        <div class="pill-row">
          <a class="chip" href="{SITE['map_full']}" target="_blank" rel="noopener">{I['pin']} Google Maps</a>
          <a class="chip" href="{SITE['waze']}" target="_blank" rel="noopener">Waze</a>
          <a class="chip" href="{SITE['moovit']}" target="_blank" rel="noopener">Moovit</a>
        </div>
      </div>
      <div class="stack" style="justify-items:stretch">
        <iframe class="map" loading="lazy" title="Χάρτης — Ensō Foot Clinic, Ρωμανού 11, Περαία"
          referrerpolicy="no-referrer-when-downgrade"
          src="https://www.google.com/maps?q={SITE['lat']},{SITE['lng']}&amp;z=16&amp;output=embed"></iframe>
        <div class="note">
          <b>Πριν το ραντεβού</b>
          <span>Φέρτε τα παπούτσια που φοράτε καθημερινά. Δείχνουν σε ένα λεπτό αυτό που η
          εξέταση θα έψαχνε σε δέκα.</span>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--tight section--mist">
  <div class="wrap">
    <div class="sec-head sec-head--split">
      <div class="stack"><p class="eyebrow">Πού θα μας βρείτε</p>
        <h2>Δύο τρόποι να κλείσετε ραντεβού.</h2></div>
      <p class="lede">Το ιατρείο είναι στην Περαία. Για την Αθήνα, το ραντεβού κλείνεται
        τηλεφωνικά.</p>
    </div>
    <div class="grid grid--2">{venues}</div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <div class="split">
      <div class="stack">
        <p class="eyebrow">Περιοχές</p>
        <h2>Από πού έρχονται οι ασθενείς μας.</h2>
        <p class="lede">Η Περαία βρίσκεται στην ανατολική παραλιακή ζώνη της Θεσσαλονίκης,
          ανάμεσα σε Νέους Επιβάτες, Αγία Τριάδα και Θέρμη. Δεν υπάρχει δεύτερο ιατρείο σε
          άλλη περιοχή — όλα γίνονται εδώ.</p>
        <div class="pill-row">{areas}</div>
      </div>
      <div class="stack">
        <p class="eyebrow">Έρχεστε από μακριά;</p>
        <h2>Συντονίζουμε αξιολόγηση και θεραπεία στην ίδια επίσκεψη.</h2>
        <p class="lede">Αν ταξιδεύετε από τη Χαλκιδική, από άλλη πόλη ή από το εξωτερικό,
          πείτε το μας όταν κλείνετε το ραντεβού. Θα οργανώσουμε το πρόγραμμα ώστε να μη
          χρειαστεί δεύτερη επίσκεψη για κάτι που μπορεί να γίνει με τη μία.</p>
        <a class="link-more" href="{rel(d)}en/">English information</a>
      </div>
    </div>
  </div>
</section>
{faq_html}
{cta_band(d)}"""

    place_ld = {
        "@context": "https://schema.org", "@type": "ContactPage",
        "name": "Επικοινωνία — Ensō Foot Clinic, Περαία",
        "url": f"{SITE['domain']}/epikoinonia/",
        "inLanguage": "el", "about": {"@id": CLINIC_ID},
        "mainEntity": {"@id": CLINIC_ID},
    }
    ld = [crumb_ld, org_graph(), place_ld]
    if faq_ld:
        ld.append(faq_ld)
    page(path="epikoinonia/",
         title="Επικοινωνία & ραντεβού — Περαία | Ensō Foot Clinic",
         desc=f"Ensō Foot Clinic — {SITE['address']}, {SITE['postcode']} Περαία. "
              f"Θεσσαλονίκη {SITE['phone']} · Αθήνα {SITE['phone_alt']}. Κατόπιν ραντεβού.",
         depth=d, body=body, jsonld=ld, active="contact")


def build_terms():
    d = 1
    body_html, _, _ = prose("oroi-chrisis", d)
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


def build_404():
    d = 0
    body = f"""<section class="section" style="min-height:56vh;display:grid;place-items:center">
  <div class="wrap wrap--narrow" style="text-align:center">
    <p class="eyebrow eyebrow--plain" style="justify-content:center">404</p>
    <h1 style="margin-block:.8rem 1.2rem">Αυτή η σελίδα δεν υπάρχει.</h1>
    <p class="lede" style="margin-inline:auto">Ο ιστότοπος ανανεώθηκε και κάποιοι σύνδεσμοι άλλαξαν.
      Ξεκινήστε από την αρχική ή αναζητήστε αυτό που ψάχνατε.</p>
    <div class="hero__actions" style="justify-content:center;margin-top:1.75rem">
      <a class="btn" href="/">Αρχική</a>
      <button class="btn btn--ghost" data-search-open>{I['search']} Αναζήτηση</button>
    </div>
  </div>
</section>"""
    page(path="404.html", title="Η σελίδα δεν βρέθηκε | Ensō Foot Clinic",
         desc="Η σελίδα που ζητήσατε δεν υπάρχει. Ο ιστότοπος του Ensō Foot Clinic "
              "ανανεώθηκε — ξεκινήστε από την αρχική ή χρησιμοποιήστε την αναζήτηση.",
         depth=d, body=body)


# ── English ─────────────────────────────────────────────────────────────────
from parts import EN_NAV

# hreflang is declared only where a page has a real 1:1 counterpart.
EN_PAIR = {
    "en/": "",
    "en/the-clinic/": "to-iatreio/",
    "en/diabetic-foot-care/": "pathiseis/diavitiko-podi/",
    "en/calluses-and-corns/": "pathiseis/skliryseis-kaloi-tyloi/",
    "en/dry-cracked-heels/": "pathiseis/ksirodermia-pelmaton/",
    "en/ingrown-toenail/": "pathiseis/eisfriksi-nychiou/",
    "en/medical-pedicure/": "ypiresies/iatriki-podologia/",
}


def en_shell(*, path, title, desc, depth, inner, active=""):
    b = rel(depth)
    nav = "".join(f'<a class="chip" href="{b}en/{s}/">{t}</a>' for s, t in EN_NAV)
    hours = "".join(f"<div><span>{a}</span><span>{c}</span></div>" for a, c in SITE["hours_en"])
    body = inner + f"""
<section class="section section--deep">
  <div class="wrap">
    <div class="split">
      <div class="stack">
        <p class="eyebrow">Visiting Thessaloniki</p>
        <h2>Appointments in English.</h2>
        <p class="lede">The full clinical site is in Greek. For an English consultation,
          call or email us — we will answer in English.</p>
        <div class="pill-row" style="margin-top:.5rem">{nav}</div>
      </div>
      <div class="stack" style="justify-items:stretch">
        <a class="btn btn--light btn--block" href="mailto:{SITE['email']}">{I['mail']} {SITE['email']}</a>
        <a class="btn btn--outline-light btn--block" href="tel:{SITE['phone_href']}">{I['phone']} {SITE['phone_href']}</a>
        <p class="tiny" style="color:#8fb8c3">{SITE['address_en']}, {SITE['postcode']}</p>
        <div class="footer__hours" style="color:#a8c9d3">{hours}</div>
      </div>
    </div>
  </div>
</section>"""
    pair = EN_PAIR.get(path)
    page(path=path, title=title, desc=desc, depth=depth, body=body, lang="en",
         active=active, alt=("el", pair) if pair is not None else None, jsonld=[{
             "@context": "https://schema.org", "@type": "MedicalWebPage",
             "name": title, "inLanguage": "en", "specialty": "Podiatric",
             "url": f"{SITE['domain']}/{path}", "publisher": {"@id": CLINIC_ID}},
             org_graph()])


def build_en_home():
    d = 1
    cards = "".join(f"""<a class="card" href="{rel(d)}en/{s}/">
      <h3>{t}</h3><p>{html.escape(plain('en/' + s, 130))}…</p>
      <p class="card__foot"><span class="link-more">Read more</span></p></a>"""
      for s, t in EN_NAV[1:] if ("en/" + s) in COPY)
    inner = f"""<section class="hero">
  <div class="wrap hero__grid">
    <div class="hero__copy">
      <p class="eyebrow">Podology clinic · Peraia, Thessaloniki</p>
      <h1 class="slogan"><span class="qm">“</span>{PRACTITIONER['quote_en']}<span class="qm">”</span></h1>
      <p class="slogan__by">{PRACTITIONER['name_en']}</p>
      <p class="lede">Diabetic foot care, calluses and corns, cracked heels and ingrown
        toenails — treated by Elpiniki Christodoulou, practising since 2002.</p>
      <div class="hero__actions">
        <a class="btn" href="mailto:{SITE['email']}">Request an appointment</a>
        <a class="btn btn--ghost" href="{rel(d)}">Ελληνικά</a>
      </div>
    </div>
    <div class="hero__figure">
      {img("hero-enso.svg", "The clinic's ensō mark", 500, 620, d, priority=True)}
      <div class="hero__badge"><b>{SITE['founded']}</b><span>Practising on the same question ever since: why does this foot hurt</span></div>
    </div>
  </div>
</section>
<section class="section section--tight"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Conditions &amp; services</p>
    <h2>What we treat.</h2></div>
  <div class="grid grid--3">{cards}</div></div></section>"""
    en_shell(path="en/", title="Ensō Foot Clinic — Podology in Thessaloniki, Greece",
             desc="Podology clinic in Peraia, Thessaloniki. Diabetic foot care, calluses "
                  "and corns, cracked heels, ingrown toenail correction. English spoken.",
             depth=1, inner=inner, active="home")


def build_en_page(slug, legacy, title):
    d = 2
    body_html, faq_title, pairs = prose(legacy, d)
    faq_html, _ = faq_block(faq_title, pairs, f"faq-{slug}", lang="en")
    crumb_html, crumb_ld = crumbs([(title, None)], d, lang="en")
    inner = f"""<section class="page-head">
  <div class="wrap wrap--narrow">
    {crumb_html}
    <h1 style="font-size:clamp(1.9rem,1.3rem+2.4vw,3rem)">{title}</h1>
  </div>
</section>
{doc_layout(d, body_html, lang="en")}{faq_html}"""
    en_shell(path=f"en/{slug}/", title=seo_title(f"{title} — Thessaloniki, Greece"),
             desc=meta_desc(legacy, title), depth=d, inner=inner, active=slug)


# ── Search index, sitemap, robots ───────────────────────────────────────────
def build_index_files():
    entries = []

    def add(url, title, blurb, keywords=""):
        entries.append({"u": url, "t": title,
                        "b": re.sub(r"\s+", " ", html.unescape(blurb))[:320], "k": keywords})

    add("", "Αρχική", "Ensō Foot Clinic — ποδολογικό ιατρείο στην Περαία Θεσσαλονίκης, από το 2002.")
    add("to-iatreio/", "Το ιατρείο", plain("to-iatreio", 300), "ποδολογικό ιατρείο περαία")
    add(f"{PRACTITIONER['slug']}/", PRACTITIONER["name"],
        plain(PRACTITIONER["slug"], 300), "ποδολόγος βιογραφικό σεμινάρια")
    add("odigos-symptomaton/", "Οδηγός συμπτωμάτων",
        "Τέσσερις ερωτήσεις σε καθημερινή γλώσσα για να καταλάβετε τι συμβαίνει στα πόδια σας.",
        "τεστ συμπτώματα")
    add("frontida-podion/", "Φροντίδα ποδιών",
        "Ημερήσιος tracker με τρεις ρουτίνες φροντίδας και σερί ημερών.",
        "καθημερινή φροντίδα διαβητικό πόδι ρουτίνα")
    add("pathiseis/", "Παθήσεις", "Διαβητικό πόδι, κάλοι και τύλοι, ξηροδερμία, είσφρηση όνυχος.")
    add("ypiresies/", "Υπηρεσίες", "Σύγκριση υπηρεσιών: χρόνος, αίσθηση, συχνότητα.")
    add("gallery/", "Εικονογραφήσεις", "Σχηματικές εικονογραφήσεις ανατομίας, παθήσεων και θεραπειών.")
    add("epikoinonia/", "Επικοινωνία",
        f"{SITE['address']} · {SITE['phone']} · {SITE['email']}", "ραντεβού χάρτης")
    add("arthra/", "Άρθρα", "Άρθρα ποδολογίας από το Ensō Foot Clinic.")
    add("seminaria/", "Σεμινάρια",
        "Σεμινάρια, workshops και masterclasses ποδολογίας για επαγγελματίες.",
        "εκπαίδευση masterclass workshop")
    for x in SEMINARS:
        add(f"seminaria/{x['slug']}/", x["title"], plain(x["slug"], 320),
            "σεμινάριο εκπαίδευση")
    add("oroi-chrisis/", "Όροι χρήσης & απόρρητο", "Όροι χρήσης και πολιτική απορρήτου.")
    for c in CONDITIONS:
        add(f"pathiseis/{c['slug']}/", c["title"], plain(c["slug"], 320), c["plain"])
    for t in TREATMENTS:
        add(f"ypiresies/{t['slug']}/", t["title"], plain(t["slug"], 320), t["short"])
    for slug, tag in ARTICLES:
        add(f"arthra/{slug}/", article_title(slug), plain(slug, 320), tag)
    add("en/", "Ensō Foot Clinic — English", "Podology in Peraia, Thessaloniki, in English.", "english")
    for slug, legacy, title in EN_PAGES:
        add(f"en/{slug}/", title, plain(legacy, 320), "english")

    write("search-index.json", json.dumps(entries, ensure_ascii=False, separators=(",", ":")))

    urls = [(e["u"], "1.0" if not e["u"] else "0.8" if "/" not in e["u"].rstrip("/") else "0.6")
            for e in entries]
    body = "".join(
        f"<url><loc>{SITE['domain']}/{u}</loc><lastmod>{TODAY}</lastmod>"
        f"<changefreq>monthly</changefreq><priority>{p}</priority></url>" for u, p in urls)
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + body + "</urlset>")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE['domain']}/sitemap.xml\n")
    return len(entries)


# ── Legacy URL redirects ────────────────────────────────────────────────────
# The URLs the current ensofootclinic.gr serves, so nothing that ranks today 404s.
# The «Διαδικτυακά Μαθήματα» section is deliberately not carried over; those URLs
# are redirected to the home page rather than left dangling.
# The two Greek paths appear percent-encoded in the current site's markup, but
# Apache, Netlify and Vercel all match against the *decoded* path — so both
# spellings are emitted for each.
_BIO = "/" + PRACTITIONER["slug"] + "/"
LEGACY_URLS = [
    ("/about", _BIO),
    ("/services", "/ypiresies/"),
    ("/services/ΔΙΑΒΗΤΙΚΟ-ΠΟΔΙ", "/pathiseis/diavitiko-podi/"),
    ("/services/%CE%94%CE%99%CE%91%CE%92%CE%97%CE%A4%CE%99%CE%9A%CE%9F-%CE%A0%CE%9F%CE%94%CE%99",
     "/pathiseis/diavitiko-podi/"),
    ("/contact", "/epikoinonia/"),
    ("/seminars", "/seminaria/"),
    ("/seminars/freeseminar", "/seminaria/1o-seminario-podologias/"),
    ("/terms", "/oroi-chrisis/"),
    ("/privacy", "/oroi-chrisis/"),
    ("/Διαδικτυακά-Μαθήματα", "/"),
    ("/%CE%94%CE%B9%CE%B1%CE%B4%CE%B9%CE%BA%CF%84%CF%85%CE%B1%CE%BA%CE%AC-%CE%9C%CE%B1%CE%B8%CE%AE%CE%BC%CE%B1%CF%84%CE%B1", "/"),
]


def build_redirects():
    rules = list(LEGACY_URLS)

    write("_redirects", "".join(f"{a}  {b}  301\n" for a, b in rules))
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
            # Without the hash, `must-revalidate` would not help: it only applies
            # once max-age has expired, so a day-old stylesheet stays "fresh".
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
    for c in CONDITIONS:
        build_condition(c)
    for t in TREATMENTS:
        build_treatment(t)
    for slug, tag in ARTICLES:
        build_article(slug, tag)
    build_conditions_hub(); build_treatments_hub(); build_articles_hub()
    build_clinic(); build_practitioner(); build_guide_page(); build_tracker_page()
    build_seminars_hub()
    for _s in SEMINARS:
        build_seminar(_s)
    build_gallery(); build_contact(); build_terms(); build_404()
    build_en_home()
    for slug, legacy, title in EN_PAGES:
        build_en_page(slug, legacy, title)
    indexed = build_index_files()
    n = build_redirects()
    pages = sum(len([f for f in fs if f.endswith(".html")]) for _, _, fs in os.walk(OUT))
    print(f"built {pages} pages · {indexed} indexed · {n} redirects · {OUT}")


if __name__ == "__main__":
    main()
