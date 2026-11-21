"""Gera os arquivos de marca Bitsoft (SVG + PNG).

Uso (requer fonttools, brotli e cairosvg, e as fontes Inter 600/800/900 em ./fonts):
    python gen.py <repo_dir>
"""
import os
import sys

import cairosvg
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = sys.argv[1]
BRAND = os.path.join(REPO, "assets", "brand")
PNG = os.path.join(BRAND, "png")
os.makedirs(PNG, exist_ok=True)

NAVY = "#0B1026"
BLUE = "#0EA5E9"
VIOLET = "#7C3AED"
WHITE = "#F8FAFC"
GRAY = "#94A3B8"

# ---------------------------------------------------------------- símbolo
# Coordenadas de origem (traçadas sobre a prancha): caixa ~ x 28..840, y 28..785
SYM_X0, SYM_Y0, SYM_W, SYM_H = 28, 28, 812, 757

UPPER = (
    "M150 28 L640 28 C760 28 840 110 840 215 C840 300 805 365 752 405 "
    "L706 405 C676 330 604 268 455 208 L76 351 Q48 362 52 334 "
    "L128 48 Q133 28 150 28 Z"
)
LOWER = (
    "M752 405 C810 445 830 520 830 592 C830 700 742 785 632 785 "
    "L56 785 Q26 785 38 758 L92 640 Q100 625 120 621 "
    "L540 530 C622 512 684 470 706 405 Z"
)
FOLD = "M150 28 L455 208 L76 351 Q48 362 52 334 L128 48 Q133 28 150 28 Z"
WAIST = "M752 405 C784 428 806 458 818 494 L660 494 C684 470 700 440 706 405 Z"
CODE = "M338 346 L268 410 L338 474 M462 318 L378 504 M498 346 L568 410 L498 474"


def symbol(uid, mode="color", fill=None, code=WHITE, code_w=40):
    """Retorna (defs, corpo) do símbolo nas coordenadas de origem."""
    if mode == "color":
        defs = f"""
    <linearGradient id="{uid}g" x1="820" y1="40" x2="60" y2="800" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#22D3EE"/>
      <stop offset=".35" stop-color="{BLUE}"/>
      <stop offset=".7" stop-color="#4F6BF5"/>
      <stop offset="1" stop-color="{VIOLET}"/>
    </linearGradient>
    <linearGradient id="{uid}f" x1="70" y1="330" x2="420" y2="160" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#6D28D9" stop-opacity=".75"/>
      <stop offset="1" stop-color="#4338CA" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="{uid}w" x1="0" y1="405" x2="0" y2="494" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#1E3A8A" stop-opacity=".45"/>
      <stop offset="1" stop-color="#1E3A8A" stop-opacity="0"/>
    </linearGradient>"""
        paint = f"url(#{uid}g)"
    else:
        dark_fill = fill.upper() in (NAVY.upper(), "#000000")
        shade = "#FFFFFF" if dark_fill else "#000000"
        defs = f"""
    <linearGradient id="{uid}f" x1="70" y1="330" x2="420" y2="160" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{shade}" stop-opacity="0"/>
      <stop offset="1" stop-color="{shade}" stop-opacity=".38"/>
    </linearGradient>
    <linearGradient id="{uid}w" x1="0" y1="405" x2="0" y2="494" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{shade}" stop-opacity=".22"/>
      <stop offset="1" stop-color="{shade}" stop-opacity="0"/>
    </linearGradient>"""
        paint = fill
        code = fill
    waist = f'<path d="{WAIST}" fill="url(#{uid}w)"/>' if mode == "color" else ""
    body = f"""
    <path d="{UPPER}" fill="{paint}"/>
    <path d="{FOLD}" fill="url(#{uid}f)"/>
    <path d="{LOWER}" fill="{paint}"/>
    {waist}
    <path d="{CODE}" fill="none" stroke="{code}" stroke-width="{code_w}" stroke-linecap="round" stroke-linejoin="round"/>"""
    return defs, body


def place(body, x, y, h):
    """Posiciona o símbolo com altura h no ponto (x, y) do canto superior esquerdo."""
    s = h / SYM_H
    return f'<g transform="translate({x:.2f} {y:.2f}) scale({s:.5f}) translate({-SYM_X0} {-SYM_Y0})">{body}\n  </g>'


