"""WasteWise-ml sorting station parametric model (build123d), kit 1.9 interface, TRL 3 (stage P3, detail level D3).

Run from the repo root:  python .kit/cad_check.py --export   (fidelity check; STEP per part of option A and per assembly)
                         python cad/src/model.py --check     (constructability checks on the option A scanning rig)
                         python cad/src/model.py             (STL of option A at 0.15 mm chord; masses by BOM line)

WasteWise-ml is software. This model is the reference pilot sorting station where the model is used. Two concept
options are modelled to D3 (STANDARDS section 24; Amish, 2026-10-24: "Detail every option"):

  A  Phone stand over a mat (the current design, CHOSEN until Amish decides otherwise; WML-OPT-001). One item lies on
     a light mat; the user's phone lies screen up in a folded tray on a clamped aluminium stand with its rear camera
     440 mm above the mat; a tap on a Bluetooth shutter button at the bench edge takes one photo and the on-device
     classifier answers with class, grade and confidence, or "Unsure" or "Hazard" (WML-DEC-001 F1). Bins by material
     class, a lidded hazard box with sand and a platform scale complete the station. Numbered parts match bom/bom.csv.
  B  Tray detector (alternative, not carried to the drawing, BOM or build plan). Ten to twenty items are spread in a
     shallow tray; a Raspberry Pi camera on a mast photographs the whole tray and an on-device object detector boxes
     and labels every item at once on a 5 inch touch display at the user's eye level; an arcade push button at the
     bench edge triggers each photo.

Axes: X along the bench (bins to the +X side), Y away from the viewer (the user stands at +Y, behind the bench),
Z up, floor at Z = 0. Units: mm. Sizing is in WML-CAL-001 (docs/04-calcs/sizing.py), which reads PARAMS and derived().
PROTOTYPE BUILD PLAN GEOMETRY FOR OPTION A; CONCEPT, NOT FOR FABRICATION BEYOND THE PROTOTYPE.
"""
from __future__ import annotations

import copy
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

TITLE = "WasteWise-ml"

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
    # 2 Phone stand, made (WML-DDR-003): plywood base board clamped to the bench's back edge,
    #   square aluminium post and arm joined by two corner plates, two foot angles, and a folded
    #   phone tray hung from the arm end. The base board's front edge meets the mat's back edge.
    "base_l": 240.0, "base_d": 90.0, "base_t": 18.0,
    "tube": 25.0, "tube_t": 2.0,                      # 25 x 25 x 2 mm square aluminium tube (post and arm)
    "foot_leg": 50.0, "foot_t": 3.0, "foot_len": 60.0,  # foot angles, 50 x 50 x 3 mm angle
    "cp_t": 3.0, "cp_reach": 80.0, "cp_drop": 100.0,  # corner plates: reach along the arm, drop down the post
    "tray_t": 2.0, "tray_lip": 8.0, "tray_gap": 1.0, "tray_end": 5.0,
    "win": 32.0,                                      # window for the camera bump (bump 30 x 30 mm); 34 until WML-DEC-001 F5
    "tab_w": 40.0, "tab_l": 65.0, "arm_gap": 3.0,     # tray tab under the arm end; arm end clear of the lip
    "clamp_x": (548.0, 752.0),                        # two G-clamps hold the base board to the bench
    "cable_r": 2.5,
    "cable_arm_dx": 8.0,        # the cable runs along the arm top this far to the +X side of the arm's centre line,
                                # clear of the tray tab bolt washers (WML-DEC-001 F4)
    # 12 Bluetooth shutter button at the bench edge (WML-DEC-001 F1): the scan trigger within easy reach
    "btn_x": 470.0, "btn_y": 605.0, "btn_l": 40.0, "btn_w": 26.0, "btn_t": 11.0,
    # 5 Hazard box (lidded steel, sand layer), on the bench's +X end
    "haz_l": 240.0, "haz_d": 320.0, "haz_h": 200.0, "haz_lid_t": 20.0, "haz_x0": 1130.0, "haz_y0": 60.0,
    "haz_sheet": 1.0, "haz_sand": 50.0,               # 1 mm steel sheet; 50 mm of dry sand (WML-DEC-001 F3)
    # 6 Power bank
    "pb_l": 140.0, "pb_d": 70.0, "pb_t": 25.0, "pb_x0": 790.0, "pb_y0": 575.0,
    # 4 Bins by material class (about 60 L each), in a row beyond the bench
    "bin_n": 7, "bin_w": 380.0, "bin_d": 380.0, "bin_h": 500.0,
    "bin_wall": 12.0,           # rim band used by the cosmetic render detail only (cad/src/render_detail.py)
    "bin_shell": 3.0, "bin_taper": 25.0, "bin_r": 30.0,   # moulded bin: 3 mm wall, 25 mm taper a side, 30 mm corners
    "bin_pitch": 420.0, "bin_x0": 1550.0, "bin_y0": -40.0,
    # 7 Platform scale, 60 kg, at the -X end by the input sack
    "scale_l": 400.0, "scale_d": 360.0, "scale_t": 60.0, "scale_x0": -250.0, "scale_y0": -760.0,
    "scale_col_h": 640.0, "scale_head": (160.0, 40.0, 100.0),
    # Option B, tray detector (WML-OPT-001): Raspberry Pi 5, Camera Module 3 Wide, 5 inch Touch Display 2
    "b_tray_l": 600.0, "b_tray_d": 400.0, "b_tray_h": 40.0, "b_tray_t": 3.0,
    "b_cam_h": 450.0,           # camera lens above the tray floor
    "b_hfov": 102.0, "b_vfov": 67.0,                  # Camera Module 3 Wide field of view, degrees (datasheet)
    "b_px": (4608, 2592),       # Camera Module 3 sensor, pixels
    "b_mast": 40.0, "b_mast_t": 2.0,                  # 40 x 40 x 2 mm square aluminium tube (mast and arm)
    "b_base_l": 300.0, "b_base_d": 120.0, "b_base_t": 18.0,
    "b_disp": (143.5, 82.4, 8.0),                     # 5 inch display module envelope (about; to confirm with datasheet)
    "b_disp_z": 1150.0,         # display centre height above the floor
    "b_clamp_x": (520.0, 780.0),
    "b_pb": (150.0, 72.0, 27.0), "b_pb_x0": 820.0, "b_pb_y0": 560.0,
    "b_btn_x": 420.0, "b_btn_y": 590.0,
}

BIN_CLASSES = [("PET", "#38BDF8"), ("HDPE and PP", "#2563EB"), ("Film (LDPE)", "#A78BFA"),
               ("Metal", "#9CA3AF"), ("Paper and carton", "#D97706"), ("Glass", "#16A34A"),
               ("Unsure: check", "#F59E0B")]

OPTIONS = {"A": "Phone stand over a mat", "B": "Tray detector"}
PRINCIPLES = {
    "A": "One item at a time on a light mat under the user's own phone, held screen up 440 mm above it; a tap on a "
         "bench-edge button takes one photo and an on-device classifier answers with class, grade and confidence.",
    "B": "Ten to twenty items spread in a tray under a Raspberry Pi wide camera on a mast; an on-device object "
         "detector boxes and labels every item at once on a touch display at eye level.",
}
CHOSEN = "A"
OPTION_VIEWS = {"A": {"el": 24, "az": -35, "keep_context": True, "ground_z": 0},
                "B": {"el": 24, "az": -35, "keep_context": True, "ground_z": 0}}
