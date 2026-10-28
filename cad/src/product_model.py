"""WasteWise-ml product appearance model for photoreal renders (kit 1.9), TRL 3, option A (the current design).

Every part of the station comes from cad/src/model.py components("A") as it is: the site's bench, the sealed sorting
mat, the clamped aluminium phone stand with its tray, bolts and cable ties, the phone, power bank and cable, the
Bluetooth shutter button at the bench edge, the seven bins, the hazard box with its sand bed and sharps container,
and the platform scale. Only the scene is added as context parts: an open-sided sorting shed (steel posts set into
the floor, beams and a corrugated roof), a concrete floor slab, an input sack, four sample items on the mat inside
the camera's picture, and a 1.75 m mannequin standing at the user's side of the bench. Ground level is z = 0; every
site part reaches below it. APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Groups: "shell" (the scanning rig: stand, phone, mat, power bank, cable, button), "station" (bench, bins, hazard box,
scale) and "context" (shed, floor, sack, sample items, mannequin).
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Cylinder, Pos, Rot, Sphere  # noqa: E402
import cad_parts as cp  # noqa: E402
from cad_parts import part  # noqa: E402
import model  # noqa: E402
from wml_parts import box, rbox  # noqa: E402

TITLE = "WasteWise-ml: phone scan rig at a sorting station"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "station", "context"], "explode": False, "el": 18, "az": -30,
     "args": ["--scene=outdoor", "--ground=concrete", "--ground-z=0", "--sun=40,-60", "--lens=35"],
     "note": "Site render from the front of the bench (-Y) and the bins' end, about 18 deg elevation: the sorting "
             "station in an open-sided shed on a concrete floor, the phone in its tray on the clamped stand over the "
             "light mat with a PET bottle, can, carton and film inside the picture, the shutter button at the bench "
             "edge, seven labelled bins, the hazard box and the scale; 1.75 m mannequin at the user's side for scale"},
    {"name": "rig", "groups": ["shell"], "explode": False, "el": 28, "az": -40,
     "note": "Studio close-up of the scanning rig from the front right, about 28 deg elevation: plywood board with its "
             "two G-clamps, foot angles, square post and arm with corner plates and bolts, folded tray with the phone "
             "screen up, cable along the arm, power bank, shutter button and the sealed mat"},
]

_RIG = {"stand", "rig", "fixings"}


def _group(p):
    if p["kind"] == "context":
        return "station"            # the site's own bench belongs with the station in the renders
    return "shell" if p["group"] in _RIG else "station"


def scene():
    p = model.derived()
    out = []
    # concrete floor slab and an open-sided shed (posts set 300 mm into the slab and the ground below it)
    out.append(part("Concrete floor slab (site)", box(-1600, 5600, -2400, 2600, -150, 0), "concrete", "context"))
    xs, ys, h = (-1200.0, 2100.0, 5300.0), (-1800.0, 2200.0), 3000.0
    for x in xs:
        for y in ys:
            out.append(part(f"Shed post at ({x:.0f}, {y:.0f}) (100 x 100 x 4 steel tube) (site)",
                            Pos(x, y, -300) * cp.shs(100, 4, h + 300), "galvanised", "context"))
    for y in ys:
        out.append(part(f"Shed beam at y {y:.0f} (site)", Pos(xs[0] - 200, y, h + 60) * Rot(0, 90, 0) * cp.rhs(120, 60, 4, xs[-1] - xs[0] + 400),
                        "galvanised", "context"))
    pts, n = [], int((xs[-1] - xs[0] + 800) / 19)
    for i in range(n + 1):
        x = xs[0] - 400 + i * 19
        pts.append((x, 9 * math.sin(2 * math.pi * x / 76)))
    from build123d import Polygon, extrude
    prof = extrude(Polygon(*([(x, z + 0.6) for x, z in pts] + [(x, z - 0.6) for x, z in reversed(pts)]), align=None), 4600)
    roof = Pos(0, ys[1] + 200, h + 130) * Rot(90, 0, 0) * prof
    out.append(part("Corrugated roof sheet (site)", roof, "galvanised", "context"))
    # input sack of mixed material at the -X end, and four sample items on the mat, inside the camera's picture
    sack = Pos(-450, 300, 0) * Cylinder(260, 600, align=None) + Pos(-450, 300, 640) * Sphere(210)
    out.append(part("Input sack, mixed material", sack, "canvas", "context"))
    z0 = p["mat_top"]
    bottle = Pos(470, 250, z0 + 38) * Rot(0, 90, 0) * (Cylinder(38, 200) + Pos(0, 0, 125) * Cylinder(14, 50))
    out.append(part("PET bottle (sample item)", bottle, "polycarbonate", "context", color="#BAE6FD"))
    out.append(part("Aluminium can (sample item)", Pos(820, 230, z0) * cp.break_edges(Cylinder(33, 122, align=None), 3.0), "aluminium", "context"))
    out.append(part("Beverage carton (sample item)", rbox(610, 680, 400, 470, z0, z0 + 195, r=3.0, edge=1.0), "label", "context", color="#FBBF24"))
    out.append(part("Crumpled film (sample item)", rbox(780, 950, 380, 500, z0, z0 + 24, r=30.0, edge=8.0), "hdpe_natural", "context", color="#C4B5FD"))
    # 1.75 m mannequin at the user's side of the bench, facing the bench (-Y), feet on the floor
    from context_parts import mannequin
    out.append(part("Picker at the bench, 1.75 m mannequin (scale)", Pos(p["mat_cx"] - 150, p["bench_d"] + 320, 0) * mannequin(1750, "stand"),
                    "skin", "context"))
    return out


def product_parts():
    out = []
    for p in model.components(model.CHOSEN):
        q = dict(p)
        q["group"] = _group(p)
        out.append(q)
    for p in scene():
        q = dict(p)
        q["group"] = "context"
        out.append(q)
    return out


if __name__ == "__main__":
    ps = product_parts()
    for p in ps:
        if p["group"] == "context":
            s = p["shape"]
            print(f"{p['name']:70s} {p['material']:12s} valid={s.is_valid} zmin={s.bounding_box().min.Z:8.1f}")
    print(len(ps), "parts")