# ---------------------------------------------------------------- texto
class Font:
    def __init__(self, path):
        self.f = TTFont(path)
        self.gs = self.f.getGlyphSet()
        self.cmap = self.f.getBestCmap()
        self.upm = self.f["head"].unitsPerEm
        self.kern = self._kerning()

    def _kerning(self):
        # Pares de kerning simples (PairPos formato 1) do GPOS
        pairs = {}
        if "GPOS" not in self.f:
            return pairs
        for lookup in self.f["GPOS"].table.LookupList.Lookup:
            for st in lookup.SubTable:
                if getattr(st, "ExtSubTable", None):
                    st = st.ExtSubTable
                if lookup.LookupType not in (2, 9) or getattr(st, "Format", 0) != 1:
                    continue
                for first, ps in zip(st.Coverage.glyphs, st.PairSet):
                    for rec in ps.PairValueRecord:
                        v = rec.Value1
                        if v is not None and getattr(v, "XAdvance", 0):
                            pairs[(first, rec.SecondGlyph)] = v.XAdvance
        return pairs

    def glyph(self, ch):
        return self.cmap[ord(ch)]

    def layout(self, text, size, tracking=0.0):
        """Lista de (nome_glifo, x) em unidades de pixel + largura total."""
        s = size / self.upm
        x, out, prev = 0.0, [], None
        for ch in text:
            g = self.glyph(ch)
            if prev is not None:
                x += self.kern.get((prev, g), 0) * s
            out.append((g, x))
            x += self.gs[g].width * s + tracking * size
            prev = g
        width = x - tracking * size
        return out, width

    def path(self, glyph, x, y, size):
        s = size / self.upm
        pen = SVGPathPen(self.gs)
        self.gs[glyph].draw(TransformPen(pen, (s, 0, 0, -s, x, y)))
        return pen.getCommands()

    def bounds(self, glyph):
        bp = BoundsPen(self.gs)
        self.gs[glyph].draw(bp)
        return bp.bounds


F900 = Font(os.path.join(HERE, "fonts", "inter900.ttf"))
F800 = Font(os.path.join(HERE, "fonts", "inter800.ttf"))
F600 = Font(os.path.join(HERE, "fonts", "inter600.ttf"))

CAP = F900.f["OS/2"].sCapHeight / F900.upm  # altura de maiúscula relativa ao corpo


def wordmark(x, y_base, cap_px, color, dot=VIOLET):
    """'Bitsoft' com o pingo do i em quadrado violeta. Retorna (svg, largura)."""
    size = cap_px / CAP
    f = F900
    text = "Bıtsoft"  # i sem pingo
    glyphs, width = f.layout(text, size, tracking=-0.025)
    d = "".join(f.path(g, x + gx, y_base, size) for g, gx in glyphs)
    # quadrado do pingo: largura da haste do i, acima da altura-x
    g_i, gx_i = glyphs[1]
    xmin, _, xmax, ymax = f.bounds(g_i)
    s = size / f.upm
    stem = (xmax - xmin) * s
    bi = f.bounds(f.glyph("i"))
    cap_top = y_base - cap_px
    top = min(y_base - bi[3] * s, cap_top - stem * 0.05)
    top = max(top, cap_top - stem * 0.25)
    sq = (
        f'<rect x="{x + gx_i + xmin * s:.2f}" y="{top:.2f}" width="{stem:.2f}" '
        f'height="{stem:.2f}" rx="{stem * 0.12:.2f}" fill="{dot}"/>'
    )
    return f'<path d="{d}" fill="{color}"/>{sq}', width


def text_line(font, text, x, y_base, cap_px, color, width=None, tracking=0.0):
    size = cap_px / (font.f["OS/2"].sCapHeight / font.upm)
    if width is not None:
        _, w0 = font.layout(text, size)
        tracking = (width - w0) / (size * (len(text) - 1))
    glyphs, w = font.layout(text, size, tracking)
    d = "".join(font.path(g, x + gx, y_base, size) for g, gx in glyphs)
    return f'<path d="{d}" fill="{color}"/>', w


def text_width(font, text, cap_px, tracking=0.0):
    size = cap_px / (font.f["OS/2"].sCapHeight / font.upm)
    return font.layout(text, size, tracking)[1]