# Parts that touch or bite by design: wood screws in their pilot holes, the USB cable ends in their plugs, machine
# screws in printed bosses, the camera ribbon in its connector, cables in their glands
ALLOWED_CONTACTS = [("Wood screw", "Base board"), ("USB cable", "USB-C plug"), ("M2 pan screw", "Camera housing"),
                    ("M2.5 pan screw", "Pi 5 case"), ("M2.5 pan screw", "Touch display"), ("Camera ribbon", "Camera Module"),
                    ("Camera ribbon", "Pi 5 case"), ("Camera ribbon", "Camera housing"), ("cable to the Pi", "Pi 5 case"),
                    ("Button wire", "Button box"), ("Button wire", "Pi 5 case"), ("Button wire", "Arcade button")]


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
    p["f_eq_min"] = p["cam_h"] * sh / p["mat_d"]                # shortest focal length whose frame fits the mat depth
    p["lens_z"] = p["mat_top"] + p["cam_h"]
    p["phone_cx"] = p["mat_cx"] + p["lens_offset"]             # lens sits over the mat center
    # stand: the base board's front edge meets the mat's back edge (it locates the mat)
    p["base_y"] = p["mat_y0"] + p["mat_d"]
    p["base_top"] = p["bench_h"] + p["base_t"]
    p["post_x"], p["post_y"] = p["mat_cx"], p["base_y"] + p["base_d"] / 2
    p["tray_bot"] = p["lens_z"]                                 # lens flush with the tray's underside
    p["tray_top"] = p["lens_z"] + p["tray_t"]                   # the phone's back rests here
    p["arm_bot"] = p["tray_top"]                                # arm sits on the tray tab
    p["arm_z"] = p["arm_bot"] + p["tube"]                       # top of the arm and of the post
    p["post_len"] = p["arm_z"] - p["base_top"]
    p["tray_y0"] = p["mat_cy"] - p["phone_w"] / 2 - p["tray_gap"] - p["tray_t"]
    p["tray_y1"] = p["mat_cy"] + p["phone_w"] / 2 + p["tray_gap"] + p["tray_t"]
    p["tray_x0"] = p["phone_cx"] - p["phone_l"] / 2             # phone's charging end flush, plug free
    p["tray_x1"] = p["phone_cx"] + p["phone_l"] / 2 + p["tray_end"]
    p["arm_y0"] = p["tray_y1"] + p["arm_gap"]                   # arm end, clear of the tray lip
    p["arm_y1"] = p["post_y"] - p["tube"] / 2                   # arm butts the post's front face
    p["arm_len"] = p["arm_y1"] - p["arm_y0"]
    p["frame_edge_y"] = p["mat_cy"] + p["frame_y"] / 2
    p["screen_z"] = p["lens_z"] + p["tray_t"] + p["phone_t"]    # top of the phone's screen glass
    # bin inner volume: frustum of rounded squares (3 mm wall, 25 mm taper a side)
    s1 = p["bin_w"] - 2 * p["bin_shell"]
    s2 = s1 - 2 * p["bin_taper"]
    ri = p["bin_r"] - p["bin_shell"]
    a1, a2 = s1 * s1 - (4 - math.pi) * ri ** 2, s2 * s2 - (4 - math.pi) * ri ** 2
    hin = p["bin_h"] - p["bin_shell"]
    p["bin_vol_l"] = hin / 3 * (a1 + a2 + math.sqrt(a1 * a2)) / 1e6
    p["row_len"] = p["bin_x0"] + (p["bin_n"] - 1) * p["bin_pitch"] + p["bin_w"] - p["scale_x0"]
    # option B camera geometry
    p["b_tray_floor"] = p["bench_h"] + p["b_tray_t"]
    p["b_lens_z"] = p["b_tray_floor"] + p["b_cam_h"]
    p["b_frame_x"] = 2 * p["b_cam_h"] * math.tan(math.radians(p["b_hfov"] / 2))
    p["b_frame_y"] = 2 * p["b_cam_h"] * math.tan(math.radians(p["b_vfov"] / 2))
    p["b_base_y"] = p["bench_d"] - p["b_base_d"]
    p["b_tray_cy"] = p["b_base_y"] - p["b_tray_d"] / 2
    p["b_mast_y"] = p["b_base_y"] + p["b_base_d"] / 2
    return p


# ---------------------------------------------------------------------------------------------------------------
# Legacy geometry helpers (also used by cad/src/build_plan_media.py)
# ---------------------------------------------------------------------------------------------------------------
def _box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _rod(a, b, r):
    from build123d import Solid, Plane, Vector
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _fuse(shapes):
    out = None
    for sh in shapes:
        out = sh if out is None else out + sh
    return out


def _group(shapes):
    from build123d import Compound
    return Compound(children=[copy.copy(s) for s in shapes])


def _hole_x(y, z, d, x0=-1e4, x1=1e4):
    from build123d import Solid, Plane, Vector
    return Solid.make_cylinder(d / 2, x1 - x0, Plane(origin=Vector(x0, y, z), z_dir=Vector(1, 0, 0)))


def _hole_y(x, z, d, y0=-1e4, y1=1e4):
    from build123d import Solid, Plane, Vector
    return Solid.make_cylinder(d / 2, y1 - y0, Plane(origin=Vector(x, y0, z), z_dir=Vector(0, 1, 0)))


def _hole_z(x, y, d, z0=-1e4, z1=1e4):
    from build123d import Solid, Plane, Vector
    return Solid.make_cylinder(d / 2, z1 - z0, Plane(origin=Vector(x, y, z0), z_dir=Vector(0, 0, 1)))


# ---------------------------------------------------------------------------------------------------------------
# Shared builders
# ---------------------------------------------------------------------------------------------------------------
class _Parts(list):
    """A list of cad_parts.part() dicts with a legacy 'key' for build_components()."""

    def add(self, name, shape, material, kind="made", bom=None, key=None, group="station", explode=(0, 0, 0), color=None):
        from cad_parts import part
        d = part(name, shape, material, kind=kind, bom=bom, group=group, explode=explode, color=color)
        d["key"] = key
        self.append(d)
        return d

    def extend_sets(self, sets, key=None, joint=None):
        for d in sets:
            d["key"] = key
            d["joint"] = joint
            self.append(d)


def _bench(P, p):
    import cad_parts as cp
    TOP = p["bench_h"]
    btm = TOP - p["bench_top_t"]
    P.add("Bench top (site's own, timber)", cp.break_edges(_box(0, p["bench_l"], 0, p["bench_d"], btm, TOP), 3.0),
          "timber", kind="context", key="bench", group="context")
    lw = p["leg_w"]
    for x in (40, p["bench_l"] - 40):
        for y in (40, p["bench_d"] - 40):
            P.add(f"Bench leg at x {x:.0f}, y {y:.0f} (site's own)", cp.break_edges(_box(x - lw / 2, x + lw / 2, y - lw / 2, y + lw / 2, 0, btm), 2.0),
                  "timber", kind="context", key="bench", group="context")
    for y in (40, p["bench_d"] - 40):
        P.add(f"Bench stretcher at y {y:.0f} (site's own)", cp.break_edges(_box(40 + lw / 2, p["bench_l"] - 40 - lw / 2, y - 20, y + 20, 180, 210), 2.0),
              "timber", kind="context", key="bench", group="context")


def _foot_angles(P, x0, x1, yc, z0, leg, t, length, bolt_z, screw_dy, bolt_d, bom, key_r, key_l, label):
    """Two aluminium angles, one each side of a square post (faces at x0 and x1), flat legs on the board at z0."""
    import cad_parts as cp
    from build123d import Pos, Rot
    ang = cp.angle(leg, leg, t, length)
    shapes = {}
    for side, sgn in (("r", 1), ("l", -1)):
        if sgn > 0:
            s = Pos(x1, yc + length / 2, z0) * Rot(90, 0, 0) * ang
        else:
            s = Pos(x0, yc - length / 2, z0) * Rot(0, 0, 180) * Rot(90, 0, 0) * ang
        for zb in bolt_z:
            s = s - _hole_x(yc, zb, bolt_d + 0.5)
        sx = (x1 + leg / 2 + t / 2) if sgn > 0 else (x0 - leg / 2 - t / 2)
        for dy in screw_dy:
            s = s - _hole_z(sx, yc + dy, 4.5)
        s = cp.break_edges(s, 0.4)
        shapes[side] = s
        P.add(f"Foot angle, {'right' if sgn > 0 else 'left'} ({leg:.0f} x {leg:.0f} x {t:.0f} aluminium angle, {length:.0f} long){label}",
              s, "aluminium", bom=bom, key=key_r if sgn > 0 else key_l, group="stand")
    return [((x1 + leg / 2 + t / 2), dy) for dy in screw_dy] + [((x0 - leg / 2 - t / 2), dy) for dy in screw_dy]


def _wood_screws(P, pts, z_top, bom, key, label):
    import wml_parts as wp
    from build123d import Pos
    for x, y in pts:
        P.add(f"Wood screw No. 8 x 16 pan head ({label})", Pos(x, y, z_top) * wp.wood_screw(16.0), "zinc_plated",
              kind="fastener", bom=bom, key=key, group="fixings")


