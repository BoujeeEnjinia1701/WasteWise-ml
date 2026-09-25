"""WasteWise-ml sorting station parametric model (build123d), TRL 3 massing-plus level.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl.

WasteWise-ml is software. This model is the reference pilot sorting station where the
model is used: the site's bench, a light sorting mat, a phone on a clamp stand with its
rear camera pointing down at the mat, a hazard box, a power bank, seven bins by material
class and a platform scale. Numbered parts match bom/bom.csv (items 1 to 7).

Axes: X along the bench (bins to the +X side), Y away from the viewer (the user stands
at +Y, behind the bench), Z up, floor at Z = 0. Units: mm.

Detail level: correct interfaces (camera height and field of view over the mat, stand
base clear of the camera frame, bin openings, hazard box lid) and main dimensions. Not
fabrication detail. PRELIMINARY, NOT FOR FABRICATION.
"""
import math
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # Site's own bench (context, not costed)
    "bench_l": 1400.0, "bench_d": 650.0, "bench_h": 760.0, "bench_top_t": 30.0, "leg_w": 50.0,
    # 3 Light sorting mat, 50 mm grid
    "mat_l": 700.0, "mat_d": 450.0, "mat_t": 4.0, "mat_x0": 300.0, "mat_y0": 110.0, "grid": 50.0,
    # 1 Phone (reference Android phone, landscape over the mat: long side along X)
    "phone_l": 160.0, "phone_w": 76.0, "phone_t": 9.0,
    "lens_offset": 55.0,        # rear camera lens from the phone center, along the long side
    "cam_h": 440.0,             # lens height above the mat surface (frame fits inside the mat)
    "focal_eq": 26.0,           # main camera 35 mm-equivalent focal length (assumed typical)
    # 2 Phone stand: weighted base, post, arm, clamp
    "base_l": 180.0, "base_d": 65.0, "base_t": 20.0, "base_y": 575.0,   # base front edge Y
    "post_d": 18.0, "arm_d": 14.0, "clamp_w": 90.0,
    # 5 Hazard box (lidded steel, sand layer), on the bench's +X end
    "haz_l": 240.0, "haz_d": 320.0, "haz_h": 200.0, "haz_lid_t": 20.0, "haz_x0": 1130.0, "haz_y0": 60.0,
    # 6 Power bank
    "pb_l": 140.0, "pb_d": 70.0, "pb_t": 25.0, "pb_x0": 770.0, "pb_y0": 560.0,
    # 4 Bins by material class (about 60 L each), in a row beyond the bench
    "bin_n": 7, "bin_w": 380.0, "bin_d": 380.0, "bin_h": 500.0, "bin_wall": 12.0,
    "bin_pitch": 420.0, "bin_x0": 1550.0, "bin_y0": -40.0,
    # 7 Platform scale, 60 kg, at the -X end by the input sack
    "scale_l": 400.0, "scale_d": 360.0, "scale_t": 60.0, "scale_x0": -250.0, "scale_y0": -760.0,
    "scale_col_h": 640.0, "scale_head": (160.0, 40.0, 100.0),
}

BIN_CLASSES = [("PET", "#38BDF8"), ("HDPE and PP", "#2563EB"), ("Film (LDPE)", "#A78BFA"),
               ("Metal", "#9CA3AF"), ("Paper and carton", "#D97706"), ("Glass", "#16A34A"),
               ("Unsure: check", "#F59E0B")]


def derived(params=None):
    """Derived dimensions used by the model, the drawing and docs/04-calcs/sizing.py."""
    p = dict(params or PARAMS)
    p["mat_top"] = p["bench_h"] + p["mat_t"]
    p["mat_cx"] = p["mat_x0"] + p["mat_l"] / 2
    p["mat_cy"] = p["mat_y0"] + p["mat_d"] / 2
    # Camera frame on the mat. A 35 mm-equivalent focal length keeps the 43.27 mm diagonal of the
    # 36 x 24 mm frame; a phone sensor is 4:3, so its equivalent frame is 34.62 x 25.96 mm.
    diag = math.hypot(36.0, 24.0)
    sw, sh = diag * 0.8, diag * 0.6
    p["hfov_deg"] = math.degrees(2 * math.atan(sw / 2 / p["focal_eq"]))
    p["vfov_deg"] = math.degrees(2 * math.atan(sh / 2 / p["focal_eq"]))
    p["frame_x"] = p["cam_h"] * sw / p["focal_eq"]             # long side of the image along X
    p["frame_y"] = p["cam_h"] * sh / p["focal_eq"]
    p["lens_z"] = p["mat_top"] + p["cam_h"]
    p["phone_cx"] = p["mat_cx"] + p["lens_offset"]             # lens sits over the mat center
    p["post_x"], p["post_y"] = p["mat_cx"], p["base_y"] + p["base_d"] / 2
    p["arm_z"] = p["lens_z"] + p["phone_t"] + 12.0             # arm above the phone back
    p["bin_vol_l"] = ((p["bin_w"] - 2 * p["bin_wall"]) * (p["bin_d"] - 2 * p["bin_wall"])
                      * (p["bin_h"] - p["bin_wall"])) / 1e6
    p["row_len"] = p["bin_x0"] + (p["bin_n"] - 1) * p["bin_pitch"] + p["bin_w"] - p["scale_x0"]
    return p


