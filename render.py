#!/usr/bin/env python3
"""Render the news-image-20261125 front page (1024x1024, PIL only).

Source of truth: the official make.fun edition
GET /api/news/editions/2026-11-25 as re-fetched on 26 Nov (39 stories,
7 regions, provisional, updated 23:20 UTC), saved at
edition-25nov-r2.json. Every number, place and framing below comes
from that edition. Two extraction fragments carry no complete
headline (a repeated Man United fragment and a truncated OPCW line),
so they are omitted: 37 stories are shown. No flags are drawn
anywhere. No network, no clock, no photos, no randomness: two runs
are byte-identical.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (178, 34, 34)
NAVY = (31, 58, 95)
TAN = (216, 201, 163)
OCEAN = (226, 235, 241)
LAND = (176, 160, 118)
LIGHT = (238, 232, 214)
GREEN = (30, 122, 52)
AMBER = (178, 106, 0)
BLUE = (31, 95, 168)
GREY = (90, 90, 90)
RULE = (26, 26, 26)


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=3,
                 max_lines=None):
    """Draw wrapped text; returns y just below the last line."""
    lines = wrap(draw, text, fnt, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def chip(draw, x, y, label, outlet):
    """Small [N . LABEL] chip + outlet; returns x just after the chip."""
    f = font(SANS_B, 9)
    tw = draw.textlength(label, font=f)
    draw.rectangle([x, y, x + tw + 10, y + 14], fill=RED)
    draw.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    f2 = font(SANS, 9)
    draw.text((x + tw + 16, y + 2), outlet, font=f2, fill=GREY)
    return x + tw + 16


# ---- World map: coarse continent polygons (lon, lat) ----
NORTH_AMERICA = [
    (-168, 66), (-165, 60), (-158, 58), (-152, 60), (-140, 60),
    (-135, 58), (-130, 54), (-125, 49), (-124, 42), (-120, 34),
    (-114, 29), (-110, 24), (-105, 20), (-97, 16), (-94, 17),
    (-90, 14), (-86, 12), (-83, 9), (-79, 9), (-81, 13), (-84, 16),
    (-87, 21), (-90, 21), (-91, 19), (-96, 19), (-97, 26), (-93, 30),
    (-89, 30), (-84, 30), (-81, 25), (-80, 32), (-76, 35), (-74, 40),
    (-70, 42), (-68, 44), (-65, 44), (-60, 47), (-55, 47), (-60, 50),
    (-64, 58), (-68, 58), (-72, 62), (-78, 62), (-85, 66), (-92, 66),
    (-95, 69), (-110, 68), (-125, 70), (-140, 70), (-155, 71),
    (-165, 68),
]
GREENLAND = [
    (-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68), (-25, 70),
    (-20, 74), (-25, 78), (-40, 80), (-58, 76), (-60, 74), (-58, 70),
]
SOUTH_AMERICA = [
    (-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
    (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-70, -50),
    (-68, -55), (-66, -55), (-65, -45), (-62, -40), (-57, -38),
    (-52, -33), (-48, -28), (-41, -23), (-40, -20), (-35, -9),
    (-35, -6), (-40, -3), (-44, -2), (-50, 0), (-53, 4), (-58, 6),
    (-62, 9), (-68, 11), (-72, 12), (-75, 10),
]
AFRICA = [
    (-17, 15), (-17, 21), (-15, 27), (-10, 31), (-6, 34), (0, 36),
    (10, 37), (11, 34), (20, 32), (30, 31), (32, 31), (35, 28),
    (37, 22), (39, 18), (43, 12), (48, 11), (51, 12), (46, 5),
    (42, 0), (40, -5), (40, -10), (38, -15), (35, -20), (32, -26),
    (28, -32), (20, -35), (17, -32), (15, -27), (12, -18), (13, -12),
    (12, -6), (9, 4), (6, 4), (-8, 5), (-13, 8), (-17, 12),
]
EURASIA = [
    (-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 50),
    (0, 51), (3, 53), (8, 54), (8, 57), (10, 59), (5, 60), (5, 62),
    (12, 65), (18, 69), (25, 71), (32, 70), (40, 68), (50, 69),
    (60, 69), (68, 72), (75, 72), (85, 73), (95, 76), (105, 77),
    (113, 74), (125, 72), (135, 72), (145, 72), (155, 70), (162, 66),
    (170, 66), (178, 65), (170, 60), (162, 60), (158, 56), (156, 51),
    (150, 60), (142, 59), (140, 55), (138, 50), (135, 43), (130, 42),
    (127, 40), (122, 38), (120, 34), (122, 30), (118, 25), (110, 21),
    (108, 18), (105, 10), (103, 8), (100, 7), (98, 10), (97, 16),
    (94, 17), (92, 21), (89, 22), (86, 20), (80, 16), (77, 8),
    (75, 12), (72, 20), (68, 23), (66, 25), (61, 25), (58, 26),
    (54, 27), (52, 28), (50, 29), (48, 30), (44, 29), (43, 27),
    (40, 27), (39, 21), (38, 18), (35, 15), (32, 15), (30, 18),
    (28, 20), (25, 22), (22, 25), (20, 28), (18, 30), (15, 32),
    (12, 34), (10, 37), (5, 37), (0, 36), (-5, 36), (-9, 37),
]
AUSTRALIA = [
    (113, -22), (114, -30), (115, -35), (118, -35), (124, -33),
    (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
    (145, -38), (150, -37), (153, -32), (153, -27), (150, -22),
    (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
    (132, -12), (130, -13), (126, -14), (122, -17), (117, -20),
]
ISLANDS = [( -2, 54), (139, 37), (113, -2), (172, -41)]  # UK, Japan, Borneo, NZ
CONTINENTS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, AFRICA,
              EURASIA, AUSTRALIA]


def inside_poly(lon, lat, poly):
    """Ray-casting point-in-polygon on lon/lat."""
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > lat) != (yj > lat):
            xint = (xj - xi) * (lat - yi) / (yj - yi) + xi
            if lon < xint:
                inside = not inside
        j = i
    return inside


def on_land(lon, lat):
    for poly in CONTINENTS:
        if inside_poly(lon, lat, poly):
            return True
    for (ilon, ilat) in ISLANDS:
        if abs(lon - ilon) < 3.5 and abs(lat - ilat) < 2.5:
            return True
    return False

# ---- Content: all from the official 25 Nov edition ----
LEADS = [
    ("1", "TRADE", "Washington",
     "US proposes tariffs of up to 20% on EU, China and 12 more",
     "Duties proposed on 14 economies over excess capacity. Vietnam "
     "faces 20%; Cambodia and Indonesia 18%. The EU and Beijing "
     "reject the premise.",
     (-77.0369, 38.9072)),
    ("2", "MARKETS", "Seoul",
     "AI doubts sink Asian chip stocks: Kospi closes -6.2%",
     "Kospi ends at 4,697.51; SK hynix falls 11.1% and Samsung 9.9%. "
     "Taiwan's Taiex drops 4.8% and Japan's Nikkei 2.8%.",
     (126.978, 37.5665)),
    ("3", "SPACE", "Jiuquan",
     "Pakistan's first astronaut docks at China's space station",
     "Muhammad Zeeshan Ali, 40, reaches Tiangong on Shenzhou-24, the "
     "first foreign astronaut there. He stays 5 to 10 days.",
     (98.4941, 39.7326)),
]

CARDS = [
    ("4", "WAR", "Ukraine",
     "Russian strikes kill 5, cut power in 5 regions",
     "Zaporizhzhia nuclear plant runs on diesel after its 17th grid "
     "loss this year.", (30.5234, 50.4501)),
    ("5", "WAR", "Ras Tanura",
     "Saudis down Houthi drones after Hodeidah strike",
     "Coalition says four drones were destroyed over Ras Tanura; no "
     "casualties reported.", (50.1595, 26.6406)),
    ("6", "ECONOMY", "London",
     "UK energy price cap to rise 26% in January",
     "Ofgem puts a typical annual bill at £2,166 from 1 January, up "
     "from £1,723.", (-0.1278, 51.5074)),
    ("7", "DIPLOMACY", "Canberra",
     "Solomon Islands signs security pact with Australia",
     "Australia becomes a security partner, with A$740m pledged over "
     "10 years.", (149.13, -35.2809)),
    ("8", "LABOUR", "Dhaka",
     "Garment workers offered higher minimum wage",
     "Offer lifts the monthly wage from 12,500 to 17,500 taka "
     "($100 to $136).", (90.4125, 23.8103)),
    ("9", "DISASTER", "Bogor",
     "9 dead, 17 still trapped in flooded gold mine",
     "Rescuers pull bodies from a 100-metre unlicensed pit in West "
     "Java.", (106.8166, -6.595)),
    ("10", "WAR", "Gaza City",
     "Israeli strike kills Hamas security chief",
     "Naeem Abu Nahel, 50, killed in western Gaza City; he had held "
     "the post since September.", (34.4668, 31.5017)),
    ("11", "JUSTICE", "Cape Town",
     "Court lifts 'Farmgate' threat to Ramaphosa",
     "Judges void the 2022 panel report that opened the way to "
     "impeachment.", (18.4241, -33.9249)),
    ("12", "JUSTICE", "Jerusalem",
     "Judges urge rethink of Netanyahu graft charges",
     "Bribery case faces 'considerable difficulties'; Netanyahu says "
     "the trial must end.", (35.2137, 31.7683)),
    ("13", "DISASTER", "Cairo",
     "Fuel tanker fire kills at least 30 near Cairo",
     "Tanker overturned and exploded on a ring road, the Health "
     "Ministry says.", (31.2357, 30.0444)),
]

BRIEFS = [
    ("14", "Pyongyang", "North Korea gives Swiss envoy 48 hours to leave."),
    ("15", "Brussels", "EU proposes a €500bn fund on quantum tech."),
    ("18", "London", "UK warns companies of Russian sabotage threat."),
    ("19", "Kyiv", "Ukraine seeks €115bn in aid for 2027, Zelensky says."),
    ("21", "Paris", "Five arrested in case of stolen 10th-century relic."),
    ("22", "Luxembourg", "EU court orders new cage-free farming timeline."),
    ("23", "Jerusalem", "Knesset advances bill for a 7 October inquiry."),
    ("24", "Gaza", "Amnesty urges ICC genocide probe over deaths."),
    ("25", "Darfur", "RSF drone attack kills at least 19 in Sudan."),
    ("27", "Kuala Lumpur", "Malaysia sues Google over YouTube content."),
    ("28", "Sydney", "Australia's inflation jumps to 4.9% in October."),
    ("29", "Sydney", "Ex-policeman guilty of murdering Baird and Davies."),
    ("31", "Lagos", "Nigeria's navy rescues 17 from capsized boat."),
    ("32", "Brasília", "US also proposes 10% tariff on Embraer jets."),
    ("34", "Washington", "FCC clears SpaceX's 1 million orbital data centers."),
    ("36", "Iowa", "US Army blows up 10,000 lb of lead azide."),
    ("37", "Mississippi", "Divers recover 6 bodies after plane crash off coast."),
    ("38", "London", "Poundland collapses, putting 11,000 jobs at risk."),
    ("39", "Karachi", "Building collapse kills at least 3, injures 14."),
    ("41", "Harare", "Court issues arrest warrant for Mugabe's son."),
    ("43", "Space", "ESA's Hera finds stadium-sized crater left by DART."),
    ("44", "Lisbon", "Champions League: Sporting 2-2 Man United."),
    ("47", "Mexico City", "Mexico protests US refusal to extradite ex-TV host."),
    ("49", "UN", "16 days of action against violence on women begin."),
]

NUMBERS = [
    ("20%", "top proposed US tariff rate"),
    ("-6.2%", "Kospi close on AI doubts"),
    ("5-10", "days on Tiangong for Zeeshan Ali"),
    ("5", "killed, power cut in 5 regions"),
    ("30+", "killed in Cairo tanker fire"),
    ("26%", "UK energy cap rise in January"),
]


def draw_masthead(draw):
    draw.rectangle([0, 0, W, 5], fill=RULE)
    draw.rectangle([0, 7, W, 9], fill=RED)
    f = font(SERIF_B, 56)
    t = "THE WORLD"
    tw = draw.textlength(t, font=f)
    draw.text(((W - tw) / 2, 12), t, font=f, fill=INK)
    f2 = font(SERIF_B, 25)
    t2 = "WEDNESDAY, 25 NOVEMBER 2026"
    tw2 = draw.textlength(t2, font=f2)
    draw.text(((W - tw2) / 2, 76), t2, font=f2, fill=RED)
    f3 = font(SANS_B, 10)
    t3 = "37 STORIES  -  7 REGIONS  -  ONE FRONT PAGE"
    tw3 = draw.textlength(t3, font=f3)
    draw.text(((W - tw3) / 2, 106), t3, font=f3, fill=NAVY)
    draw.line([16, 122, W - 16, 122], fill=RULE, width=1)


def draw_numbers(draw):
    y = 128
    f = font(SANS_B, 9)
    draw.text((16, y), "THE DAY IN NUMBERS", font=f, fill=GREY)
    y += 16
    box_w = (W - 32 - 5 * 8) / 6
    for i, (num, label) in enumerate(NUMBERS):
        x = 16 + i * (box_w + 8)
        draw.rectangle([x, y, x + box_w, y + 40], outline=TAN, width=1)
        fn = font(SANS_B, 15)
        fl = font(SANS, 8)
        ntw = draw.textlength(num, font=fn)
        draw.text((x + (box_w - ntw) / 2, y + 2), num, font=fn, fill=NAVY)
        lines = wrap(draw, label, fl, box_w - 8)
        ly = y + 20
        for line in lines[:2]:
            ltw = draw.textlength(line, font=fl)
            draw.text((x + (box_w - ltw) / 2, ly), line, font=fl, fill=GREY)
            ly += 10
    draw.line([16, y + 46, W - 16, y + 46], fill=RULE, width=1)
    return y + 52


def draw_leads(draw, y):
    col_w = (W - 32 - 2 * 12) / 3
    fh = font(SERIF_B, 16)
    fd = font(SANS, 11)
    top = y
    for i, (num, label, outlet, head, deck, _geo) in enumerate(LEADS):
        x = 16 + i * (col_w + 12)
        chip(draw, x, y, num + "  " + label, outlet)
        hy = y + 20
        hy = draw_wrapped(draw, x, hy, head, fh, col_w, fill=INK,
                          leading=2, max_lines=3)
        draw_wrapped(draw, x, hy + 2, deck, fd, col_w, fill=INK,
                     leading=2, max_lines=4)
        if i < 2:
            draw.line([x + col_w + 6, top, x + col_w + 6, top + 148],
                      fill=TAN, width=1)
    return top + 154

# Pins that would collide are nudged, with a leader line to the true spot.
NUDGE = {"12": (16, -10), "13": (-16, 10)}
PINNED = LEADS + CARDS


def draw_map(draw, y):
    f = font(SANS_B, 9)
    draw.text((16, y), "THE WORLD AT A GLANCE  -  13 STORIES PINNED, NUMBERED AS IN THE TEXT",
              font=f, fill=GREY)
    top = y + 16
    mx0, my0, mx1, my1 = 16, top, W - 16, top + 152
    draw.rectangle([mx0, my0, mx1, my1], fill=OCEAN)
    draw.rectangle([mx0, my0, mx1, my1], outline=TAN, width=1)

    def px(lon):
        return mx0 + (lon + 180.0) / 360.0 * (mx1 - mx0)

    def py(lat):
        return my0 + (83.0 - lat) / 141.0 * (my1 - my0)

    step = 6
    gx, gy = mx0 + 3, my0 + 3
    while gy < my1 - 2:
        gx = mx0 + 3
        while gx < mx1 - 2:
            lon = (gx - mx0) / (mx1 - mx0) * 360.0 - 180.0
            lat = 83.0 - (gy - my0) / (my1 - my0) * 141.0
            if on_land(lon, lat):
                draw.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=LAND)
            gx += step
        gy += 5
    for (num, _label, _outlet, _head, _deck, geo) in PINNED:
        lon, lat = geo
        x, y = px(lon), py(lat)
        dx, dy = NUDGE.get(num, (0, 0))
        nx, ny = x + dx, y + dy
        if (dx, dy) != (0, 0):
            draw.line([x, y, nx, ny], fill=RED, width=1)
        draw.ellipse([nx - 7, ny - 7, nx + 7, ny + 7], fill=RED,
                     outline=(255, 255, 255), width=1)
        fn = font(SANS_B, 8 if len(num) < 2 else 7)
        tw = draw.textlength(num, font=fn)
        draw.text((nx - tw / 2, ny - 5), num, font=fn, fill=(255, 255, 255))
    return my1


def draw_cards_briefs(draw, y0, y1):
    f = font(SANS_B, 9)
    draw.text((16, y0), "MORE OF THE DAY", font=f, fill=GREY)
    draw.text((684, y0), "ALSO TODAY", font=f, fill=GREY)
    draw.line([16, y0 + 13, W - 16, y0 + 13], fill=TAN, width=1)
    draw.line([676, y0 + 18, 676, y1], fill=TAN, width=1)
    top = y0 + 20
    col_w = 320
    rows = 5
    row_h = (y1 - top) // rows
    fh = font(SANS_B, 11)
    fd = font(SANS, 9)
    left = CARDS[:5]
    right = CARDS[5:]
    for ci, cards in enumerate((left, right)):
        x = 16 + ci * (col_w + 12)
        for ri, (num, label, outlet, head, deck, _geo) in enumerate(cards):
            cy = top + ri * row_h
            chip(draw, x, cy, num + "  " + label, outlet)
            hy = cy + 17
            hy = draw_wrapped(draw, x, hy, head, fh, col_w, fill=INK,
                              leading=1, max_lines=1)
            draw_wrapped(draw, x, hy + 1, deck, fd, col_w, fill=INK,
                         leading=1, max_lines=3)
            if ri < len(cards) - 1:
                draw.line([x, cy + row_h - 6, x + col_w, cy + row_h - 6],
                          fill=LIGHT, width=1)
    fb = font(SANS, 9)
    fbp = font(SANS_B, 9)
    by = top
    for (num, place, text) in BRIEFS:
        pref = num + " " + place + ": "
        pw = draw.textlength(pref, font=fbp)
        draw.text((684, by), pref, font=fbp, fill=NAVY)
        by = draw_wrapped(draw, 684 + pw, by, text, fb, 324 - pw,
                          fill=INK, leading=1, max_lines=2)
        by += 2
    return y1


def draw_datecheck(draw, y):
    draw.line([16, y, W - 16, y], fill=RULE, width=1)
    f = font(SANS_B, 10)
    draw.text((16, y + 6), "DATE CHECK", font=f, fill=RED)
    f2 = font(SANS, 9)
    t = ("Every story above is dated to Wednesday 25 November 2026 in the "
         "official make.fun edition for that day (provisional, updated "
         "23:20 UTC). Two extraction fragments with no complete headline "
         "are omitted; every other story in the edition is shown.")
    draw_wrapped(draw, 16, y + 20, t, f2, W - 32, fill=INK, leading=2,
                 max_lines=2)
    draw.line([16, H - 8, W - 16, H - 8], fill=RULE, width=1)
    return H - 8


def render():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    y = draw_numbers(draw)
    y = draw_leads(draw, y + 6)
    y = draw_map(draw, y + 8)
    y = draw_cards_briefs(draw, y + 8, 942)
    bottom = draw_datecheck(draw, 950)
    print("sections: numbers/leads/map/cards end, datecheck bottom =", bottom)
    img.save(OUT, format="PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    render()