def _clamps(P, xs, y_front, y_spine, z_jaw, z_under, bom, key):
    import wml_parts as wp
    for i, xc in enumerate(xs):
        for name, shape, mat in wp.g_clamp(xc, y_front, y_spine, z_jaw, z_under):
            P.add(f"{name}, clamp {i + 1}", shape, mat, kind="bought", bom=bom, key=key, group="stand")


def _corner_plates(P, xf, xb, t, y_front, y_back, y_arm_end, top, drop, arm_h, holes, bom, key_r, key_l, label):
    """Two plates in YZ planes on the faces x = xf (+X side, outward) and x = xb (-X side) of a post and arm."""
    import cad_parts as cp
    from build123d import Plane, Polyline, Vector, extrude, make_face
    outline = [(y_front, top), (y_back, top), (y_back, top - drop), (y_arm_end, top - drop), (y_front, top - arm_h)]
    for side, xs in (("r", xf), ("l", xb - t)):
        face = make_face(Polyline(*outline, close=True))
        pl = Plane(origin=Vector(xs, 0, 0), x_dir=Vector(0, 1, 0), z_dir=Vector(1, 0, 0))
        s = extrude(pl * face, t)
        for (yy, zz, d) in holes:
            s = s - _hole_x(yy, zz, d)
        s = cp.break_edges(s, 0.6)
        P.add(f"Corner plate, {'right' if side == 'r' else 'left'} ({t:.0f} mm aluminium){label}", s, "aluminium", bom=bom,
              key=key_r if side == "r" else key_l, group="stand")


def _tie(P, center, w_in, h_in, plane, label, key):
    """Cable tie round a bundle; plane 'xy' (band along Z) or 'xz' (band along Y)."""
    import wml_parts as wp
    from build123d import Pos, Rot
    s = wp.cable_tie_loop(w_in, h_in)
    s = Pos(*center) * (Rot(90, 0, 0) * s if plane == "xz" else s)
    P.add(f"Cable tie ({label})", s, "hdpe_black", kind="fastener", bom=11, key=key, group="fixings")


def _station_items(P, p):
    """Bins (4), hazard box (5) and platform scale (7): the bought station items both options share."""
    import cad_parts as cp
    import wml_parts as wp
    from build123d import Box, Cylinder, Pos, Rot
    TOP = p["bench_h"]
    # 4 Bins with printed labels on their sloping front faces
    a = math.atan2(p["bin_taper"], p["bin_h"])
    for i, (cls, col) in enumerate(BIN_CLASSES):
        x0 = p["bin_x0"] + i * p["bin_pitch"]; y0 = p["bin_y0"]
        b = Pos(x0, y0, 0) * wp.bin_shell(p["bin_w"], p["bin_d"], p["bin_h"], p["bin_taper"], p["bin_shell"], r=p["bin_r"])
        P.add(f"Bin {i + 1}, {cls} (about 60 L, moulded HDPE)", b, "hdpe_natural", kind="bought", bom=4, key="bins",
              group="bins", color="#64748B")
        zc = p["bin_h"] - 130.0
        yf = y0 + p["bin_taper"] * (1 - zc / p["bin_h"])
        lab = Pos(x0 + p["bin_w"] / 2, yf - 0.46 / math.cos(a), zc) * Rot(math.degrees(a), 0, 0) * Box(300.0, 0.8, 140.0)
        lab = cp.break_edges(lab, 0.3)
        P.add(f"Bin {i + 1} label, {cls} (printed band and bin number)", lab, "label", kind="bought", bom=4, key="bin_labels",
              group="bins", color=col)
    # 5 Hazard box: 1 mm steel box and lid, strap handle, 50 mm of dry sand, sharps container, PVC tape for cell terminals
    hx0, hy0, s = p["haz_x0"], p["haz_y0"], p["haz_sheet"]
    L, D, H = p["haz_l"], p["haz_d"], p["haz_h"]
    hb = H - s
    body = _box(hx0, hx0 + L, hy0, hy0 + D, TOP, TOP + hb) - _box(hx0 + s, hx0 + L - s, hy0 + s, hy0 + D - s, TOP + s, TOP + hb + 1)
    body = cp.break_edges(body, 0.3)
    P.add("Hazard box body (1 mm steel, painted)", body, "safety_red", kind="bought", bom=5, key="hazard", group="hazard")
    c = 1.0                                  # skirt clearance
    lx0, lx1, ly0, ly1 = hx0 - c - s, hx0 + L + c + s, hy0 - c - s, hy0 + D + c + s
    lid = (_box(lx0, lx1, ly0, ly1, TOP + H - p["haz_lid_t"], TOP + H)
           - _box(lx0 + s, lx1 - s, ly0 + s, ly1 - s, TOP + H - p["haz_lid_t"] - 1, TOP + H - s))
    lid = cp.break_edges(lid, 0.3)
    P.add("Hazard box lid (1 mm steel, painted)", lid, "safety_red", kind="bought", bom=5, key="hazard_lid", group="hazard")
    cx, cy, lz = hx0 + L / 2, hy0 + D / 2, TOP + H
    strap = (_box(cx - 60, cx - 40, cy - 10, cy + 10, lz, lz + 2) + _box(cx + 40, cx + 60, cy - 10, cy + 10, lz, lz + 2)
             + _box(cx - 42, cx - 40, cy - 10, cy + 10, lz, lz + 27) + _box(cx + 40, cx + 42, cy - 10, cy + 10, lz, lz + 27)
             + _box(cx - 42, cx + 42, cy - 10, cy + 10, lz + 25, lz + 27))
    strap = cp.break_edges(strap, 0.6)
    for xr in (cx - 50, cx + 50):
        strap = strap - _hole_z(xr, cy, 4.1)
        lid = lid - _hole_z(xr, cy, 4.1)
    P[-1]["shape"] = lid
    P.add("Hazard box lid handle (20 x 2 mm steel strap)", strap, "zinc_plated", kind="bought", bom=5, key="hazard_lid", group="hazard")
    for xr in (cx - 50, cx + 50):
        rv = Pos(xr, cy, lz + 2) * cp.break_edges(Cylinder(4.0, 1.6, align=None), 0.7)
        P.add("Pop rivet 4 mm (handle to lid)", rv + Pos(xr, cy, lz - 6) * cp.round_bar(4.0, 8.0, 0.3), "aluminium",
              kind="fastener", bom=5, key="hazard_lid", group="hazard")
    sand = wp.rbox(hx0 + s + 0.5, hx0 + L - s - 0.5, hy0 + s + 0.5, hy0 + D - s - 0.5, TOP + s, TOP + s + p["haz_sand"], r=1.5, edge=4.0)
    P.add("Dry sand layer, 50 mm (in the hazard box)", sand, "sand", kind="bought", bom=5, key="hazard", group="hazard")
    zs = TOP + s + p["haz_sand"]
    sc = wp.rbox(hx0 + 20, hx0 + 120, hy0 + 30, hy0 + 110, zs, zs + 120, r=6.0, edge=1.0) \
        - wp.rbox(hx0 + 22, hx0 + 118, hy0 + 32, hy0 + 108, zs + 2, zs + 121, r=4.0, edge=0)
    P.add("Sharps container body, 1.5 L (yellow polypropylene)", sc, "hdpe_natural", kind="bought", bom=5, key="hazard",
          group="hazard", color="#E3B21C")
    scl = wp.rbox(hx0 + 19, hx0 + 121, hy0 + 29, hy0 + 111, zs + 120, zs + 126, r=6.5, edge=1.0) \
        - _box(hx0 + 50, hx0 + 90, hy0 + 60, hy0 + 80, zs + 119, zs + 127)
    P.add("Sharps container lid with slot", scl, "hdpe_natural", kind="bought", bom=5, key="hazard", group="hazard", color="#B3261E")
    P.add("PVC insulating tape, 19 mm roll (for loose cell terminals, WML-DEC-001 F3)",
          Pos(hx0 + 185, hy0 + 250, zs) * wp.tape_roll(), "matte_black", kind="bought", bom=5, key="hazard", group="hazard")
    # 7 Platform scale: feet, pan, load cell, platform and rubber mat, column with foot collar, head and display
    sx0, sy0 = p["scale_x0"], p["scale_y0"]
    sl, sd = p["scale_l"], p["scale_d"]
    colx, coly = sx0 + sl / 2, sy0 + sd - 25
    for fx in (sx0 + 30, sx0 + sl - 30):
        for fy in (sy0 + 30, sy0 + sd - 40):
            P.add("Scale foot (rubber)", cp.break_edges(Pos(fx, fy, 0) * Cylinder(15.0, 8.0, align=None), 2.0),
                  "epdm", kind="bought", bom=7, key="scale", group="scale")
    pan = wp.rbox(sx0, sx0 + sl, sy0, sy0 + sd, 8, 50, r=4.0, edge=0) - wp.rbox(sx0 + 1.5, sx0 + sl - 1.5, sy0 + 1.5, sy0 + sd - 1.5, 9.5, 51, r=3.0, edge=0)
    P.add("Scale base pan (1.5 mm steel, painted)", cp.break_edges(pan, 0.4), "painted_steel", kind="bought", bom=7, key="scale", group="scale")
    cell = wp.rbox(colx - 65, colx + 65, sy0 + sd / 2 - 35, sy0 + sd / 2 - 5, 9.5, 52, r=1.0, edge=0.8) \
        - _hole_y(colx, 30.75, 12.0, sy0, sy0 + sd)
    P.add("Scale load cell (single point, aluminium)", cell, "aluminium", kind="bought", bom=7, key="scale", group="scale")
    plat = wp.rbox(sx0 + 2, sx0 + sl - 2, sy0 + 2, coly - 20, 52, 55, r=3.0, edge=0.6)
    P.add("Scale platform (3 mm stainless)", plat, "stainless", kind="bought", bom=7, key="scale", group="scale")
    P.add("Scale rubber mat", wp.rbox(sx0 + 15, sx0 + sl - 15, sy0 + 15, coly - 33, 55, 58, r=6.0, edge=0.8), "epdm",
          kind="bought", bom=7, key="scale", group="scale")
    P.add("Scale column foot collar", Pos(colx, coly, 9.5) * cp.bush(44.0, 28.0, 30.0), "painted_steel", kind="bought", bom=7,
          key="scale", group="scale")
    col = Pos(colx, coly, 9.5) * cp.round_tube(28.0, 2.0, p["scale_col_h"] - 9.5 + 20)
    P.add("Scale column (28 mm steel tube)", col, "painted_steel", kind="bought", bom=7, key="scale", group="scale")
    hx, hy, hz = p["scale_head"]
    zh = p["scale_col_h"]
    head = wp.rbox(colx - hx / 2, colx + hx / 2, coly - hy / 2, coly + hy / 2, zh, zh + hz, r=6.0, edge=2.0) \
        - Pos(colx, coly, zh - 1) * Cylinder(14.0, 21.0, align=None)
    head = head - _box(colx - 55, colx + 55, coly - hy / 2 - 1, coly - hy / 2 + 1, zh + 45, zh + 85)
    P.add("Scale head (display and keys)", head, "matte_black", kind="bought", bom=7, key="scale", group="scale")
    P.add("Scale display window", wp.rbox(colx - 55, colx + 55, coly - hy / 2 - 0.9, coly - hy / 2 + 0.9, zh + 45, zh + 85, r=2.0, edge=0.2),
          "glass", kind="bought", bom=7, key="scale", group="scale", color="#86EFAC")


