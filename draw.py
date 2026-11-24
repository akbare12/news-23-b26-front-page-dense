#!/usr/bin/env python3
"""news-23 b26 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (250, 247, 238)
INK = (20, 20, 20)
RED = (178, 34, 34)
NAVY = (16, 32, 64)
TEAL = (0, 122, 110)
GOLD = (198, 145, 30)
GREY = (90, 90, 90)

FD = "/usr/share/fonts/truetype/dejavu/"
FL = "/usr/share/fonts/truetype/liberation/"


def fb(sz):
    return ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", sz)


def fr(sz):
    return ImageFont.truetype(FD + "DejaVuSans.ttf", sz)


def serif_b(sz):
    return ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", sz)


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, font, max_w, max_lines):
    """Wrap text, shrinking font until it fits max_lines x max_w. Returns (lines, font)."""
    f = font
    while True:
        lines = wrap(draw, text, f, max_w)
        if len(lines) <= max_lines:
            return lines, f
        sz = f.size - 1
        if sz < 7:
            return lines[:max_lines], f
        f = ImageFont.truetype(f.path, sz) if hasattr(f, "path") else fb(sz)


def chip(draw, x, y, label, kind):
    """Draw REPORTED (navy) / CLAIM (red) chip; returns right edge."""
    f = fb(8)
    w = int(draw.textlength(label, font=f)) + 10
    col = NAVY if kind == "REPORTED" else RED
    draw.rounded_rectangle([x, y, x + w, y + 13], radius=3, fill=col)
    draw.text((x + 5, y + 2), label, font=f, fill="white")
    return x + w


def draw():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 62], fill=(12, 12, 12))
    d.text((16, 6), "THE WORLD TODAY", font=serif_b(44), fill="white")
    d.text((W - 16 - d.textlength("MONDAY  23 NOVEMBER 2026", font=fb(20)),
            22), "MONDAY  23 NOVEMBER 2026", font=fb(20), fill=(212, 175, 55))

    # ---------- kicker ----------
    d.text((16, 68), "AI rout hits Asia  ·  UN chief urges AI rules  ·  US lead over China at record low  ·  Anthropic IPO $107.3B",
           font=fb(13), fill=RED)

    # ---------- number strip (2 rows x 5) ----------
    nums = [
        ("-3.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", NAVY),
        ("11,762", "EBOLA CASES, DRC", (90, 90, 20)), ("10T won", "SEOUL STABILISATION FUND", (120, 70, 10)),
        ("2%", "BILLIONAIRE TAX IN PARIS", (0, 110, 60)),
        ("$450M", "SKUBAL DEAL", (140, 40, 140)), ("165", "RUSSIAN MISSILES IN A WEEK", RED),
        ("12,000", "CLEARED IN MANCHESTER", (30, 90, 160)), ("264 kg", "EXPLOSIVES SEIZED IN LEBANON", (120, 70, 10)),
        ("$107.3B", "ANTHROPIC IPO — LARGEST EVER", (150, 30, 150)),
    ]
    cw = (W - 32) // 5
    for i, (num, lab, col) in enumerate(nums):
        r, c = divmod(i, 5)
        x = 16 + c * cw
        y = 88 + r * 36
        d.text((x, y), num, font=fb(25), fill=col)
        d.text((x, y + 27), lab, font=fb(8), fill=INK)
    d.line([16, 160, W - 16, 160], fill=(180, 180, 170), width=1)

    # ---------- region bar ----------
    regions = [("ASIA-PACIFIC 7", (0, 122, 110)), ("AMERICAS 8", NAVY), ("MIDDLE EAST 6", (150, 110, 20)),
               ("EUROPE 5", (90, 60, 140)), ("AFRICA 3", (150, 90, 30)), ("WORLD 2", (110, 110, 110))]
    rw = (W - 32) // 6
    for i, (lab, col) in enumerate(regions):
        x = 16 + i * rw
        d.rectangle([x, 164, x + rw - 2, 182], fill=col)
        tw = d.textlength(lab, font=fb(10))
        d.text((x + (rw - 2 - tw) / 2, 168), lab, font=fb(10), fill="white")

    # ---------- UTC strip ----------
    d.rectangle([16, 186, W - 16, 200], fill=NAVY)
    d.text((20, 189), "THE DAY IN UTC", font=fb(9), fill=(212, 175, 55))
    d.text((130, 189), "~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles   ~18:00 Anthropic $97.17",
           font=fr(9), fill="white")
    d.text((W - 76, 189), "~ APPROX", font=fr(9), fill=(200, 200, 200))

    # ---------- heroes ----------
    heroes = [
        dict(kind="chart", num="1", head="AI ROUT HITS ASIA",
             body="Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5.",
             src="KOREA EXCHANGE"),
        dict(kind="globe", num="2", head="GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
             body="UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
             src="UNITED NATIONS"),
        dict(kind="bars", num="3", head="US LEAD OVER CHINA AT RECORD LOW",
             body="Asia Power Index 2026: US 78.9, China 73.6 — gap 5.3, narrowest since 2018. India third at 40.5.",
             src="LOWY INSTITUTE"),
    ]
    hw = 320
    hx0 = 16
    hy = 206
    scene_h = 108
    for i, h in enumerate(heroes):
        x = hx0 + i * (hw + 8)
        # scene
        if h["kind"] == "chart":
            d.rectangle([x, hy, x + hw, hy + scene_h], fill=(10, 24, 54))
            # skyline
            import random
            random.seed(7)
            bx = x + 8
            while bx < x + hw - 12:
                bw = random.randint(10, 22)
                bh = random.randint(18, 52)
                d.rectangle([bx, hy + scene_h - 26 - bh, bx + bw, hy + scene_h - 26], fill=(30, 60, 110))
                for wy in range(hy + scene_h - 26 - bh + 4, hy + scene_h - 28, 8):
                    for wx in range(bx + 3, bx + bw - 2, 6):
                        d.rectangle([wx, wy, wx + 2, wy + 2], fill=(255, 220, 100))
                bx += bw + 4
            # falling line — starts below the big "-3.3%" text so no dot lands on it
            pts = [(x + 10 + j * 34, hy + 32 + j * 6 + (4 if j % 2 else -3)) for j in range(10)]
            d.line(pts, fill=(230, 60, 50), width=3)
            for px, py in pts:
                d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 200, 80))
            d.text((x + 8, hy + 2), "-3.3%", font=fb(26), fill=(230, 60, 50))
            d.rectangle([x, hy + scene_h - 22, x + hw, hy + scene_h], fill=(8, 8, 8))
            d.text((x + 8, hy + scene_h - 20), "KOSPI  4,708.54   ·   -161 PTS", font=fb(11), fill="white")
        elif h["kind"] == "globe":
            d.rectangle([x, hy, x + hw, hy + scene_h], fill=(0, 110, 96))
            d.text((x + 8, hy + 4), "150 DELEGATES", font=fb(26), fill=(255, 215, 60))
            d.text((x + 8, hy + 34), "BACK A RISK", font=fb(20), fill="white")
            d.text((x + 8, hy + 58), "FRAMEWORK", font=fb(20), fill="white")
            # globe bottom-right, small so it never covers text
            cx, cy, r = x + hw - 42, hy + scene_h - 34, 24
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(190, 235, 225))
            d.ellipse([cx - 12, cy - 8, cx - 2, cy + 2], fill=(90, 180, 120))
            d.ellipse([cx + 2, cy + 4, cx + 12, cy + 14], fill=(90, 180, 120))
            # flags
            for j, col in enumerate([(200, 40, 40), (40, 60, 200), (220, 180, 40)]):
                fx = x + 10 + j * 34
                d.line([fx, hy + 82, fx, hy + 104], fill="white", width=2)
                d.polygon([(fx, hy + 82), (fx + 22, hy + 88), (fx, hy + 94)], fill=col)
            d.rectangle([x, hy + scene_h - 22, x + hw, hy + scene_h], fill=(8, 8, 8))
            d.text((x + 8, hy + scene_h - 20), "UN  ·  BRIDGETOWN", font=fb(11), fill="white")
        else:
            d.rectangle([x, hy, x + hw, hy + scene_h], fill=(245, 244, 238))
            d.rectangle([x, hy, x + hw, hy + 20], fill=(245, 244, 238))
            d.text((x + 8, hy + 2), "NARROWEST SINCE 2018", font=fb(11), fill=INK)
            d.text((x + hw - 62, hy + 2), "GAP 5.3", font=fb(11), fill=GOLD)
            bars = [("US", 78.9, NAVY), ("CHINA", 73.6, RED), ("INDIA", 40.5, GOLD)]
            bw = 52
            for j, (lab, val, col) in enumerate(bars):
                bx = x + 30 + j * 96
                bh = int(val * 0.62)
                d.rectangle([bx, hy + 84 - bh, bx + bw, hy + 84], fill=col)
                d.text((bx + 8, hy + 84 - bh + 4), f"{val}", font=fb(11), fill="white")
                d.text((bx + 8, hy + 88), lab, font=fb(10), fill=INK)
            d.rectangle([x, hy + scene_h - 22, x + hw, hy + scene_h], fill=(8, 8, 8))
            d.text((x + 8, hy + scene_h - 20), "ASIA POWER INDEX 2026", font=fb(11), fill="white")
        # headline + body + source
        ty = hy + scene_h + 8
        lines, f = fit(d, h["head"], fb(15), hw - 24, 2)
        for j, ln in enumerate(lines):
            d.text((x + 24, ty + j * 17), ln, font=f, fill=INK)
        # number badge
        d.ellipse([x, ty, x + 18, ty + 18], fill=RED)
        d.text((x + 6, ty + 3), h["num"], font=fb(11), fill="white")
        by = ty + len(lines) * 17 + 4
        blines, bf = fit(d, h["body"], fr(9), hw - 4, 2)
        for j, ln in enumerate(blines):
            d.text((x, by + j * 12), ln, font=bf, fill=(40, 40, 40))
        sy = by + len(blines) * 12 + 4
        d.text((x, sy + 1), h["src"], font=fr(8), fill=GREY)
        chip(d, x + hw - 62, sy, "REPORTED", "REPORTED")

    # ---------- more of the day ----------
    my = 448
    d.rectangle([16, my, W - 16, my + 2], fill=INK)
    d.text((16, my + 6), "MORE OF THE DAY  —  10 STORIES", font=fb(13), fill=INK)

    cards = [
        ("AMERICAS", "4", "BESSENT: NVIDIA ANSWERS", "Treasury chief wants China answers.", "Reuters", "REPORTED"),
        ("FBI", "5", "FBI PROBES NCIC HACK", "Hackers hit police NCIC database.", "AP", "REPORTED"),
        ("WHITE HOUSE", "6", "TRUMP: IRAN STRIKES MAY RESUME", "Strikes could resume in the New Year.", "Reuters", "REPORTED"),
        ("MARKETS", "7", "US FUTURES JUMP 3%", "Holiday rally lifts Nasdaq futures 3%.", "Bloomberg", "REPORTED"),
        ("SPORT", "8", "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever for a pitcher.", "AP", "REPORTED"),
        ("SPORT", "9", "TOM JACKSON DIES AT 75", "Broncos LB turned ESPN voice dies.", "ESPN", "REPORTED"),
        ("LEGAL", "10", "STATES SUE SPACEX", "Ten states challenge AI safety claims.", "AP", "REPORTED"),
        ("TECH", "11", "ANTHROPIC IPO: $107.3B", "Raises at $83; debut closes $97.17.", "WSJ", "REPORTED"),
        ("EUROPE", "12", "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: three Kh-101s crossed airspace.", "AP", "CLAIM"),
        ("SPACE", "13", "RUSSIAN NUCLEAR SATELLITE", "Intel: satellite built to carry a nuke.", "Reuters", "CLAIM"),
    ]
    tagcols = {"AMERICAS": RED, "FBI": (120, 60, 160), "WHITE HOUSE": (150, 110, 20),
               "MARKETS": TEAL, "SPORT": (0, 130, 60), "LEGAL": (120, 60, 160),
               "TECH": (150, 30, 150), "EUROPE": RED, "SPACE": (90, 90, 90)}
    cw2 = 198
    ch2 = 80
    for i, (tag, num, head, body, src, kind) in enumerate(cards):
        r, c = divmod(i, 5)
        x = 16 + c * (cw2 + 2)
        y = 474 + r * (ch2 + 4)
        d.rectangle([x, y, x + cw2, y + ch2], outline=(190, 185, 175), width=1, fill=(255, 255, 255))
        d.rectangle([x, y, x + cw2, y + 14], fill=tagcols[tag])
        d.text((x + 5, y + 2), tag, font=fb(8), fill="white")
        d.text((x + cw2 - 16, y + 2), num, font=fb(9), fill="white")
        hlines, hf = fit(d, head, fb(10), cw2 - 10, 2)
        for j, ln in enumerate(hlines):
            d.text((x + 5, y + 17 + j * 12), ln, font=hf, fill=INK)
        blines, bf = fit(d, body, fr(8), cw2 - 10, 1)
        by = y + 17 + len(hlines) * 12 + 1
        for ln in blines:
            d.text((x + 5, by), ln, font=bf, fill=(50, 50, 50))
        sy = y + ch2 - 15
        d.text((x + 5, sy + 1), src, font=fr(8), fill=GREY)
        chip(d, x + cw2 - 62, sy, kind, kind)

    # ---------- map + ALSO ----------
    my2 = 646
    d.rectangle([16, my2, W - 16, my2 + 2], fill=INK)
    d.text((16, my2 + 6), "WHERE IT HAPPENED", font=fb(13), fill=INK)
    d.text((500, my2 + 6), "ALSO ON MONDAY", font=fb(13), fill=INK)

    mapx, mapy, mapw, maph = 16, 670, 464, 186
    d.rectangle([mapx, mapy, mapx + mapw, mapy + maph], fill=(214, 230, 240))
    for gx in range(mapx, mapx + mapw, 16):
        d.line([gx, mapy, gx, mapy + maph], fill=(190, 205, 215), width=1)
    for gy in range(mapy, mapy + maph, 16):
        d.line([mapx, gy, mapx + mapw, gy], fill=(190, 205, 215), width=1)
    # stylised continents (rough blobs)
    land = (165, 200, 140)
    d.polygon([(mapx + 20, mapy + 30), (mapx + 110, mapy + 8), (mapx + 170, mapy + 22),
               (mapx + 150, mapy + 70), (mapx + 90, mapy + 88), (mapx + 30, mapy + 70)], fill=land)  # N America
    d.polygon([(mapx + 120, mapy + 100), (mapx + 160, mapy + 92), (mapx + 175, mapy + 130),
               (mapx + 150, mapy + 165), (mapx + 125, mapy + 140)], fill=land)  # S America
    d.polygon([(mapx + 215, mapy + 20), (mapx + 280, mapy + 10), (mapx + 300, mapy + 40),
               (mapx + 270, mapy + 70), (mapx + 225, mapy + 60)], fill=land)  # Europe
    d.polygon([(mapx + 285, mapy + 78), (mapx + 330, mapy + 70), (mapx + 345, mapy + 120),
               (mapx + 320, mapy + 160), (mapx + 295, mapy + 130)], fill=land)  # Africa
    d.polygon([(mapx + 320, mapy + 15), (mapx + 440, mapy + 8), (mapx + 455, mapy + 60),
               (mapx + 420, mapy + 95), (mapx + 350, mapy + 80), (mapx + 315, mapy + 45)], fill=land)  # Asia
    d.polygon([(mapx + 395, mapy + 140), (mapx + 440, mapy + 135), (mapx + 445, mapy + 165),
               (mapx + 410, mapy + 172)], fill=land)  # Oceania
    pins = [(1, 428, 54), (2, 148, 138), (3, 396, 18), (4, 62, 52), (5, 92, 46),
            (6, 300, 62), (7, 82, 62), (8, 38, 58), (9, 66, 78), (10, 88, 92),
            (11, 250, 24), (12, 272, 42), (13, 294, 20)]
    for n, px, py in pins:
        cx, cy = mapx + px, mapy + py
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED, outline="white", width=1)
        d.text((cx - 3 if n < 10 else cx - 6, cy - 5), str(n), font=fb(8), fill="white")
    # pin legend (2 lines, inside map column width)
    leg = "Pins 1–13:  1 Seoul · 2 Bridgetown · 3 Beijing · 4 Washington · 5 New York · 6 Tehran · 7 Chicago · 8 San Francisco · 9 Denver · 10 Austin · 11 Warsaw · 12 Kyiv · 13 Moscow"
    llines = wrap(d, leg, fr(8), mapw)
    for j, ln in enumerate(llines[:2]):
        d.text((mapx, mapy + maph + 4 + j * 11), ln, font=fr(8), fill=GREY)

    also = [
        "14. Paris: 100+ back 2% billionaire tax", "15. Manchester: 12,000 cleared",
        "16. Zelenskyy: 165 missiles in a week", "17. COP31: the day after pact rejected",
        "18. Benghazi: UN demands port probe", "19. Israel unity talks resume",
        "20. Gaza: two killed in Israeli strike", "21. West Bank settler attacks",
        "22. Iran war: no deal in sight", "23. Lebanon seizes 264 kg explosives",
        "24. Bahrain: strike hits plant, 2 hurt", "25. Sudan: defences down drones",
        "26. DRC: fighting traps Ebola teams", "27. Bangladesh: Hasina jailed if she returns",
        "28. Seoul minister quits in exam row", "29. SK Telecom -7.3% as hype cools",
        "30. China eases margin rules", "31. Seoul readies 10T-won fund",
    ]
    for i, item in enumerate(also):
        col, row = divmod(i, 9)
        ax = 500 + col * 256
        ay = 670 + row * 20
        d.text((ax, ay), item, font=fr(9), fill=INK)

    # ---------- DATE CHECK ----------
    dy = 884
    d.rectangle([16, dy, W - 16, dy + 66], outline=RED, width=2)
    d.text((24, dy + 4), "DATE CHECK", font=fb(12), fill=RED)
    d.text((140, dy + 5), "READ 23 NOV 2026, 23:59 UTC  —  STORIES DATED 23 NOV ONLY", font=fb(10), fill=INK)
    left = "LEFT OUT — NOT 23 NOV:  Democrats reach 258 seats (22 Nov) · Sparta II fire (22 Nov) · El Chapo Isidro captured (22 Nov) · EU-Indonesia pact (21 Nov) · Nigeria boat (21 Nov) · ICJ Myanmar ruling (19 Nov)"
    llines = wrap(d, left, fr(9), W - 48)
    for j, ln in enumerate(llines[:2]):
        d.text((24, dy + 22 + j * 12), ln, font=fr(9), fill=INK)
    ny = dy + 22 + len(llines[:2]) * 12
    d.text((24, ny), "NOT YET:  Dymer search continues (14 missing) · 4 House races uncalled · COP32 venue not set · WHO evacuating trapped Ebola staff",
           font=fr(9), fill=INK)

    # ---------- footer ----------
    d.text((16, 958), "Sources: Reuters · AP · Bloomberg · AFP · Yonhap · BBC · WSJ · NYT · ESPN · Lowy Institute (Asia Power Index 2026).",
           font=fr(8), fill=GREY)
    d.text((16, 970), "CHIPS: REPORTED = confirmed by wires · CLAIM = one side's claim, not independently confirmed · ONGOING = still developing",
           font=fr(8), fill=GREY)

    # ---------- bottom bar ----------
    d.rectangle([0, 984, W, H], fill=(12, 12, 12))
    d.text((16, 996), "Scenes are drawn illustrations, not photographs.   ·   THE WORLD TODAY — Monday 23 November 2026   ·   31 stories   ·   6 regions",
           font=fb(10), fill=(212, 175, 55))

    img.save("entry.png")
    print("saved entry.png", img.size)


if __name__ == "__main__":
    draw()
