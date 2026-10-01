"""WasteWise-ml scanning rig build plan pictures (WML-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every rig component pulled apart, numbered in build order
    cad/drawings/WML-DWG-101 to 107        making sketches for the made components
    docs/05-build-plan/tray-blank.png      the phone tray's flat blank with fold lines
    docs/05-build-plan/frame.png           the camera's picture on the mat, seen from above
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import functools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import drawing  # noqa: E402
# This repo is MIT licensed (software only); the kit's sheet defaults to the hardware license.
drawing.Sheet = functools.partial(drawing.Sheet, license="MIT")
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
import model  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-09-30"
C = model.build_components()
p = C["_p"]
TOP, BT, T = p["bench_h"], p["base_top"], p["arm_z"]
PX, PY = p["post_x"], p["post_y"]

COL = {"base": "#B08D57", "foot": "#1D4ED8", "post": "#0E7490", "arm": "#0F766E", "plate": "#6D28D9",
       "tray": "#D97706", "mat": "#CBD5E1", "clamps": "#DC2626", "phone": "#111827", "pb": "#0EA5E9",
       "bolt": "#374151", "bench": "#A8A29E"}


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def win(sh, x0, x1, y0, y1, z0, z1):
    import build123d as b
    return sh & (b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0))


# fixings, sorted into their joints by where they sit
def _fix_groups():
    g = {"foot": [], "plate": [], "tab": [], "screw": []}
    for s in C["fixings"].solids():
        bb = s.bounding_box()
        if bb.size.Z > 30 and bb.center().Z > BT + 100:
            g["tab"].append(s)
        elif bb.size.X < 10 and bb.size.Y < 10 and bb.size.Z < 25:
            g["screw"].append(s)
        elif bb.center().Z < BT + 60:
            g["foot"].append(s)
        else:
            g["plate"].append(s)
    return {k: _fuse(v) for k, v in g.items()}


FX = _fix_groups()


def bench_top(x0=380, x1=1060):
    """The part of the site's bench top around the rig, for orientation."""
    return model._box(x0, x1, 0, p["bench_d"], TOP - p["bench_top_t"], TOP)


def made():
    return {
        "base": part("Base board", C["base"], COL["base"]),
        "feet": part("Foot angles (2)", C["foot_r"] + C["foot_l"], COL["foot"]),
        "post": part("Post", C["post"], COL["post"]),
        "arm": part("Arm", C["arm"], COL["arm"]),
        "plates": part("Corner plates (2)", C["plate_r"] + C["plate_l"], COL["plate"]),
        "tray": part("Phone tray", C["tray"], COL["tray"]),
        "mat": part("Sorting mat", C["mat"], COL["mat"]),
        "clamps": part("G-clamps (2)", C["clamps"], COL["clamps"]),
        "phone": part("Phone", C["phone"], COL["phone"]),
        "pb": part("Power bank and cable", C["powerbank"] + C["cable"], COL["pb"]),
    }


ORDER = ["base", "feet", "post", "arm", "plates", "tray", "mat", "clamps", "phone", "pb"]


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    off = {"base": (0, 120, -90), "feet": (0, 120, 20), "post": (0, 120, 150), "arm": (0, -30, 300),
           "plates": (0, 120, 420), "tray": (0, -110, 260), "mat": (0, -230, -120), "clamps": (0, 320, -110),
           "phone": (0, -110, 420), "pb": (330, 200, -60)}
    parts = []
    for k in ORDER:
        q = M[k]
        q.explode = off[k]
        parts.append(q)
    return bv.overview(parts, OUT / "overview.png", "WasteWise-ml scanning rig: every component, pulled apart",
                       subtitle="Numbered in build order: 1 to 7 are made, 8 to 10 are bought. Seen from the front right and above",
                       elev=20, azim=-55, size=(11, 8.5), dpi=150)