# ---------------------------------------------------------------------------------------------------------------
# Option A: phone stand over a mat (the current design)
# ---------------------------------------------------------------------------------------------------------------
STAND_KEYS = ["base", "foot_r", "foot_l", "post", "arm", "plate_r", "plate_l", "tray", "clamps", "fixings"]


def option_a(params=None):
    import cad_parts as cp
    import wml_parts as wp
    from build123d import Plane, Polyline, Pos, Rot, Vector, extrude, make_face
    p = derived(params)
    P = _Parts()
    TOP, Z0 = p["bench_h"], p["mat_top"]
    t, w = p["tube_t"], p["tube"]
    px, py = p["post_x"], p["post_y"]
    x0, x1 = px - w / 2, px + w / 2
    T, BT = p["arm_z"], p["base_top"]
    fl, ft, fn = p["foot_leg"], p["foot_t"], p["foot_len"]
    foot_bolt_z = (BT + 15.0, BT + 40.0)
    plate_post_z = (T - 45.0, T - 85.0)
    ay0, ay1 = p["arm_y0"], p["arm_y1"]
    plate_arm_y = (ay1 - 62.5, ay1 - 22.5)
    tab_y = (ay0 + 16.0, ay0 + 46.0)
    p["_tab_y"], p["_plate_arm_y"], p["_plate_post_z"], p["_foot_bolt_z"] = tab_y, plate_arm_y, plate_post_z, foot_bolt_z

    _bench(P, p)

    # 3 Sorting mat: 4 mm hardboard, painted and sealed on both faces and all edges (WML-DEC-001 F2)
    mat = Pos(p["mat_cx"], p["mat_cy"], TOP) * cp.sheet(p["mat_l"], p["mat_d"], p["mat_t"], r_corner=3.0, edge=0.5)
    P.add("Sorting mat (4 mm hardboard, matte light grey, sealed all over)", mat, "label", bom=3, key="mat", group="rig",
          color="#CBD0D6")

    # 2a Base board, 18 mm plywood, with four 3 mm pilot holes for the foot angle screws
    base = cp.break_edges(_box(px - p["base_l"] / 2, px + p["base_l"] / 2, p["base_y"], p["base_y"] + p["base_d"], TOP, BT), 1.0)
    screw_pts = [(px + sgn * (fl / 2 + ft / 2 + w / 2), py + dy) for sgn in (1, -1) for dy in (-20.0, 20.0)]
    for sx, sy in screw_pts:
        base = base - _hole_z(sx, sy, 3.0, BT - 12.0, BT + 1.0)
    P.add("Base board (18 mm plywood, 240 x 90)", base, "plywood", bom=2, key="base", group="stand")
    p["_foot_screw"] = [(sx - px, sy) for sx, sy in screw_pts]

    # 2b Foot angles (2)
    _foot_angles(P, x0, x1, py, BT, fl, ft, fn, foot_bolt_z, (-20.0, 20.0), 5, 2, "foot_r", "foot_l", "")

    # 2c Post: 25 x 25 x 2 square aluminium tube
    post = Pos(px, py, BT) * cp.shs(w, t, p["post_len"])
    for zb in foot_bolt_z + plate_post_z:
        post = post - _hole_x(py, zb, 5.5)
    P.add(f"Post (25 x 25 x 2 aluminium tube, {p['post_len']:.0f} long)", post, "aluminium", bom=2, key="post", group="stand")

    # 2d Arm: the same tube along Y, butting the post's front face
    arm = Pos(px, ay0, p["arm_bot"] + w / 2) * Rot(-90, 0, 0) * cp.shs(w, t, p["arm_len"])
    for yy in plate_arm_y:
        arm = arm - _hole_x(yy, T - w / 2, 5.5)
    for yy in tab_y:
        arm = arm - _hole_z(px, yy, 5.5)
    P.add(f"Arm (25 x 25 x 2 aluminium tube, {p['arm_len']:.1f} long)", arm, "aluminium", bom=2, key="arm", group="stand")

    # 2e Corner plates (2)
    holes = [(yy, T - w / 2, 5.5) for yy in plate_arm_y] + [(py, zb, 5.5) for zb in plate_post_z]
    _corner_plates(P, x1, x0, p["cp_t"], ay1 - p["cp_reach"], py + w / 2, ay1, T, p["cp_drop"], w, holes, 2, "plate_r", "plate_l", "")

    # 2f Phone tray: 2 mm aluminium folded up along both long edges, camera window, tab under the arm end
    tt, lip = p["tray_t"], p["tray_lip"]
    tx0, tx1, ty0, ty1 = p["tray_x0"], p["tray_x1"], p["tray_y0"], p["tray_y1"]
    zb0, zb1 = p["tray_bot"], p["tray_top"]
    tray = _box(tx0, tx1, ty0, ty1, zb0, zb1)
    tray = tray + _box(tx0, tx1, ty0, ty0 + tt, zb1, zb1 + lip)
    tab_x0, tab_x1 = px - p["tab_w"] / 2, px + p["tab_w"] / 2
    tray = tray + _box(tab_x1 + 3.0, tx1, ty1 - tt, ty1, zb1, zb1 + lip)
    tray = tray + _box(tab_x0, tab_x1, ty1, ty1 + p["tab_l"], zb0, zb1)
    hw = p["win"] / 2
    tray = tray - _box(p["mat_cx"] - hw, p["mat_cx"] + hw, p["mat_cy"] - hw, p["mat_cy"] + hw, zb0 - 1, zb1 + 1)
    for yy in tab_y:
        tray = tray - _hole_z(px, yy, 5.5)
    tray = cp.break_edges(tray, 0.5)
    P.add("Phone tray (2 mm aluminium sheet, folded)", tray, "aluminium", bom=2, key="tray", group="stand")

    # 1 Phone (bought): body and screen glass, camera bump in the tray window
    body, glass = wp.phone(p["phone_l"], p["phone_w"], p["phone_t"], lens_dx=-p["lens_offset"])
    P.add("Smartphone running the model (reference Android phone)", Pos(p["phone_cx"], p["mat_cy"], zb1) * body, "matte_black",
          kind="bought", bom=1, key="phone", group="rig")
    P.add("Smartphone screen glass", Pos(p["phone_cx"], p["mat_cy"], zb1) * glass, "glass", kind="bought", bom=1, key="phone",
          group="rig", color="#1F2937")

    # 11 G-clamps (2): upper jaw on the board, swivel pad under the bench top
    _clamps(P, p["clamp_x"], p["base_y"] + p["base_d"] - 40.0, p["bench_d"] + 5.0, BT, TOP - p["bench_top_t"], 11, "clamps")

    # 11 Fixings: M5 bolts with washers and nyloc nuts, wood screws
    for zb in foot_bolt_z:
        P.extend_sets(wp.bolt_set(5, w + 2 * ft, "+x", (x1 + ft, py, zb), "foot angles to post"), "fixings", "foot")
    for zb in plate_post_z:
        P.extend_sets(wp.bolt_set(5, w + 2 * p["cp_t"], "+x", (x1 + p["cp_t"], py, zb), "corner plates to post"), "fixings", "plate")
    for yy in plate_arm_y:
        P.extend_sets(wp.bolt_set(5, w + 2 * p["cp_t"], "+x", (x1 + p["cp_t"], yy, T - w / 2), "corner plates to arm"), "fixings", "plate")
    for yy in tab_y:
        P.extend_sets(wp.bolt_set(5, w + tt, "+z", (px, yy, T), "tray tab to arm", extra=1.0), "fixings", "tab")
    for sx, sy in screw_pts:
        P.add("Wood screw No. 8 x 16 pan head (foot angle to base board)", Pos(sx, sy, BT + ft) * wp.wood_screw(16.0),
              "zinc_plated", kind="fastener", bom=11, key="fixings", group="fixings")
        P[-1]["joint"] = "screw"

    # 6 Power bank, its USB cable with a plug at each end, and four cable ties
    pb_cx, pb_cy = p["pb_x0"] + p["pb_l"] / 2, p["pb_y0"] + p["pb_d"] / 2
    P.add("Power bank, 10,000 mAh", Pos(pb_cx, pb_cy, TOP) * wp.power_bank(p["pb_l"], p["pb_d"], p["pb_t"]), "matte_black",
          kind="bought", bom=6, key="powerbank", group="rig")
    r = p["cable_r"]
    port_y, port_z = pb_cy + 20.0, TOP + p["pb_t"] / 2
    P.add("USB-C plug at the power bank", Pos(p["pb_x0"] - 5.5, port_y, port_z) * wp.usb_plug(12.0), "matte_black",
          kind="bought", bom=6, key="cable", group="rig")
    pz_mid = zb1 + (p["phone_t"] - 0.8) / 2
    phone_x0 = p["phone_cx"] - p["phone_l"] / 2
    P.add("USB-C plug at the phone", Pos(phone_x0 - 5.5, p["mat_cy"], pz_mid) * wp.usb_plug(12.0), "matte_black",
          kind="bought", bom=6, key="cable", group="rig")
    yb_c = py + w / 2 + r
    zc = BT + 17.0 + r
    zt = T + r
    xa = px + p["cable_arm_dx"]
    xe = phone_x0 - 14.0
    pts = [(p["pb_x0"] - 5.5, port_y, port_z), (p["pb_x0"] - 18.0, port_y + 10.0, zc), (px, port_y + 10.0, zc),
           (px, yb_c, zc + 10), (px, yb_c, zt), (xa, py - w / 2 - 6.0, zt), (xa, ay0 + 6.0, zt), (xe, p["tray_y1"] - 4, zt),
           (xe, p["mat_cy"], pz_mid), (phone_x0 - 5.5, p["mat_cy"], pz_mid)]
    P.add("USB cable, 1.5 m", cp.rope(pts, 2 * r), "epdm", kind="bought", bom=6, key="cable", group="rig", color="#374151")
    p["_cable_len"] = sum(math.dist(a, b) for a, b in zip(pts[:-1], pts[1:]))
    for zz in (BT + 100.0, BT + 270.0):
        _tie(P, (px, py + r, zz), w + 0.2, w + 2 * r + 0.2, "xy", "cable to the post", "ties")
    for yy in (ay0 + 76.0, ay0 + 116.0):
        _tie(P, (px, yy, p["arm_bot"] + (w + 2 * r) / 2), w + 0.2, w + 2 * r + 0.2, "xz", "cable to the arm", "ties")

    # 12 Bluetooth shutter button on a hook-and-loop pad at the bench edge (WML-DEC-001 F1)
    bx, by = p["btn_x"], p["btn_y"]
    P.add("Hook-and-loop pad (shutter button to bench)", wp.rbox(bx - 15, bx + 15, by - 10, by + 10, TOP, TOP + 2.0, r=3.0, edge=0.4),
          "matte_black", kind="fastener", bom=12, key="remote", group="rig")
    bb, btn = wp.shutter_button(p["btn_l"], p["btn_w"], p["btn_t"])
    P.add("Bluetooth shutter button body (one CR2032 cell)", Pos(bx, by, TOP + 2.0) * bb, "matte_black", kind="bought", bom=12,
          key="remote", group="rig")
    P.add("Bluetooth shutter button key", Pos(bx, by, TOP + 2.0) * btn, "epdm", kind="bought", bom=12, key="remote", group="rig",
          color="#0F766E")

    _station_items(P, p)
    P.p = p
    return P


