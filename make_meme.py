"""Meme for poidh bounty 1527 (Best poidh Meme): 1200x1250 PNG.

Idea: poidh's founding line is "pics or it didn't happen", so the claim flips
the demand back at the escrow: everyone proves their work, so prove the pot.
Drawn programmatically (Pillow + Windows fonts), no stock assets.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 1250
BG = (11, 13, 16)
CARD = (18, 22, 28)
EDGE = (43, 51, 64)
WHITE = (245, 247, 250)
GREY = (125, 135, 148)
YELLOW = (255, 212, 0)

IMPACT = "C:/Windows/Fonts/impact.ttf"
SEMI = "C:/Windows/Fonts/seguisb.ttf"
MONO = "C:/Windows/Fonts/consola.ttf"


def fit(draw, text, path, max_w, start, min_size=20):
    size = start
    while size > min_size:
        f = ImageFont.truetype(path, size)
        if draw.textbbox((0, 0), text, font=f)[2] <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(path, min_size)


def outlined(draw, xy, text, font, fill, stroke=9):
    draw.text(xy, text, font=font, fill=fill, anchor="mm",
              stroke_width=stroke, stroke_fill=(0, 0, 0))


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# top caption
f1 = fit(d, "PICS OR IT", IMPACT, 1080, 150)
f2 = fit(d, "DIDN'T HAPPEN", IMPACT, 1080, 150)
outlined(d, (W // 2, 130), "PICS OR IT", f1, WHITE)
outlined(d, (W // 2, 265), "DIDN'T HAPPEN", f2, WHITE)

# escrow card
x0, y0, x1, y1 = 250, 400, 950, 900
d.rounded_rectangle([x0, y0, x1, y1], radius=28, fill=CARD, outline=EDGE, width=4)
d.rounded_rectangle([x0 + 46, y0 + 52, x0 + 126, y0 + 106], radius=10,
                    fill=(52, 60, 74))  # chip
d.text((x0 + 152, y0 + 62), "POIDH  ·  ESCROW", font=ImageFont.truetype(MONO, 30), fill=GREY)
f_eth = fit(d, "0.007 ETH", SEMI, 560, 120)
d.text((W // 2 + 30, y0 + 210), "0.007 ETH", font=f_eth, fill=WHITE, anchor="mm")
d.text((W // 2 + 30, y0 + 300), "bounty #541  ·  base", font=ImageFont.truetype(MONO, 30), fill=GREY, anchor="mm")
d.text((W // 2 + 30, y0 + 365), "status: escrowed, unseen", font=ImageFont.truetype(MONO, 26),
       fill=(96, 200, 130), anchor="mm")

# magnifier over the amount
cx, cy, r = 640, y0 + 215, 132
lens = Image.new("RGBA", (2 * r + 12, 2 * r + 12), (0, 0, 0, 0))
ld = ImageDraw.Draw(lens)
ld.ellipse([6, 6, 2 * r + 6, 2 * r + 6], fill=(255, 255, 255, 26), outline=WHITE, width=13)
ld.line([(2 * r - 10, 2 * r - 10), (2 * r + 2, 2 * r + 2)], fill=WHITE, width=20)
img.paste(lens, (cx - r, cy - r), lens)

# bottom caption
f3 = fit(d, "ok. pics of the escrow then.", IMPACT, 1080, 118)
outlined(d, (W // 2, 1030), "ok. pics of the escrow then.", f3, YELLOW)

# footer
d.text((W // 2, 1170), "pics or it didn't happen  ·  so prove the pot",
       font=ImageFont.truetype(MONO, 24), fill=(90, 98, 110), anchor="mm")

img.save("C:/Users/nicoa/poidh-auto/claims/1527/meme1527.png", optimize=True)
print("ok", img.size)