# ----------------------------------------------------------------- making sketches
def sheets():
    import build123d as b
    M = made()
    base = dict(project="WasteWise-ml", date=DATE)
    out = []
    at0 = lambda sh: b.Pos(-sh.bounding_box().min.X, -sh.bounding_box().min.Y, -sh.bounding_box().min.Z) * sh  # noqa: E731

    out.append(bv.component_sheet(
        M["base"], [M["feet"], M["post"], M["mat"], part("Bench top", bench_top(), COL["bench"])],
        dwg_no="WML-DWG-101", title="WasteWise-ml base board: making sketch",
        material="Plywood 18 mm, exterior or birch grade", view_shape=at0(C["base"]), inset_view=(30, -60),
        notes=["Cut one piece 240 long x 90 deep from 18 mm plywood; sand the edges.",
               "Mark a centre line across it, 120 mm from each end, on the top face and",
               "  down the front edge: it lines up with the mat's centre mark.",
               "The post stands on the centre line, 45 mm back from the front edge.",
               "Four pilot holes 3 mm, 12 mm deep, for the foot angle screws:",
               "  39 mm each side of the centre line, 25 and 65 mm back from the front edge.",
               "  Better: drill them through the foot angles when fitting (step 2).",
               "Paint the front edge the mat's grey so it disappears if it shows at all.",
               "Fit: back edge flush with the back edge of the bench, held by two",
               "  G-clamps 20 mm in from each end. The front edge is where the mat stops.",
               "Check: flat, square corners, centre line marked on top and front."],
        **base))

    foot = C["foot_r"]
    out.append(bv.component_sheet(
        part("Foot angle", foot, COL["foot"]), [M["base"], M["post"], part("Left foot angle", C["foot_l"], "#9CA3AF")],
        dwg_no="WML-DWG-102", title="WasteWise-ml foot angle (make 2): making sketch",
        material="Aluminium equal angle 50 x 50 x 3 mm, 6063 class", view_shape=at0(foot), inset_view=(25, -35),
        notes=["Make two, the same. Cut 60 mm lengths of 50 x 50 x 3 angle; square",
               "  and deburr the ends.",
               "Upright leg (against the post): two 5.5 mm holes at mid-length (30 mm),",
               "  15 and 40 mm up from the underside of the flat leg.",
               "Flat leg (on the board): two 4.5 mm holes, 26.5 mm out from the back",
               "  of the upright leg, 10 and 50 mm along the length.",
               "Drill the two angles clamped together so the holes match, then",
               "  countersink the flat-leg holes lightly for the screw heads.",
               "Fit: the back of the upright leg sits flat on a side face of the post,",
               "  the flat leg points away from the post and sits flat on the board.",
               "  Two M5 bolts go through both angles and the post (step 1).",
               "Check: the two angles stand square and level on a flat bench."],
        **base))

    post = C["post"]
    out.append(bv.component_sheet(
        M["post"], [M["base"], M["feet"], M["arm"], M["plates"]],
        dwg_no="WML-DWG-103", title="WasteWise-ml post: making sketch (drawn laid flat)",
        material="Square aluminium tube 25 x 25 x 2 mm, 6063 class", view_shape=at0(b.Rot(0, 90, 0) * post), inset_view=(18, -40),
        notes=[f"Cut one {p['post_len']:.0f} mm length of 25 x 25 x 2 tube; ends square",
               "  within 0.5 mm (use a mitre box), deburred inside and out.",
               "Mark the bottom end. All four holes go through both side walls,",
               "  on the centre line of one pair of faces (the side faces):",
               "  two 5.5 mm holes 15 and 40 mm up from the bottom (foot angles);",
               "  two 5.5 mm holes 45 and 85 mm down from the top (corner plates).",
               "Drill from one side through both walls in a drill stand so the",
               "  holes run straight; check a bolt passes freely.",
               f"The length sets the camera height: {p['post_len']:.0f} mm puts the lens",
               f"  {p['cam_h']:.0f} mm above the mat with an 18 mm board and 4 mm mat.",
               "Fit: stands on the board between the foot angles; the arm butts its",
               "  front face; the cable runs up its back face.",
               "Check: length within 0.5 mm; ends square; four holes line up."],
        **base))

    arm = C["arm"]
    out.append(bv.component_sheet(
        M["arm"], [M["post"], M["plates"], M["tray"], M["phone"]],
        dwg_no="WML-DWG-104", title="WasteWise-ml arm: making sketch",
        material="Square aluminium tube 25 x 25 x 2 mm, 6063 class", view_shape=at0(arm), inset_view=(20, -50),
        notes=[f"Cut one {p['arm_len']:.1f} mm length of 25 x 25 x 2 tube; square the end",
               "  that meets the post carefully (it sets the arm level); deburr.",
               f"This length suits a phone whose lens is on its centre line across the",
               "  width. If yours is d mm off that line, lay the phone with the lens",
               "  on the side away from the post and cut the arm d mm shorter.",
               "Side holes, across the side faces, 12.5 mm down from the top:",
               "  two 5.5 mm holes 22.5 and 62.5 mm from the post end.",
               "Top-to-bottom holes, on the centre line of the top face:",
               "  two 5.5 mm holes 16 and 46 mm from the free end.",
               "Fit: square end against the post's front face, top faces level;",
               "  corner plates on both sides; the tray tab under the free end.",
               "Check: both ends square; side holes match the corner plate holes."],
        **base))

    pr = C["plate_r"]
    out.append(bv.component_sheet(
        part("Corner plate", pr, COL["plate"]), [M["post"], M["arm"], part("Left corner plate", C["plate_l"], "#9CA3AF")],
        dwg_no="WML-DWG-105", title="WasteWise-ml corner plate (make 2): making sketch",
        material="Aluminium sheet 3 mm, 5052 or 6061 class", view_shape=at0(pr), inset_view=(20, -10),
        notes=["Make two, the same. Mark a 105 x 100 mm rectangle on 3 mm sheet: the",
               "  105 mm edge is the top (level with the top of the arm), the 100 mm",
               "  edge at one end is the back (it lines up with the post's back face).",
               "Cut off the lower front corner: from 25 mm down the front edge to",
               "  25 mm in from the back along the bottom edge. File the cut straight.",
               "Holes 5.5 mm, 12.5 mm below the top edge, 17.5 and 57.5 mm from",
               "  the front edge (into the arm).",
               "Holes 5.5 mm, 12.5 mm in from the back edge, 45 and 85 mm below",
               "  the top edge (into the post).",
               "Drill the two plates clamped together. Round the corners about 2 mm.",
               "Fit: one plate flat on each side of the post and arm, top edge level",
               "  with the arm top; four M5 bolts through plates and tubes (step 3).",
               "Check: the plates match each other hole for hole."],
        **base))

    tr = C["tray"]
    out.append(bv.component_sheet(
        M["tray"], [M["arm"], M["phone"], M["post"]],
        dwg_no="WML-DWG-106", title="WasteWise-ml phone tray: making sketch",
        material="Aluminium sheet 2 mm, 5052 class (folds without cracking)", view_shape=at0(tr), inset_view=(-28, -55),
        notes=["Cut the flat blank from the tray blank picture: 165 x 98 mm with a",
               "  40 x 55 mm tab on one long edge, 5 mm from the charging end.",
               "Fold lines 10 mm in from each long edge. On the tab side, cut the",
               "  10 mm strip away from the charging end to 48 mm (beside the tab).",
               "Window for the camera bump: 34 x 34 mm, centred 25 mm from the",
               "  charging end on the centre line. Measure your phone first: the",
               "  window is the bump plus 2 mm all round, wherever the bump is.",
               "Two 5.5 mm holes in the tab, on its centre line, 19 and 49 mm",
               "  out from the fold line.",
               "Fold both strips up 90 degrees in a vice between hardwood blocks:",
               "  78 mm inside between the lips for a 76 mm phone.",
               "Fit: tab flat under the arm end; the phone lies screen up, its bump",
               "  in the window. Check: the phone drops in and lifts out freely."],
        **base))

    mt = C["mat"]
    out.append(bv.component_sheet(
        M["mat"], [M["base"], M["post"], part("Bench top", bench_top(250, 1100), COL["bench"])],
        dwg_no="WML-DWG-107", title="WasteWise-ml sorting mat: making sketch",
        material="Hardboard 4 mm (or 4 mm plywood), painted matte light grey", view_shape=at0(mt), inset_view=(35, -60),
        notes=["Cut one piece 700 x 450 mm from 4 mm hardboard; sand the edges and",
               "  round the corners about 3 mm.",
               "Prime, then paint the smooth face matte light grey (two coats).",
               "Rule a 50 mm grid in mid grey from the two centre lines: 13 lines",
               "  across (the last 50 mm from each end), 9 lines deep (25 from the edges).",
               "  Lines about 1 mm wide (a fine paint marker along a steel rule).",
               "Mark the centre of the long back edge with a short line on the edge:",
               "  it lines up with the base board's centre mark.",
               "Seal with clear matte varnish so it wipes clean; no gloss (glare).",
               "Fit: lies flat on the bench, back edge against the base board's",
               "  front edge, centre marks lined up. Nothing fixes it.",
               "Check: flat on the bench; no shine under a lamp from the phone's view."],
        **base))
    return out


