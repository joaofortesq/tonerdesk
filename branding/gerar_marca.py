"""Gera todos os ícones e logos do TonerDesk a partir das cores abaixo.

Uso (na raiz do repositório):  python branding/gerar_marca.py
Para trocar a identidade visual, altere COR_1 / COR_2 / NOME e rode de novo.
Se existir branding/icone_custom.png (quadrado, >= 512px), ele é usado no lugar do desenho padrão.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

NOME = "TonerDesk"
COR_1 = (13, 71, 161)    # azul escuro (topo)
COR_2 = (0, 172, 193)    # ciano (base)
ROOT = Path(__file__).resolve().parent.parent
FONTE = "C:/Windows/Fonts/segoeuib.ttf"


def gradiente(tam):
    img = Image.new("RGBA", (tam, tam))
    d = ImageDraw.Draw(img)
    for y in range(tam):
        t = y / (tam - 1)
        cor = tuple(int(COR_1[i] + (COR_2[i] - COR_1[i]) * t) for i in range(3)) + (255,)
        d.line([(0, y), (tam, y)], fill=cor)
    return img


def icone(tam=1024):
    custom = ROOT / "branding" / "icone_custom.png"
    if custom.exists():
        return Image.open(custom).convert("RGBA").resize((tam, tam), Image.LANCZOS)
    s = tam / 1024
    fundo = gradiente(tam)
    mask = Image.new("L", (tam, tam), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, tam - 1, tam - 1], radius=int(220 * s), fill=255)
    img = Image.new("RGBA", (tam, tam), (0, 0, 0, 0))
    img.paste(fundo, (0, 0), mask)
    d = ImageDraw.Draw(img)
    branco = (255, 255, 255, 255)
    # monitor
    d.rounded_rectangle([170 * s, 190 * s, 854 * s, 690 * s], radius=int(60 * s), outline=branco, width=int(64 * s))
    # pé do monitor
    d.rectangle([462 * s, 690 * s, 562 * s, 790 * s], fill=branco)
    d.rounded_rectangle([330 * s, 780 * s, 694 * s, 850 * s], radius=int(35 * s), fill=branco)
    # letra T dentro da tela
    d.rectangle([330 * s, 300 * s, 694 * s, 385 * s], fill=branco)
    d.rectangle([469 * s, 300 * s, 555 * s, 600 * s], fill=branco)
    return img


def logo(cor_texto, alt=120):
    ic = icone(alt)
    fonte = ImageFont.truetype(FONTE, int(alt * 0.62))
    w = int(fonte.getlength(NOME)) + alt + int(alt * 0.25)
    img = Image.new("RGBA", (w, alt), (0, 0, 0, 0))
    img.paste(ic, (0, 0), ic)
    d = ImageDraw.Draw(img)
    d.text((alt + int(alt * 0.2), alt / 2), NOME, font=fonte, fill=cor_texto, anchor="lm")
    return img


def svg_icone():
    c1 = "#%02x%02x%02x" % COR_1
    c2 = "#%02x%02x%02x" % COR_2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>
<rect width="1024" height="1024" rx="220" fill="url(#g)"/>
<rect x="202" y="222" width="620" height="436" rx="40" fill="none" stroke="#fff" stroke-width="64"/>
<rect x="462" y="690" width="100" height="100" fill="#fff"/>
<rect x="330" y="780" width="364" height="70" rx="35" fill="#fff"/>
<rect x="330" y="300" width="364" height="85" fill="#fff"/>
<rect x="469" y="300" width="86" height="300" fill="#fff"/>
</svg>
'''


def main():
    base = icone(1024)
    res = ROOT / "res"
    tamanhos_ico = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    for destino in [res / "icon.ico", res / "tray-icon.ico",
                    ROOT / "flutter/windows/runner/resources/app_icon.ico"]:
        base.save(destino, sizes=tamanhos_ico)
    for nome, t in [("icon.png", 1024), ("32x32.png", 32), ("64x64.png", 64),
                    ("128x128.png", 128), ("128x128@2x.png", 256), ("mac-icon.png", 1024)]:
        base.resize((t, t), Image.LANCZOS).save(res / nome)
    svg = svg_icone()
    for destino in [res / "icon.svg" if (res / "icon.svg").exists() else None,
                    res / "logo.svg", res / "scalable.svg", ROOT / "flutter/assets/icon.svg"]:
        if destino:
            destino.write_text(svg, encoding="utf-8")
    assets = ROOT / "flutter/assets"
    base.resize((256, 256), Image.LANCZOS).save(assets / "icon.png")
    logo((30, 41, 59, 255)).save(assets / "logo.png")
    logo((30, 41, 59, 255)).save(assets / "logo_light.png")
    logo((255, 255, 255, 255)).save(assets / "logo_dark.png")
    base.resize((256, 256), Image.LANCZOS).save(ROOT / "branding/icone_preview.png")
    print("Marca gerada.")


if __name__ == "__main__":
    main()