SLOGAN = "SOLUÇÕES EM APLICAÇÕES WEB"


# ---------------------------------------------------------------- arquivos
def svg(w, h, title, defs, content, bg=None):
    bgrect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{title}">
  <title>{title}</title>
  <defs>{defs}
  </defs>
  {bgrect}{content}
</svg>
"""


def write(name, data, png_widths=()):
    p = os.path.join(BRAND, name)
    with open(p, "w") as fh:
        fh.write(data)
    for w in png_widths:
        out = os.path.join(PNG, f"{name[:-4]}-{w}.png")
        cairosvg.svg2png(bytestring=data.encode(), write_to=out, output_width=w)
    return p


def horizontal(light, slogan=True):
    text = NAVY if light else WHITE
    sub = "#334155" if light else "#CBD5E1"
    code = NAVY if light else WHITE
    H = 200  # altura do símbolo
    pad = 8
    defs, body = symbol("s", code=code)
    sym_w = SYM_W * H / SYM_H
    tx = pad + sym_w + H * 0.14
    cap = H * 0.47
    if slogan:
        base = pad + H * 0.60
    else:
        cap = H * 0.56
        base = pad + H / 2 + cap / 2
    wm, ww = wordmark(tx, base, cap, text)
    slo = text_line(F600, SLOGAN, tx + 2, base + H * 0.25, H * 0.075, sub, width=ww - 4)[0] if slogan else ""
    W = tx + ww + pad
    return svg(W, H + pad * 2, "Bitsoft — Soluções em aplicações web", defs, place(body, pad, pad, H) + wm + slo)


def vertical(light):
    text = NAVY if light else WHITE
    sub = "#334155" if light else "#CBD5E1"
    code = NAVY if light else WHITE
    H = 200
    pad = 8
    defs, body = symbol("s", code=code)
    sym_w = SYM_W * H / SYM_H
    cap = H * 0.50
    ww = text_width(F900, "Bıtsoft", cap, -0.025)
    slo_w = ww * 0.98
    W = max(ww, slo_w, sym_w) + pad * 2
    cx = W / 2
    base = pad + H + H * 0.18 + cap
    wm, _ = wordmark(cx - ww / 2, base, cap, text)
    slo, _ = text_line(F600, SLOGAN, cx - slo_w / 2, base + H * 0.27, H * 0.078, sub, width=slo_w)
    Ht = base + H * 0.27 + pad
    return svg(W, Ht, "Bitsoft — Soluções em aplicações web", defs, place(body, cx - sym_w / 2, pad, H) + wm + slo)


def icon(mode="color", fill=None, code=WHITE, title="Bitsoft"):
    S = 512
    h = 440
    defs, body = symbol("s", mode=mode, fill=fill, code=code)
    w = SYM_W * h / SYM_H
    return svg(S, S, title, defs, place(body, (S - w) / 2, (S - h) / 2, h))


def app_icon(size=512, tile=NAVY, mode="color", fill=None, code=WHITE, radius=0.225, title="Bitsoft", scale=0.58, code_w=40):
    S = size
    h = S * scale
    defs, body = symbol("s", mode=mode, fill=fill, code=code, code_w=code_w)
    w = SYM_W * h / SYM_H
    glow = ""
    if tile == NAVY:
        defs += f"""
    <radialGradient id="tg" cx=".2" cy="1" r="1">
      <stop offset="0" stop-color="{VIOLET}" stop-opacity=".35"/>
      <stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
    </radialGradient>"""
        glow = f'<rect width="{S}" height="{S}" rx="{S * radius:.1f}" fill="url(#tg)"/>'
    bg = f'<rect width="{S}" height="{S}" rx="{S * radius:.1f}" fill="{tile}"/>' + glow
    return svg(S, S, title, defs, bg + place(body, (S - w) / 2 + S * 0.01, (S - h) / 2, h))


def og_image():
    W, Hh = 1200, 630
    defs, body = symbol("s", code=WHITE)
    defs += f"""
    <radialGradient id="g1" cx="0" cy="1" r=".9">
      <stop offset="0" stop-color="{VIOLET}" stop-opacity=".55"/>
      <stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="g2" cx="1" cy="0" r=".8">
      <stop offset="0" stop-color="{BLUE}" stop-opacity=".35"/>
      <stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
    </radialGradient>"""
    H = 190
    sym_w = SYM_W * H / SYM_H
    cap = H * 0.47
    ww = text_width(F900, "Bıtsoft", cap, -0.025)
    total = sym_w + H * 0.14 + ww
    x0 = (W - total) / 2
    y0 = 150
    tx = x0 + sym_w + H * 0.14
    base = y0 + H * 0.60
    wm, _ = wordmark(tx, base, cap, WHITE)
    slo, _ = text_line(F600, SLOGAN, tx + 2, base + H * 0.25, H * 0.075, "#CBD5E1", width=ww - 4)
    tag_text = "Tecnologia que transforma ideias em soluções."
    tw = text_width(F600, tag_text, 26)
    tag, _ = text_line(F600, tag_text, (W - tw) / 2, 470, 26, "#CBD5E1")
    url_text = "bitsoft.dev.br"
    uw = text_width(F800, url_text, 20, 0.02)
    url, _ = text_line(F800, url_text, (W - uw) / 2, 530, 20, "#38BDF8", tracking=0.02)
    bg = f'<rect width="{W}" height="{Hh}" fill="{NAVY}"/><rect width="{W}" height="{Hh}" fill="url(#g1)"/><rect width="{W}" height="{Hh}" fill="url(#g2)"/>'
    return svg(W, Hh, "Bitsoft — Soluções em aplicações web", defs, bg + place(body, x0, y0, H) + wm + slo + tag + url)


def main():
    write("logo-horizontal.svg", horizontal(False), (1000, 2000))
    write("logo-horizontal-light.svg", horizontal(True), (1000, 2000))
    write("logo-compact.svg", horizontal(False, slogan=False), (800,))
    write("logo-compact-light.svg", horizontal(True, slogan=False), (800,))
    write("logo-vertical.svg", vertical(False), (800, 1600))
    write("logo-vertical-light.svg", vertical(True), (800, 1600))
    write("icon.svg", icon(code=WHITE, title="Bitsoft — ícone"), (512, 1024))
    write("icon-light-bg.svg", icon(code=NAVY, title="Bitsoft — ícone (fundo claro)"), (512, 1024))
    write("icon-white.svg", icon("mono", WHITE, title="Bitsoft — ícone branco"), (512, 1024))
    write("icon-dark.svg", icon("mono", NAVY, title="Bitsoft — ícone escuro"), (512, 1024))
    write("icon-mono-violet.svg", icon("mono", VIOLET, title="Bitsoft — ícone violeta"), (512,))
    write("icon-mono-blue.svg", icon("mono", BLUE, title="Bitsoft — ícone azul"), (512,))
    write("icon-mono-gray.svg", icon("mono", GRAY, title="Bitsoft — ícone cinza"), (512,))
    write("app-icon.svg", app_icon(title="Bitsoft — ícone de app"), (180, 192, 512, 1024))
    write("app-icon-white.svg", app_icon(tile=WHITE, mode="mono", fill=NAVY, title="Bitsoft — ícone de app (branco)"), (512, 1024))
    write("app-icon-dark.svg", app_icon(tile=NAVY, mode="mono", fill=WHITE, title="Bitsoft — ícone de app (escuro)"), (512, 1024))

    # favicon / ícones do site
    fav = app_icon(radius=0.22, title="Bitsoft", scale=0.72, code_w=58)
    with open(os.path.join(REPO, "assets", "favicon.svg"), "w") as fh:
        fh.write(fav)
    cairosvg.svg2png(bytestring=fav.encode(), write_to=os.path.join(REPO, "assets", "favicon-32.png"), output_width=32)
    # apple-touch-icon: quadrado cheio (iOS aplica a máscara)
    apple = app_icon(radius=0, title="Bitsoft")
    cairosvg.svg2png(bytestring=apple.encode(), write_to=os.path.join(REPO, "assets", "apple-touch-icon.png"), output_width=180)
    for w in (192, 512):
        cairosvg.svg2png(bytestring=apple.encode(), write_to=os.path.join(REPO, "assets", f"icon-{w}.png"), output_width=w)
    og = og_image()
    write("og-image.svg", og)
    cairosvg.svg2png(bytestring=og.encode(), write_to=os.path.join(REPO, "assets", "og-image.png"), output_width=1200)


if __name__ == "__main__":
    main()