# ----------------------------------------------------------------- layouts
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Polygon
    INK, MUT, AC, WARN = "#111827", "#4B5563", "#0F766E", "#B45309"
    res = []
    repo = "github.com/BoujeeEnjinia1701/WasteWise-ml"

    # tray flat blank, seen from above with the charging end on the left and the tab side at the top
    L, Wd, s, tab_w, tab_l, tab_x = 165.0, 98.0, 10.0, 40.0, 55.0, 5.0
    fig = plt.figure(figsize=(11, 7.4), dpi=150)
    ax = fig.add_axes([0.05, 0.1, 0.62, 0.75]); ax.set_aspect("equal"); ax.set_axis_off()
    outline = [(0, 0), (L, 0), (L, Wd), (48, Wd), (48, Wd - s), (tab_x + tab_w, Wd - s), (tab_x + tab_w, Wd + tab_l),
               (tab_x, Wd + tab_l), (tab_x, Wd - s), (0, Wd - s)]
    ax.add_patch(Polygon(outline, closed=True, fc="#FEF3C7", ec=INK, lw=1.3))
    ax.plot([0, L], [s, s], color=WARN, lw=1.0, ls=(0, (6, 3)))
    ax.plot([48, L], [Wd - s, Wd - s], color=WARN, lw=1.0, ls=(0, (6, 3)))
    ax.text(L - 3, s + 1.5, "fold line: fold up 90", ha="right", va="bottom", fontsize=7.5, color=WARN)
    ax.text(L - 3, Wd - s - 1.5, "fold line: fold up 90", ha="right", va="top", fontsize=7.5, color=WARN)
    ax.add_patch(Rectangle((25 - 17, Wd / 2 - 17), 34, 34, fc="white", ec=INK, lw=1.1))
    ax.text(25, Wd / 2, "window\n34 x 34", ha="center", va="center", fontsize=7.5, color=INK)
    for d in (19.0, 49.0):
        ax.add_patch(plt.Circle((tab_x + tab_w / 2, Wd - s + d), 2.75, fc="white", ec=INK, lw=1.0))
    ax.text(tab_x + tab_w + 12, Wd + 42, "tab: two 5.5 holes on its centre line,\n19 and 49 from the fold line", fontsize=7.5,
            color=INK, va="center")
    ax.annotate("lip strip from 48 to the far end only;\nnone beside the tab or at the charging end", xy=(46.5, Wd - 2),
                xytext=(tab_x + tab_w + 12, Wd + 16), fontsize=7.5, color=MUT, va="center",
                arrowprops=dict(arrowstyle="-", color=MUT, lw=0.6))
    def dim(x0, y0, x1, y1, t, off, horiz=True):
        if horiz:
            ax.annotate("", xy=(x0, y0 + off), xytext=(x1, y0 + off), arrowprops=dict(arrowstyle="<->", color=AC, lw=0.7))
            ax.text((x0 + x1) / 2, y0 + off - 2, t, ha="center", va="top", fontsize=7.5, color=AC)
        else:
            ax.annotate("", xy=(x0 + off, y0), xytext=(x0 + off, y1), arrowprops=dict(arrowstyle="<->", color=AC, lw=0.7))
            ax.text(x0 + off - 2, (y0 + y1) / 2, t, ha="right", va="center", fontsize=7.5, color=AC, rotation=90)
    dim(0, 0, L, 0, "165", -8)
    dim(0, 0, 0, Wd, "98", -8, horiz=False)
    for y0_ in (0.0, Wd - s):
        ax.annotate("", xy=(L + 8, y0_), xytext=(L + 8, y0_ + s), arrowprops=dict(arrowstyle="<->", color=AC, lw=0.7))
        ax.text(L + 11, y0_ + s / 2, "10", va="center", fontsize=7.5, color=AC)
    dim(tab_x, Wd + tab_l, tab_x + tab_w, Wd + tab_l, "40", 9)
    dim(0, Wd + tab_l, tab_x, Wd + tab_l, "", 9)
    ax.text(-2, Wd + tab_l + 12, "5", ha="right", va="center", fontsize=7.5, color=AC)
    ax.plot([25, 25], [s, Wd / 2 - 17], color=MUT, lw=0.5, ls=":")
    ax.text(26, s + 4, "centre 25 from the charging end", fontsize=7.5, color=MUT, va="bottom")
    ax.text(L / 2 + 20, Wd / 2, "phone lies here,\nscreen up", ha="center", va="center", fontsize=8.5, color=MUT)
    ax.text(-3, -18, "charging end", ha="left", fontsize=7.5, color=MUT)
    ax.set_xlim(-48, L + 45); ax.set_ylim(-26, Wd + tab_l + 22)
    fig.text(0.03, 0.97, "Phone tray: flat blank and fold lines", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.93, "2 mm aluminium sheet, seen from above before folding. Sizes in mm. Dashed: fold lines (both strips fold up).",
             fontsize=8.5, color=MUT, va="top")
    key = ["How to cut and fold it", "", "1  Mark the blank on the sheet's film.",
           "2  Cut the outline with snips or a jigsaw;", "   file the edges smooth.",
           "3  Drill a 6 mm hole in each window corner,", "   cut between them, file square.",
           "4  Drill the two tab holes 5.5 mm.", "5  Fold both strips up 90 degrees in a vice",
           "   between hardwood blocks, one strip", "   at a time. The tab stays flat.",
           "6  Inside width between the lips: 78.", "", "Window: the camera bump plus 2 mm",
           "all round. Measure your phone and", "move the window to suit."]
    for i, t in enumerate(key):
        fig.text(0.70, 0.84 - i * 0.03, t, fontsize=8.5 if i else 9.5, fontweight="bold" if i == 0 else "normal",
                 color=INK, va="top")
    fig.text(0.03, 0.015, bv.BANNER, fontsize=7, color=WARN)
    fig.text(0.97, 0.015, repo, fontsize=7, color=AC, ha="right", family="monospace")
    fig.savefig(OUT / "tray-blank.png", facecolor="white"); plt.close(fig); res.append(OUT / "tray-blank.png")

    # camera picture on the mat, seen from above (front of the bench at the bottom)
    fig = plt.figure(figsize=(11, 8), dpi=150)
    ax = fig.add_axes([0.05, 0.08, 0.66, 0.8]); ax.set_aspect("equal"); ax.set_axis_off()
    mx0, my0 = p["mat_x0"], p["mat_y0"]
    ax.add_patch(Rectangle((mx0, my0), p["mat_l"], p["mat_d"], fc="#E5E7EB", ec=INK, lw=1.2))
    for i in range(-6, 7):
        ax.plot([p["mat_cx"] + 50 * i] * 2, [my0, my0 + p["mat_d"]], color="#9CA3AF", lw=1.0 if i == 0 else 0.5)
    for j in range(-4, 5):
        ax.plot([mx0, mx0 + p["mat_l"]], [p["mat_cy"] + 50 * j] * 2, color="#9CA3AF", lw=1.0 if j == 0 else 0.5)
    fx0, fy0 = p["mat_cx"] - p["frame_x"] / 2, p["mat_cy"] - p["frame_y"] / 2
    ax.add_patch(Rectangle((fx0, fy0), p["frame_x"], p["frame_y"], fc="none", ec=AC, lw=1.8, ls="--"))
    ax.add_patch(Rectangle((PX - p["base_l"] / 2, p["base_y"]), p["base_l"], p["base_d"], fc="#D6C3A0", ec=INK, lw=1))
    ax.add_patch(Rectangle((PX - 12.5, PY - 12.5), 25, 25, fc=COL["post"], ec=INK, lw=0.8))
    ax.add_patch(Rectangle((PX - 12.5, p["arm_y0"]), 25, p["arm_len"], fc="none", ec=COL["arm"], lw=1, ls=":"))
    ax.add_patch(Rectangle((p["tray_x0"], p["tray_y0"]), p["tray_x1"] - p["tray_x0"], p["tray_y1"] - p["tray_y0"],
                           fc="none", ec=COL["tray"], lw=1, ls=":"))
    ax.plot(p["mat_cx"], p["mat_cy"], marker="+", ms=14, color=INK, mew=1.2)
    ax.plot([PX, PX], [p["base_y"] - 8, p["base_y"] + 8], color=INK, lw=1.5)
    ax.text(fx0 + 6, fy0 + p["frame_y"] - 8, f"camera picture {p['frame_x']:.0f} x {p['frame_y']:.0f}", fontsize=8.5, color=AC, va="top",
            bbox=dict(boxstyle="round,pad=0.15", fc="#E5E7EB", ec="none"))
    ax.text(p["mat_cx"] + 10, p["mat_cy"] - 14, "lens straight above", fontsize=8, color=INK, va="top")
    ax.text(mx0, my0 - 16, f"sorting mat {p['mat_l']:.0f} x {p['mat_d']:.0f}, 50 grid from the centre lines", fontsize=8.5,
            color=INK, va="top")
    ax.text(PX + p["base_l"] / 2 + 8, p["base_y"] + p["base_d"] / 2, "base board,\npost behind", fontsize=8, color=INK, va="center")
    ax.annotate("centre marks line up", xy=(PX, p["base_y"]), xytext=(PX - 330, p["base_y"] + 30), fontsize=8, color=INK,
                arrowprops=dict(arrowstyle="-", color=MUT, lw=0.6))
    ax.annotate("", xy=(fx0 + p["frame_x"] + 2, p["mat_cy"]), xytext=(mx0 + p["mat_l"], p["mat_cy"]),
                arrowprops=dict(arrowstyle="<->", color=AC, lw=0.7))
    ax.text(mx0 + p["mat_l"] + 4, p["mat_cy"], f"{(p['mat_l'] - p['frame_x']) / 2:.0f} spare\neach side", fontsize=7.5, color=AC, va="center")
    ax.text(mx0 + p["mat_l"] + 4, fy0 + p["frame_y"] - 4, f"{p['mat_y0'] + p['mat_d'] - fy0 - p['frame_y']:.1f} spare\nfront and back",
            fontsize=7.5, color=AC, va="top")
    ax.text(mx0 + p["mat_l"], my0 - 16, "far side of the bench", ha="right", fontsize=8, color=MUT, va="top")
    ax.text(PX - p["base_l"] / 2 - 8, p["base_y"] + p["base_d"] - 6, "the user stands on this side", ha="right", fontsize=8,
            color=MUT, va="top")
    ax.set_xlim(mx0 - 20, mx0 + p["mat_l"] + 95); ax.set_ylim(my0 - 40, p["base_y"] + p["base_d"] + 15)
    fig.text(0.03, 0.97, "What the camera sees: the picture on the mat", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.93, "Seen from above. Sizes in mm, from the model, for a 26 mm-equivalent main camera 440 mm above the mat (WML-CAL-001).\n"
             "Dotted: the arm and phone tray above. The board stays out of the picture; the picture stays on the mat.",
             fontsize=8.5, color=MUT, va="top")
    key = ["How to check it (first checks)", "", "1  Lay the mat against the board,",
           "   centre marks lined up.", "2  Open the app's camera view.",
           "3  Every edge of the picture should", "   show grey mat; no bench, no board.",
           "4  The grid squares should look", "   square, not stretched: if not, the",
           "   phone is not level in the tray.", "", "If the board shows, the lens is not",
           "where the model puts it: see the", "arm making sketch (lens offset)."]
    for i, t in enumerate(key):
        fig.text(0.74, 0.84 - i * 0.032, t, fontsize=8.5 if i else 9.5, fontweight="bold" if i == 0 else "normal", color=INK, va="top")
    fig.text(0.03, 0.015, bv.BANNER, fontsize=7, color=WARN)
    fig.text(0.97, 0.015, repo, fontsize=7, color=AC, ha="right", family="monospace")
    fig.savefig(OUT / "frame.png", facecolor="white"); plt.close(fig); res.append(OUT / "frame.png")
    return res


