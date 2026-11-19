#!/usr/bin/env python3
"""Draw the news-image-20261118 entry: a dense newspaper front page that
sums up world news of Wednesday 18 November 2026.

Run:  python3 draw_news.py
Out:  entry.png  (1024x1024, well under the 1 MiB gate)

Layout: masthead + big date, 3 lead stories, a world map with 16 hotspots,
a count bar (stories by region, seven regions), a "day in numbers" strip,
and 45 more stories in brief -- 48 stories from seven regions.

The coastline data (coast.txt) is a simplified public-domain world outline
(Natural Earth data, decimated to 88 polygons / 649 points); this script
renders it. The map is drawn by this code, not copied as artwork.

Every story was checked against live news on 18 Nov 2026 (Times of India
live blog, Outlook India, Anadolu Agency morning briefing, Just Security
early edition, Level Headlines daily brief, MercoPress, TBS News). Leads:
  1. US strikes Qeshm Island and sinks five Iranian tankers; Iran hits
     back in Kuwait and Bahrain.
  2. Ukraine hits the Kerch Bridge a second night; part of the span falls.
  3. Trump lands in Shenzhen for the first Trump-Xi-Putin trilateral.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
OUT = os.path.join(HERE, "entry.png")

PAPER = (250, 247, 240)
INK = (20, 33, 61)
RED = (169, 22, 33)
GREY = (90, 92, 96)
LIGHT = (214, 210, 200)
WHITE = (255, 255, 255)
LAND = (196, 198, 190)
LAND_EDGE = (150, 152, 144)
SEA = (233, 236, 232)
CHIP = (238, 235, 228)
CHIP_EDGE = (200, 196, 186)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_NAME = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
F_REG = lambda s: font("DejaVuSans.ttf", s)

LEADS = [
    {
        "kicker": "WAR IN THE GULF",
        "head": "U.S. STRIKES QESHM, SINKS FIVE IRANIAN TANKERS",
        "body": "U.S. jets strike Qeshm and sink five tankers; Iran hits back "
                "in Kuwait and Bahrain.",
        "color": (163, 22, 33),
    },
    {
        "kicker": "WAR IN UKRAINE",
        "head": "KERCH BRIDGE SPAN FALLS AS UKRAINE STRIKES AGAIN",
        "body": "Ukraine hits the Crimea bridge a second night; the crossing "
                "shuts.",
        "color": (15, 82, 87),
    },
    {
        "kicker": "SUMMIT IN SHENZHEN",
        "head": "TRUMP LANDS IN SHENZHEN SUMMIT",
        "body": "Xi greets him at the airport; Xi and Putin met for the 50th "
                "time.",
        "color": (27, 58, 92),
    },
]

# (lon, lat, label, dx, dy, big) -- hotspots marked on the map.
DOTS = [
    (56.3, 26.9, "Qeshm", 8, -8, True),
    (36.5, 45.3, "Kerch", 8, -16, True),
    (114.1, 22.5, "Shenzhen", 8, -8, True),
    (50.5, 26.2, "Bahrain", 8, 14, False),
    (121.0, 14.6, "Manila", 8, -4, False),
    (77.2, 28.6, "New Delhi", 8, -8, False),
    (13.4, 52.5, "Berlin", 8, -16, False),
    (-161.0, -10.4, "Cook Is.", 8, 4, False),
    (147.0, -6.5, "Papua N.G.", 8, -4, False),
    (-149.9, 61.2, "Alaska", 8, -8, False),
    (30.2, 1.6, "Congo", 8, -4, False),
    (30.7, 36.9, "Antalya", 8, -12, False),
    (2.35, 48.85, "Paris", 8, 8, False),
    (35.2, 31.8, "Jerusalem", -78, 14, False),
    (-46.0, -4.5, "Amazon", 8, -4, False),
    (-58.4, -34.6, "Buenos Aires", -95, -4, False),
]

# stories by region (7 regions) -- must sum to 48 (3 leads + 45 briefs).
# North America 9, South America 2, Europe 14, Africa 3,
# Middle East 7, Asia 10, Oceania 3.
REGION_COUNTS = [
    ("N. AMERICA", 9),
    ("S. AMERICA", 2),
    ("EUROPE", 14),
    ("AFRICA", 3),
    ("M. EAST", 7),
    ("ASIA", 10),
    ("OCEANIA", 3),
]

# (big number, label) -- the day in numbers.
NUMBERS = [
    ("5", "tankers sunk off Qeshm"),
    ("140,000", "march in France"),
    ("11,000", "Ebola cases in Congo"),
    ("$92.47", "Brent crude"),
    ("6.0", "quake in Papua N.G."),
    ("56\u201344", "new U.S. Senate"),
]

BRIEF = [
    # column 1 -- conflict, disaster, security
    "Cyclone Xavier, Cat 5, hits Cook Islands",
    "M6 quake strikes Papua New Guinea",
    "Russian military plane crashes; 19 killed",
    "Serbian MiG-29 crashes; pilot killed",
    "Houthis press toward Aden",
    "Bahrain intercepts Iranian attacks",
    "ADNOC ship hit in Hormuz; crew missing",
    "Gaza ceasefire may collapse, Board warns",
    "Clashes near Eritrean border raise fears",
    "Ebola in DR Congo passes 11,000 cases",
    "Five EU states plan Rwanda return hubs",
    "Pakistani gets 27 years over Trump plot",
    "U.S. soldier in UK spy case moved to U.S.",
    "Bangladesh violence: local leader killed",
    "Fiji declares disaster over drought",
    # column 2 -- politics, diplomacy, economy
    "Peltola wins Alaska; Democrats reach 56",
    "Trump open to meeting Kim Jong Un",
    "Quad leaders meet in Manila, first in 2 yrs",
    "Modi returns after ASEAN summit",
    "Eisenkot ally elected Knesset speaker",
    "Turkey takes over Sozcu TV",
    "Student list takes Serbia parliament",
    "140,000 join French pay protests",
    "U.S. criticizes Ukraine deep strikes",
    "Germany pledges new Ukraine aid, F-16s",
    "UK sanctions 8 firms over West Bank",
    "COP31 talks enter decisive phase",
    "Stocks slide; Brent crude $92.47",
    "S. Korea raises 2027 growth to 3.9%",
    "Nepal to import 350 MW from India",
    # column 3 -- tech, economy, culture, sport, health
    "Cyclone Akvan strengthens off India",
    "U.S. tightens chip rules for China",
    "Nvidia beats forecasts after Huang exit",
    "Anthropic to list on Nasdaq Nov. 19",
    "U.S. loses measles-elimination status",
    "France-Malaysia strike rare-earths deal",
    "Brazil real falls on Lula fiscal plan",
    "Europe pays up for LNG; stocks low",
    "Pakistan solar share hits 28%",
    "Pattinson named the new James Bond",
    "Fela Kuti enters Rock Hall of Fame",
    "'Human' is Cambridge word of the year",
    "Zverev reaches ATP Finals knockouts",
    "Argentina thrash Costa Rica 7-0",
    "GTA VI launches tomorrow",
]


def wrap(draw, text, fnt, width):
    lines, line = [], ""
    for word in text.split(" "):
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def load_coast():
    polys = []
    with open(os.path.join(HERE, "coast.txt")) as fh:
        for line in fh:
            pts = []
            for tok in line.split():
                lon, lat = tok.split(",")
                pts.append((float(lon), float(lat)))
            if len(pts) >= 4:
                polys.append(pts)
    return polys


def project(lon, lat, box):
    """Equirectangular projection into box (x0, y0, x1, y1).
    Longitude -170..190, latitude -56..84 (Antarctica cut)."""
    x0, y0, x1, y1 = box
    x = x0 + (lon + 170.0) / 360.0 * (x1 - x0)
    y = y0 + (84.0 - lat) / 140.0 * (y1 - y0)
    return (x, y)


def draw_map(d, box):
    d.rectangle(box, fill=SEA)
    for poly in load_coast():
        pts = [project(lon, lat, box) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # faint graticule
    for lon in range(-150, 181, 30):
        x, _ = project(lon, 0, box)
        d.line([x, box[1], x, box[3]], fill=(220, 223, 219), width=1)
    for lat in (-30, 0, 30, 60):
        _, y = project(0, lat, box)
        d.line([box[0], y, box[2], y], fill=(220, 223, 219), width=1)
    # ocean labels
    fo = F_REG(13)
    for txt, lon, lat in (("PACIFIC", -150, -32), ("ATLANTIC", -30, -28),
                          ("INDIAN", 85, -38)):
        x, y = project(lon, lat, box)
        d.text((x, y), txt, font=fo, fill=(150, 154, 150))
    # hotspots
    fd = F_BOLD(12)
    for lon, lat, label, dx, dy, big in DOTS:
        x, y = project(lon, lat, box)
        r = 7 if big else 5
        d.ellipse([x - r, y - r, x + r, y + r], fill=RED,
                  outline=WHITE, width=2)
        d.text((x + dx, y + dy), label, font=fd, fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 10], fill=RED)
    name = "THE WORLD IN ONE DAY"
    f = F_NAME(52)
    d.text(((W - d.textlength(name, font=f)) / 2, 20), name, font=f, fill=INK)
    sub = "48 stories from seven regions, in one picture"
    fs = F_REG(18)
    d.text(((W - d.textlength(sub, font=fs)) / 2, 80), sub, font=fs, fill=GREY)
    d.rectangle([0, 104, W, 156], fill=RED)
    date = "WEDNESDAY  18  NOVEMBER  2026"
    fd = F_BOLD(36)
    d.text(((W - d.textlength(date, font=fd)) / 2, 112), date, font=fd,
           fill=WHITE)
    d.line([0, 162, W, 162], fill=INK, width=2)

    # --- leads ---------------------------------------------------------
    col_w, gap = 304, 32
    x0 = 24
    for i, s in enumerate(LEADS):
        x = x0 + i * (col_w + gap)
        d.rectangle([x, 172, x + col_w, 176], fill=s["color"])
        fk, fh, fb = F_BOLD(14), F_BOLD(19), F_REG(14)
        d.text((x, 180), s["kicker"], font=fk, fill=RED)
        hy = 198
        for line in wrap(d, s["head"], fh, col_w):
            d.text((x, hy), line, font=fh, fill=INK)
            hy += 23
        by = hy + 2
        for line in wrap(d, s["body"], fb, col_w):
            d.text((x, by), line, font=fb, fill=(52, 54, 60))
            by += 18
    d.line([0, 290, W, 290], fill=LIGHT, width=1)

    # --- map -----------------------------------------------------------
    draw_map(d, (24, 298, 1000, 470))

    # --- count bar: stories by region ----------------------------------
    d.text((24, 478), "STORIES BY REGION", font=F_BOLD(13), fill=INK)
    total = sum(n for _, n in REGION_COUNTS)
    d.text((W - 24 - d.textlength("48 IN ALL", font=F_BOLD(13)), 478),
           "48 IN ALL", font=F_BOLD(13), fill=RED)
    chip_w, chip_gap = 132, 8
    cx = 24
    cy = 498
    for name_r, n in REGION_COUNTS:
        d.rectangle([cx, cy, cx + chip_w, cy + 28], fill=CHIP,
                    outline=CHIP_EDGE, width=1)
        d.rectangle([cx, cy, cx + chip_w, cy + 4], fill=RED)
        fr = F_BOLD(11)
        d.text((cx + 8, cy + 8), name_r, font=fr, fill=GREY)
        fn = F_BOLD(16)
        d.text((cx + chip_w - 8 - d.textlength(str(n), font=fn), cy + 7),
               str(n), font=fn, fill=INK)
        cx += chip_w + chip_gap

    # --- the day in numbers --------------------------------------------
    d.text((24, 536), "THE DAY IN NUMBERS", font=F_BOLD(13), fill=INK)
    nw = (W - 48) // len(NUMBERS)
    for i, (num, label) in enumerate(NUMBERS):
        x = 24 + i * nw
        fn = F_BOLD(20)
        d.text((x, 554), num, font=fn, fill=RED)
        fl = F_REG(12)
        d.text((x, 578), label, font=fl, fill=(52, 54, 60))

    # --- the day in brief ----------------------------------------------
    d.rectangle([0, 600, W, 626], fill=INK)
    fb2 = F_BOLD(16)
    d.text((24, 606), "THE DAY IN BRIEF  \u2014  45 MORE STORIES",
           font=fb2, fill=WHITE)
    f_item = F_REG(14)
    for col in range(3):
        x = 24 + col * (col_w + gap)
        for row in range(15):
            item = BRIEF[col * 15 + row]
            y = 634 + row * 22
            d.rectangle([x, y + 4, x + 7, y + 11], fill=RED)
            d.text((x + 12, y), item, font=f_item, fill=(32, 34, 40))

    # --- footer --------------------------------------------------------
    d.line([0, 972, W, 972], fill=INK, width=2)
    foot = "Every story above was reported on Wednesday 18 November 2026."
    ff = F_REG(16)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 982), foot, font=ff,
           fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT}: {img.size}, {size} bytes ({size / 1048576:.2f} MiB)")
    # sanity: story count
    print(f"stories: {len(LEADS)} leads + {len(BRIEF)} briefs = "
          f"{len(LEADS) + len(BRIEF)}; regions sum to {total}; "
          f"hotspots: {len(DOTS)}")


if __name__ == "__main__":
    main()
