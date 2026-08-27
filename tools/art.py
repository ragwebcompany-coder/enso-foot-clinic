# -*- coding: utf-8 -*-
"""Generates every brand asset and illustration for the site.

    python3 enso-new/tools/art.py

Writes into site/assets/img/:
  · logo.svg / logo-light.svg / favicon.svg / favicon-144.png / og-enso.png
  · hero-enso.svg / hero-enso-dark.svg / clinic-enso.svg
  · elpiniki-christodoulou.svg
  · gal-*.svg — the fourteen schematic illustrations used by /gallery/

Everything is drawn here, from scratch, in the clinic's palette. Nothing is
traced from a photograph and nothing depicts a real patient.
"""
import os, sys, math

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IMG = os.path.join(ROOT, "site", "assets", "img")

# ── Palette (mirrors :root in enso.css) ──────────────────────────────────────
BRAND   = "#63aabc"   # the Ensō brand teal
TEAL    = "#2b7f96"
DEEP    = "#14424f"
ABYSS   = "#0b2a34"
TEAL300 = "#a5d3de"
MIST    = "#e0eff3"
MIST2   = "#f0f8fa"
PAPER   = "#fbfdfd"
LINE    = "#d5e5ea"
INK3    = "#6f8d96"
SKIN    = "#fdf1e8"
SKIN2   = "#f6e0d1"
SKIN_L  = "#e0c6b3"
NAIL    = "#f3e7dc"
WARN    = "#c2865a"
ALERT   = "#c2544f"
KERAT   = "#d9a066"

FONT = ('font-family="Commissioner,-apple-system,BlinkMacSystemFont,'
        '\'Segoe UI\',Helvetica,Arial,sans-serif"')


def w(name, body):
    open(os.path.join(IMG, name), "w", encoding="utf-8").write(body)
    return name


# ── Palette of the mark ──────────────────────────────────────────────────────
# The real Ensō logo is a watercolour brush circle: indigo pigment pooling in
# blooms, thinning to a pale wash where the brush ran dry. These four steps
# reproduce that range while staying inside the site palette.
INK_DEEP = "#1b4f7d"   # where the pigment pools
INK_MID  = "#2b7f96"
INK_SOFT = "#63aabc"   # the brand teal
INK_PALE = "#a5d3de"

# The brush lands at about one o'clock and sweeps clockwise, lifting just short
# of where it began — so the circle stays open at the top right, as it does in
# the clinic's own mark.
ENSO_START, ENSO_SWEEP = -52.0, 336.0


# ── The ensō mark ────────────────────────────────────────────────────────────
def enso_path(cx, cy, r, thick=16.0, start=ENSO_START, sweep=ENSO_SWEEP, steps=150):
    """A single brush stroke closing (almost) into a circle.

    The body of the stroke breathes between roughly 62% and 100% of full weight —
    enough for a brush to read as a brush — and only the first and last few
    percent taper to a point, where the bristles land and lift. A little radial
    wobble keeps it from looking like a machined ring.
    """
    def taper(u):
        body = 0.62 + 0.38 * math.sin(math.pi * (0.20 + 0.66 * u))
        land = min(1.0, u / 0.05) ** 0.7
        lift = min(1.0, (1.0 - u) / 0.13) ** 0.8
        return body * land * lift

    def wobble(u):
        return 1.0 + 0.016 * math.sin(u * 7.1 + 0.7) + 0.010 * math.sin(u * 3.3 + 2.1)

    outer, inner = [], []
    for i in range(steps + 1):
        u = i / steps
        a = math.radians(start + sweep * u)
        t = thick * taper(u)
        rr = r * wobble(u)
        ca, sa = math.cos(a), math.sin(a)
        outer.append((cx + (rr + t / 2) * ca, cy + (rr + t / 2) * sa))
        inner.append((cx + (rr - t / 2) * ca, cy + (rr - t / 2) * sa))
    pts = outer + inner[::-1]
    # One decimal is below the resolution of a displaced, blurred watercolour edge
    # and roughly halves the file.
    d = "M%.1f %.1f " % pts[0] + " ".join("L%.1f %.1f" % p for p in pts[1:]) + " Z"
    return d


def _at(cx, cy, r, u, start=ENSO_START, sweep=ENSO_SWEEP):
    """Point on the stroke centreline, u from 0 (brush lands) to 1 (brush lifts)."""
    a = math.radians(start + sweep * u)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def _arc(cx, cy, r, u0, u1, steps=44, start=ENSO_START, sweep=ENSO_SWEEP):
    pts = [_at(cx, cy, r, u0 + (u1 - u0) * i / steps, start, sweep) for i in range(steps + 1)]
    return "M%.1f %.1f " % pts[0] + " ".join("L%.1f %.1f" % p for p in pts[1:])


# Where the pigment pools, as (position along the stroke, size × thickness,
# opacity). Irregular on purpose — evenly spaced blooms read as a pattern rather
# than as paint. The two heaviest sit where the brush was still fully loaded.
_BLOOMS = [(0.03, 1.45, .90), (0.12, 1.05, .55), (0.26, 1.60, .95),
           (0.38, 0.90, .45), (0.52, 1.25, .68), (0.66, 0.95, .40),
           (0.79, 1.15, .48), (0.91, 0.85, .28)]

# Where the brush ran dry — pale, soft-edged gaps rather than hard scratches.
_DRY = [(0.30, 0.16, 0.44, .34), (-0.30, 0.54, 0.72, .30), (0.14, 0.80, 0.96, .26)]


def _rgb(hexs):
    hexs = hexs.lstrip("#")
    return tuple(round(int(hexs[i:i + 2], 16) / 255, 4) for i in (0, 2, 4))


