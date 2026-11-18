#!/usr/bin/env python3
"""Render captured terminal text (real command output) to a PNG 'screenshot'."""
import sys
from PIL import Image, ImageDraw, ImageFont
def render(txt_path, out_path, title):
    lines = open(txt_path).read().rstrip("\n").split("\n")
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 15)
    bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 15)
    cw = font.getlength("M"); lh = 21
    width = int(max(len(l) for l in lines) * cw) + 40
    width = max(width, 760)
    bar = 34
    h = bar + lh * len(lines) + 30
    im = Image.new("RGB", (width, h), (24, 26, 31))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, width, bar], fill=(52, 56, 66))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([14 + i * 22, 11, 26 + i * 22, 23], fill=c)
    d.text((width // 2 - len(title) * 4, 8), title, fill=(210, 214, 224), font=font)
    y = bar + 14
    for l in lines:
        if l.startswith("$"):
            d.text((20, y), l, fill=(120, 220, 140), font=bold)
        elif "OK" in l.split()[-1:] or "IDENTICAL" in l:
            d.text((20, y), l, fill=(120, 220, 140), font=font)
        elif "HIGH" in l or "ALERT" in l:
            d.text((20, y), l, fill=(255, 150, 130), font=font)
        else:
            d.text((20, y), l, fill=(215, 218, 226), font=font)
        y += lh
    im.save(out_path)
if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2], sys.argv[3])