def _box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _rod(a, b, r):
    from build123d import Solid, Plane, Vector
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def build_parts(params=None):
    """Return a dict of named build123d solids, plus '_p' with the derived parameters."""
    p = derived(params)
    B, TOP, Z0 = p["bench_h"], p["bench_h"], p["mat_top"]

    # Site's bench: top, four legs, two stretchers
    bench = _box(0, p["bench_l"], 0, p["bench_d"], TOP - p["bench_top_t"], TOP)
    lw = p["leg_w"]
    for x in (40, p["bench_l"] - 40):
        for y in (40, p["bench_d"] - 40):
            bench = bench + _box(x - lw / 2, x + lw / 2, y - lw / 2, y + lw / 2, 0, TOP - p["bench_top_t"])
    for y in (40, p["bench_d"] - 40):
        bench = bench + _box(40, p["bench_l"] - 40, y - 20, y + 20, 180, 210)

    # 3 Mat, with shallow grid grooves every grid pitch on the top face (massing cue only)
    mat = _box(p["mat_x0"], p["mat_x0"] + p["mat_l"], p["mat_y0"], p["mat_y0"] + p["mat_d"], TOP, Z0)

    # 1 Phone, screen up, rear camera bump facing the mat
    pz0 = p["lens_z"]
    phone = _box(p["phone_cx"] - p["phone_l"] / 2, p["phone_cx"] + p["phone_l"] / 2,
                 p["mat_cy"] - p["phone_w"] / 2, p["mat_cy"] + p["phone_w"] / 2, pz0 + 2, pz0 + 2 + p["phone_t"])
    phone = phone + _box(p["mat_cx"] - 15, p["mat_cx"] + 15, p["mat_cy"] - 15, p["mat_cy"] + 15, pz0, pz0 + 2)

    # 2 Stand: base behind the mat (out of the camera frame), post, arm over to a clamp on the phone
    base = _box(p["post_x"] - p["base_l"] / 2, p["post_x"] + p["base_l"] / 2,
                p["base_y"], p["base_y"] + p["base_d"], Z0 - p["mat_t"], Z0 - p["mat_t"] + p["base_t"])
    post = _rod((p["post_x"], p["post_y"], TOP + p["base_t"]), (p["post_x"], p["post_y"], p["arm_z"]), p["post_d"] / 2)
    cy = p["mat_cy"]
    arm = _rod((p["post_x"], p["post_y"], p["arm_z"]), (p["phone_cx"], cy, p["arm_z"]), p["arm_d"] / 2)
    clamp = (_box(p["phone_cx"] - p["clamp_w"] / 2, p["phone_cx"] + p["clamp_w"] / 2, cy - 12, cy + 12,
                  pz0 + 2 + p["phone_t"], p["arm_z"] + 6)
             + _box(p["phone_cx"] - p["clamp_w"] / 2 - 6, p["phone_cx"] - p["clamp_w"] / 2, cy - 12, cy + 12,
                    pz0 - 2, p["arm_z"] + 6)
             + _box(p["phone_cx"] + p["clamp_w"] / 2, p["phone_cx"] + p["clamp_w"] / 2 + 6, cy - 12, cy + 12,
                    pz0 - 2, p["arm_z"] + 6))
    clamp = clamp - _box(p["phone_cx"] - p["phone_l"] / 2 - 1, p["phone_cx"] + p["phone_l"] / 2 + 1,
                         cy - p["phone_w"] / 2 - 1, cy + p["phone_w"] / 2 + 1, pz0 + 2, pz0 + 2 + p["phone_t"])
    stand = base + post + arm + clamp

    # 6 Power bank on the bench, cable up the post
    pb = _box(p["pb_x0"], p["pb_x0"] + p["pb_l"], p["pb_y0"], p["pb_y0"] + p["pb_d"], TOP, TOP + p["pb_t"])
    cable = (_rod((p["pb_x0"], p["pb_y0"] + 35, TOP + 12), (p["post_x"] + 14, p["post_y"], TOP + 40), 3)
             + _rod((p["post_x"] + 14, p["post_y"], TOP + 40), (p["post_x"] + 14, p["post_y"], p["arm_z"] - 20), 3))
    powerbank = pb + cable

    # 5 Hazard box: open steel box with a lid resting on top
    hx0, hy0 = p["haz_x0"], p["haz_y0"]
    hbody_h = p["haz_h"] - p["haz_lid_t"]
    hazard = (_box(hx0, hx0 + p["haz_l"], hy0, hy0 + p["haz_d"], TOP, TOP + hbody_h)
              - _box(hx0 + 3, hx0 + p["haz_l"] - 3, hy0 + 3, hy0 + p["haz_d"] - 3, TOP + 3, TOP + hbody_h + 1))
    hazard_lid = _box(hx0 - 10, hx0 + p["haz_l"] + 10, hy0 - 10, hy0 + p["haz_d"] + 10,
                      TOP + hbody_h, TOP + p["haz_h"])

    # 4 Bins: open-top boxes in a row
    bins, labels = [], []
    for i in range(p["bin_n"]):
        x0 = p["bin_x0"] + i * p["bin_pitch"]; y0 = p["bin_y0"]; w = p["bin_wall"]
        b = (_box(x0, x0 + p["bin_w"], y0, y0 + p["bin_d"], 0, p["bin_h"])
             - _box(x0 + w, x0 + p["bin_w"] - w, y0 + w, y0 + p["bin_d"] - w, w, p["bin_h"] + 1))
        bins.append(b)
        labels.append(_box(x0 + 40, x0 + p["bin_w"] - 40, y0 - 6, y0, p["bin_h"] - 200, p["bin_h"] - 60))

    # 7 Platform scale: platform, column, display head
    sx0, sy0 = p["scale_x0"], p["scale_y0"]
    hx, hy, hz = p["scale_head"]
    colx = sx0 + p["scale_l"] / 2
    scale = (_box(sx0, sx0 + p["scale_l"], sy0, sy0 + p["scale_d"], 0, p["scale_t"])
             + _rod((colx, sy0 + p["scale_d"] - 10, p["scale_t"]), (colx, sy0 + p["scale_d"] - 10, p["scale_col_h"]), 14)
             + _box(colx - hx / 2, colx + hx / 2, sy0 + p["scale_d"] - 30, sy0 + p["scale_d"] + 10,
                    p["scale_col_h"], p["scale_col_h"] + hz))

    return {"bench": bench, "mat": mat, "phone": phone, "stand": stand, "powerbank": powerbank,
            "hazard": hazard, "hazard_lid": hazard_lid, "bins": bins, "bin_labels": labels,
            "scale": scale, "_p": p}


