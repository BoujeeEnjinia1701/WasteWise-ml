"""WasteWise-ml concept massing scene and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main items only; not for fabrication.

WasteWise-ml is software. The 3D scene shows where it is used: a waste picker's sorting
station with a phone on a small stand pointing down at a light sorting mat, sample items
(bottle, can, carton, film), color-labeled bins by material class, a hazard box and a
platform scale. A 1.75 m person stands behind the bench for scale.

Coordinates in mm. X along the bench, Y away from the viewer (the person stands at +Y),
Z up, floor at Z = 0. Numbered parts match bom/bom.csv; lines 8 to 10 (dataset, evaluation
set and training compute) have no geometry.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
from build123d import Box, Cylinder, Sphere, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all, human_figure, INK, ACCENT
import functools
import drawing
# This repo is MIT licensed (software only); the kit's sheet defaults to the hardware license.
drawing.Sheet = functools.partial(drawing.Sheet, license="MIT")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def rod(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


TOP = 760.0                      # bench top height

# ---------------- site's existing sorting bench (grey, no BOM number) ----------------
bench = box(0, 1400, 0, 650, TOP - 30, TOP)
for x in (40, 1360):
    for y in (40, 610):
        bench = bench + box(x - 25, x + 25, y - 25, y + 25, 0, TOP - 30)
bench = bench + box(40, 1360, 20, 60, 180, 210) + box(40, 1360, 590, 630, 180, 210)
# input sack of mixed material on the floor at the left end
sack = Pos(-450, 300, 330) * Cylinder(260, 660) + Pos(-450, 300, 690) * Sphere(200)

# ---------------- 3 light sorting mat ----------------
MAT = (300, 1000, 110, 560)
mat = box(MAT[0], MAT[1], MAT[2], MAT[3], TOP, TOP + 4)
Z0 = TOP + 4

# ---------------- sample items on the mat (no BOM number) ----------------
bottle = (Pos(470, 250, Z0 + 38) * Rot(0, 90, 0) * Cylinder(38, 200)
          + Pos(470 + 100 + 25, 250, Z0 + 38) * Rot(0, 90, 0) * Cylinder(14, 50))     # PET bottle lying down
can = Pos(820, 230, Z0 + 61) * Cylinder(33, 122)                                     # aluminum can
carton = box(610, 680, 400, 470, Z0, Z0 + 195)                                       # 1 L beverage carton
film = Pos(860, 440, Z0 + 12) * Box(170, 120, 24)                                    # crumpled film, flattened

# ---------------- 2 phone stand, 1 phone ----------------
PX, PY = 650, 330                 # point on the mat below the phone
base = box(560, 740, 575, 640, Z0 - 4, Z0 + 16)
post = rod((650, 610, Z0 + 16), (650, 610, Z0 + 470), 9)
arm = rod((650, 610, Z0 + 470), (PX, PY + 70, Z0 + 470), 7)
clamp = box(PX - 45, PX + 45, PY + 60, PY + 90, Z0 + 440, Z0 + 470)
stand = base + post + arm + clamp
phone = box(PX - 38, PX + 38, PY - 80, PY + 80, Z0 + 470, Z0 + 479)                  # face-down, camera at the mat
cam_bump = box(PX - 12, PX + 12, PY + 40, PY + 70, Z0 + 464, Z0 + 470)

# ---------------- 6 power bank on the bench ----------------
powerbank = box(770, 910, 560, 630, Z0, Z0 + 25)
cable = rod((770, 595, Z0 + 12), (662, 610, Z0 + 40), 3) + rod((662, 616, Z0 + 40), (662, 616, Z0 + 460), 3)

# ---------------- 5 hazard box, on the bench's right end ----------------
hazard = box(1130, 1370, 60, 380, Z0 - 4, Z0 + 180) + box(1120, 1380, 50, 390, Z0 + 180, Z0 + 200)

# ---------------- 4 bins by material class, in a row to the right of the bench ----------------
BIN_W, BIN_D, BIN_H = 380.0, 380.0, 640.0
classes = [("PET", "#38BDF8"), ("HDPE and PP", "#2563EB"), ("Film (LDPE)", "#A78BFA"),
           ("Metal", "#9CA3AF"), ("Paper and carton", "#D97706"), ("Glass", "#16A34A"),
           ("Unsure: check", "#F59E0B")]
bins = None
labels = []
for i, (name, col) in enumerate(classes):
    x0 = 1550 + i * 420
    b = box(x0, x0 + BIN_W, -40, -40 + BIN_D, 0, BIN_H) - box(x0 + 12, x0 + BIN_W - 12, -28, -40 + BIN_D - 12, 12, BIN_H + 1)
    bins = b if bins is None else bins + b
    labels.append(Part(f"Bin label: {name}", box(x0 + 40, x0 + BIN_W - 40, -46, -40, BIN_H - 200, BIN_H - 60), col, None, (0, -700, 0)))

# ---------------- 7 platform scale in front of the input sack ----------------
scale = box(-250, 150, -760, -400, 0, 60) + rod((-50, -410, 60), (-50, -410, 700), 14) + box(-130, 30, -430, -390, 700, 800)

parts = [
    Part("Sorting bench (site's own)", bench, "#8B7355", None),
    Part("Input sack, mixed material", sack, "#A8A29E", None),
    Part("Smartphone running the model", phone + cam_bump, "#111827", 1, (0, -700, 900)),
    Part("Phone stand, clamp arm", stand, ACCENT, 2, (0, -250, 350)),
    Part("Light sorting mat", mat, "#E5E7EB", 3, (0, -150, 80)),
    Part("Bins by material class (7)", bins, "#64748B", 4, (0, -700, 0)),
    Part("Hazard box, lidded steel", hazard, "#DC2626", 5, (250, -350, 450)),
    Part("Power bank and cable", powerbank + cable, "#0EA5E9", 6, (350, 350, 150)),
    Part("Platform scale, 60 kg", scale, "#475569", 7, (-300, -400, 0)),
    Part("PET bottle", bottle, "#7DD3FC", None),
    Part("Aluminum can", can, "#CBD5E1", None),
    Part("Beverage carton", carton, "#FBBF24", None),
    Part("Plastic film", film, "#C4B5FD", None),
] + labels

person = human_figure(1750, x=700, y=1050, z=0)

render_all(
    parts, project="WasteWise-ml", title="Sorting station concept", dwg_no="WML-DWG-010",
    key_figures=["Phone on a stand photographs one item on a light mat",
                 "On-device model, MobileNetV3 class, about 5 MB int8 (estimate)",
                 "Result in under 0.3 s: class, grade, confidence (target)",
                 "Low confidence goes to 'Unsure'; hazards are flagged, never auto-sorted",
                 "Pilot station about $285, indicative, outside any hardware budget"],
    cut=False, scale_figure=False, context=[person],
)


# ---------------- flow diagram: data and material flow (custom, two lanes) ----------------
def flow_png(out):
    fig, ax = plt.subplots(figsize=(15, 6.4), dpi=160)
    ax.set_xlim(0, 30); ax.set_ylim(0, 13); ax.set_axis_off()

    def node(x, y, w, h, head, sub, fc="#F0FDFA", ec=ACCENT, dashed=False):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.18", fc=fc, ec=ec,
                                    lw=1.4, ls="--" if dashed else "-"))
        ax.text(x + w / 2, y + h * 0.66, head, ha="center", va="center", fontsize=8.8, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h * 0.3, sub, ha="center", va="center", fontsize=7.6, color="#374151", linespacing=1.25)
        return (x, y, w, h)

    def arrow(p, q, label=None, color=ACCENT, lw=1.8, dashed=False, lx=0, ly=0.25, rad=0.0):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=13, lw=lw, color=color, alpha=0.8,
                                     ls="--" if dashed else "-", connectionstyle=f"arc3,rad={rad}"))
        if label:
            ax.text((p[0] + q[0]) / 2 + lx, (p[1] + q[1]) / 2 + ly, label, ha="center", va="bottom", fontsize=7.4,
                    color=color)

    H = 1.9
    y1 = 8.2
    a = node(0.3, y1, 3.6, H, "1  Item on the mat", "picker holds or places\none item under the phone")
    b = node(4.7, y1, 3.6, H, "2  Photo", "phone camera,\ncropped to 224 x 224 px")
    c = node(9.1, y1, 3.9, H, "3  On-device model", "MobileNetV3 class, int8,\noffline, under 0.3 s (target)")
    d = node(13.8, y1, 4.6, H, "4  Class, grade, confidence", "e.g. 'Plastic, PET (1), 0.94'\nshown as icon and color")
    e = node(19.2, y1, 4.0, H, "5  Sorted bins", "one bin per class and\nlocal buyer grade")
    f = node(24.0, y1, 5.6, H, "6  Weigh and sell", "to a buyer at the grade price\n(local price list)")
    for p, q in ((a, b), (b, c), (c, d), (d, e), (e, f)):
        arrow((p[0] + p[2] + 0.05, y1 + H / 2), (q[0] - 0.05, y1 + H / 2))

    # linked steps below the main lane
    y2 = 4.3
    hz = node(11.0, y2, 4.2, H, "Hazard box", "batteries, sharps, chemicals:\nflagged, never auto-sorted", fc="#FEF2F2", ec="#DC2626")
    s = node(16.2, y2, 5.0, H, "Unsure: check", "WasteWise Scan (linked) reads\nresin by NIR; else picker judgment", fc="#EFF6FF", ec="#2563EB")
    r = node(24.4, y2, 4.8, H, "ReflowEconomy (linked)", "local micro-factory buys\nclean PET, HDPE and PP", fc="#EFF6FF", ec="#2563EB")
    arrow((14.6, y1 - 0.05), (13.4, y2 + H + 0.05), "hazard flag, about 3 %", color="#DC2626", lx=-1.9, ly=-0.1)
    arrow((17.2, y1 - 0.05), (18.2, y2 + H + 0.05), "unsure, about 22 %", color="#2563EB", lx=1.9, ly=-0.1)
    arrow((s[0] + s[2] + 0.05, y2 + H * 0.7), (e[0] + 2.8, y1 - 0.05), "resolved", color="#2563EB", lx=0.9, ly=-0.3)
    arrow((f[0] + f[2] / 2, y1 - 0.05), (r[0] + r[2] / 2, y2 + H + 0.05), "sorted PET, HDPE, PP", color="#2563EB", lx=-1.6, ly=-0.1)

    # data loop
    y3 = 0.6
    ph = node(0.3, y3, 4.6, 1.8, "Consented field photos", "opt-in, no faces; labels checked\nby pickers and buyers", fc="#FFFBEB", ec="#B45309", dashed=True)
    tr = node(5.5, y3, 5.2, 1.8, "Retraining and evaluation", "public weights and model card\n(MIT); field test set", fc="#FFFBEB", ec="#B45309", dashed=True)
    arrow((b[0] + 0.6, y1 - 0.05), (ph[0] + 2.6, y3 + 1.85), "opt-in upload", color="#B45309", dashed=True, lx=-0.9, ly=0)
    arrow((ph[0] + ph[2] + 0.05, y3 + 0.9), (tr[0] - 0.05, y3 + 0.9), color="#B45309", dashed=True)
    arrow((10.0, y3 + 1.85), (10.0, y1 - 0.05), "updated model", color="#B45309", dashed=True, lx=-1.3, ly=0)
    ax.text(21.2, y1 + H + 0.1, "confident: about 75 % of items (estimate)", ha="center", va="bottom", fontsize=7.4, color=ACCENT)

    ax.text(0.3, 12.2, "WasteWise-ml: data and material flow at one sorting station", fontsize=11, fontweight="bold", color=INK)
    ax.text(0.3, 11.65, "CONCEPT, NOT FOR FABRICATION. Percentages are estimates for a mixed dry stream, to be replaced by field data.",
            fontsize=7.5, color="#B45309")
    ax.text(0.3, 11.2, "Teal: material and decisions.  Blue: linked WasteWise Scan and ReflowEconomy steps.  Red: hazards.  Dashed: data loop.",
            fontsize=7.5, color="#4B5563")
    fig.savefig(out, facecolor="white", bbox_inches="tight"); plt.close(fig)


flow_png(ROOT / "media" / "flow.png")

# remove renderer scratch folders
import shutil
for d in (ROOT / "media").glob("_views*"):
    shutil.rmtree(d, ignore_errors=True)
