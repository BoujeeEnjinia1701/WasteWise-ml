"""WasteWise-ml concept media from the TRL 3 parametric station model.

Run from the repo root:  python cad/src/concept_media.py
Station geometry comes from cad/src/model.py; proportions and main items only; not for fabrication.

WasteWise-ml is software. The 3D scene shows where it is used: a waste picker's sorting
station with a phone on a small stand pointing down at a light sorting mat, sample items
(bottle, can, carton and film), color-labeled bins by material class, a hazard box and a
platform scale. A 1.75 m person stands behind the bench for scale.

Coordinates in mm. X along the bench, Y away from the viewer (the person stands at +Y),
Z up, floor at Z = 0. Numbered parts match bom/bom.csv; lines 8 to 10 (dataset, evaluation
set and training compute) have no geometry.
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(ROOT / "cad" / "src"))
from build123d import Box, Cylinder, Sphere, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all, human_figure, INK, ACCENT
import functools
import drawing
import model
# This repo is MIT licensed (software only); the kit's sheet defaults to the hardware license.
drawing.Sheet = functools.partial(drawing.Sheet, license="MIT")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


M = model.build_parts()
p = M["_p"]
Z0 = p["mat_top"]

# input sack of mixed material on the floor at the left end (context, no BOM number)
sack = Pos(-450, 300, 330) * Cylinder(260, 660) + Pos(-450, 300, 690) * Sphere(200)

# sample items on the mat (no BOM number), inside the camera frame
bottle = (Pos(470, 250, Z0 + 38) * Rot(0, 90, 0) * Cylinder(38, 200)
          + Pos(470 + 100 + 25, 250, Z0 + 38) * Rot(0, 90, 0) * Cylinder(14, 50))     # PET bottle lying down
can = Pos(820, 230, Z0 + 61) * Cylinder(33, 122)                                     # aluminum can
carton = box(610, 680, 400, 470, Z0, Z0 + 195)                                       # 1 L beverage carton
film = Pos(860, 440, Z0 + 12) * Box(170, 120, 24)                                    # crumpled film, flattened

labels = [Part(f"Bin label: {name}", lab, col, None, (0, -700, 0))
          for (name, col), lab in zip(model.BIN_CLASSES, M["bin_labels"])]
bins = M["bins"][0]
for b in M["bins"][1:]:
    bins = bins + b

parts = [
    Part("Sorting bench (site's own)", M["bench"], "#8B7355", None),
    Part("Input sack, mixed material", sack, "#A8A29E", None),
    Part("Smartphone running the model", M["phone"], "#111827", 1, (0, -700, 900)),
    Part("Phone stand, clamped post and arm", M["stand"], ACCENT, 2, (0, -250, 350)),
    Part("Light sorting mat", M["mat"], "#E5E7EB", 3, (0, -150, 80)),
    Part("Bins by material class (7)", bins, "#64748B", 4, (0, -700, 0)),
    Part("Hazard box, lidded steel", M["hazard"] + M["hazard_lid"], "#DC2626", 5, (250, -350, 450)),
    Part("Power bank and cable", M["powerbank"], "#0EA5E9", 6, (350, 350, 150)),
    Part("Platform scale, 60 kg", M["scale"], "#475569", 7, (-300, -400, 0)),
    Part("PET bottle", bottle, "#7DD3FC", None),
    Part("Aluminum can", can, "#CBD5E1", None),
    Part("Beverage carton", carton, "#FBBF24", None),
    Part("Plastic film", film, "#C4B5FD", None),
] + labels

person = human_figure(1750, x=700, y=1050, z=0)

render_all(
    parts, project="WasteWise-ml", title="Sorting station concept", dwg_no="WML-DWG-010",
    date="2026-10-02",
    key_figures=["Phone camera 440 mm over a 700 x 450 mm mat; frame 586 x 439 mm",
                 "MobileNetV3-Large, 4.4 MB int8; 64 to 201 ms per scan (WML-CAL-001)",
                 "8 % of battery per 500-scan shift if the screen sleeps between scans",
                 "About 65 % graded, 32 % 'Unsure', 3 % hazard (estimate); hazards never sorted",
                 "Pilot station $309, indicative; no hardware budget"],
    cut=False, scale_figure=False, context=[person],
)


# ---------------- flow diagram: data and material flow (custom, two lanes) ----------------
def flow_png(out):
    fig, ax = plt.subplots(figsize=(15, 6.4), dpi=160)
    ax.set_xlim(0, 30); ax.set_ylim(0, 13); ax.set_axis_off()

    def node(x, y, w, h, head, sub, fc="#F0FDFA", ec=ACCENT, dashed=False):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.18", fc=fc, ec=ec,
                                    lw=1.4, ls="--" if dashed else "-"))
        ax.text(x + w / 2, y + h * 0.66, head, ha="center", va="center", fontsize=8.0, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h * 0.3, sub, ha="center", va="center", fontsize=7.0, color="#374151", linespacing=1.25)
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
    c = node(9.1, y1, 3.9, H, "3  On-device model", "MobileNetV3-Large, 4.4 MB,\noffline, 64 to 201 ms (calc.)")
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
    arrow((17.2, y1 - 0.05), (18.2, y2 + H + 0.05), "unsure, about 32 %", color="#2563EB", lx=1.9, ly=-0.1)
    arrow((s[0] + s[2] + 0.05, y2 + H * 0.7), (e[0] + 2.8, y1 - 0.05), "resolved", color="#2563EB", lx=0.9, ly=-0.3)
    arrow((f[0] + f[2] / 2, y1 - 0.05), (r[0] + r[2] / 2, y2 + H + 0.05), "sorted PET, HDPE, PP", color="#2563EB", lx=-1.6, ly=-0.1)

    # data loop
    y3 = 0.6
    ph = node(0.3, y3, 4.6, 1.8, "Consented field photos", "opt-in, no faces; labels checked\nby pickers and buyers", fc="#FFFBEB", ec="#B45309", dashed=True)
    tr = node(5.5, y3, 5.2, 1.8, "Retraining and evaluation", "public weights and model card\n(MIT); field test set", fc="#FFFBEB", ec="#B45309", dashed=True)
    arrow((b[0] + 0.6, y1 - 0.05), (ph[0] + 2.6, y3 + 1.85), "opt-in upload", color="#B45309", dashed=True, lx=-0.9, ly=0)
    arrow((ph[0] + ph[2] + 0.05, y3 + 0.9), (tr[0] - 0.05, y3 + 0.9), color="#B45309", dashed=True)
    arrow((10.0, y3 + 1.85), (10.0, y1 - 0.05), "updated model", color="#B45309", dashed=True, lx=-1.3, ly=0)
    ax.text(21.2, y1 + H + 0.1, "graded: about 65 % of items (estimate, WML-CAL-001)", ha="center", va="bottom", fontsize=7.4, color=ACCENT)

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
