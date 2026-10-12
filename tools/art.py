# -*- coding: utf-8 -*-
"""Generates every brand asset and illustration for the site.

    python3 enso-new/tools/art.py

Writes into site/assets/img/:
  · logo.svg / logo-light.svg / favicon.svg / favicon-144.png / og-enso.png
  · enso-badge.svg / enso-badge-light.svg — the ring alone (entry screen, home)

The mark itself is the clinic's own watercolour (brand/enso-mark.png); only the
lockups around it are composed here.
"""
import os, sys, math, io, base64

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
IMG = os.path.join(ROOT, "site", "assets", "img")

# ── Palette (mirrors :root in enso.css) ──────────────────────────────────────
BRAND   = "#45b3e8"   # the Ensō brand blue — the cyan edge of the watercolour mark
TEAL    = "#1673bd"
DEEP    = "#0c3f7c"
ABYSS   = "#071f42"
TEAL300 = "#a3d9f4"
MIST    = "#e2f1fb"
MIST2   = "#f0f8fe"
PAPER   = "#fbfdff"
LINE    = "#d2e4f2"
INK3    = "#6a83a3"
SKIN    = "#fdf1e8"
SKIN2   = "#f6e0d1"
SKIN_L  = "#e0c6b3"
NAIL    = "#f3e7dc"
WARN    = "#c2865a"
ALERT   = "#c2544f"
KERAT   = "#d9a066"

FONT = ('font-family="M PLUS Rounded 1c,Manrope,-apple-system,BlinkMacSystemFont,'
        '\'Segoe UI\',Helvetica,Arial,sans-serif"')


# ── The card's typeface, set as outlines ─────────────────────────────────────
# The clinic's business card is set in M PLUS Rounded 1c. The pages load it from
# Google Fonts, but an SVG viewed through <img> cannot reach a web font, so the
# lockups below draw the wordmark as paths from a Latin+Greek subset kept in
# brand/. The same files feed the PNG share card.
BRAND_FONT = {400: os.path.join(ROOT, "brand", "mplus-rounded-1c-400.ttf"),
              700: os.path.join(ROOT, "brand", "mplus-rounded-1c-700.ttf")}
_TT = {}


def _tt(weight):
    if weight not in _TT:
        from fontTools.ttLib import TTFont
        _TT[weight] = TTFont(BRAND_FONT[weight])
    return _TT[weight]


def text_path(text, x, y, size, *, weight=400, fill="#000", tracking=0.0,
              anchor="start", extra=""):
    """`text` at (x, y) baseline as a single <path>, in the card's typeface.
    `tracking` is extra letter-spacing in user units."""
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    f = _tt(weight)
    upem = f["head"].unitsPerEm
    cmap = f.getBestCmap(); gs = f.getGlyphSet(); hmtx = f["hmtx"]
    k = size / upem
    names = [cmap.get(ord(ch), ".notdef") for ch in text]
    width = sum(hmtx[n][0] * k for n in names) + tracking * (len(text) - 1)
    x0 = x - width / 2 if anchor == "middle" else (x - width if anchor == "end" else x)
    pen = SVGPathPen(gs)
    pos = 0.0
    for n in names:
        tp = TransformPen(pen, (k, 0, 0, -k, x0 + pos, y))
        gs[n].draw(tp)
        pos += hmtx[n][0] * k + tracking
    d = pen.getCommands()
    return f'<path d="{d}" fill="{fill}" {extra}/>' if d else ""


def w(name, body):
    open(os.path.join(IMG, name), "w", encoding="utf-8").write(body)
    return name


# ── The clinic's own mark ────────────────────────────────────────────────────
# brand/enso-mark.png is the clinic's watercolour ensō, cut out of the scan it
# arrived as (brand/enso-mark-source.jpg): the grey paper, its drop shadow and
# the export watermark are gone, the pigment is not touched. The mark is no
# longer drawn here — only the lockups around it are.
MARK = os.path.join(ROOT, "brand", "enso-mark.png")
_MARK = {}


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mark_png(px, light=False):
    """The mark at `px` square. `light=True` walks the pigment up to the pale end
    of the palette, so on the deep ground it reads the way the white wordmark
    beside it does instead of sinking into the navy."""
    from PIL import Image
    import numpy as np
    key = (px, light)
    if key in _MARK:
        return _MARK[key]
    im = Image.open(MARK).convert("RGBA").resize((px, px), Image.LANCZOS)
    if light:
        a = np.asarray(im).astype(np.float32)
        rgb, al = a[..., :3], a[..., 3]
        lum = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
        dens = np.clip(1 - (lum - 40) / 175, 0, 1)[..., None]
        pale = np.array([hex_rgb(TEAL300)], "float32")
        im = Image.fromarray(
            np.dstack([pale + (255 - pale) * dens, al]).astype("uint8"), "RGBA")
    _MARK[key] = im
    return im


def _mark_b64(px, light):
    """Quantised to 128 colours: the granulation survives, the bytes roughly
    third — which matters, because every lockup carries its own copy inline."""
    from PIL import Image
    key = ("b64", px, light)
    if key not in _MARK:
        q = mark_png(px, light).quantize(colors=128, method=Image.FASTOCTREE,
                                         dither=Image.FLOYDSTEINBERG)
        buf = io.BytesIO()
        q.save(buf, "PNG", optimize=True)
        _MARK[key] = base64.b64encode(buf.getvalue()).decode()
    return _MARK[key]


