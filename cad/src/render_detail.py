"""Cosmetic detail for the photoreal renders only (media/hero.png and media/detail.png).

Nothing here changes the design: the drawings, CAL-001 and bom/bom.csv use model.py alone.
These parts add surface cues that make a render read as a real object: a lit phone screen,
bin rims and printed label text, a hazard sticker and lid handle, the scale's display and
the mat's printed 50 mm grid. Coordinates in mm, as in model.py.
"""
from build123d import Box, Pos, Plane, Text, extrude
from concept import Part
import model

# material class per part name (read by .kit/photoreal.py); anything not listed is classified by name
MATERIALS = {
    "Phone screen (cosmetic)": "emissive",
    "Scale display (cosmetic)": "emissive",
    "Hazard sticker (cosmetic)": "paper",
    "Hazard lid handle (cosmetic)": "metal",
    "Bin rims (cosmetic)": "plastic",
    "Bin label text (cosmetic)": "paper",
    "Mat grid print (cosmetic)": "paper",
    "Platform scale, 60 kg": "painted",
    "Bins by material class (7)": "plastic",
}


def _box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _text_on_front(s, x, y, z, size, depth=0.6):
    """Raised text on a face that looks toward -Y, centered on (x, z), face at y."""
    t = extrude(Plane.XZ * Text(s, size), depth)
    return Pos(x, y, z) * t


def detail_parts(M):
    p = M["_p"]
    TOP, Z0 = p["bench_h"], p["mat_top"]
    out = []

    # phone screen: inset glass on the top face (the phone lies screen up)
    pz = p["lens_z"] + 2 + p["phone_t"]
    out.append(Part("Phone screen (cosmetic)", _box(
        p["phone_cx"] - p["phone_l"] / 2 + 5, p["phone_cx"] + p["phone_l"] / 2 - 5,
        p["mat_cy"] - p["phone_w"] / 2 + 4, p["mat_cy"] + p["phone_w"] / 2 - 4, pz, pz + 0.4), "#67E8F9"))

    # mat: printed 50 mm grid
    g = p["grid"]; lines = None
    x = p["mat_x0"] + g
    while x < p["mat_x0"] + p["mat_l"] - 1:
        s = _box(x - 1, x + 1, p["mat_y0"] + 4, p["mat_y0"] + p["mat_d"] - 4, Z0, Z0 + 0.3)
        lines = s if lines is None else lines + s; x += g
    y = p["mat_y0"] + g
    while y < p["mat_y0"] + p["mat_d"] - 1:
        lines = lines + _box(p["mat_x0"] + 4, p["mat_x0"] + p["mat_l"] - 4, y - 1, y + 1, Z0, Z0 + 0.3); y += g
    out.append(Part("Mat grid print (cosmetic)", lines, "#9CA3AF"))

    # bins: rolled rim and printed class names on the labels
    rims, texts = None, None
    for i, (name, _) in enumerate(model.BIN_CLASSES):
        x0 = p["bin_x0"] + i * p["bin_pitch"]; y0 = p["bin_y0"]; w, d, h = p["bin_w"], p["bin_d"], p["bin_h"]
        t_ = p["bin_wall"]
        rim = (_box(x0 - 8, x0 + w + 8, y0 - 8, y0 + t_, h - 22, h) + _box(x0 - 8, x0 + w + 8, y0 + d - t_, y0 + d + 8, h - 22, h)
               + _box(x0 - 8, x0 + t_, y0 + t_, y0 + d - t_, h - 22, h) + _box(x0 + w - t_, x0 + w + 8, y0 + t_, y0 + d - t_, h - 22, h))
        rims = rim if rims is None else rims + rim
        size = 50 if len(name) <= 6 else (34 if len(name) <= 12 else 27)
        t = _text_on_front(name.upper(), x0 + w / 2, y0 - 6, h - 130, size)
        texts = t if texts is None else texts + t
    out.append(Part("Bin rims (cosmetic)", rims, "#64748B"))
    out.append(Part("Bin label text (cosmetic)", texts, "#111827"))

    # hazard box: sticker on the front and a handle on the lid
    hx0, hy0 = p["haz_x0"], p["haz_y0"]
    hbody_h = p["haz_h"] - p["haz_lid_t"]
    cx = hx0 + p["haz_l"] / 2
    out.append(Part("Hazard sticker (cosmetic)", _box(cx - 60, cx + 60, hy0 - 0.6, hy0, TOP + 40, TOP + 130), "#FACC15"))
    out.append(Part("Hazard sticker text (cosmetic)",
                    _text_on_front("SHARPS", cx, hy0 - 0.6, TOP + 76, 24, 0.4), "#111827"))
    lz = TOP + p["haz_h"]
    handle = (_box(cx - 50, cx - 40, hy0 + p["haz_d"] / 2 - 6, hy0 + p["haz_d"] / 2 + 6, lz, lz + 25)
              + _box(cx + 40, cx + 50, hy0 + p["haz_d"] / 2 - 6, hy0 + p["haz_d"] / 2 + 6, lz, lz + 25)
              + _box(cx - 50, cx + 50, hy0 + p["haz_d"] / 2 - 6, hy0 + p["haz_d"] / 2 + 6, lz + 25, lz + 33))
    out.append(Part("Hazard lid handle (cosmetic)", handle, "#9CA3AF"))

    # scale: display window on the head, rubber pad on the platform
    sx0, sy0 = p["scale_x0"], p["scale_y0"]
    hx, hy, hz = p["scale_head"]
    colx = sx0 + p["scale_l"] / 2
    fy = sy0 + p["scale_d"] - 30
    out.append(Part("Scale display (cosmetic)", _box(colx - 55, colx + 55, fy - 0.6, fy,
                                                     p["scale_col_h"] + 45, p["scale_col_h"] + 85), "#86EFAC"))
    out.append(Part("Scale pad, rubber (cosmetic)", _box(sx0 + 15, sx0 + p["scale_l"] - 15, sy0 + 15,
                                                         sy0 + p["scale_d"] - 15, p["scale_t"], p["scale_t"] + 3), "#1F2937"))
    return out