def station(params=None, with_bench=True):
    """Station assembly (the object on the general arrangement drawing)."""
    from build123d import Compound
    P = build_parts(params)
    kids = [P["mat"], P["phone"], P["stand"], P["powerbank"], P["hazard"], P["hazard_lid"], P["scale"]] + P["bins"]
    if with_bench:
        kids = [P["bench"]] + kids
    return Compound(children=kids)


def bench_group(params=None):
    """Bench, mat, phone, stand, power bank and hazard box only (for the bench detail view)."""
    from build123d import Compound
    P = build_parts(params)
    return Compound(children=[P[k] for k in ("bench", "mat", "phone", "stand", "powerbank", "hazard", "hazard_lid")])


def export(out=None):
    from build123d import Compound, export_step, export_stl
    out = Path(out) if out else Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    asm = station()
    export_step(asm, str(out / "step" / "wastewise-station-assembly.step"))
    export_stl(asm, str(out / "stl" / "wastewise-station-assembly.stl"))
    P = build_parts()
    singles = {"phone-stand": Compound(children=[P["stand"], P["phone"]]), "sorting-mat": P["mat"],
               "hazard-box": Compound(children=[P["hazard"], P["hazard_lid"]]), "bin": P["bins"][0]}
    for name, shape in singles.items():
        export_step(shape, str(out / "step" / f"wastewise-{name}.step"))
        export_stl(shape, str(out / "stl" / f"wastewise-{name}.stl"))
    return P


if __name__ == "__main__":
    P = export()
    p = P["_p"]
    bb = station().bounding_box()
    print(f"Station envelope: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm (X x Y x Z)")
    print(f"Lens height above floor {p['lens_z']:.0f} mm; above mat {p['cam_h']:.0f} mm")
    print(f"Camera frame on mat {p['frame_x']:.0f} x {p['frame_y']:.0f} mm; mat {p['mat_l']:.0f} x {p['mat_d']:.0f} mm")
    print(f"Bin inner volume {p['bin_vol_l']:.1f} L each, {p['bin_n']} bins")
    print("Wrote cad/step/*.step and cad/stl/*.stl")