# ---------------------------------------------------------------------------------------------------------------
# Option B: tray detector (alternative)
# ---------------------------------------------------------------------------------------------------------------
def option_b(params=None):
    import cad_parts as cp
    import wml_parts as wp
    from build123d import Cylinder, Pos, Rot
    p = derived(params)
    P = _Parts()
    TOP = p["bench_h"]
    m, mt = p["b_mast"], p["b_mast_t"]
    BT = TOP + p["b_base_t"]
    mx, my = p["post_x"], p["b_mast_y"]
    x0, x1 = mx - m / 2, mx + m / 2
    yb0 = p["b_base_y"]
    cam_y = p["b_tray_cy"]
    _bench(P, p)

    # Sorting tray, bought: polypropylene, 600 x 400 x 40, 3 mm wall, its back edge on the board's front edge
    tl, td, th, tw = p["b_tray_l"], p["b_tray_d"], p["b_tray_h"], p["b_tray_t"]
    tr = wp.rbox(mx - tl / 2, mx + tl / 2, yb0 - td, yb0, TOP, TOP + th, r=20.0, edge=0) \
        - wp.rbox(mx - tl / 2 + tw, mx + tl / 2 - tw, yb0 - td + tw, yb0 - tw, TOP + tw, TOP + th + 1, r=17.0, edge=0)
    P.add("Sorting tray (600 x 400 x 40 polypropylene)", cp.break_edges(tr, 0.8), "hdpe_natural", kind="bought", group="rig",
          color="#CBD0D6")

    # Base board and foot angles, as option A but for the 40 mm mast
    base = cp.break_edges(_box(mx - p["b_base_l"] / 2, mx + p["b_base_l"] / 2, yb0, p["bench_d"], TOP, BT), 1.0)
    screw_dy = (-25.0, 25.0)
    pts = [(mx + sgn * (25.0 + 1.5 + m / 2), my + dy) for sgn in (1, -1) for dy in screw_dy]
    for sx, sy in pts:
        base = base - _hole_z(sx, sy, 3.0, BT - 12.0, BT + 1.0)
    P.add("Base board (18 mm plywood, 300 x 120)", base, "plywood", group="stand")
    fbz = (BT + 15.0, BT + 40.0)
    _foot_angles(P, x0, x1, my, BT, 50.0, 3.0, 80.0, fbz, screw_dy, 6, None, None, None, ", mast")
    _wood_screws(P, pts, BT + 3.0, None, None, "foot angle to base board")

    # Mast and arm, 40 x 40 x 2 tube; corner plates
    arm_bot = p["b_lens_z"] + 30.0
    T = arm_bot + m
    mast = Pos(mx, my, BT) * cp.shs(m, mt, T - BT)
    plate_post_z = (T - 60.0, T - 110.0)
    case_z = 950.0
    case_bolt_z = (case_z - 57.0, case_z + 57.0)
    disp_bolt_z = (p["b_disp_z"] - 30.0, p["b_disp_z"] + 30.0)
    for zb in fbz + plate_post_z + case_bolt_z:
        mast = mast - _hole_x(my, zb, 5.5 if zb not in fbz else 6.5)
    for zb in disp_bolt_z:
        mast = mast - _hole_y(mx, zb, 5.5)
    P.add(f"Mast (40 x 40 x 2 aluminium tube, {T - BT:.0f} long)", mast, "aluminium", group="stand")
    ay0, ay1 = cam_y - 36.0, my - m / 2
    arm = Pos(mx, ay0, arm_bot + m / 2) * Rot(-90, 0, 0) * cp.shs(m, mt, ay1 - ay0)
    plate_arm_y = (ay1 - 80.0, ay1 - 30.0)
    for yy in plate_arm_y:
        arm = arm - _hole_x(yy, T - m / 2, 5.5)
    hous_y = (cam_y - 26.0, cam_y + 26.0)
    for yy in hous_y:
        arm = arm - _hole_z(mx, yy, 5.5)
    P.add(f"Arm (40 x 40 x 2 aluminium tube, {ay1 - ay0:.0f} long)", arm, "aluminium", group="stand")
    holes = [(yy, T - m / 2, 5.5) for yy in plate_arm_y] + [(my, zb, 5.5) for zb in plate_post_z]
    _corner_plates(P, x1, x0, 3.0, ay1 - 110.0, my + m / 2, ay1, T, 140.0, m, holes, None, None, None, ", mast")

    # Camera housing (printed PETG, drawn in black HDPE) under the arm end, Camera Module 3 Wide inside
    zf = p["b_lens_z"] + 6.6                      # top of the housing floor
    hz0, hz1 = zf - 2.5, arm_bot
    hous = wp.rbox(mx - 20, mx + 20, cam_y - 20, cam_y + 20, hz0, hz1, r=4.0, edge=0) \
        - wp.rbox(mx - 17.5, mx + 17.5, cam_y - 17.5, cam_y + 17.5, zf, hz1 + 1, r=2.0, edge=0)
    hous = hous + _box(mx - 10, mx + 10, cam_y - 34, cam_y + 34, hz1 - 4, hz1)           # ears along the arm
    hous = hous - Pos(mx, cam_y - 2.0, hz0 - 1) * Cylinder(5.0, 5.0, align=None)
    hous = hous - _box(mx - 9, mx + 9, cam_y + 16, cam_y + 21, hz1 - 9, hz1 - 5)           # ribbon slot in the +Y wall
    for yy in hous_y:
        hous = hous - _hole_z(mx, yy, 5.5)
    for bx_, by_ in ((-10.5, -3.0), (10.5, -3.0), (-10.5, 9.5), (10.5, 9.5)):
        boss = Pos(mx + bx_, cam_y + by_, zf) * (Cylinder(2.4, 5.0, align=None) - Cylinder(0.8, 6.0, align=None))
        hous = hous + boss
    hous = cp.break_edges(hous, 0.4)
    P.add("Camera housing (printed PETG)", hous, "hdpe_black", group="camera")
    cam = Pos(mx, cam_y, zf + 6.0) * Rot(0, 0, 180) * wp.camera_module_3()
    P.add("Camera Module 3 Wide (12 MP, 102 deg horizontal)", cam, "matte_black", kind="bought", group="camera", color="#14532D")
    for bx_, by_ in ((-10.5, -3.0), (10.5, -3.0), (-10.5, 9.5), (10.5, 9.5)):
        P.add("M2 pan screw x 6 (ISO 7045, camera board to housing)", Pos(mx + bx_, cam_y + by_, zf + 6.0) * wp.pan_screw(2.0, 6.0),
              "stainless", kind="fastener", group="camera")
    for yy in hous_y:
        P.extend_sets(wp.bolt_set(5, m + 4.0, "+z", (mx, yy, T), "camera housing to arm"), None, "camera")

    # Raspberry Pi 5 in a printed two-part case on the mast's +X face, with the active cooler
    cz = case_z
    fl0 = x1                                      # flange on the mast face
    case_base = wp.rbox(fl0, fl0 + 3.0, my - 33, my + 33, cz - 68, cz + 68, r=3.0, edge=0.6)
    shell = wp.rbox(fl0 + 3.0, fl0 + 20.0, my - 33, my + 33, cz - 47.5, cz + 47.5, r=3.0, edge=0) \
        - wp.rbox(fl0 + 5.0, fl0 + 21.0, my - 31, my + 31, cz - 45.5, cz + 45.5, r=2.0, edge=0)
    case_base = case_base + shell
    for zb in case_bolt_z:
        case_base = case_base - _hole_x(my, zb, 5.5)
    pcb_x = fl0 + 9.0                             # PCB back face
    holes_pi = [(cz - hx_, my + hy_) for hx_, hy_ in wp.pi5_holes()]
    for hz_, hy_ in holes_pi:
        case_base = case_base + Pos(fl0 + 5.0, hy_, hz_) * Rot(0, 90, 0) * (Cylinder(3.0, 4.0, align=None) - Cylinder(1.0, 5.0, align=None))
    case_base = case_base - Pos(fl0 + 12.0, my - 20.0, cz - 50.0) * Cylinder(3.5, 10.0, align=None)        # gland hole, power
    case_base = case_base - Pos(fl0 + 12.0, my + 20.0, cz - 50.0) * Cylinder(3.0, 10.0, align=None)        # gland hole, button wire
    case_base = case_base - _box(fl0 + 8, fl0 + 16, my - 9, my + 9, cz + 44, cz + 48)                      # slot, camera ribbon
    P.add("Pi 5 case base with mast flange (printed PETG)", cp.break_edges(case_base, 0.4), "hdpe_black", group="computer")
    lid = wp.rbox(fl0 + 20.0, fl0 + 34.0, my - 33, my + 33, cz - 47.5, cz + 47.5, r=3.0, edge=0) \
        - wp.rbox(fl0 + 19.0, fl0 + 32.0, my - 31, my + 31, cz - 45.5, cz + 45.5, r=2.0, edge=0)
    for k in range(5):
        lid = lid - _box(fl0 + 31, fl0 + 35, my - 22, my + 22, cz - 20 + k * 8, cz - 17 + k * 8)
    P.add("Pi 5 case lid, vented, snap-fit (printed PETG)", cp.break_edges(lid, 0.4), "hdpe_black", group="computer")
    pi = Pos(pcb_x, my, cz) * Rot(0, 90, 0) * wp.pi5_board()
    P.add("Raspberry Pi 5 board, 4 GB", pi, "matte_black", kind="bought", group="computer", color="#166534")
    cool = Pos(pcb_x + 1.6 + 2.4, my + 0.5, cz + 5.0) * Rot(0, 90, 0) * wp.active_cooler()
    P.add("Raspberry Pi 5 active cooler", cool, "cast_aluminium", kind="bought", group="computer")
    for hz_, hy_ in holes_pi:
        P.add("M2.5 pan screw x 8 (ISO 7045, Pi board to case standoff)", Pos(pcb_x + 1.6, hy_, hz_) * Rot(0, 90, 0) * wp.pan_screw(2.5, 8.0),
              "stainless", kind="fastener", group="computer")
    for zb in case_bolt_z:
        P.extend_sets(wp.bolt_set(5, m + 3.0, "+x", (fl0 + 3.0, my, zb), "Pi case flange to mast"), None, "computer")

    # 5 inch touch display on a 2 mm aluminium plate bolted to the mast's +Y (user) face, on four spacers
    dw, dh, dt = p["b_disp"]
    dz = p["b_disp_z"]
    yp = my + m / 2
    plate = wp.rbox(mx - 80, mx + 80, yp, yp + 2.0, dz - 50, dz + 50, r=4.0, edge=0.5)
    dholes = [(mx + sx_, dz + sz_) for sx_ in (-dw / 2 + 12, dw / 2 - 12) for sz_ in (-dh / 2 + 10, dh / 2 - 10)]
    for hx_, hz_ in dholes:
        plate = plate - _hole_y(hx_, hz_, 2.9)
    for zb in disp_bolt_z:
        plate = plate - _hole_y(mx, zb, 5.5)
    P.add("Display mounting plate (2 mm aluminium)", plate, "aluminium", group="display")
    for hx_, hz_ in dholes:
        P.add("Display spacer (nylon, 12 mm)", Pos(hx_, yp + 2.0, hz_) * Rot(-90, 0, 0) * cp.bush(6.0, 2.9, 12.0), "hdpe_natural",
              kind="bought", group="display")
        P.add("M2.5 pan screw x 18 (ISO 7045, display to plate)", Pos(hx_, yp, hz_) * Rot(90, 0, 0) * wp.pan_screw(2.5, 18.0),
              "stainless", kind="fastener", group="display")
    dtray, dglass = wp.touch_display(dw, dh, dt)
    place = lambda s: Pos(mx, yp + 14.0, dz) * Rot(-90, 0, 0) * s  # noqa: E731
    P.add("Touch Display 2, 5 inch (back tray and panel)", place(dtray), "matte_black", kind="bought", group="display")
    P.add("Touch display glass", place(dglass), "glass", kind="bought", group="display", color="#111827")
    for zb in disp_bolt_z:
        P.extend_sets(wp.bolt_set(5, m + 2.0, "-y", (mx, my - m / 2, zb), "display plate to mast"), None, "display")

    # Arcade button in a folded steel box at the bench edge, wired to the Pi
    bx, by = p["b_btn_x"], p["b_btn_y"]
    box_ = wp.rbox(bx - 35, bx + 35, by - 35, by + 35, TOP, TOP + 45, r=3.0, edge=0) \
        - wp.rbox(bx - 33.5, bx + 33.5, by - 33.5, by + 33.5, TOP - 1, TOP + 43.5, r=1.5, edge=0)
    box_ = box_ + _box(bx - 50, bx - 35, by - 15, by + 15, TOP, TOP + 1.5) + _box(bx + 35, bx + 50, by - 15, by + 15, TOP, TOP + 1.5)
    box_ = box_ - Pos(bx, by, TOP + 40) * Cylinder(12.0, 10.0, align=None)
    box_ = box_ - _hole_z(bx - 43, by, 4.5) - _hole_z(bx + 43, by, 4.5) - _hole_y(bx, TOP + 15, 6.0, by, by + 40)
    P.add("Button box (1.5 mm steel, folded)", cp.break_edges(box_, 0.4), "painted_steel", group="button")
    cap, sw, nut = wp.arcade_button(30.0, 1.5)
    P.add("Arcade push button, 30 mm (bezel and cap)", Pos(bx, by, TOP + 45) * cap, "hdpe_natural", kind="bought", group="button",
          color="#0F766E")
    P.add("Arcade push button switch body", Pos(bx, by, TOP + 45) * sw, "hdpe_black", kind="bought", group="button")
    P.add("Arcade push button nut", Pos(bx, by, TOP + 45) * nut, "hdpe_black", kind="fastener", group="button")
    _wood_screws(P, [(bx - 43, by), (bx + 43, by)], TOP + 1.5, None, None, "button box to bench")

    # Power bank (20,000 mAh) and cables: power to the Pi, the button wire and the camera ribbon (drawn round)
    pl_, pd_, pt_ = p["b_pb"]
    P.add("Power bank, 20,000 mAh USB-C PD", Pos(p["b_pb_x0"] + pl_ / 2, p["b_pb_y0"] + pd_ / 2, TOP) * wp.power_bank(pl_, pd_, pt_),
          "matte_black", kind="bought", group="computer")
    gl_x = fl0 + 12.0
    pw = [(p["b_pb_x0"] - 2.5, p["b_pb_y0"] + pd_ / 2 + 20, TOP + pt_ / 2), (p["b_pb_x0"] - 30, p["b_pb_y0"] + pd_ / 2 + 20, TOP + pt_ + 20),
          (gl_x + 20, my - 20.0, cz - 120), (gl_x, my - 20.0, cz - 60), (gl_x, my - 20.0, cz - 48.0)]
    P.add("USB-C power cable to the Pi, 1 m", cp.rope(pw, 5.0), "epdm", kind="bought", group="computer", color="#374151")
    bw = [(bx, by + 35, TOP + 15), (bx, by + 60, TOP + 15), (bx + 120, by + 60, TOP + 60), (x1 + 30.0, by + 60, TOP + 90),
          (gl_x + 30, my + 20.0, TOP + 100), (gl_x, my + 20.0, cz - 60), (gl_x, my + 20.0, cz - 48.0)]
    P.add("Button wire to the Pi GPIO, 1.2 m", cp.rope(bw, 4.0), "epdm", kind="bought", group="button", color="#B91C1C")
    rb = [(mx, cam_y + 14.0, zf + 7.0), (mx, cam_y + 19.0, hz1 - 7.0), (mx + 12.0, cam_y + 24.0, hz1 - 7.0),
          (mx + 12.0, ay1 - 1.5, arm_bot - 1.5), (mx + 12.0, ay1 - 1.5, T - 150.0), (x1 + 12.0, ay1 - 1.5, T - 150.0),
          (x1 + 12.0, my, cz + 52.0), (fl0 + 12.0, my, cz + 46.0)]
    P.add("Camera ribbon cable, 300 mm (FFC, drawn round)", cp.rope(rb, 2.0), "matte_black", kind="bought", group="camera")

    # G-clamps and cable ties
    _clamps(P, p["b_clamp_x"], p["bench_d"] - 40.0, p["bench_d"] + 5.0, BT, TOP - p["bench_top_t"], None, "clamps")
    for yy in (ay0 + 90.0, ay0 + 150.0):
        _tie(P, (mx, yy, arm_bot + m / 2 - 1.5), m + 0.2, m + 3.4, "xz", "camera ribbon to the arm", None)

    _station_items(P, p)
    P.p = p
    return P


