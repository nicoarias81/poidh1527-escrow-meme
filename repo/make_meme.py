"""Meme for poidh bounty 1527 (Best poidh Meme): 1200x1250 PNG, v2.

Idea: poidh is "pics or it didn't happen", so the claim demands photographic
proof of the escrow itself. Drawn with Pillow + Windows fonts, no stock assets.
v2: magnifier moved off the amount, higher-contrast secondary text, footer cut.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 1250
BG = (11, 13, 16)
CARD = (19, 23, 30)
EDGE = (54, 64, 80)
WHITE = (247, 249, 252)
GREY = (168, 178, 192)
GREEN = (86, 214, 132)
YELLOW = (255, 212, 0)

IMPACT = "C:/Windows/Fonts/impact.ttf"
SEMI = "C:/Windows/Fonts/seguisb.ttf"
MONO = "C:/Windows/Fonts/consola.ttf"


def fit(d, text, path, max_w, start, min_size=20):
    size = start
    while size > min_size:
        f = ImageFont.truetype(path, size)
        if d.textbbox((0, 0), text, font=f)[2] <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(path, min_size)


def outlined(d, xy, text, font, fill, stroke=9):
    d.text(xy, text, font=font, fill=fill, anchor="mm",
           stroke_width=stroke, stroke_fill=(0, 0, 0))


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

f1 = fit(d, "PICS OR IT", IMPACT, 1080, 152)
f2 = fit(d, "DIDN'T HAPPEN", IMPACT, 1080, 152)
outlined(d, (W // 2, 128), "PICS OR IT", f1, WHITE)
outlined(d, (W // 2, 262), "DIDN'T HAPPEN", f2, WHITE)

x0, y0, x1, y1 = 210, 400, 990, 880
d.rounded_rectangle([x0, y0, x1, y1], radius=30, fill=CARD, outline=EDGE, width=4)
d.rounded_rectangle([x0 + 52, y0 + 56, x0 + 132, y0 + 112], radius=10, fill=(58, 68, 84))
d.text((x0 + 158, y0 + 68), "POIDH  ·  ESCROW", font=ImageFont.truetype(MONO, 31), fill=GREY)

f_eth = fit(d, "0.007 ETH", SEMI, 520, 128)
d.text((W // 2, y0 + 232), "0.007 ETH", font=f_eth, fill=WHITE, anchor="mm")

d.line([(x0 + 70, y0 + 335), (x1 - 70, y0 + 335)], fill=(46, 55, 70), width=3)
d.text((W // 2, y0 + 385), "bounty #541  ·  base  ·  deadline nov 30",
       font=ImageFont.truetype(MONO, 29), fill=GREY, anchor="mm")
d.text((W // 2, y0 + 435), "status: escrowed   |   seen by a human: no",
       font=ImageFont.truetype(MONO, 29), fill=GREEN, anchor="mm")

# magnifier sitting on the card's top-right corner, clear of the amount
r = 92
cx, cy = x1 - 40, y0 + 10
lens = Image.new("RGBA", (2 * r + 40, 2 * r + 40), (0, 0, 0, 0))
ld = ImageDraw.Draw(lens)
ld.ellipse([10, 10, 2 * r + 10, 2 * r + 10], fill=(255, 255, 255, 30), outline=WHITE, width=11)
ld.line([(2 * r - 6, 2 * r - 6), (2 * r + 34, 2 * r + 34)], fill=WHITE, width=17)
ld.text((r + 10, r + 6), "no pics", font=ImageFont.truetype(MONO, 33), fill=(255, 88, 88), anchor="mm")
img.paste(lens, (cx - r, cy - r), lens)

f3 = fit(d, "ok. pics of the escrow then.", IMPACT, 1080, 120)
outlined(d, (W // 2, 1000), "ok. pics of the escrow then.", f3, YELLOW)

img.save("C:/Users/nicoa/poidh-auto/claims/1527/meme1527.png", optimize=True)
print("ok", img.size)