def mark_image(cx, cy, size, *, light=False, px=None):
    """The mark centred on (cx, cy) in a `size` square. Embedded rather than
    linked: these SVGs are loaded through <img>, where an external reference
    would never resolve."""
    px = px or max(96, min(720, int(size * 1.3)))
    h = size / 2
    return (f'<image x="{cx - h:.1f}" y="{cy - h:.1f}" '
            f'width="{size:.1f}" height="{size:.1f}" '
            f'href="data:image/png;base64,{_mark_b64(px, light)}"/>')


# ── Palette of the mark ──────────────────────────────────────────────────────
# The real Ensō logo is a watercolour brush circle: indigo pigment pooling in
# blooms, thinning to a pale wash where the brush ran dry. These four steps
# reproduce that range while staying inside the site palette.
INK_DEEP = "#0a3a80"   # where the pigment pools
INK_MID  = "#1a7fcf"
INK_SOFT = "#4fbde9"   # the brand blue
INK_PALE = "#a3d9f4"

# The brush lands at about one o'clock and sweeps clockwise, lifting just short
# of where it began — so the circle stays open at the top right, as it does in
# the clinic's own mark.
ENSO_START, ENSO_SWEEP = -52.0, 336.0


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
    h = 124 if descriptor else 96
    cy = 62 if descriptor else 48
    # At header size the mark lands about 40px across, so it is embedded at 208px
    # — enough for a 2× screen, and the whole file still weighs less than the
    # drawn mark it replaced.
    mark = mark_image(58, cy, 96, light=light, px=208)
    tail = ("\n  " + text_path("HOLISTIC PODOLOGY", 128, 95, 12.5, weight=700,
                                fill=desc, tracking=3.2)
            if descriptor else "")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 396 {h}" width="396" height="{h}"
  role="img" aria-label="Ensō Foot Clinic — Ολιστική ποδολογία">
  {mark}
  {text_path("Ensō", 126, cy + 8, 34, weight=400, fill=name)}
  {text_path("Foot Clinic", 209, cy + 8, 34, weight=700, fill=second)}{tail}
</svg>"""


def favicon():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64"
  role="img" aria-label="Ensō Foot Clinic">
  <rect width="64" height="64" rx="14" fill="{DEEP}"/>
  {mark_image(32, 33, 52, light=True, px=128)}
</svg>"""



# ── The ring on its own ─────────────────────────────────────────────────────
def enso_badge():
    """The mark alone, square and centred, for the phone cover where it stands as
    a badge above the wordmark — nothing set inside the ring, the brush carries
    it. The cover is on paper, not on the deep ground the desktop hero uses, so
    this one keeps the pigment's own colour."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400"
  role="img" aria-label="Το σήμα ensō του Ensō Foot Clinic">
  {mark_image(200, 200, 356, px=460)}
</svg>"""


def enso_badge_light():
    """The same square badge with the pigment walked up to the pale end, for the
    homepage lockup, where it sits on the deep ground under the wordmark."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400"
  role="img" aria-label="Το σήμα ensō του Ensō Foot Clinic">
  {mark_image(200, 200, 356, light=True, px=460)}
</svg>"""



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

    def font(size, bold=False):
        for path in (BRAND_FONT[700 if bold else 400],
                     "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
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
    m = mark_png(int(s * 0.74), light=True)
    ico.alpha_composite(m, ((s - m.width) // 2, int(s * 0.515 - m.height / 2)))
    ico.resize((144, 144), Image.LANCZOS).save(os.path.join(IMG, "favicon-144.png"))

    # og-enso.png — 1200×630 share card
    W, H = 2400, 1260
    og = Image.new("RGB", (W, H), hexrgb(DEEP))
    d = ImageDraw.Draw(og)
    for y in range(H):                      # vertical wash, deep → abyss
        k = y / H
        a, b = hexrgb(DEEP), hexrgb(ABYSS)
        d.line([(0, y), (W, y)], fill=tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3)))
    m = mark_png(int(H * 0.80), light=True)
    og.paste(m, (int(W * 0.755 - m.width / 2), int(H * 0.5 - m.height / 2)), m)
    d.text((150, 400), "Ensō", font=font(190), fill=(255, 255, 255))
    d.text((156, 640), "F O O T   C L I N I C", font=font(74, bold=True), fill=hexrgb(TEAL300))
    d.text((160, 748), "H O L I S T I C   P O D O L O G Y", font=font(40),
           fill=hexrgb(BRAND))
    d.text((156, 856), "Ποδολογικό κέντρο · Θεσσαλονίκη · Αθήνα", font=font(56),
           fill=hexrgb(TEAL300))
    d.text((156, 946), "Χριστοδούλου Ελπινίκη · από το 2002", font=font(56),
           fill=hexrgb(BRAND))
    (og.resize((1200, 630), Image.LANCZOS)
       .quantize(colors=256, method=Image.FASTOCTREE, dither=Image.FLOYDSTEINBERG)
       .save(os.path.join(IMG, "og-enso.png"), optimize=True))
    return 2



def main():
    os.makedirs(IMG, exist_ok=True)
    made = []
    made.append(w("logo.svg", logo(False)))
    made.append(w("logo-light.svg", logo(True)))
    made.append(w("favicon.svg", favicon()))
    made.append(w("enso-badge.svg", enso_badge()))
    made.append(w("enso-badge-light.svg", enso_badge_light()))
    n = rasterise()
    print(f"drew {len(made)} SVG + {n} PNG assets → {IMG}")


if __name__ == "__main__":
    main()