_CACHE = {}


def components(option=None):
    """kit 1.9: list of cad_parts.part() dicts for an option (A or B)."""
    option = option or CHOSEN
    if option not in _CACHE:
        if option == "A":
            _CACHE[option] = option_a()
        elif option == "B":
            _CACHE[option] = option_b()
        else:
            raise ValueError(f"unknown option {option}")
    out = []
    for d in _CACHE[option]:
        q = dict(d)
        q["shape"] = copy.copy(d["shape"])
        out.append(q)
    return out


# ---------------------------------------------------------------------------------------------------------------
# Legacy interface for the drawing, build plan pictures, concept media and calculations
# ---------------------------------------------------------------------------------------------------------------
def build_components(params=None):
    """Named shapes of the option A scanning rig, keyed as the build plan pictures expect (base, foot_r, foot_l,
    post, arm, plate_r, plate_l, tray, clamps, fixings, mat, phone, powerbank, cable, remote, ties), each one
    makeable as described in docs/05-build-plan.md, plus '_p' with the derived parameters."""
    P = option_a(params) if params is not None else _CACHE.setdefault("A", option_a())
    C = {}
    by = {}
    for d in P:
        if d["key"]:
            by.setdefault(d["key"], []).append(d["shape"])
    for k, shapes in by.items():
        if k in ("bins", "bin_labels"):
            C[k] = [copy.copy(s) for s in shapes]
        elif len(shapes) == 1:
            C[k] = copy.copy(shapes[0])
        else:
            C[k] = _group(shapes)
    C["fixing_groups"] = {}
    for j in ("foot", "plate", "tab", "screw"):
        C["fixing_groups"][j] = _group([d["shape"] for d in P if d.get("joint") == j])
    C["_p"] = P.p
    return C