def enso_mark(cx, cy, r, thick, uid, *, deep=INK_DEEP, mid=INK_MID,
              soft=INK_SOFT, pale=INK_PALE, seed=7, wash=True, texture=1.0):
    """The mark as watercolour: a washed body, pigment blooming into it, granulation
    settling in the paper's tooth, dry-brush gaps, and a ragged wet edge.

    Everything sits inside one filtered group, so the displacement that roughens
    the outline moves the paint with it and nothing escapes the stroke.

    `texture` scales every effect that eats into the stroke — the edge
    displacement, the dry-brush gaps and the granulation. At a 40px header logo,
    texture tuned for a 340px hero simply dissolves the mark, so small lockups
    pass a fraction here and keep their mass.
    """
    texture = max(0.0, min(1.0, texture))
    d = enso_path(cx, cy, r, thick)
    box = (cx - r - thick, cy - r - thick, 2 * (r + thick), 2 * (r + thick))
    dr, dg, db = _rgb(deep)

    blooms = "".join(
        f'<circle cx="{_at(cx, cy, r, u)[0]:.1f}" cy="{_at(cx, cy, r, u)[1]:.1f}" '
        f'r="{thick * size:.1f}" fill="url(#bloom{uid})" opacity="{op}"/>'
        for u, size, op in _BLOOMS)

    dry = "".join(
        f'<path d="{_arc(cx, cy, r + off * thick, u0, u1)}" fill="none" stroke="{pale}" '
        f'stroke-width="{thick * 0.30 * texture:.2f}" stroke-linecap="round" '
        f'opacity="{op * texture:.2f}"/>'
        for off, u0, u1, op in _DRY)

    halo = (f'<path d="{d}" fill="{pale}" opacity=".28" filter="url(#wash{uid})"/>'
            if wash else "")
    return f"""<defs>
    <filter id="wet{uid}" x="-30%" y="-30%" width="160%" height="160%">
      <feTurbulence type="fractalNoise" baseFrequency="0.022 0.030" numOctaves="4"
                    seed="{seed}" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="{thick * 0.42 * texture:.2f}"
                         xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <filter id="wash{uid}" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="{thick * 0.30:.1f}"/>
    </filter>
    <filter id="soft{uid}" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="{thick * 0.20:.2f}"/>
    </filter>
    <!-- Granulation: pigment settling into the tooth of the paper. The matrix
         turns the noise's red channel into a patchy alpha over a flat deep ink. -->
    <filter id="grain{uid}" x="0%" y="0%" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="{0.9 / max(1.0, thick / 14):.3f}"
                    numOctaves="3" seed="{seed + 4}" result="t"/>
      <feColorMatrix in="t" type="matrix"
        values="0 0 0 0 {dr}  0 0 0 0 {dg}  0 0 0 0 {db}  1.15 0 0 0 -0.42"/>
    </filter>
    <linearGradient id="body{uid}" x1="0" y1="0" x2=".85" y2="1">
      <stop offset="0" stop-color="{mid}"/>
      <stop offset=".45" stop-color="{soft}"/>
      <stop offset="1" stop-color="{pale}"/>
    </linearGradient>
    <radialGradient id="bloom{uid}">
      <stop offset="0" stop-color="{deep}" stop-opacity=".95"/>
      <stop offset=".5" stop-color="{deep}" stop-opacity=".42"/>
      <stop offset="1" stop-color="{deep}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="clip{uid}"><path d="{d}"/></clipPath>
  </defs>
  {halo}
  <g filter="url(#wet{uid})">
    <path d="{d}" fill="url(#body{uid})"/>
    <g clip-path="url(#clip{uid})">
      <g filter="url(#soft{uid})">{blooms}</g>
      <g filter="url(#soft{uid})">{dry}</g>
      <rect x="{box[0]:.1f}" y="{box[1]:.1f}" width="{box[2]:.1f}" height="{box[3]:.1f}"
            filter="url(#grain{uid})" opacity="{0.55 * texture:.2f}"/>
    </g>
    <path d="{d}" fill="none" stroke="{deep}" stroke-width="{max(0.7, thick * 0.05):.2f}"
          opacity=".30"/>
  </g>"""


# Schematic plantar view of a right foot: wide across the ball, waisted at the
# arch, rounded at the heel, with five separate toes. Drawn in a 180×300 box
# with the toes at the top.
_SOLE = ("M34 92C34 62 56 48 84 50C112 52 148 60 150 88C152 116 138 140 134 168"
         "C130 196 140 220 138 246C136 276 116 292 94 292C70 292 52 276 52 248"
         "C52 218 64 196 66 170C68 142 34 122 34 92Z")
_TOES = [(48, 30, 17, 20, -16), (82, 22, 12.5, 15.5, -6),
         (105, 21, 11.5, 14.5, 0), (126, 26, 10.5, 13, 8), (145, 36, 9, 11, 16)]


