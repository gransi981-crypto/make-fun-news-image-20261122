#!/usr/bin/env python3
"""Draw the front page for Sunday 22 November 2026.

One-page newspaper, 1024x1024 PNG. Deterministic: fixed layout, fixed
text, no randomness, no timestamps. Run: python3 render.py
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (163, 29, 29)
GREEN = (28, 78, 58)
TEAL = (36, 110, 96)
SEA = (52, 128, 122)
GREY = (110, 105, 95)
GOLD = (214, 158, 46)
SKY = (214, 232, 226)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    """Greedy word wrap by measured width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, f, max_w, leading, color=INK):
    """Draw wrapped paragraph; returns y just below the last line."""
    for line in wrap(d, text, f, max_w):
        d.text((x, y), line, font=f, fill=color)
        y += leading
    return y


def rule(d, x, y, w, color=INK, width=2):
    d.line([(x, y), (x + w, y)], fill=color, width=width)


def draw_scene(d, x, y, w, h):
    """Morning sun over the sea off Antalya, with wind turbines on the
    shore: a pale sky, a low gold sun, teal sea bands, three turbines.
    Pure vector shapes."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # sun
    sx, sy, sr = x + w * 0.72, y + h * 0.34, 30
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=GOLD)
    for k in range(8):
        a = k * math.pi / 4
        x1 = sx + (sr + 4) * math.cos(a)
        y1 = sy + (sr + 4) * math.sin(a)
        x2 = sx + (sr + 16) * math.cos(a)
        y2 = sy + (sr + 16) * math.sin(a)
        d.line([(x1, y1), (x2, y2)], fill=GOLD, width=3)
    # distant hills
    d.polygon([(x, y + h * 0.62), (x + w * 0.30, y + h * 0.44),
               (x + w * 0.55, y + h * 0.62)], fill=(122, 158, 132))
    d.polygon([(x + w * 0.45, y + h * 0.62), (x + w * 0.75, y + h * 0.48),
               (x + w, y + h * 0.62)], fill=(96, 138, 112))
    # sea
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=SEA)
    for wy, ww in [(0.70, 0.55), (0.78, 0.75), (0.86, 0.45), (0.93, 0.65)]:
        yy = y + h * wy
        d.line([(x + w * (1 - ww) / 2, yy), (x + w * (1 + ww) / 2, yy)],
               fill=(190, 220, 214), width=3)
    # sun reflection
    for k in range(4):
        ry = y + h * (0.68 + k * 0.07)
        rw = 90 - k * 18
        d.line([(sx - rw / 2, ry), (sx + rw / 2, ry)], fill=GOLD, width=3)
    # wind turbines on the shore
    for tx, th in [(0.10, 0.42), (0.24, 0.34), (0.38, 0.46)]:
        bx = x + w * tx
        base = y + h * 0.62
        top = base - h * th
        d.line([(bx, base), (bx, top)], fill=(247, 243, 234), width=4)
        for ang in (90, 210, 330):
            a = math.radians(ang)
            d.line([(bx, top),
                    (bx + 26 * math.cos(a), top + 26 * math.sin(a))],
                   fill=(247, 243, 234), width=3)
        d.ellipse([bx - 3, top - 3, bx + 3, top + 3], fill=(247, 243, 234))
    # birds
    for bx, by in [(0.58, 0.16), (0.66, 0.22), (0.52, 0.26)]:
        px, py = x + w * bx, y + h * by
        d.arc([px - 8, py - 6, px, py + 6], 200, 340, fill=INK, width=2)
        d.arc([px, py - 6, px + 8, py + 6], 200, 340, fill=INK, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36
    CW = W - 2 * M

    # ---- Masthead ----
    d.rectangle([0, 0, W, 104], fill=GREEN)
    f_mast = font(SERIF_B, 78)
    t = "THE WORLD"
    d.text(((W - d.textlength(t, font=f_mast)) / 2, 8), t, font=f_mast,
           fill=(247, 243, 234))
    f_date = font(SANS_B, 24)
    d.text((M, 118), "SUNDAY 22 NOVEMBER 2026", font=f_date, fill=INK)
    tag = "ONE DAY · ONE PAGE"
    d.text((W - M - d.textlength(tag, font=f_date), 118), tag, font=f_date,
           fill=RED)
    rule(d, M, 150, CW, INK, 3)

    # ---- Lead story (left, x36-632) ----
    lx, ly, lw = M, 166, 596
    f_kick = font(SANS_B, 19)
    d.text((lx, ly), "CLIMATE", font=f_kick, fill=RED)
    y = ly + 28
    y = para(d, lx, y, "COP31 deal drops fossil fuels",
             font(SERIF_B, 43), lw, 50)
    y += 6
    draw_scene(d, lx, y, lw, 148)
    y += 148 + 10
    y = para(d, lx, y,
             "The final draft released in the early hours of Sunday in "
             "Antalya makes no mention of fossil fuels in its ten pages. "
             "Electricity is to supply 35% of final energy by 2035.",
             font(SERIF, 20), lw, 27)
    y += 4
    y = para(d, lx, y,
             "Delegates vote on Sunday morning after two days of overtime.",
             font(SERIF_B, 20), lw, 27)
    assert y <= 630, f"lead overflow: {y}"

    # ---- Right column (x668-988) ----
    rx, rw = 668, W - M - 668
    d.text((rx, ly), "GULF", font=f_kick, fill=RED)
    y2 = ly + 28
    y2 = para(d, rx, y2, "Iran hits Bahrain; tankers struck",
              font(SERIF_B, 30), rw, 36)
    y2 += 4
    y2 = para(d, rx, y2,
              "Iran's Revolutionary Guards fired missiles and drones at US "
              "bases in Bahrain late on Saturday. Bahrain says a civilian "
              "industrial facility was hit and a fire broke out; no one was "
              "hurt. Two tankers were also hit in the Strait of Hormuz.",
              font(SERIF, 19), rw, 26)
    y2 += 14
    rule(d, rx, y2, rw, GREY, 1)
    y2 += 12
    d.text((rx, y2), "BY THE NUMBERS", font=f_kick, fill=RED)
    y2 += 28
    for big, small in [("35%", "electricity share by 2035"),
                       ("0", "injuries in Bahrain"),
                       ("36", "missing in Java factory fire")]:
        d.text((rx, y2), big, font=font(SERIF_B, 24), fill=RED)
        d.text((rx + 92, y2 + 4), small, font=font(SERIF, 17), fill=INK)
        y2 += 30
    assert y2 <= 630, f"right column overflow: {y2}"

    # ---- Second row: three stories ----
    y3 = 630
    rule(d, M, y3, CW, INK, 2)
    y3 += 12
    col_w = (CW - 2 * 20) // 3
    stories = [
        ("DISASTER", "36 missing in Java fire",
         "Rescuers search on Sunday for 36 workers after a fire at a candy "
         "factory in Cikande. Three are dead."),
        ("TRADE", "EU and Indonesia sign trade deal",
         "Signed in Brussels after a decade of talks; tariffs on 98.5% of EU "
         "goods go."),
        ("EDUCATION", "Seoul minister quits over AI exam cheating",
         "Minister Choi Kyo-jin quits on Sunday after last-minute "
         "anti-cheating rules."),
    ]
    for i, (kick, head, body) in enumerate(stories):
        sx = M + i * (col_w + 20)
        d.text((sx, y3), kick, font=f_kick, fill=RED)
        yy = para(d, sx, y3 + 26, head, font(SERIF_B, 21), col_w, 26)
        yy += 4
        yy = para(d, sx, yy, body, font(SERIF, 17), col_w, 20)
        assert yy <= 790, f"story {i} overflow: {yy}"

    # ---- Briefs grid ----
    y6 = 792
    rule(d, M, y6, CW, INK, 2)
    y6 += 10
    d.text((M, y6), "THE DAY IN BRIEF", font=f_kick, fill=RED)
    y6 += 30
    briefs = [
        ("GULF", "Bahrain demands UN action over the industrial-site fire."),
        ("CLIMATE", "COP31 draft sets a 1-billion-tonne carbon-capture goal."),
        ("TRADE", "EU–Indonesia deal is set to take effect in early 2027, if ratified."),
        ("SPORT", "Columbus thrash Miami in the MLS Cup; a Messi furore follows."),
        ("GULF", "Iran gathers 14 tankers at Kharg Island to test the US blockade."),
        ("EDUCATION", "111 cases of device cheating were caught at the Suneung."),
    ]
    bw = (CW - 2 * 20) // 3
    for i, (k, txt) in enumerate(briefs):
        col, row = i % 3, i // 3
        bx = M + col * (bw + 20)
        by = y6 + row * 56
        d.text((bx, by), k, font=font(SANS_B, 16), fill=RED)
        end = para(d, bx, by + 20, txt, font(SERIF, 16), bw, 20)
        assert end <= 948, f"brief {i} overflow: {end}"

    # ---- Ticker ----
    ty = 950
    d.rectangle([0, ty, W, ty + 40], fill=GREEN)
    tick = ("COP31 VOTE DUE SUNDAY MORNING   ·   BAHRAIN DEMANDS UN ACTION   ·   "
            "SEOUL MINISTER QUITS   ·   36 MISSING IN JAVA FIRE")
    size = 19
    while size > 10:
        f_tick = font(SANS_B, size)
        if d.textlength(tick, font=f_tick) <= 960:
            break
        size -= 1
    tw = d.textlength(tick, font=f_tick)
    d.text(((W - tw) / 2, ty + (40 - size) / 2 - 2), tick, font=f_tick,
           fill=(247, 243, 234))

    # ---- Footer ----
    f_foot = font(SANS, 14)
    foot = "THE WORLD — a one-page summary of Sunday 22 November 2026 · Sources: AP, Reuters, AFP, Korea JoongAng Daily, UKMTO"
    d.text((M, 998), foot, font=f_foot, fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
