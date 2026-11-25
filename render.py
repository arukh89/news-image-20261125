#!/usr/bin/env python3
"""Render the news-image-20261125 front page (1024x1024, PIL only).

Source of truth: the official make.fun edition
GET /api/news/editions/2026-11-25 (37 stories, 6 regions, provisional,
extracted 04:36 UTC), saved at edition-25nov.json. Every number, outlet
and framing below comes from that edition. Two wires in the edition
carry the same headline twice, so each is shown once: the England T20
report (#46/#48) and the Dell forecast (#47/#49). 35 stories are shown.
No flags are drawn anywhere. No network, no clock, no photos, no
randomness: two runs are byte-identical.
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
    ("1", "REPORTED", "Reuters",
     "Shenzhou-24 lifts off with Pakistan's first astronaut",
     "Long March 2F launches at 00:18 UTC. Zeeshan Ali, 40, a former "
     "Pakistan Air Force pilot, is the first foreign visitor to Tiangong. "
     "Crew of three to run about 90 experiments.",
     (100.29, 40.96)),
    ("2", "REPORTED", "Xinhua",
     "China probes Politburo member Chen Jining",
     "Shanghai party chief under investigation, the fourth of the "
     "24-member Politburo probed since 2025. First sitting Shanghai "
     "chief probed since 2006.",
     (116.4, 39.9)),
    ("3", "REPORTED", "Reuters",
     "Huawei guilty of stealing trade secrets",
     "US jury convicts on 10 of 12 counts, including bank fraud and "
     "evading Iran sanctions; acquitted of racketeering. Sentencing "
     "set for 14 September 2027; Huawei to appeal.",
     (-74.01, 40.71)),
]

CARDS = [
    ("4", "FORECAST", "Reuters",
     "Trump set to unveil new tariffs",
     "USTR to release Section 301 findings in coming days; duties on 16 "
     "partners over excess capacity.", ( -77.04, 38.9)),
    ("5", "REPORTED", "Reuters",
     "Nvidia bounce fades, shares slide 6%",
     "Relief rally over Huang's return fizzles; Nasdaq falls 1.5%.",
     (-121.95, 37.35)),
    ("6", "REPORTED", "Reuters",
     "CIA and spy agency hit by cyber breach",
     "Breach exposed some unclassified data; ODNI says no disruption to "
     "critical capabilities.", (-77.15, 38.95)),
    ("7", "REPORTED", "Al Jazeera",
     "Houthi drone hits Riyadh tower, 11 hurt",
     "Two Saudis, two Indians, three Nepalese and four Egyptians hurt; "
     "third strike on the financial district this month.", (46.68, 24.71)),
    ("8", "REPORTED", "BBC",
     "Israeli strike kills Hamas security chief",
     "Naeem Abu Nahel, 50, among seven killed in Gaza City; he held the "
     "post since September.", (34.47, 31.5)),
    ("9", "REPORTED", "AP",
     "Russian strike kills 2, wounds 48",
     "Glide bomb destroys a house and partly destroys a five-storey block "
     "in Zaporizhzhia.", (35.14, 47.84)),
    ("10", "REPORTED", "AP",
     "Gunmen hold hostages in Cartagena",
     "About 20 still held in a supermarket after a failed robbery; 10 "
     "freed; gunmen demand 7bn pesos.", (-75.51, 10.39)),
    ("11", "REPORTED", "BBC",
     "UK sanctions Myanmar generals",
     "Five officers hit with asset freezes and travel bans after the ICJ "
     "Rohingya genocide ruling.", (-0.13, 51.51)),
    ("12", "REPORTED", "Reuters",
     "Real Madrid rout PSV 5-1",
     "Mbappe scores twice, Vinicius adds one; Madrid top the league "
     "phase with 15 points.", (-3.7, 40.42)),
    ("13", "REPORTED", "Reuters",
     "Bucks end 13-game skid",
     "Tyler Herro scores 32 in a 116-111 win at Toronto; Myles Turner "
     "adds 27 and reaches 10,000 points.", (-87.91, 43.04)),
    ("14", "REPORTED", "AP",
     "Miss Universe crowns its 75th winner",
     "Jennifer Barreto of Puerto Rico takes the crown; the crown holds "
     "3,150 diamonds.", (-66.11, 18.47)),
    ("15", "REPORTED", "BBC",
     "Zimbabwean convicted over Ukraine fight",
     "Five-year suspended sentence and deportation; one of five arrested "
     "at OR Tambo on 8 November.", (28.05, -26.2)),
    ("16", "REPORTED", "BBC",
     "COP31 chief blames EU for failure",
     "Longer-term climate talks end without a deal; the COP31 chief "
     "blames the EU.", (30.71, 36.89)),
]

BRIEFS = [
    ("17", "Berlin", "German business morale rises, Ifo index 90.6 in November."),
    ("20", "New York", "S&P 500 seen gaining another 10% in 2027, poll finds."),
    ("22", "Caracas", "Venezuela reports $27.5bn debt ahead of talks."),
    ("23", "London", "UK first secretary vows to fight court order on emails."),
    ("25", "Brussels", "EU proposes 22nd Russia sanctions package, 60 banks hit."),
    ("26", "Kyiv", "Ukraine shares video of its strike on Russian ship off Libya."),
    ("27", "Kyiv", "Ukraine's 20-point peace plan will be put to a vote."),
    ("28", "Damascus", "Landmine casualties soar in Syria two years after war."),
    ("31", "Gaza", "15 killed since 'pause' as strikes hit aid sites."),
    ("32", "New York", "Gold sells for $3,344 ahead of US inflation data."),
    ("36", "London", "Two arrested over suspected burglary at Sandringham."),
    ("37", "London", "UK firms aiding Ukraine warned to brace for sabotage."),
    ("39", "Istanbul", "Galatasaray edge Aston Villa 3-0 in Champions League."),
    ("40", "Indianapolis", "Pacers beat champions Thunder 125-120."),
    ("41", "Houston", "Durant scores 32 as Rockets beat Clippers 116-104."),
    ("44", "Minneapolis", "Timberwolves rout Nets 142-116."),
    ("46", "Australia", "England level T20 series with eight-wicket win."),
    ("47", "New York", "Dell's first forecast after record quarter on AI servers."),
    ("50", "New Delhi", "BJP and Akali Dal unite for 2027 Punjab elections."),
]

NUMBERS = [
    ("90", "experiments on Shenzhou-24"),
    ("10 of 12", "counts Huawei convicted on"),
    ("16", "partners face new US tariffs"),
    ("11", "hurt in Riyadh drone hit"),
    ("2 / 48", "killed / wounded in Zaporizhzhia"),
    ("5-1", "Real Madrid rout PSV"),
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
    t3 = "35 STORIES  -  6 CONTINENTS  -  ONE FRONT PAGE"
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
NUDGE = {"6": (-16, 14), "8": (-16, 10), "12": (-14, 8), "16": (16, 12)}
PINNED = LEADS + CARDS


def draw_map(draw, y):
    f = font(SANS_B, 9)
    draw.text((16, y), "THE WORLD AT A GLANCE  -  16 STORIES PINNED, NUMBERED AS IN THE TEXT",
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
    rows = 7
    row_h = (y1 - top) // rows
    fh = font(SANS_B, 11)
    fd = font(SANS, 9)
    left = CARDS[:7]
    right = CARDS[7:]
    for ci, cards in enumerate((left, right)):
        x = 16 + ci * (col_w + 12)
        for ri, (num, label, outlet, head, deck, _geo) in enumerate(cards):
            cy = top + ri * row_h
            chip(draw, x, cy, num + "  " + label, outlet)
            hy = cy + 17
            hy = draw_wrapped(draw, x, hy, head, fh, col_w, fill=INK,
                              leading=1, max_lines=1)
            draw_wrapped(draw, x, hy + 1, deck, fd, col_w, fill=INK,
                         leading=1, max_lines=2)
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
        by += 4
    return y1


def draw_datecheck(draw, y):
    draw.line([16, y, W - 16, y], fill=RULE, width=1)
    f = font(SANS_B, 10)
    draw.text((16, y + 6), "DATE CHECK", font=f, fill=RED)
    f2 = font(SANS, 9)
    t = ("Every story above is dated to Wednesday 25 November 2026 in the "
         "official make.fun edition for that day (provisional, verified "
         "04:36 UTC). Two wires that repeat one headline each - the England "
         "T20 report and the Dell forecast - appear once. Sources: Reuters, "
         "BBC, AP, Xinhua, Al Jazeera.")
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