def foot_outline(dx=0.0, dy=0.0, scale=1.0, fill=SKIN, stroke=SKIN_L, sw=2.0):
    toes = "".join(
        f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" transform="rotate({rot} {x} {y})" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        for x, y, rx, ry, rot in _TOES)
    return (f'<g transform="translate({dx},{dy}) scale({scale})">'
            f'<path d="{_SOLE}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
            f"{toes}</g>")


def label(x, y, text, *, size=15, colour=DEEP, weight=560, anchor="start"):
    return (f'<text x="{x}" y="{y}" {FONT} font-size="{size}" font-weight="{weight}" '
            f'fill="{colour}" text-anchor="{anchor}">{text}</text>')


def lead(d, colour=INK3, dash="4 5"):
    return (f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="1.3" '
            f'stroke-dasharray="{dash}"/>')


# ── Logo ─────────────────────────────────────────────────────────────────────
# The clinic's own lockup stacks «Ensō» over «Foot Clinic» over the practitioner's
# name and «Podology - Podiatry». A site header cannot carry four lines, so the
# two halves of the name sit on one line in two weights — the same two-tone split
# the original makes with colour — and the descriptor keeps its own line.
def logo(light=False, descriptor=None):
    """`descriptor=True` adds the «Podology · Podiatry» line the clinic's own mark
    carries. It is dropped from the header lockup, where the logo renders about
    170px wide and the line would be four pixels tall — the footer and the banner
    keep it, because there it is legible."""
    if descriptor is None:
        descriptor = light
    name = "#ffffff" if light else DEEP
    second = TEAL300 if light else TEAL
    desc = TEAL300 if light else INK3
    uid = "L" if light else "D"
    h = 124 if descriptor else 96
    cy = 62 if descriptor else 48
    # At header size the mark renders about 40px across, where a full watercolour
    # range washes out to nothing. The dark lockup therefore keeps the texture but
    # compresses the palette into its deeper half, and drops the soft outer halo.
    mark = enso_mark(60, cy, 40, 15, uid, wash=light,
                     texture=0.55 if descriptor else 0.42,
                     deep=(TEAL if light else INK_DEEP),
                     mid=(INK_SOFT if light else INK_DEEP),
                     soft=(TEAL300 if light else INK_MID),
                     pale=("#d6ecf2" if light else INK_SOFT))
    tail = (f'\n  <text x="128" y="95" {FONT} font-size="12.5" font-weight="500" '
            f'letter-spacing="4.2" fill="{desc}">PODOLOGY · PODIATRY</text>'
            if descriptor else "")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 396 {h}" width="396" height="{h}"
  role="img" aria-label="Ensō Foot Clinic — Ποδολογία, Ποδιατρική">
  {mark}
  <text x="126" y="{cy + 8}" {FONT} font-size="34" fill="{name}">
    <tspan font-weight="600" letter-spacing="-.5">Ensō</tspan><tspan
       font-weight="300" fill="{second}" letter-spacing=".2"> Foot Clinic</tspan></text>{tail}
</svg>"""


def favicon():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64"
  role="img" aria-label="Ensō Foot Clinic">
  <rect width="64" height="64" rx="14" fill="{DEEP}"/>
  {enso_mark(32, 33, 20, 7.6, "F", deep=INK_SOFT, mid=TEAL300, soft="#c4e4ec",
             pale="#e4f4f8", wash=False, texture=0.3)}
</svg>"""


# ── Hero / clinic / portrait panels ──────────────────────────────────────────
def hero():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 620" width="500" height="620"
  role="img" aria-label="Το υδατογραφικό σήμα ensō του ιατρείου με σχηματικό περίγραμμα πέλματος">
  <defs>
    <linearGradient id="hbg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{MIST2}"/><stop offset="1" stop-color="{MIST}"/>
    </linearGradient>
  </defs>
  <rect width="500" height="620" fill="url(#hbg)"/>
  {enso_mark(250, 300, 168, 54, "H", seed=3)}
  {foot_outline(dx=168, dy=148, scale=0.82, fill="#ffffff", stroke=TEAL300, sw=2.4)}
  <g fill="none" stroke="{TEAL}" stroke-width="2" opacity=".5" stroke-linecap="round">
    <path d="M212 388c26 7 52 8 78 3"/>
    <path d="M204 300c14-8 30-12 46-12"/>
  </g>
  <circle cx="250" cy="470" r="5" fill="{BRAND}"/>
  <circle cx="228" cy="352" r="5" fill="{BRAND}"/>
  <circle cx="272" cy="252" r="5" fill="{BRAND}"/>
</svg>"""


def hero_dark():
    """The hero mark for the deep homepage ground: no background of its own, so the
    glass panel behind it shows through, and the ink shifted up the palette so it
    glows rather than sinks."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 620" width="500" height="620"
  role="img" aria-label="Το υδατογραφικό σήμα ensō του ιατρείου με σχηματικό περίγραμμα πέλματος">
  {enso_mark(250, 300, 168, 54, "HD", deep=TEAL, mid=INK_SOFT, soft=TEAL300,
             pale="#d9eef4", seed=3)}
  {foot_outline(dx=168, dy=148, scale=0.82, fill="none", stroke="#ffffff", sw=2.6)}
  <g fill="none" stroke="{TEAL300}" stroke-width="2" opacity=".65" stroke-linecap="round">
    <path d="M212 388c26 7 52 8 78 3"/>
    <path d="M204 300c14-8 30-12 46-12"/>
  </g>
  <circle cx="250" cy="470" r="5" fill="#ffffff"/>
  <circle cx="228" cy="352" r="5" fill="#ffffff"/>
  <circle cx="272" cy="252" r="5" fill="#ffffff"/>
</svg>"""


def clinic_banner():
    """The full four-line lockup the clinic uses, on its own ground."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 700" width="1600" height="700"
  role="img" aria-label="Ensō Foot Clinic — Χριστοδούλου Ελπινίκη, Ποδολογία & Ποδιατρική">
  <defs>
    <linearGradient id="cbg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{DEEP}"/><stop offset="1" stop-color="{ABYSS}"/>
    </linearGradient>
  </defs>
  <rect width="1600" height="700" fill="url(#cbg)"/>
  <g opacity=".10" fill="none" stroke="{BRAND}" stroke-width="1.4">
    {"".join(f'<circle cx="1170" cy="350" r="{r}"/>' for r in range(60, 640, 42))}
  </g>
  {enso_mark(1170, 350, 212, 70, "C", deep=TEAL, mid=INK_SOFT, soft=TEAL300,
             pale="#d9eef4", seed=11)}
  {foot_outline(dx=1084, dy=180, scale=0.9, fill="none", stroke="#ffffff", sw=2.6)}
  <text x="120" y="292" {FONT} font-size="76" fill="#ffffff">
    <tspan font-weight="600">Ensō</tspan><tspan font-weight="300" fill="{TEAL300}"> Foot Clinic</tspan></text>
  <text x="124" y="352" {FONT} font-size="30" font-weight="500" letter-spacing="7"
        fill="{BRAND}">PODOLOGY · PODIATRY</text>
  <text x="122" y="440" {FONT} font-size="30" font-weight="400" fill="{TEAL300}"
        opacity=".9">Χριστοδούλου Ελπινίκη · Περαία, Θεσσαλονίκη · από το 2002</text>
</svg>"""


def portrait():
    """Brand panel used where a photograph of the practitioner will eventually go.
    Deliberately a monogram, not an invented likeness."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 900" width="900" height="900"
  role="img" aria-label="Ελπινίκη Χριστοδούλου — Ποδολόγος, Ensō Foot Clinic">
  <defs>
    <linearGradient id="pbg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{MIST2}"/><stop offset="1" stop-color="{MIST}"/>
    </linearGradient>
  </defs>
  <rect width="900" height="900" fill="url(#pbg)"/>
  {enso_mark(450, 400, 232, 74, "P", seed=5)}
  <text x="450" y="436" {FONT} font-size="146" font-weight="300" fill="#ffffff"
        text-anchor="middle">ΕΧ</text>
  <text x="450" y="700" {FONT} font-size="42" font-weight="560" fill="{DEEP}"
        text-anchor="middle">Ελπινίκη Χριστοδούλου</text>
  <text x="450" y="748" {FONT} font-size="26" font-weight="420" fill="{TEAL}"
        text-anchor="middle" letter-spacing="2.4">ΠΟΔΟΛΟΓΟΣ · ΑΠΟ ΤΟ 2002</text>
</svg>"""


# ── Gallery illustrations ────────────────────────────────────────────────────
GW, GH = 800, 500
PAD_X, PAD_Y = 62, 10


def frame(inner, aria):
    """Artwork is authored in a 640×480 field and inset here, which leaves a
    gutter on each side for the callout labels to live in."""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {GW} {GH}" '
            f'width="{GW}" height="{GH}" role="img" aria-label="{aria}">'
            f'<rect width="{GW}" height="{GH}" fill="{PAPER}"/>'
            f'<g transform="translate({PAD_X},{PAD_Y})">{inner}</g></svg>')


def g_foot_anatomy():
    zones = [(320, 128, 74, 34, KERAT, "Μετατάρσια"),
             (320, 352, 90, 46, KERAT, "Πτέρνα"),
             (278, 96, 24, 26, TEAL300, "Μέγας δάκτυλος")]
    blobs = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}" opacity=".38"/>'
                    for x, y, rx, ry, c, _n in zones)
    return frame(f"""
  {foot_outline(dx=220, dy=60, scale=1.2, fill=SKIN, stroke=SKIN_L, sw=2.2)}
  {blobs}
  <g fill="none" stroke="{TEAL}" stroke-width="1.8" opacity=".7" stroke-linecap="round">
    <path d="M258 176c40 46 66 100 62 156"/>
  </g>
  {lead("M394 128H470")}{label(478, 133, "Ζώνη μεταταρσίων")}
  {lead("M410 352H470")}{label(478, 357, "Ζώνη πτέρνας")}
  {lead("M278 70V34h-58")}{label(212, 39, "Μέγας δάκτυλος", anchor="end")}
  {lead("M300 268h-84")}{label(208, 273, "Καμάρα", anchor="end")}
  {label(40, 444, "Οι δύο σκούρες ζώνες σηκώνουν το μεγαλύτερο φορτίο σε κάθε βήμα.", size=13.5, colour=INK3, weight=420)}
""", "Ζώνες πίεσης του πέλματος")


def g_nail_anatomy():
    return frame(f"""
  <rect x="130" y="120" width="380" height="230" rx="26" fill="{SKIN}" stroke="{SKIN_L}" stroke-width="2"/>
  <rect x="176" y="150" width="288" height="170" rx="20" fill="{NAIL}" stroke="{SKIN_L}" stroke-width="1.6"/>
  <path d="M176 208c96-22 192-22 288 0" fill="none" stroke="{TEAL300}" stroke-width="2.4"/>
  <path d="M176 170h288" fill="none" stroke="{SKIN_L}" stroke-width="1.4" stroke-dasharray="4 5"/>
  <rect x="176" y="150" width="288" height="34" rx="16" fill="{TEAL300}" opacity=".5"/>
  {lead("M320 150V96h100")}{label(428, 101, "Ονυχική μήτρα (ρίζα)")}
  {lead("M320 235h150")}{label(478, 240, "Πλάκα")}
  {lead("M320 320v42h116")}{label(444, 367, "Ελεύθερο άκρο")}
  {lead("M176 260H96")}{label(88, 265, "Πλάγια πτυχή", anchor="end")}
  {label(40, 444, "Το νύχι μεγαλώνει από την ονυχική μήτρα προς το ελεύθερο άκρο.", size=13.5, colour=INK3, weight=420)}
""", "Τομή νυχιού")


def g_arch_types():
    """Three lateral foot profiles side by side. What changes between them is the
    clearance under the arch — and therefore where the weight lands."""
    def panel(x, h, name, note):
        g = 300  # ground line
        sole = (f"M16 {g}L76 {g}C104 {g} 108 {g - h} 134 {g - h}"
                f"C158 {g - h} 160 {g} 184 {g}"
                f"C196 {g} 197 268 190 246C182 216 168 202 140 200"
                f"C110 198 84 216 62 244C46 264 30 284 16 {g}Z")
        return (f'<g transform="translate({x},0)">'
                f'<rect x="-4" y="150" width="212" height="230" rx="18" fill="{MIST2}"/>'
                f'<path d="{sole}" fill="{SKIN}" stroke="{SKIN_L}" stroke-width="2"/>'
                f'<path d="M76 {g}C104 {g} 108 {g - h} 134 {g - h}C158 {g - h} 160 {g} 184 {g}" '
                f'fill="none" stroke="{TEAL}" stroke-width="4"/>'
                f'<path d="M4 {g + 6}h196" stroke="{LINE}" stroke-width="5" stroke-linecap="round"/>'
                f'<circle cx="46" cy="{g}" r="6" fill="{KERAT}"/>'
                f'<circle cx="184" cy="{g}" r="6" fill="{KERAT}"/>'
                + label(100, 336, name, size=15, anchor="middle")
                + label(100, 358, note, size=12, colour=INK3, weight=420, anchor="middle")
                + "</g>")
    return frame(f"""
  {label(40, 66, "Πώς αλλάζει η κατανομή του βάρους", size=19, weight=560)}
  {label(40, 96, "Όσο πέφτει η καμάρα, τόσο μετακινείται το φορτίο μπροστά και μέσα.", size=13.5, colour=INK3, weight=420)}
  {panel(14, 66, "Κοίλος πους", "Ψηλή καμάρα · φορτίο σε δύο σημεία")}
  {panel(224, 36, "Φυσιολογικό", "Ισορροπημένη κατανομή")}
  {panel(434, 8, "Πλατυποδία", "Χαμηλή καμάρα · φορτίο προς τα μέσα")}
  {label(40, 444, "Οι δύο κουκκίδες δείχνουν πού ακουμπά πραγματικά το πόδι στο έδαφος.", size=13.5, colour=INK3, weight=420)}
""", "Τύποι ποδικής καμάρας")


def g_callus():
    return frame(f"""
  <rect x="70" y="150" width="500" height="70" fill="{SKIN}" stroke="none"/>
  <rect x="70" y="220" width="500" height="96" fill="{SKIN2}" stroke="none"/>
  <path d="M70 150h500" stroke="{SKIN_L}" stroke-width="2"/>
  <path d="M70 316h500" stroke="{SKIN_L}" stroke-width="2"/>
  <path d="M148 150c46-26 96-26 140 0z" fill="{KERAT}" opacity=".65"/>
  <path d="M148 150c46-26 96-26 140 0" fill="none" stroke="{WARN}" stroke-width="2"/>
  <path d="M366 150c34-34 78-34 112 0z" fill="{KERAT}" opacity=".65"/>
  <path d="M366 150c34-34 78-34 112 0" fill="none" stroke="{WARN}" stroke-width="2"/>
  <path d="M422 150l-14 88h28z" fill="{WARN}"/>
  <circle cx="422" cy="246" r="12" fill="{ALERT}" opacity=".28"/>
  {label(148, 108, "Τύλος", size=17)}
  {label(366, 100, "Κάλος με πυρήνα", size=17)}
  {lead("M422 260v46h96")}{label(526, 311, "Πυρήνας που πιέζει", size=13.5, colour=ALERT, weight=520)}
  {label(586, 190, "Κεράτινη", size=12.5, colour=INK3, weight=420, anchor="end")}
  {label(586, 276, "Χόριο", size=12.5, colour=INK3, weight=420, anchor="end")}
  {label(40, 444, "Ο τύλος απλώνεται· ο κάλος στέλνει κώνο προς τα μέσα και πονάει σημειακά.", size=13.5, colour=INK3, weight=420)}
""", "Τύλος και κάλος σε τομή")


def g_heel_fissure():
    cracks = "".join(f'<path d="M{x} 176v{d}" stroke="{ALERT}" stroke-width="5" stroke-linecap="round"/>'
                     for x, d in ((196, 96), (256, 118), (316, 104), (376, 126), (436, 92)))
    return frame(f"""
  <path d="M120 176c96-40 304-40 400 0v122c-96 34-304 34-400 0z" fill="{SKIN}" stroke="{SKIN_L}" stroke-width="2"/>
  <path d="M120 176c96-40 304-40 400 0v34c-96 26-304 26-400 0z" fill="{KERAT}" opacity=".55"/>
  {cracks}
  <path d="M120 330c96 40 304 40 400 0" fill="none" stroke="{LINE}" stroke-width="5" stroke-linecap="round"/>
  {lead("M256 160V104h130")}{label(394, 109, "Παχυσμένη κεράτινη", size=14)}
  {lead("M376 316v44h96")}{label(480, 365, "Ραγάδα σε βάθος", size=14, colour=ALERT, weight=520)}
  {label(40, 92, "Ραγάδα πτέρνας", size=19, weight=560)}
  {label(40, 444, "Το άκαμπτο δέρμα δεν ακολουθεί το πλάτυσμα της πτέρνας — και σχίζεται κάθετα.", size=13.5, colour=INK3, weight=420)}
""", "Ραγάδα πτέρνας")


def g_ingrown():
    return frame(f"""
  <path d="M140 300c0-104 76-176 180-176s180 72 180 176z" fill="{SKIN}" stroke="{SKIN_L}" stroke-width="2"/>
  <path d="M198 300c0-72 52-122 122-122s122 50 122 122z" fill="{NAIL}" stroke="{SKIN_L}" stroke-width="1.8"/>
  <path d="M198 300c0-72 52-122 122-122" fill="none" stroke="{TEAL}" stroke-width="3"/>
  <path d="M442 300c0-72-52-122-122-122" fill="none" stroke="{ALERT}" stroke-width="5"/>
  <path d="M436 268c14 24 12 44-2 56" fill="none" stroke="{ALERT}" stroke-width="6" stroke-linecap="round"/>
  <ellipse cx="460" cy="296" rx="34" ry="26" fill="{ALERT}" opacity=".24"/>
  <path d="M140 300h360" stroke="{SKIN_L}" stroke-width="2"/>
  {lead("M488 296h56")}{label(552, 301, "Φλεγμονή", size=14, colour=ALERT, weight=520)}
  {lead("M260 190V128h-92")}{label(160, 133, "Υγιής πλευρά", size=14, anchor="end")}
  {label(40, 92, "Είσφρηση όνυχος", size=19, weight=560)}
  {label(40, 444, "Η αιχμή του νυχιού πιέζει την πλάγια πτυχή· η φλεγμονή τη σπρώχνει πιο κοντά.", size=13.5, colour=INK3, weight=420)}
""", "Είσφρηση όνυχος")


def g_diabetic_foot():
    return frame(f"""
  {foot_outline(dx=112, dy=54, scale=1.2, fill=SKIN, stroke=SKIN_L, sw=2.2)}
  <path d="M232 96c-6 96-30 168-72 224" fill="none" stroke="{TEAL}" stroke-width="5"
        stroke-linecap="round" stroke-dasharray="10 9" opacity=".8"/>
  <path d="M182 300c-14 46-26 82-38 108" fill="none" stroke="{ALERT}" stroke-width="6"
        stroke-linecap="round" opacity=".45"/>
  <g fill="none" stroke="{ALERT}" stroke-width="3">
    <circle cx="212" cy="140" r="14"/><circle cx="176" cy="330" r="14"/><circle cx="212" cy="388" r="14"/>
  </g>
  <circle cx="176" cy="330" r="6" fill="{ALERT}"/>
  {lead("M232 96V56h140")}{label(380, 61, "Νεύρα: χαμένη αίσθηση", size=14)}
  {lead("M182 300h-96")}{label(78, 305, "Αγγεία: αργή επούλωση", size=14, anchor="end")}
  {lead("M226 388h150")}{label(384, 393, "Σημεία υπερπίεσης", size=14, colour=ALERT, weight=520)}
  {label(40, 444, "Το πρόβλημα δεν είναι ότι πονάει. Είναι ότι δεν πονάει.", size=13.5, colour=INK3, weight=420)}
""", "Διαβητικό πόδι")


def g_onychomycosis():
    return frame(f"""
  <g>
    <rect x="90" y="170" width="180" height="150" rx="20" fill="{NAIL}" stroke="{SKIN_L}" stroke-width="1.8"/>
    <path d="M90 250c60-14 120-14 180 0" fill="none" stroke="{TEAL300}" stroke-width="2"/>
    {label(180, 356, "Υγιές νύχι", size=15, anchor="middle")}
  </g>
  <g>
    <rect x="370" y="160" width="180" height="170" rx="20" fill="#e9d5b6" stroke="{WARN}" stroke-width="2"/>
    <path d="M370 250c60-14 120-14 180 0" fill="none" stroke="{WARN}" stroke-width="2"/>
    <path d="M470 160v170" stroke="#c9a06a" stroke-width="2" stroke-dasharray="5 6"/>
    <path d="M506 168c18 40 16 96-2 148" fill="none" stroke="#b07f42" stroke-width="5"/>
    <path d="M534 176c10 44 8 100-4 146" fill="none" stroke="#9a6b33" stroke-width="4"/>
    {label(460, 356, "Προσβεβλημένο νύχι", size=15, anchor="middle")}
  </g>
  {label(40, 92, "Ονυχομυκητίαση", size=19, weight=560)}
  {label(40, 444, "Πάχυνση, αποχρωματισμός και θρυμματισμός — από την άκρη προς τη ρίζα.", size=13.5, colour=INK3, weight=420)}
""", "Ονυχομυκητίαση")


def g_brace():
    return frame(f"""
  <path d="M150 320c0-108 76-182 180-182s180 74 180 182z" fill="{SKIN}" stroke="{SKIN_L}" stroke-width="2"/>
  <path d="M204 320c0-74 56-126 126-126s126 52 126 126z" fill="{NAIL}" stroke="{SKIN_L}" stroke-width="1.8"/>
  <path d="M212 268c72-40 164-40 236 0" fill="none" stroke="{TEAL}" stroke-width="11" stroke-linecap="round"/>
  <path d="M212 268c72-40 164-40 236 0" fill="none" stroke="{TEAL300}" stroke-width="4" stroke-linecap="round"/>
  <g fill="none" stroke="{TEAL}" stroke-width="3" stroke-linecap="round">
    <path d="M212 250v-30M216 244l-8 12M212 244l8 12"/>
    <path d="M448 250v-30M444 244l-8 12M448 244l8 12"/>
  </g>
  <path d="M150 320h360" stroke="{SKIN_L}" stroke-width="2"/>
  {lead("M330 262V150h136")}{label(474, 155, "Υαλώδης νάρθηκας", size=14, colour=TEAL, weight=560)}
  {lead("M448 300h74")}{label(530, 305, "Ανοδική τάση", size=13.5, colour=INK3, weight=420)}
  {label(40, 92, "Ορθονυχία", size=19, weight=560)}
  {label(40, 444, "Ίδια λογική με τα ορθοδοντικά σιδεράκια: μικρή δύναμη, συνεχώς, για μήνες.", size=13.5, colour=INK3, weight=420)}
""", "Νάρθηκας ορθονυχίας")


def g_debridement():
    layers = "".join(
        f'<path d="M170 {y}c56-{18 - i * 3} 172-{18 - i * 3} 228 0" fill="none" '
        f'stroke="{KERAT}" stroke-width="9" opacity="{0.9 - i * 0.16:.2f}" stroke-linecap="round"/>'
        for i, y in enumerate((190, 212, 234, 256)))
    return frame(f"""
  <rect x="120" y="270" width="360" height="80" fill="{SKIN2}"/>
  <rect x="120" y="266" width="360" height="8" fill="{SKIN_L}"/>
  {layers}
  <path d="M470 128l86-58 20 26-86 58z" fill="{TEAL300}"/>
  <path d="M470 128l-38 26 44 6z" fill="{DEEP}"/>
  <path d="M120 350h360" stroke="{LINE}" stroke-width="3"/>
  {lead("M300 178V112h-140")}{label(152, 117, "Στρώση-στρώση", size=14, anchor="end")}
  {lead("M300 300h190")}{label(498, 305, "Υγιές δέρμα", size=13.5, colour=INK3, weight=420)}
  {label(40, 92, "Αφαίρεση τύλου", size=19, weight=560)}
  {label(40, 444, "Αφαιρείται νεκρή κεράτινη — δεν έχει νεύρα, γι' αυτό δεν πονάει.", size=13.5, colour=INK3, weight=420)}
""", "Αφαίρεση τύλου")


def g_offloading():
    arrows = "".join(f'<path d="M{x} 150v56" stroke="{ALERT}" stroke-width="5" stroke-linecap="round"/>'
                     f'<path d="M{x - 9} 196l9 12 9-12" fill="none" stroke="{ALERT}" stroke-width="5" '
                     f'stroke-linecap="round" stroke-linejoin="round"/>' for x in (190, 450))
    return frame(f"""
  <path d="M120 300c92-34 268-34 360 0v34c-92 30-268 30-360 0z" fill="{SKIN}" stroke="{SKIN_L}" stroke-width="2"/>
  <path d="M232 288c40-22 96-22 136 0v22c-40 18-96 18-136 0z" fill="{TEAL300}" opacity=".8"/>
  <ellipse cx="300" cy="300" rx="26" ry="12" fill="{PAPER}" stroke="{TEAL}" stroke-width="2"/>
  <path d="M300 156v50" stroke="{TEAL}" stroke-width="5" stroke-linecap="round" stroke-dasharray="6 8"/>
  {arrows}
  <path d="M120 348h360" stroke="{LINE}" stroke-width="4" stroke-linecap="round"/>
  {lead("M368 274V128h108")}{label(484, 133, "Πέλμα σιλικόνης", size=14, colour=TEAL, weight=560)}
  {lead("M300 322v40h-116")}{label(176, 367, "Το σημείο μένει ελεύθερο", size=13.5, colour=INK3, weight=420, anchor="end")}
  {label(40, 92, "Αποφόρτιση", size=19, weight=560)}
  {label(40, 444, "Το βάρος μοιράζεται περιμετρικά, όχι πάνω στο σημείο που πονάει.", size=13.5, colour=INK3, weight=420)}
""", "Αποφόρτιση με πέλμα σιλικόνης")


def g_nail_cutting():
    def toe(x, path_d, ok):
        colour = TEAL if ok else ALERT
        mark = (f'<circle cx="{x + 90}" cy="120" r="19" fill="none" stroke="{colour}" stroke-width="3.4"/>'
                + (f'<path d="M{x + 81} 120l7 8 12-15" fill="none" stroke="{colour}" stroke-width="3.4" '
                   f'stroke-linecap="round" stroke-linejoin="round"/>' if ok else
                   f'<path d="M{x + 83} 113l14 14M{x + 97} 113l-14 14" stroke="{colour}" stroke-width="3.4" '
                   f'stroke-linecap="round"/>'))
        return (f'<g transform="translate({x},0)">'
                f'<path d="M20 330c0-92 70-156 160-156s160 64 160 156z" fill="{SKIN}" stroke="{SKIN_L}" stroke-width="2"/>'
                f'<path d="{path_d}" fill="{NAIL}" stroke="{colour}" stroke-width="3"/>'
                f'<path d="M20 330h320" stroke="{SKIN_L}" stroke-width="2"/></g>') + mark
    return frame(f"""
  <g transform="translate(-6,0) scale(.62) translate(60,150)">
    {toe(0, "M70 330V254c0-40 50-62 110-62s110 22 110 62v76z", True)}
  </g>
  <g transform="translate(330,0) scale(.62) translate(60,150)">
    {toe(0, "M70 330v-46c0-64 50-92 110-92s110 28 110 92v46z", False)}
  </g>
  {label(126, 400, "Ίσια — σωστό", size=16, colour=TEAL, anchor="middle")}
  {label(456, 400, "Στρογγυλά — λάθος", size=16, colour=ALERT, anchor="middle")}
  {label(40, 92, "Πώς κόβουμε τα νύχια", size=19, weight=560)}
  {label(40, 444, "Οι στρογγυλεμένες γωνίες αφήνουν αιχμή που τρυπάει την πτυχή του δέρματος.", size=13.5, colour=INK3, weight=420)}
""", "Σωστό κόψιμο νυχιών")


def g_shoe_fit():
    """Top-down: the foot inside the last, with the three things worth measuring.
    The drawing sits in its own scaled group so it clears the title and caption."""
    shoe = ("M250 150C250 92 288 52 336 52C384 52 422 92 422 150"
            "C422 214 412 268 406 320C400 380 388 436 336 436"
            "C284 436 272 380 266 320C260 268 250 214 250 150Z")
    art = f"""
  <path d="{shoe}" fill="#ffffff" stroke="{DEEP}" stroke-width="3.6"/>
  {foot_outline(dx=230, dy=84.5, scale=1.15, fill=SKIN, stroke=SKIN_L, sw=2.2)}
  <path d="M266 352h140" fill="none" stroke="{TEAL300}" stroke-width="2.2" stroke-dasharray="6 7"/>
  <path d="M256 210h176" fill="none" stroke="{TEAL300}" stroke-width="2.2" stroke-dasharray="6 7"/>
  <g stroke="{TEAL}" stroke-width="3.2" stroke-linecap="round" fill="none">
    <path d="M448 52h26M448 92h26M461 56v32"/>
    <path d="M455 62l6-8 6 8M455 82l6 8 6-8"/>
  </g>
  {label(490, 78, "≈1 εκ. κενό", size=16, colour=TEAL, weight=560)}
  {lead("M256 210h-46")}{label(202, 206, "Το φαρδύτερο σημείο", size=15, anchor="end")}
  {label(202, 228, "συμπίπτει με το δικό σας", size=13.5, colour=INK3, weight=420, anchor="end")}
  {lead("M300 128h-90")}{label(202, 133, "Τα δάχτυλα ισιώνουν", size=15, anchor="end")}
  {lead("M432 352h44")}{label(484, 348, "Η φτέρνα δεν", size=15)}
  {label(484, 372, "γλιστράει πίσω", size=15)}"""
    return frame(f"""
  {label(40, 62, "Πώς πατάει το πόδι μέσα στο παπούτσι", size=19, weight=560)}
  <g transform="translate(-18,44) scale(.88)">{art}</g>
  {label(40, 444, "Δοκιμάζετε απόγευμα, όρθιοι, με τις κάλτσες που θα φοράτε.", size=13.5, colour=INK3, weight=420)}
""", "Σωστή εφαρμογή υποδήματος")


def g_daily_check():
    return frame(f"""
  {foot_outline(dx=90, dy=110, scale=0.95, fill=SKIN, stroke=SKIN_L, sw=2.2)}
  <ellipse cx="430" cy="266" rx="112" ry="112" fill="{MIST2}" stroke="{TEAL}" stroke-width="4"/>
  <path d="M430 154v-32M540 266h32M430 378v32M318 266h-32" stroke="{TEAL300}" stroke-width="4" stroke-linecap="round"/>
  {foot_outline(dx=384, dy=190, scale=0.32, fill="#ffffff", stroke=TEAL300, sw=2)}
  <circle cx="404" cy="290" r="12" fill="{ALERT}" opacity=".4"/>
  <circle cx="404" cy="290" r="20" fill="none" stroke="{ALERT}" stroke-width="2.6"/>
  {lead("M318 266h-84")}{label(226, 271, "Καθρέφτης", size=14, anchor="end")}
  {lead("M424 312v56h96")}{label(528, 373, "Κοκκινίλα", size=13.5, colour=ALERT, weight=520)}
  {label(40, 92, "Ο καθημερινός έλεγχος", size=19, weight=560)}
  {label(40, 444, "Δύο λεπτά κάθε βράδυ — και κάτω από τα δάχτυλα.", size=13.5, colour=INK3, weight=420)}
""", "Καθημερινός έλεγχος πελμάτων")


GALLERY_ART = {
    "gal-foot-anatomy": g_foot_anatomy, "gal-nail-anatomy": g_nail_anatomy,
    "gal-arch-types": g_arch_types, "gal-callus": g_callus,
    "gal-heel-fissure": g_heel_fissure, "gal-ingrown": g_ingrown,
    "gal-diabetic-foot": g_diabetic_foot, "gal-onychomycosis": g_onychomycosis,
    "gal-brace": g_brace, "gal-debridement": g_debridement,
    "gal-offloading": g_offloading, "gal-nail-cutting": g_nail_cutting,
    "gal-shoe-fit": g_shoe_fit, "gal-daily-check": g_daily_check,
}


# ── Raster assets (favicon PNG + OG card) ────────────────────────────────────
def rasterise():
    """Pillow only — no cairosvg dependency, so the two PNGs are drawn directly."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("  ! Pillow not installed — favicon-144.png and og-enso.png not regenerated")
        return 0

    def hexrgb(h):
        h = h.lstrip("#")
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

    def mix(a, b, k):
        return tuple(round(a[i] + (b[i] - a[i]) * k) for i in range(3))

    def draw_enso(dr, cx, cy, r, thick, ramp, steps=900):
        """The SVG stroke, stamped as overlapping discs. Pillow has no gradients
        or filters, so the colour is interpolated per stamp along `ramp` and the
        blooms are stamped darker — enough to read as the same mark at card size."""
        for i in range(steps + 1):
            u = i / steps
            a = math.radians(ENSO_START + ENSO_SWEEP * u)
            body = 0.62 + 0.38 * math.sin(math.pi * (0.20 + 0.66 * u))
            t = thick * body * (min(1.0, u / 0.05) ** 0.7) * (min(1.0, (1 - u) / 0.13) ** 0.8)
            rr = r * (1 + 0.016 * math.sin(u * 7.1 + 0.7) + 0.010 * math.sin(u * 3.3 + 2.1))
            x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
            # Base colour walks the ramp; blooms pull it back towards the deep end.
            k = min(1.0, u * 1.05)
            col = mix(ramp[0], ramp[1], k) if k < .5 else mix(ramp[1], ramp[2], (k - .5) * 2)
            # Smooth, wide falloff — a hard cutoff stamps visible round lumps
            # instead of pigment settling.
            near = min(abs(u - bu) / (0.05 + 0.05 * sz) for bu, sz, _op in _BLOOMS)
            if near < 1:
                col = mix(col, ramp[0], 0.55 * (0.5 + 0.5 * math.cos(math.pi * near)))
            dr.ellipse([x - t / 2, y - t / 2, x + t / 2, y + t / 2], fill=col)

    def font(size, bold=False):
        for path in ("/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
                     "/System/Library/Fonts/Helvetica.ttc",
                     "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except OSError:
                    continue
        return ImageFont.load_default()

    # favicon-144.png — the mark on the deep ground, at 4× then downsampled
    s = 576
    ico = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(ico)
    d.rounded_rectangle([0, 0, s, s], radius=int(s * 0.22), fill=hexrgb(DEEP))
    draw_enso(d, s / 2, s * 0.515, s * 0.30, s * 0.115,
              (hexrgb(INK_SOFT), hexrgb(TEAL300), hexrgb("#dcf0f5")))
    ico.resize((144, 144), Image.LANCZOS).save(os.path.join(IMG, "favicon-144.png"))

    # og-enso.png — 1200×630 share card
    W, H = 2400, 1260
    og = Image.new("RGB", (W, H), hexrgb(DEEP))
    d = ImageDraw.Draw(og)
    for y in range(H):                      # vertical wash, deep → abyss
        k = y / H
        a, b = hexrgb(DEEP), hexrgb(ABYSS)
        d.line([(0, y), (W, y)], fill=tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3)))
    draw_enso(d, W * 0.755, H * 0.5, H * 0.335, H * 0.115,
              (hexrgb(TEAL), hexrgb(INK_SOFT), hexrgb(TEAL300)))
    d.text((150, 400), "Ensō", font=font(190), fill=(255, 255, 255))
    d.text((156, 640), "F O O T   C L I N I C", font=font(74), fill=hexrgb(TEAL300))
    d.text((160, 748), "P O D O L O G Y   ·   P O D I A T R Y", font=font(40),
           fill=hexrgb(BRAND))
    d.text((156, 856), "Ποδολογικό ιατρείο · Περαία, Θεσσαλονίκη", font=font(56),
           fill=hexrgb(TEAL300))
    d.text((156, 946), "Χριστοδούλου Ελπινίκη · από το 2002", font=font(56),
           fill=hexrgb(BRAND))
    og.resize((1200, 630), Image.LANCZOS).save(os.path.join(IMG, "og-enso.png"), optimize=True)
    return 2


def main():
    os.makedirs(IMG, exist_ok=True)
    made = []
    made.append(w("logo.svg", logo(False)))
    made.append(w("logo-light.svg", logo(True)))
    made.append(w("favicon.svg", favicon()))
    made.append(w("hero-enso.svg", hero()))
    made.append(w("hero-enso-dark.svg", hero_dark()))
    made.append(w("clinic-enso.svg", clinic_banner()))
    made.append(w("elpiniki-christodoulou.svg", portrait()))
    for stem, fn in GALLERY_ART.items():
        made.append(w(stem + ".svg", fn()))
    n = rasterise()
    print(f"drew {len(made)} SVG + {n} PNG assets → {IMG}")


if __name__ == "__main__":
    main()