# ----------------------------------------------------------------- joints
def joints():
    out = []
    # 01 foot angle, post and board (right side)
    bx = (595, 725, 565, 645, TOP, BT + 70)
    out.append(bv.joint([
        part("Base board", win(C["base"], *bx), COL["base"]),
        part("Post", win(C["post"], *bx), COL["post"]),
        part("Foot angle", win(C["foot_r"] + C["foot_l"], *bx), COL["foot"]),
        part("Two M5 bolts through both angles and the post", win(FX["foot"], *bx), COL["bolt"]),
        part("Wood screws, two per angle", win(FX["screw"], *bx), "#78716C")],
        OUT / "joint-01.png", "Joint 1: the post's foot",
        subtitle="Seen from the front right. Each angle sits flat on the board and flat on a side face of the post",
        elev=22, azim=-35, size=(8, 6)))
    # 02 corner plates at the top of the post
    bx = (600, 700, 500, 640, T - 115, T + 10)
    out.append(bv.joint([
        part("Post", win(C["post"], *bx), COL["post"]),
        part("Arm (butts the post's front face)", win(C["arm"], *bx), COL["arm"]),
        part("Corner plate (one each side)", win(C["plate_r"] + C["plate_l"], *bx), COL["plate"]),
        part("Four M5 bolts, nyloc nuts", win(FX["plate"], *bx), COL["bolt"])],
        OUT / "joint-02.png", "Joint 2: arm to post, with the corner plates",
        subtitle="Seen from the right. Two bolts into the arm, two into the post; the plates make the corner rigid",
        elev=12, azim=-20, size=(8, 6)))
    # 03 tray tab under the arm end, cut through the bolt centres and seen from the side
    bx = (PX, 700, 340, 470, p["tray_bot"] - 12, T + 12)
    out.append(bv.joint([
        part("Arm, cut open", win(C["arm"], *bx), COL["arm"]),
        part("Phone tray: tab and lip", win(C["tray"], *bx), COL["tray"]),
        part("Two M5 bolts, heads on top, nuts under the tab", win(FX["tab"], *bx), COL["bolt"])],
        OUT / "joint-03.png", "Joint 3: tray tab under the arm end (cut through the bolts)",
        subtitle="Seen from the left, slightly below. The tab lies flat under the arm; the arm end stops 3 mm short of the lip",
        elev=-8, azim=-165, size=(8, 6)))
    # 04 camera bump in the window, from below
    import build123d as b
    bx = (615, 800, 285, 385, p["tray_bot"] - 5, p["tray_top"] + 15)
    bump = C["phone"] & model._box(600, 800, 280, 390, p["lens_z"] - 1, p["lens_z"] + 2)
    body = C["phone"] - model._box(600, 800, 280, 390, p["lens_z"] - 1, p["lens_z"] + 2)
    out.append(bv.joint([
        part("Phone tray", win(C["tray"], *bx), COL["tray"]),
        part("Phone back (grey, in the 2 mm gap)", win(body, *bx), "#9CA3AF"),
        part("Camera bump in the window", bump, COL["phone"])],
        OUT / "joint-04.png", "Joint 4: the phone in its tray, seen from below",
        subtitle="The camera bump sits in the window, 2 mm clear all round, and holds the phone in place; the lens looks straight down",
        elev=-62, azim=-75, size=(8, 6)))
    # 05 G-clamp holding the board to the bench's back edge, cut through the clamp
    xc = p["clamp_x"][1]
    bx = (xc - 60, xc + 0.01, 520, 690, TOP - 60, BT + 25)
    out.append(bv.joint([
        part("Bench top (site's own)", win(bench_top(), *bx), COL["bench"]),
        part("Base board", win(C["base"], *bx), COL["base"]),
        part("G-clamp, cut through", win(C["clamps"], *bx), COL["clamps"]),
        part("Sorting mat", win(C["mat"], *bx), COL["mat"])],
        OUT / "joint-05.png", "Joint 5: G-clamp on the bench's back edge (right clamp, cut through)",
        subtitle="Seen from the right. The board's back edge is flush with the bench edge; the clamp grips board and bench top",
        elev=8, azim=-2, size=(8, 6)))
    # 06 mat against the board
    bx = (540, 760, 470, 650, TOP - 5, BT + 30)
    out.append(bv.joint([
        part("Sorting mat", win(C["mat"], *bx), COL["mat"]),
        part("Base board", win(C["base"], *bx), COL["base"]),
        part("Post and foot angles", win(C["post"] + C["foot_r"] + C["foot_l"], *bx), COL["post"]),
        part("Centre marks, lined up", model._box(PX - 1.5, PX + 1.5, p["base_y"] - 25, p["base_y"], p["mat_top"], p["mat_top"] + 0.6)
             + model._box(PX - 1.5, PX + 1.5, p["base_y"] - 0.6, p["base_y"], p["mat_top"], BT)
             + model._box(PX - 1.5, PX + 1.5, p["base_y"], p["base_y"] + 25, BT, BT + 0.6), "#111827")],
        OUT / "joint-06.png", "Joint 6: the mat's back edge against the base board",
        subtitle="Seen from the front right. Nothing fixes the mat; the board places it, centre mark to centre mark",
        elev=30, azim=-60, size=(8, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps():
    M = made()
    out = []

    def st(n, done, new, title, sub, **kw):
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(q, e):
        return Part(q.name, q.shape, q.color, None, tuple(e), q.alpha)
    bench = [part("Bench top (site's own)", bench_top(), COL["bench"])]
    st(1, [M["post"]], [mv(part("Right foot angle", C["foot_r"], COL["foot"]), (70, 0, 0)),
                        mv(part("Left foot angle", C["foot_l"], COL["foot"]), (-70, 0, 0)),
                        mv(part("Two M5 x 40 bolts", FX["foot"], COL["bolt"]), (-120, 0, 0))],
       "foot angles onto the post",
       "Backs of the upright legs flat on the post's side faces, flat legs flush with the post's bottom end; snug the nuts",
       elev=20, azim=-40)
    stand_lo = part("Post with its foot angles", C["post"] + C["foot_r"] + C["foot_l"] + FX["foot"], COL["post"])
    st(2, [M["base"]], [mv(stand_lo, (0, 0, 140)), mv(part("Four wood screws", FX["screw"], "#78716C"), (0, 0, 240))],
       "post onto the base board",
       "Post on the centre line, 45 mm back from the front edge, upright both ways; drill pilots through the angles, then screw",
       elev=24, azim=-50, label_done=True)
    lower = [M["base"], part("Post and foot angles", C["post"] + C["foot_r"] + C["foot_l"], COL["post"])]
    st(3, lower, [mv(M["arm"], (0, -90, 0)),
                  mv(part("Right corner plate", C["plate_r"], COL["plate"]), (70, 0, 0)),
                  mv(part("Left corner plate", C["plate_l"], COL["plate"]), (-70, 0, 0))],
       "arm and corner plates onto the post",
       "Arm square end against the post, tops level; a plate each side; four M5 x 40 bolts, then check the arm is square and tighten",
       elev=18, azim=-40, label_done=False)
    upper = lower + [M["arm"], M["plates"]]
    st(4, upper, [mv(M["tray"], (0, 0, -90)), mv(part("Two M5 x 35 bolts", FX["tab"], COL["bolt"]), (0, 0, 70))],
       "phone tray onto the arm",
       "Lips up, tab flat under the arm end; two bolts down through arm and tab, nuts under; tray square to the arm",
       elev=-15, azim=-55, label_done=False)
    stand = upper + [M["tray"]]
    st(5, stand, [mv(M["clamps"], (0, 90, 60))], "stand onto the bench with two G-clamps",
       "Board's back edge flush with the bench's back edge; a clamp 20 mm in from each end; hand tight plus a quarter turn",
       context=bench, elev=20, azim=-60, label_done=False)
    st(6, stand + [M["clamps"]], [mv(M["mat"], (0, -220, 0))], "sorting mat onto the bench",
       "Slide it back until its back edge touches the board; line up the centre marks",
       context=bench, elev=28, azim=-60, label_done=False)
    st(7, stand + [M["clamps"], M["mat"]], [mv(M["phone"], (0, 0, 110))], "phone into the tray",
       "Screen up, charging end at the open end of the tray; lower it so the camera bump drops into the window",
       context=bench, elev=26, azim=-60, label_done=False)
    st(8, stand + [M["clamps"], M["mat"], M["phone"]],
       [mv(part("Power bank", C["powerbank"], COL["pb"]), (160, 0, 0)), part("Cable, in place", C["cable"], "#0369A1")],
       "power bank and cable",
       "Seen from behind, the user's side. Power bank beside the board; cable up the post's back face and along the arm top, two ties on each",
       context=bench, elev=24, azim=40, label_done=False)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "layouts", "joints", "steps"]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps}
    for w in what:
        r = fns[w]()
        print(w, "->", r)
