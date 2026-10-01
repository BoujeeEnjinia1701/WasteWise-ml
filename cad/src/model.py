"""WasteWise-ml sorting station parametric model (build123d), TRL 3 massing-plus level.

Run from the repo root:  python cad/src/model.py          (exports STEP and STL into cad/step and cad/stl)
                         python cad/src/model.py --check  (constructability checks on the scanning rig)

WasteWise-ml is software. This model is the reference pilot sorting station where the
model is used: the site's bench, a light sorting mat, a phone on a made stand with its
rear camera pointing down at the mat, a hazard box, a power bank, seven bins by material
class and a platform scale. Numbered parts match bom/bom.csv (items 1 to 7).

Axes: X along the bench (bins to the +X side), Y away from the viewer (the user stands
at +Y, behind the bench), Z up, floor at Z = 0. Units: mm.

Detail level: the scanning rig (mat, phone stand, phone tray, power bank and cable) is
constructable (WML-DDR-003): every made part can be cut, drilled and folded as the build plan
WML-BLD-001 says, and every joint is face to face and bolted, screwed or clamped. The rest of
the station (bins, hazard box, scale) is bought and shown at massing level. PROTOTYPE BUILD
PLAN GEOMETRY; PRELIMINARY, NOT FOR FABRICATION BEYOND THE PROTOTYPE.
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
    # 2 Phone stand, made (WML-DDR-003): plywood base board clamped to the bench's back edge,
    #   square aluminium post and arm joined by two corner plates, two foot angles, and a folded
    #   phone tray hung from the arm end. The base board's front edge meets the mat's back edge.
    "base_l": 240.0, "base_d": 90.0, "base_t": 18.0,
    "tube": 25.0, "tube_t": 2.0,                      # 25 x 25 x 2 mm square aluminium tube (post and arm)
    "foot_leg": 50.0, "foot_t": 3.0, "foot_len": 60.0,  # foot angles, 50 x 50 x 3 mm angle
    "cp_t": 3.0, "cp_reach": 80.0, "cp_drop": 100.0,  # corner plates: reach along the arm, drop down the post
    "tray_t": 2.0, "tray_lip": 8.0, "tray_gap": 1.0, "tray_end": 5.0,
    "win": 34.0,                                      # window for the camera bump (bump 30 x 30 mm)
    "tab_w": 40.0, "tab_l": 65.0, "arm_gap": 3.0,     # tray tab under the arm end; arm end clear of the lip
    "clamp_x": (548.0, 752.0),                        # two G-clamps hold the base board to the bench
    "cable_r": 2.5,
    # 5 Hazard box (lidded steel, sand layer), on the bench's +X end
    "haz_l": 240.0, "haz_d": 320.0, "haz_h": 200.0, "haz_lid_t": 20.0, "haz_x0": 1130.0, "haz_y0": 60.0,
    # 6 Power bank
    "pb_l": 140.0, "pb_d": 70.0, "pb_t": 25.0, "pb_x0": 790.0, "pb_y0": 575.0,
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


def _fuse(shapes):
    out = None
    for sh in shapes:
        out = sh if out is None else out + sh
    return out


def _tube_y(x0, x1, y0, y1, z0, z1, t):
    """Square tube running along Y (open ends)."""
    return _box(x0, x1, y0, y1, z0, z1) - _box(x0 + t, x1 - t, y0 - 1, y1 + 1, z0 + t, z1 - t)


def _tube_z(x0, x1, y0, y1, z0, z1, t):
    """Square tube running along Z (open ends)."""
    return _box(x0, x1, y0, y1, z0, z1) - _box(x0 + t, x1 - t, y0 + t, y1 - t, z0 - 1, z1 + 1)


def _bolt_x(x0, x1, y, z, d=5.0, head=8.0):
    """Bolt along X from x0 to x1 with a hex-ish head and nut (round massing), centred at (y, z)."""
    from build123d import Solid, Plane, Vector
    r = d / 2
    shank = Solid.make_cylinder(r, x1 - x0 + 10, Plane(origin=Vector(x0 - 5, y, z), z_dir=Vector(1, 0, 0)))
    h1 = Solid.make_cylinder(head / 2, 4, Plane(origin=Vector(x0 - 4, y, z), z_dir=Vector(1, 0, 0)))
    h2 = Solid.make_cylinder(head / 2, 5, Plane(origin=Vector(x1, y, z), z_dir=Vector(1, 0, 0)))
    return shank + h1 + h2


def _bolt_z(x, y, z0, z1, d=5.0, head=8.0):
    from build123d import Solid, Plane, Vector
    shank = Solid.make_cylinder(d / 2, z1 - z0 + 10, Plane(origin=Vector(x, y, z0 - 5), z_dir=Vector(0, 0, 1)))
    h1 = Solid.make_cylinder(head / 2, 4, Plane(origin=Vector(x, y, z1), z_dir=Vector(0, 0, 1)))
    h2 = Solid.make_cylinder(head / 2, 5, Plane(origin=Vector(x, y, z0 - 5), z_dir=Vector(0, 0, 1)))
    return shank + h1 + h2


def _hole_x(y, z, d, x0=-1e4, x1=1e4):
    from build123d import Solid, Plane, Vector
    return Solid.make_cylinder(d / 2, x1 - x0, Plane(origin=Vector(x0, y, z), z_dir=Vector(1, 0, 0)))


def _hole_z(x, y, d, z0=-1e4, z1=1e4):
    from build123d import Solid, Plane, Vector
    return Solid.make_cylinder(d / 2, z1 - z0, Plane(origin=Vector(x, y, z0), z_dir=Vector(0, 0, 1)))


# Made and bought parts of the phone stand, in build order (the build plan follows this list).
STAND_KEYS = ["base", "foot_r", "foot_l", "post", "arm", "plate_r", "plate_l", "tray", "clamps", "fixings"]


def build_components(params=None):
    """Named solids of the scanning rig (mat, stand, phone, power bank and cable), each one
    makeable as described in docs/05-build-plan.md. Holes are cut where the fixings go."""
    from build123d import Polyline, make_face, extrude, Plane, Vector, Pos
    p = derived(params)
    TOP, Z0 = p["bench_h"], p["mat_top"]
    t, w = p["tube_t"], p["tube"]
    px, py = p["post_x"], p["post_y"]
    x0, x1 = px - w / 2, px + w / 2                      # post and arm faces
    T = p["arm_z"]
    BT = p["base_top"]
    C = {}

    # 3 Sorting mat: hardboard, painted (grid is printed, not cut)
    C["mat"] = _box(p["mat_x0"], p["mat_x0"] + p["mat_l"], p["mat_y0"], p["mat_y0"] + p["mat_d"], TOP, Z0)

    # 2a Base board: 18 mm plywood, front edge on the mat's back edge, back edge flush with the bench
    C["base"] = _box(px - p["base_l"] / 2, px + p["base_l"] / 2, p["base_y"], p["base_y"] + p["base_d"], TOP, BT)

    # 2b Foot angles (2): 50 x 50 x 3 angle, upright leg bolted to the post, flat leg screwed to the board
    fl, ft, fn = p["foot_leg"], p["foot_t"], p["foot_len"]
    fy0, fy1 = py - fn / 2, py + fn / 2
    foot_bolt_z = (BT + 15.0, BT + 40.0)
    screw_y = (py - 20.0, py + 20.0)
    for side, sgn in (("r", 1), ("l", -1)):
        xa = x1 if sgn > 0 else x0 - ft                # upright leg against the post face
        xb0, xb1 = (x1, x1 + fl) if sgn > 0 else (x0 - fl, x0)
        ang = _box(xa, xa + ft, fy0, fy1, BT, BT + fl) + _box(xb0, xb1, fy0, fy1, BT, BT + ft)
        for zb in foot_bolt_z:
            ang = ang - _hole_x(py, zb, 5.5)
        sx = (xb0 + xb1) / 2 + sgn * ft / 2
        for yy in screw_y:
            ang = ang - _hole_z(sx, yy, 4.5)
        C[f"foot_{side}"] = ang
    p["_foot_screw"] = [(sgn * (fl / 2 + ft / 2 + w / 2), yy) for sgn in (1, -1) for yy in screw_y]

    # 2c Post: 25 x 25 x 2 square aluminium tube, standing on the board between the foot angles
    post = _tube_z(x0, x1, py - w / 2, py + w / 2, BT, T, t)
    plate_post_z = (T - 45.0, T - 85.0)
    for zb in foot_bolt_z + plate_post_z:
        post = post - _hole_x(py, zb, 5.5)
    C["post"] = post

    # 2d Arm: the same tube, along Y, butting the post's front face; its end sits on the tray tab
    ay0, ay1 = p["arm_y0"], p["arm_y1"]
    arm = _tube_y(x0, x1, ay0, ay1, p["arm_bot"], T, t)
    plate_arm_y = (ay1 - 62.5, ay1 - 22.5)
    tab_y = (ay0 + 16.0, ay0 + 46.0)
    for yy in plate_arm_y:
        arm = arm - _hole_x(yy, T - w / 2, 5.5)
    for yy in tab_y:
        arm = arm - _hole_z(px, yy, 5.5)
    C["arm"] = arm

    # 2e Corner plates (2): 3 mm aluminium, one each side, bolted through the post and the arm
    yb, yf = py + w / 2, ay1 - p["cp_reach"]
    outline = [(yf, T), (yb, T), (yb, T - p["cp_drop"]), (ay1, T - p["cp_drop"]), (yf, T - w)]
    for side, xs in (("r", x1), ("l", x0 - p["cp_t"])):
        face = make_face(Polyline(*[(yy, zz) for yy, zz in outline], close=True))
        plate = Plane(origin=Vector(xs, 0, 0), x_dir=Vector(0, 1, 0), z_dir=Vector(1, 0, 0))
        cp = extrude(plate * face, p["cp_t"])
        for yy in plate_arm_y:
            cp = cp - _hole_x(yy, T - w / 2, 5.5)
        for zb in plate_post_z:
            cp = cp - _hole_x(py, zb, 5.5)
        C[f"plate_{side}"] = cp

    # 2f Phone tray: 2 mm aluminium sheet folded up along both long edges, window for the camera bump,
    #    tab bolted under the arm end. The +Y lip stops either side of the tab (only the outer run is kept).
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
    C["tray"] = tray

    # 1 Phone (bought): body on the tray, camera bump in the window
    pz0 = p["lens_z"]
    phone = _box(p["phone_cx"] - p["phone_l"] / 2, p["phone_cx"] + p["phone_l"] / 2,
                 p["mat_cy"] - p["phone_w"] / 2, p["mat_cy"] + p["phone_w"] / 2, pz0 + 2, pz0 + 2 + p["phone_t"])
    phone = phone + _box(p["mat_cx"] - 15, p["mat_cx"] + 15, p["mat_cy"] - 15, p["mat_cy"] + 15, pz0, pz0 + 2)
    C["phone"] = phone

    # Bought: two G-clamps holding the board to the bench (jaw on the board, pad under the bench top)
    cl = []
    yc0, yc1 = p["base_y"] + p["base_d"] - 40.0, p["bench_d"] + 15.0
    btm = TOP - p["bench_top_t"]
    for xc in p["clamp_x"]:
        cl.append(_box(xc - 8, xc + 8, yc0, yc1, BT, BT + 10)                    # upper jaw on the board
                  + _box(xc - 8, xc + 8, p["bench_d"] + 5, yc1, btm - 18, BT + 10)  # frame behind the bench edge
                  + _box(xc - 8, xc + 8, yc0, yc1, btm - 18, btm - 8)            # lower arm
                  + _box(xc - 10, xc + 10, yc0 + 5, yc0 + 25, btm - 8, btm))     # screw pad under the bench top
    C["clamps"] = _fuse(cl)

    # Bought fixings: M5 bolts with nyloc nuts (post foot, corner plates, tray tab), wood screws
    fx = []
    for zb in foot_bolt_z:
        fx.append(_bolt_x(x0 - ft, x1 + ft, py, zb))
    for zb in plate_post_z:
        fx.append(_bolt_x(x0 - p["cp_t"], x1 + p["cp_t"], py, zb))
    for yy in plate_arm_y:
        fx.append(_bolt_x(x0 - p["cp_t"], x1 + p["cp_t"], yy, T - w / 2))
    for yy in tab_y:
        fx.append(_bolt_z(px, yy, zb0, T))
    for dx, yy in p["_foot_screw"]:
        from build123d import Solid
        fx.append(Pos(px + dx, yy, BT + ft) * Solid.make_cylinder(4.0, 2.5)
                  + Pos(px + dx, yy, BT + ft - 16.0) * Solid.make_cylinder(2.0, 16.0))   # No. 8 x 16 wood screw
    C["fixings"] = _fuse(fx)

    # 6 Power bank and its 1.5 m cable: over the board behind the clamp jaw, up the post's back
    #   face, along the top of the arm, down to the phone's charging end
    C["powerbank"] = _box(p["pb_x0"], p["pb_x0"] + p["pb_l"], p["pb_y0"], p["pb_y0"] + p["pb_d"], TOP, TOP + p["pb_t"])
    r = p["cable_r"]
    yb_c = py + w / 2 + r
    zc = BT + 17.0 + r
    zt = T + r
    xe = p["tray_x0"] - 7.0
    pts = [(p["pb_x0"], p["pb_y0"] + 65, TOP + 12), (p["pb_x0"] - 10, p["pb_y0"] + 65, zc), (px, p["pb_y0"] + 65, zc),
           (px, yb_c, zc + 10), (px, yb_c, zt), (px, p["tray_y1"] - 4, zt), (xe, p["tray_y1"] - 4, zt),
           (xe, p["mat_cy"], pz0 + 6.5)]
    cab = _fuse([_rod(a, b, r) for a, b in zip(pts[:-1], pts[1:])])
    plug = _box(p["tray_x0"] - 12, p["tray_x0"], p["mat_cy"] - 5, p["mat_cy"] + 5, pz0 + 3, pz0 + 10)
    C["cable"] = cab + plug
    p["_cable_len"] = sum(math.dist(a, b) for a, b in zip(pts[:-1], pts[1:]))
    C["_p"] = p
    return C


def check(params=None, verbose=True):
    """Constructability checks on the rig: parts that must touch do, parts that must not are apart
    by at least the stated clearance, and the stand is outside the camera picture."""
    C = build_components(params)
    p = C["_p"]
    P = build_parts(params)
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
    apart("cable", "post", 0.0, "cable outside the post"); apart("cable", "arm", 0.0, "cable on top of the arm")
    apart("cable", "plate_r", 0.0, ""); apart("cable", "plate_l", 0.0, "")
    apart("cable", "tray", 0.0, "cable clear of the tray"); apart("cable", "clamps", 0.0, "cable clear of the clamps")
    apart("cable", "base", 0.0, "cable over the board"); apart("cable", "foot_r", 0.0, ""); apart("cable", "foot_l", 0.0, "")
    apart("powerbank", "clamps", 5.0, "room to lift the power bank"); apart("powerbank", "base", 5.0, "")
    btm = p["bench_h"] - p["bench_top_t"]
    C["_bench_frame"] = P["bench"] - _box(-1, p["bench_l"] + 1, -1, p["bench_d"] + 1, btm, p["bench_h"] + 1)
    apart("clamps", "_bench_frame", 5.0, "clamps clear of the bench legs and rails")
    C["bench"] = P["bench"]
    touch("clamps", "bench", "clamp pad under the bench top")
    names = list(STAND_KEYS) + ["mat", "phone", "powerbank"]
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if b == "fixings" or a == "fixings":
                continue
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

    # 2 Stand (made) and 6 power bank with its cable: see build_components()
    C = build_components(p)
    stand = _fuse([C[k] for k in STAND_KEYS])
    powerbank = C["powerbank"] + C["cable"]

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
    export_stl(asm, str(out / "stl" / "wastewise-station-assembly.stl"), tolerance=0.5, angular_tolerance=0.5)
    P = build_parts()
    C = build_components()
    singles = {"phone-stand": Compound(children=[C[k] for k in STAND_KEYS] + [C["phone"]]), "sorting-mat": P["mat"],
               "hazard-box": Compound(children=[P["hazard"], P["hazard_lid"]]), "bin": P["bins"][0]}
    C2 = build_components()        # fresh copies: a shape placed in a compound is re-parented
    for k in ("base", "foot_r", "post", "arm", "plate_r", "tray"):
        singles[f"stand-{k.replace('_r', '').replace('_', '-')}"] = C2[k]
    for name, shape in singles.items():
        export_step(shape, str(out / "step" / f"wastewise-{name}.step"))
        export_stl(shape, str(out / "stl" / f"wastewise-{name}.stl"), tolerance=0.2, angular_tolerance=0.3)
    return P


if __name__ == "__main__":
    import sys
    if "--check" in sys.argv:
        r = check()
        sys.exit(0 if all(ok for _, ok, _ in r) else 1)
    P = export()
    p = P["_p"]
    bb = station().bounding_box()
    print(f"Station envelope: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm (X x Y x Z)")
    print(f"Lens height above floor {p['lens_z']:.0f} mm; above mat {p['cam_h']:.0f} mm")
    print(f"Camera frame on mat {p['frame_x']:.0f} x {p['frame_y']:.0f} mm; mat {p['mat_l']:.0f} x {p['mat_d']:.0f} mm")
    print(f"Stand: post {p['post_len']:.0f} mm, arm {p['arm_len']:.1f} mm; board front edge {p['base_y']:.0f}, frame edge {p['frame_edge_y']:.1f}")
    print(f"Bin inner volume {p['bin_vol_l']:.1f} L each, {p['bin_n']} bins")
    print("Wrote cad/step/*.step and cad/stl/*.stl")