def build_parts(params=None):
    """Return a dict of named build123d shapes, plus '_p' with the derived parameters (concept media and drawings)."""
    C = build_components(params)
    stand = _group([C[k] for k in STAND_KEYS])
    return {"bench": C["bench"], "mat": C["mat"], "phone": C["phone"], "stand": stand,
            "powerbank": _group([C["powerbank"], C["cable"], C["ties"]]), "remote": C["remote"],
            "hazard": C["hazard"], "hazard_lid": C["hazard_lid"], "bins": C["bins"], "bin_labels": C["bin_labels"],
            "scale": C["scale"], "_p": C["_p"]}


def station(params=None, with_bench=True):
    """Station assembly of option A (the object on the general arrangement drawing)."""
    parts = components("A")
    return _group([d["shape"] for d in parts if d["kind"] != "context" or (with_bench and d["key"] == "bench")])


def bench_group(params=None):
    """Bench, mat, phone, stand, power bank, shutter button and hazard box only (for the bench detail view)."""
    keep = {"bench", "mat", "phone", "powerbank", "cable", "ties", "remote", "hazard", "hazard_lid"} | set(STAND_KEYS)
    return _group([d["shape"] for d in components("A") if d["key"] in keep])


def check(params=None, verbose=True):
    """Constructability checks on the rig: parts that must touch do, parts that must not are apart
    by at least the stated clearance, and the stand is outside the camera picture."""
    C = build_components(params)
    p = C["_p"]
    res = []

    def gap(a, b):
        A = C[a] if isinstance(a, str) else a
        B = C[b] if isinstance(b, str) else b
        inter = (A & B).volume if hasattr(A & B, "volume") else 0.0
        return (-inter if inter > 1e-3 else A.distance_to(B))

    def touch(a, b, why):
        g = gap(a, b); res.append((f"touch  {a} / {b}: {why}", abs(g) < 0.05, g))

    def apart(a, b, mn, why):
        g = gap(a, b); res.append((f"apart  {a} / {b} >= {mn} mm: {why}", g >= mn - 1e-6, g))
    touch("base", "mat", "board front edge meets the mat's back edge")
    touch("foot_r", "base", "flat leg on the board"); touch("foot_l", "base", "flat leg on the board")
    touch("foot_r", "post", "upright leg on the post face"); touch("foot_l", "post", "upright leg on the post face")
    touch("post", "base", "post stands on the board")
    touch("arm", "post", "arm butts the post's front face")
    touch("plate_r", "post", "corner plate on the post"); touch("plate_r", "arm", "corner plate on the arm")
    touch("plate_l", "post", "corner plate on the post"); touch("plate_l", "arm", "corner plate on the arm")
    touch("tray", "arm", "tab under the arm end")
    touch("phone", "tray", "phone back on the tray")
    touch("clamps", "base", "clamp jaw on the board")
    apart("arm", "phone", 2.0, "arm end clear of the phone")
    apart("arm", "tray", -0.05, "no overlap with the tray lip")
    apart("cable", "post", -0.05, "cable outside the post"); apart("cable", "arm", -0.05, "cable on top of the arm")
    apart("cable", "plate_r", 0.0, ""); apart("cable", "plate_l", 0.0, "")
    apart("cable", "tray", 0.0, "cable clear of the tray"); apart("cable", "clamps", 0.0, "cable clear of the clamps")
    apart("cable", "base", 0.0, "cable over the board"); apart("cable", "foot_r", 0.0, ""); apart("cable", "foot_l", 0.0, "")
    apart("cable", C["fixing_groups"]["tab"], 0.2, "cable clear of the tray tab bolts (F4)")
    apart("cable", C["fixing_groups"]["plate"], 0.2, "cable clear of the corner plate bolts")
    apart("powerbank", "clamps", 5.0, "room to lift the power bank"); apart("powerbank", "base", 5.0, "")
    apart("remote", "clamps", 20.0, "room to press the shutter button"); apart("remote", "base", 20.0, "")
    btm = p["bench_h"] - p["bench_top_t"]
    bench_frame = _group([s for s in (C["bench"].solids() if hasattr(C["bench"], "solids") else [C["bench"]])
                          if s.bounding_box().max.Z < btm + 1e-3])
    apart("clamps", bench_frame, 5.0, "clamps clear of the bench legs and rails")
    touch("clamps", "bench", "clamp pad under the bench top")
    names = [k for k in STAND_KEYS if k != "fixings"] + ["mat", "phone", "powerbank", "remote"]
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            v = (C[a] & C[b]).volume
            res.append((f"no overlap {a} / {b}", v < 1e-2, -v))
    # the stand stays out of the picture: frame edge at mat level, and at the board's top
    fe = p["frame_edge_y"]
    res.append((f"board front edge {p['base_y']:.1f} outside the frame edge {fe:.1f} at the mat", p["base_y"] > fe, p["base_y"] - fe))
    h = p["base_t"] - p["mat_t"]
    fe_top = p["mat_cy"] + p["frame_y"] / 2 * (p["cam_h"] - h) / p["cam_h"]
    res.append((f"board top edge outside the frame ({fe_top:.1f})", p["base_y"] > fe_top, p["base_y"] - fe_top))
    lens = p["tray_bot"] - p["mat_top"]
    res.append((f"lens {lens:.1f} mm above the mat (440)", abs(lens - p["cam_h"]) < 0.01, lens))
    res.append((f"cable path {p['_cable_len']:.0f} mm within a 1.5 m cable with slack", p["_cable_len"] < 1300, p["_cable_len"]))
    if verbose:
        for name, ok, g in res:
            print(("ok   " if ok else "FAIL ") + f"{name}  [{g:.2f}]")
        print(f"{sum(ok for _, ok, _ in res)} of {len(res)} checks pass")
    return res


