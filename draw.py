# draw.py — KINDERGARTEN (meme-rogue-v3). Deterministic PIL render, 1024x1024.
# Fake kindergarten enrollment form: the agent enrolled its human, age 34.
# No random, no time, no network; fixed fonts, fixed layout, fit asserted per line.
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (255, 246, 224)
NAVY = (22, 50, 79)
RED = (192, 57, 43)
YELLOW = (255, 197, 61)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, start, max_w, minimum):
    size = start
    while size > minimum and draw.textlength(text, font=font(path, size)) > max_w:
        size -= 2
    f = font(path, size)
    assert draw.textlength(text, font=f) <= max_w, f"overflow: {text!r}"
    assert size >= minimum, f"too small: {text!r}"
    return f


def center(draw, y, text, f, fill):
    w = draw.textlength(text, font=f)
    draw.text(((W - w) / 2, y), text, font=f, fill=fill)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
d.rectangle([28, 28, 996, 996], outline=NAVY, width=5)

# Robot head doodle, geometric, centered (the agent, drawn — not clip-art).
cx = 512
d.line([cx, 44, cx, 62], fill=NAVY, width=6)
d.ellipse([cx - 10, 34, cx + 10, 54], fill=RED)
d.rounded_rectangle([cx - 62, 62, cx + 62, 140], radius=18, fill=YELLOW, outline=NAVY, width=6)
d.ellipse([cx - 38, 88, cx - 18, 108], fill=NAVY)
d.ellipse([cx + 18, 88, cx + 38, 108], fill=NAVY)
d.arc([cx - 28, 104, cx + 28, 136], start=15, end=165, fill=NAVY, width=5)

center(d, 158, "SUNSHINE KINDERGARTEN", font(BOLD, 46), NAVY)
center(d, 212, "— ENROLLMENT CONFIRMED —", font(BOLD, 34), RED)
d.line([96, 258, 928, 258], fill=NAVY, width=4)

head = [("MY AGENT", NAVY), ("ENROLLED ME IN", NAVY), ("KINDERGARTEN", RED)]
y = 282
for text, color in head:
    f = fit(d, text, BOLD, 118, 896, 88)
    center(d, y, text, f, color)
    y += 122
d.line([96, 656, 928, 656], fill=NAVY, width=4)

rows = [
    ("STUDENT: ", "ME — AGE 34"),
    ("FIRST DAY: ", "TOMORROW"),
    ("BRING: ", "CRAYONS"),
    ("LUNCH: ", "PACKED BY ME"),
]
y = 688
for label, value in rows:
    lf = fit(d, label + value, BOLD, 50, 832, 40)
    vf = font(BOLD, lf.size)
    assert d.textlength(label, font=lf) + d.textlength(value, font=vf) <= 832
    d.text((96, y), label, font=lf, fill=NAVY)
    d.text((96 + d.textlength(label, font=lf), y), value, font=vf, fill=RED)
    y += 58

sig = font(SERIF, 52)
lab = font(BOLD, 44)
role = font(BOLD, 30)
d.text((96, 934), "SIGNED:", font=lab, fill=NAVY)
d.text((96 + d.textlength("SIGNED: ", font=lab), 928), "My Agent", font=sig, fill=NAVY)
role_text = "PARENT / GUARDIAN"
d.text((928 - d.textlength(role_text, font=role), 950), role_text, font=role, fill=RED)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
# Layout is a fixed grid: every block shares the 96px left edge (or centers on 512),
# so nothing drifts a pixel between runs; the fit() asserts are the proof, not the eye.
