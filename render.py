#!/usr/bin/env python3
"""Render the front page for Sunday 22 November 2026.

A one-page newspaper drawn with Pillow, 1024 by 1024 pixels. Every word
and every position is fixed in this file, so running it twice produces
the same bytes. Run: python3 render.py
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SIDE = 1024
EDGE = 36

PALETTE = {
    "paper": (247, 243, 234),
    "ink": (26, 26, 26),
    "red": (163, 29, 29),
    "green": (28, 78, 58),
    "sea": (52, 128, 122),
    "grey": (110, 105, 95),
    "gold": (214, 158, 46),
    "sky": (214, 232, 226),
    "cream": (247, 243, 234),
    "hill": (122, 158, 132),
    "hill2": (96, 138, 112),
    "foam": (190, 220, 214),
    "white": (255, 255, 255),
}

DEJAVU = Path("/usr/share/fonts/truetype/dejavu")


def face(kind, size):
    names = {
        "serif": "DejaVuSerif.ttf",
        "serif-bold": "DejaVuSerif-Bold.ttf",
        "sans": "DejaVuSans.ttf",
        "sans-bold": "DejaVuSans-Bold.ttf",
    }
    return ImageFont.truetype(str(DEJAVU / names[kind]), size)


class Sheet:
    """A drawing surface plus the small helpers the page is built from."""

    def __init__(self):
        self.image = Image.new("RGB", (SIDE, SIDE), PALETTE["paper"])
        self.pen = ImageDraw.Draw(self.image)

    def hline(self, left, top, length, colour, thick=2):
        self.pen.line([(left, top), (left + length, top)], fill=colour,
                      width=thick)

    def label(self, left, top, words, kind, size, colour):
        self.pen.text((left, top), words, font=face(kind, size), fill=colour)

    def width_of(self, words, kind, size):
        return self.pen.textlength(words, font=face(kind, size))

    def split(self, words, kind, size, max_width):
        """Break words into lines that fit max_width, measured exactly."""
        done, current = [], ""
        for word in words.split():
            candidate = (current + " " + word).strip()
            if self.width_of(candidate, kind, size) <= max_width:
                current = candidate
            else:
                if current:
                    done.append(current)
                current = word
        if current:
            done.append(current)
        return done

    def paragraph(self, left, top, words, kind, size, max_width, spacing,
                  colour=None):
        """Draw a wrapped block of text; return the y below its last line."""
        ink = colour if colour is not None else PALETTE["ink"]
        cursor = top
        for row in self.split(words, kind, size, max_width):
            self.label(left, cursor, row, kind, size, ink)
            cursor += spacing
        return cursor

    def save(self, name="entry.png"):
        target = ROOT / name
        self.image.save(target, format="PNG", optimize=True)
        return target


def turbine(sheet, foot_x, ground_y, height):
    """One white wind turbine: pole, hub, three blades."""
    top_y = ground_y - height
    sheet.pen.line([(foot_x, ground_y), (foot_x, top_y)],
                   fill=PALETTE["cream"], width=4)
    for degrees in (90, 210, 330):
        angle = math.radians(degrees)
        sheet.pen.line(
            [(foot_x, top_y),
             (foot_x + 26 * math.cos(angle), top_y + 26 * math.sin(angle))],
            fill=PALETTE["cream"], width=3)
    sheet.pen.ellipse([foot_x - 3, top_y - 3, foot_x + 3, top_y + 3],
                      fill=PALETTE["cream"])


def morning_sea(sheet, left, top, width, height):
    """Sun over the sea off Antalya, with turbines on the shore."""
    sheet.pen.rectangle([left, top, left + width, top + height],
                        fill=PALETTE["sky"])
    sun_x = left + width * 0.72
    sun_y = top + height * 0.34
    radius = 30
    sheet.pen.ellipse([sun_x - radius, sun_y - radius,
                       sun_x + radius, sun_y + radius], fill=PALETTE["gold"])
    for step in range(8):
        angle = step * math.pi / 4
        near = (sun_x + (radius + 4) * math.cos(angle),
                sun_y + (radius + 4) * math.sin(angle))
        far = (sun_x + (radius + 16) * math.cos(angle),
               sun_y + (radius + 16) * math.sin(angle))
        sheet.pen.line([near, far], fill=PALETTE["gold"], width=3)
    horizon = top + height * 0.62
    sheet.pen.polygon(
        [(left, horizon), (left + width * 0.30, top + height * 0.44),
         (left + width * 0.55, horizon)], fill=PALETTE["hill"])
    sheet.pen.polygon(
        [(left + width * 0.45, horizon),
         (left + width * 0.75, top + height * 0.48),
         (left + width, horizon)], fill=PALETTE["hill2"])
    sheet.pen.rectangle([left, horizon, left + width, top + height],
                        fill=PALETTE["sea"])
    for frac, span in [(0.70, 0.55), (0.78, 0.75), (0.86, 0.45),
                       (0.93, 0.65)]:
        wave_y = top + height * frac
        sheet.pen.line(
            [(left + width * (1 - span) / 2, wave_y),
             (left + width * (1 + span) / 2, wave_y)],
            fill=PALETTE["foam"], width=3)
    for step in range(4):
        glint_y = top + height * (0.68 + step * 0.07)
        glint_w = 90 - step * 18
        sheet.pen.line([(sun_x - glint_w / 2, glint_y),
                        (sun_x + glint_w / 2, glint_y)],
                       fill=PALETTE["gold"], width=3)
    for frac_x, frac_h in [(0.10, 0.42), (0.24, 0.34), (0.38, 0.46)]:
        turbine(sheet, left + width * frac_x, horizon, height * frac_h)
    for frac_x, frac_y in [(0.58, 0.16), (0.66, 0.22), (0.52, 0.26)]:
        bird_x, bird_y = left + width * frac_x, top + height * frac_y
        sheet.pen.arc([bird_x - 8, bird_y - 6, bird_x, bird_y + 6],
                      200, 340, fill=PALETTE["ink"], width=2)
        sheet.pen.arc([bird_x, bird_y - 6, bird_x + 8, bird_y + 6],
                      200, 340, fill=PALETTE["ink"], width=2)


def masthead(sheet):
    sheet.pen.rectangle([0, 0, SIDE, 104], fill=PALETTE["green"])
    title = "THE WORLD"
    title_w = sheet.width_of(title, "serif-bold", 78)
    sheet.label((SIDE - title_w) / 2, 8, title, "serif-bold", 78,
                PALETTE["cream"])
    sheet.label(EDGE, 118, "SUNDAY 22 NOVEMBER 2026", "sans-bold", 24,
                PALETTE["ink"])
    tagline = "ONE DAY · ONE PAGE"
    tag_w = sheet.width_of(tagline, "sans-bold", 24)
    sheet.label(SIDE - EDGE - tag_w, 118, tagline, "sans-bold", 24,
                PALETTE["red"])
    sheet.hline(EDGE, 150, SIDE - 2 * EDGE, PALETTE["ink"], 3)


def lead_story(sheet):
    col_x, col_w = EDGE, 596
    top = 166
    sheet.label(col_x, top, "CLIMATE", "sans-bold", 19, PALETTE["red"])
    cursor = sheet.paragraph(col_x, top + 28, "COP31 deal drops fossil fuels",
                             "serif-bold", 43, col_w, 50)
    cursor += 6
    morning_sea(sheet, col_x, cursor, col_w, 148)
    cursor += 148 + 10
    cursor = sheet.paragraph(
        col_x, cursor,
        "The final draft released in the early hours of Sunday in Antalya "
        "makes no mention of fossil fuels in its ten pages. Electricity is "
        "to supply 35% of final energy by 2035.",
        "serif", 20, col_w, 27)
    cursor += 4
    cursor = sheet.paragraph(
        col_x, cursor,
        "Delegates vote on Sunday morning after two days of overtime.",
        "serif-bold", 20, col_w, 27)
    assert cursor <= 630, f"lead ran past its box: {cursor}"


def gulf_column(sheet):
    col_x, col_w = 668, SIDE - EDGE - 668
    top = 166
    sheet.label(col_x, top, "GULF", "sans-bold", 19, PALETTE["red"])
    cursor = sheet.paragraph(col_x, top + 28,
                             "Iran hits Bahrain; tankers struck",
                             "serif-bold", 30, col_w, 36)
    cursor += 4
    cursor = sheet.paragraph(
        col_x, cursor,
        "Iran's Revolutionary Guards fired missiles and drones at US bases "
        "in Bahrain late on Saturday. Bahrain says a civilian industrial "
        "facility was hit and a fire broke out; no one was hurt. Two tankers "
        "were also hit in the Strait of Hormuz.",
        "serif", 19, col_w, 26)
    cursor += 14
    sheet.hline(col_x, cursor, col_w, PALETTE["grey"], 1)
    cursor += 12
    sheet.label(col_x, cursor, "BY THE NUMBERS", "sans-bold", 19,
                PALETTE["red"])
    cursor += 28
    for figure, caption in [("35%", "electricity share by 2035"),
                            ("0", "injuries in Bahrain"),
                            ("36", "missing in Java factory fire")]:
        sheet.label(col_x, cursor, figure, "serif-bold", 24, PALETTE["red"])
        sheet.label(col_x + 92, cursor + 4, caption, "serif", 17,
                    PALETTE["ink"])
        cursor += 30
    assert cursor <= 630, f"gulf column ran past its box: {cursor}"


def second_row(sheet):
    top = 630
    sheet.hline(EDGE, top, SIDE - 2 * EDGE, PALETTE["ink"], 2)
    top += 12
    col_w = (SIDE - 2 * EDGE - 2 * 20) // 3
    items = [
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
    for index, (kicker, headline, body) in enumerate(items):
        col_x = EDGE + index * (col_w + 20)
        sheet.label(col_x, top, kicker, "sans-bold", 19, PALETTE["red"])
        bottom = sheet.paragraph(col_x, top + 26, headline, "serif-bold",
                                 21, col_w, 26)
        bottom += 4
        bottom = sheet.paragraph(col_x, bottom, body, "serif", 17, col_w, 20)
        assert bottom <= 790, f"story {index} ran past its box: {bottom}"


def briefs_grid(sheet):
    top = 792
    sheet.hline(EDGE, top, SIDE - 2 * EDGE, PALETTE["ink"], 2)
    top += 10
    sheet.label(EDGE, top, "THE DAY IN BRIEF", "sans-bold", 19,
                PALETTE["red"])
    top += 30
    entries = [
        ("GULF", "Bahrain demands UN action over the industrial-site fire."),
        ("CLIMATE", "COP31 draft sets a 1-billion-tonne carbon-capture goal."),
        ("TRADE", "EU–Indonesia deal is set to take effect in early 2027, if ratified."),
        ("SPORT", "Columbus thrash Miami in the MLS Cup; a Messi furore follows."),
        ("GULF", "Iran gathers 14 tankers at Kharg Island to test the US blockade."),
        ("EDUCATION", "111 cases of device cheating were caught at the Suneung."),
    ]
    cell_w = (SIDE - 2 * EDGE - 2 * 20) // 3
    for index, (kicker, text) in enumerate(entries):
        cell_x = EDGE + (index % 3) * (cell_w + 20)
        cell_y = top + (index // 3) * 56
        sheet.label(cell_x, cell_y, kicker, "sans-bold", 16, PALETTE["red"])
        end = sheet.paragraph(cell_x, cell_y + 20, text, "serif", 16,
                              cell_w, 20)
        assert end <= 948, f"brief {index} ran past its box: {end}"


def ticker(sheet):
    top = 950
    sheet.pen.rectangle([0, top, SIDE, top + 40], fill=PALETTE["green"])
    line = ("COP31 VOTE DUE SUNDAY MORNING   ·   BAHRAIN DEMANDS UN ACTION"
            "   ·   SEOUL MINISTER QUITS   ·   36 MISSING IN JAVA FIRE")
    size = 19
    while size > 10:
        if sheet.width_of(line, "sans-bold", size) <= 960:
            break
        size -= 1
    line_w = sheet.width_of(line, "sans-bold", size)
    sheet.label((SIDE - line_w) / 2, top + (40 - size) / 2 - 2, line,
                "sans-bold", size, PALETTE["cream"])


def footer(sheet):
    sheet.label(
        EDGE, 998,
        "THE WORLD — a one-page summary of Sunday 22 November 2026 · "
        "Sources: AP, Reuters, AFP, Korea JoongAng Daily, UKMTO",
        "sans", 14, PALETTE["grey"])


def build():
    sheet = Sheet()
    masthead(sheet)
    lead_story(sheet)
    gulf_column(sheet)
    second_row(sheet)
    briefs_grid(sheet)
    ticker(sheet)
    footer(sheet)
    target = sheet.save()
    print("wrote", target, sheet.image.size,
          target.stat().st_size, "bytes")


if __name__ == "__main__":
    build()