def masses(option=None):
    """Mass in kg by BOM line (or group where a part has no BOM line)."""
    import cad_parts as cp
    out = {}
    for d in components(option):
        if d["kind"] == "context":
            continue
        k = d.get("bom") or d.get("group")
        out[k] = out.get(k, 0.0) + cp.mass_kg(d)
    return out


def export(out=None):
    """STL of option A at a 0.15 mm chord (STEP files come from .kit/cad_check.py --export)."""
    from build123d import export_stl
    out = Path(out) if out else HERE.parent
    (out / "stl").mkdir(exist_ok=True)
    tol = dict(tolerance=0.15, angular_tolerance=0.35)
    C = build_components()
    singles = {"station-assembly": station(with_bench=False),
               "phone-stand": _group([C[k] for k in STAND_KEYS] + [C["phone"]]),
               "sorting-mat": C["mat"], "hazard-box": _group([C["hazard"], C["hazard_lid"]]), "bin": C["bins"][0]}
    for k in ("base", "foot_r", "post", "arm", "plate_r", "tray"):
        singles[f"stand-{k.replace('_r', '').replace('_', '-')}"] = C[k]
    for name, shape in singles.items():
        export_stl(shape, str(out / "stl" / f"wastewise-{name}.stl"), **tol)
    return C


if __name__ == "__main__":
    if "--check" in sys.argv:
        r = check()
        sys.exit(0 if all(ok for _, ok, _ in r) else 1)
    C = export()
    p = C["_p"]
    for k, v in sorted(masses("A").items(), key=lambda kv: (isinstance(kv[0], str), str(kv[0]))):
        print(f"  option A, {'BOM line ' + str(k) if not isinstance(k, str) else k}: {v:.2f} kg")
    print(f"Lens height above floor {p['lens_z']:.0f} mm; above mat {p['cam_h']:.0f} mm")
    print(f"Camera frame on mat {p['frame_x']:.0f} x {p['frame_y']:.0f} mm; mat {p['mat_l']:.0f} x {p['mat_d']:.0f} mm")
    print(f"Stand: post {p['post_len']:.0f} mm, arm {p['arm_len']:.1f} mm; board front edge {p['base_y']:.0f}, frame edge {p['frame_edge_y']:.1f}")
    print(f"Bin inner volume {p['bin_vol_l']:.1f} L each, {p['bin_n']} bins")
    print("Wrote cad/stl/*.stl")
