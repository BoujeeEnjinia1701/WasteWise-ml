"""WasteWise-ml repo-specific CAD helpers (kit 1.9). Used by cad/src/model.py; nothing here belongs in .kit/.

Bought items the kit parts library does not carry (a phone, a power bank, a G-clamp, a sorting bin, a platform
scale, a Raspberry Pi board, a camera module, a touch display, a Bluetooth shutter button), plus fastener sizes the
kit's ISO table does not list (nyloc nuts, No. 8 wood screws, M2 and M2.5 pan head screws, cable ties).
Every function returns build123d solids in millimetres. Shapes are drawn at catalogue envelope with real wall
thickness, rounded corners and the features that make them recognisable; they are not manufacturer models.
CONCEPT, NOT FOR FABRICATION.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import (Box, Circle, Compound, Cylinder, Plane, Polyline, Pos, RectangleRounded, Rot,  # noqa: E402
                       RegularPolygon, Sketch, Solid, Vector, extrude, loft, make_face, Location)
import cad_parts as cp  # noqa: E402
from cad_parts import part  # noqa: E402


# ---------------------------------------------------------------------------------------------------------------
# Placement
# ---------------------------------------------------------------------------------------------------------------
def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box between two corners."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def rbox(x0, x1, y0, y1, z0, z1, r=2.0, edge=0.5):
    """Box with rounded vertical corners (radius r) and broken edges: a moulded or bought body."""
    w, d = x1 - x0, y1 - y0
    s = extrude(RectangleRounded(w, d, min(r, min(w, d) / 2 - 0.05)), z1 - z0)
    s = Pos((x0 + x1) / 2, (y0 + y1) / 2, z0) * s
    return cp.break_edges(s, edge) if edge else s


# local +Z of a kit fastener mapped to a global direction (the head sits on that side of the joint)
_TURN = {"+z": (0, 0, 0), "-z": (180, 0, 0), "+x": (0, 90, 0), "-x": (0, -90, 0), "+y": (-90, 0, 0), "-y": (90, 0, 0)}


def orient(shape, axis, xyz=(0, 0, 0)):
    """Turn a shape built along +Z so that +Z points along axis ('+x', '-y', ...) and move it to xyz."""
    return Pos(*xyz) * Rot(*_TURN[axis]) * shape


def hole(p0, axis, d, length=400.0):
    """A drilling cylinder of diameter d through point p0 along axis, centred on p0 (subtract it)."""
    return orient(Pos(0, 0, -length / 2) * Cylinder(d / 2, length), axis, p0)


# ---------------------------------------------------------------------------------------------------------------
# Fasteners not in the kit's ISO table
# ---------------------------------------------------------------------------------------------------------------
NYLOC_H = {5: 5.0, 6: 6.0, 8: 8.0}       # ISO 10511 thin nyloc nut height (max)


def _hex(s, h):
    prism = extrude(RegularPolygon(s / math.sqrt(3), 6), h)
    try:
        cap = cp.chamfer((Pos(0, 0, h / 2) * Cylinder(s / math.sqrt(3), h)).edges(), s / math.sqrt(3) - s / 2 * 0.95)
        return prism & cap
    except Exception:
        return prism


def nyloc_nut(d):
    """ISO 10511 prevailing torque nut: hex body with the nylon collar step at the top."""
    s = cp.ISO[d][0]
    h = NYLOC_H[d]
    body = _hex(s, h * 0.75)
    collar = Pos(0, 0, h * 0.75) * Cylinder(s * 0.47, h * 0.25, align=None)
    return (body + collar) - Pos(0, 0, h / 2) * Cylinder(d / 2, h + 1)


def bolt_set(d, grip, axis, xyz, label, explode=(0, 0, 0), extra=None, nut="nyloc", group="fixings"):
    """Bolt, two ISO 7089 washers and a nut clamping a joint 'grip' thick. The joint face on the head side is at
    xyz and the bolt points along -axis (axis is the head side). Returns part dicts (kind fastener). The length is
    rounded up to the next 5 mm so 1 to 3 threads show beyond the nut."""
    s, k, m, d2, h, p = cp.ISO[d]
    mn = NYLOC_H[d] if nut == "nyloc" else m
    L = math.ceil((grip + 2 * h + mn + (extra if extra is not None else 2.5 * p)) / 5) * 5
    nut_shape = nyloc_nut(d) if nut == "nyloc" else cp.hex_nut(d)
    nut_name = f"M{d} nyloc nut (ISO 10511)" if nut == "nyloc" else f"M{d} hex nut (ISO 4032)"
    local = [(f"M{d}x{L} hex bolt (ISO 4017)", Pos(0, 0, h) * cp.hex_bolt(d, L)),
             (f"M{d} washer (ISO 7089)", cp.washer(d)),
             (f"M{d} washer (ISO 7089)", Pos(0, 0, -grip - h) * cp.washer(d)),
             (nut_name, Pos(0, 0, -grip - h - mn) * nut_shape)]
    return [part(f"{n}, {label}", orient(sh, axis, xyz), "stainless", kind="fastener", bom=11, group=group,
                 explode=explode) for n, sh in local]


def wood_screw(length=16.0, d=4.2, head_d=8.0):
    """No. 8 pan head wood screw: head on z 0 to 3, threaded shank down to -length with a pointed tip."""
    head = cp.break_edges(Pos(0, 0, 1.5) * Cylinder(head_d / 2, 3.0), 0.8)
    slot = box(-head_d / 2, head_d / 2, -0.4, 0.4, 2.0, 3.1)
    shank = Pos(0, 0, -(length - 2) / 2) * Cylinder(d / 2, length - 2)
    tip = extrude(Circle(d / 2), 2.0, taper=40)
    tip = Pos(0, 0, -length + 2) * Rot(180, 0, 0) * tip
    return (head - slot) + shank + tip


def pan_screw(d, length):
    """ISO 7045 cross-recess pan head machine screw (M2, M2.5, M3): head z 0 to 0.7d, shank down to -length."""
    hd, hk = 2 * d, 0.7 * d
    head = cp.break_edges(Pos(0, 0, hk / 2) * Cylinder(hd / 2, hk), d * 0.2)
    cross = box(-d * 0.6, d * 0.6, -d * 0.12, d * 0.12, hk * 0.4, hk + 0.1) + box(-d * 0.12, d * 0.12, -d * 0.6, d * 0.6, hk * 0.4, hk + 0.1)
    return (head - cross) + Pos(0, 0, -length / 2) * Cylinder(d / 2, length)


def cable_tie_loop(w_in, h_in, band=2.5, t=1.2, head=(6.0, 4.0, 5.0)):
    """A cable tie closed round a w_in x h_in bundle: a band in the XY plane around the origin, head on +X."""
    outer = extrude(RectangleRounded(w_in + 2 * t, h_in + 2 * t, t + 0.6), band)
    inner = extrude(RectangleRounded(w_in, h_in, 0.6), band)
    loop = outer - inner
    hx = Pos(w_in / 2 + t + head[0] / 2 - 0.5, 0, band / 2) * Box(head[0], head[1], head[2])
    return Pos(0, 0, -band / 2) * cp.break_edges(loop + hx, 0.3)


# ---------------------------------------------------------------------------------------------------------------
# Bought items
# ---------------------------------------------------------------------------------------------------------------
def phone(l, w, t, bump=30.0, bump_h=2.0, lens_dx=0.0):
    """Smartphone lying screen up, its back on z = 0 ... returns (body, screen glass). The camera bump hangs below
    z = 0 by bump_h, centred lens_dx from the body centre along X. Body corners r 9 mm, glass 0.8 mm."""
    body = extrude(RectangleRounded(l, w, 9.0), t - 0.8)
    body = cp.break_edges(body, 1.2)
    bp = Pos(lens_dx, 0, -bump_h) * extrude(RectangleRounded(bump, bump, 6.0), bump_h)
    lens = Pos(lens_dx - bump * 0.18, bump * 0.18, -bump_h - 0.01) * Cylinder(5.0, 1.2, align=None)
    lens2 = Pos(lens_dx + bump * 0.18, -bump * 0.18, -bump_h - 0.01) * Cylinder(3.5, 1.2, align=None)
    port = box(-l / 2 - 0.1, -l / 2 + 7, -4.5, 4.5, (t - 0.8) / 2 - 1.6, (t - 0.8) / 2 + 1.6)
    btn = box(-20, 5, w / 2 - 0.01, w / 2 + 0.6, (t - 0.8) / 2 - 1.2, (t - 0.8) / 2 + 1.2)
    body = (body + bp + btn) - lens - lens2 - port
    glass = Pos(0, 0, t - 0.8) * cp.break_edges(extrude(RectangleRounded(l - 1.0, w - 1.0, 8.5), 0.8), 0.3)
    return body, glass


def power_bank(l, d, t):
    """USB power bank lying flat, z 0 to t: rounded body with USB-A and USB-C ports on its -X end and an LED strip."""
    b = rbox(-l / 2, l / 2, -d / 2, d / 2, 0, t, r=8.0, edge=1.5)
    for y, w_, h_ in ((-16, 13.0, 5.5), (2, 13.0, 5.5), (20, 9.0, 3.2)):
        b = b - box(-l / 2 - 1, -l / 2 + 8, y - w_ / 2, y + w_ / 2, t / 2 - h_ / 2, t / 2 + h_ / 2)
    for i in range(4):
        b = b - box(l / 2 - 30 + 6 * i, l / 2 - 27 + 6 * i, -d / 2 - 0.5, -d / 2 + 0.6, t / 2 - 1, t / 2 + 1)
    return b


def usb_plug(length=12.0):
    """USB-C plug overmould along +X from x = 0 (the cable end) to x = length (the phone end)."""
    body = rbox(0, length - 6.5, -5.0, 5.0, -3.5, 3.5, r=3.0, edge=0.8)
    tongue = rbox(length - 6.5, length, -4.2, 4.2, -1.3, 1.3, r=1.2, edge=0.2)
    return body + tongue


def g_clamp(xc, y_front, y_spine, z_jaw, z_under, throat_t=12.0, screw_d=10.0):
    """Malleable iron G-clamp in a YZ plane at x = xc: the fixed upper jaw rests on z_jaw (the board top) from
    y_front back to the spine behind the bench edge at y_spine, the screw comes up from the lower arm to a swivel pad
    pressing the bench top's underside at z_under. Returns [(name, shape, material), ...]."""
    sp0, sp1 = y_spine, y_spine + 15.0
    ys = y_front + 15.0                       # screw axis
    z_lo1 = z_under - 30.0                    # top of the lower arm
    z_lo0 = z_lo1 - 12.0
    # outline in the YZ plane, then extruded throat_t along X
    outline = [(y_front, z_jaw), (sp0, z_jaw), (sp0, z_lo1), (y_front - 8, z_lo1), (y_front - 8, z_lo0),
               (sp1, z_lo0), (sp1, z_jaw + 10.0), (y_front, z_jaw + 10.0)]
    face = make_face(Polyline(*outline, close=True))
    pl = Plane(origin=Vector(xc - throat_t / 2, 0, 0), x_dir=Vector(0, 1, 0), z_dir=Vector(1, 0, 0))
    frame = extrude(pl * face, throat_t)
    frame = cp.break_edges(frame, 1.5)
    frame = frame - Pos(xc, ys, z_lo0 - 5) * Cylinder(screw_d / 2, 30, align=None)
    pad_t = 8.0
    pad = cp.break_edges(Pos(xc, ys, z_under - pad_t) * Cylinder(11.0, pad_t, align=None), 1.0)
    screw_len = (z_under - pad_t) - (z_lo0 - 40.0)
    screw = Pos(xc, ys, z_lo0 - 40.0) * cp.round_bar(screw_d, screw_len, 0.8)
    tbar = Pos(xc, ys, z_lo0 - 33.0) * Rot(0, 90, 0) * Pos(0, 0, -35) * cp.round_bar(6.0, 70, 0.6)
    tbar = tbar - Pos(xc, ys, z_lo0 - 40.0) * Cylinder(screw_d / 2, 20, align=None)
    return [("G-clamp frame (100 mm, malleable iron)", frame, "painted_steel"),
            ("G-clamp screw (M10)", screw, "zinc_plated"),
            ("G-clamp swivel pad", pad, "zinc_plated"),
            ("G-clamp tommy bar", tbar, "zinc_plated")]


def bin_shell(w, d, h, taper, t, r=30.0, rim=8.0, rim_h=22.0):
    """Tapered moulded bin, open top, z 0 to h: outer top w x d, bottom smaller by taper on every side, wall t,
    with an outward rim lip at the top. Origin at the top outline's -X -Y corner."""
    top = Plane.XY.offset(h) * RectangleRounded(w, d, r)
    bot = Plane.XY * RectangleRounded(w - 2 * taper, d - 2 * taper, max(r - taper * 0.5, 6.0))
    outer = loft([bot, top])
    itop = Plane.XY.offset(h + 1) * RectangleRounded(w - 2 * t, d - 2 * t, r - t)
    ibot = Plane.XY.offset(t) * RectangleRounded(w - 2 * taper - 2 * t, d - 2 * taper - 2 * t, max(r - taper * 0.5 - t, 4.0))
    inner = loft([ibot, itop])
    lip = Pos(0, 0, h - rim_h) * (extrude(RectangleRounded(w + 2 * rim, d + 2 * rim, r + rim), rim_h)
                                   - extrude(RectangleRounded(w - 0.2, d - 0.2, r), rim_h))
    s = outer - inner + lip
    return Pos(w / 2, d / 2, 0) * s


def touch_display(w, h, t):
    """Touch display module: glass face on +Z (z t - 1.1 to t), metal back tray with the four mounting bosses."""
    glass = rbox(-w / 2, w / 2, -h / 2, h / 2, t - 1.1, t, r=4.0, edge=0.3)
    tray = rbox(-w / 2 + 1, w / 2 - 1, -h / 2 + 1, h / 2 - 1, 0, t - 1.1, r=3.5, edge=0.6)
    for x in (-w / 2 + 12, w / 2 - 12):
        for y in (-h / 2 + 10, h / 2 - 10):
            tray = tray - Pos(x, y, -0.1) * Cylinder(1.1, 4.0, align=None)
    return tray, glass


def pi5_board():
    """Raspberry Pi 5 at catalogue envelope: 85 x 56 x 1.6 mm PCB (corner radius 3, four 2.7 mm mounting holes on
    58 x 49 mm centres, 3.5 mm in from the edges) with the USB, Ethernet, USB-C and micro HDMI connectors, the
    SoC and the RP1 chip. PCB underside at z = 0, origin at the PCB centre."""
    L, W, T = 85.0, 56.0, 1.6
    pcb = extrude(RectangleRounded(L, W, 3.0), T)
    for x, y in pi5_holes():
        pcb = pcb - Pos(x, y, -0.1) * Cylinder(1.35, T + 0.2, align=None)
    parts = [pcb]
    x1 = L / 2
    parts += [rbox(x1 - 17.5, x1 + 2.5, -W / 2 + 2 + o, -W / 2 + 2 + o + 13.2, T, T + 15.6, r=0.5, edge=0.2) for o in (0.0, 18.0)]   # USB-A stacks
    parts.append(rbox(x1 - 19.5, x1 + 2.5, W / 2 - 18.0, W / 2 - 2.0, T, T + 13.5, r=0.5, edge=0.2))                               # Ethernet
    parts.append(rbox(-L / 2 + 6.0, -L / 2 + 15.0, -W / 2 - 1.0, -W / 2 + 6.5, T, T + 3.2, r=1.0, edge=0.2))                       # USB-C
    for x in (-L / 2 + 22.0, -L / 2 + 35.5):
        parts.append(rbox(x, x + 6.5, -W / 2 - 1.0, -W / 2 + 6.0, T, T + 3.0, r=0.6, edge=0.2))                                     # micro HDMI
    parts.append(rbox(-12.0, 5.0, -8.0, 9.0, T, T + 2.4, r=0.5, edge=0.2))                                                          # SoC
    parts.append(rbox(10.0, 20.0, -12.0, -2.0, T, T + 1.2, r=0.4, edge=0.2))                                                        # RP1
    head =box(-L / 2 + 3.5 + 29 - 25.4, -L / 2 + 3.5 + 29 + 25.4, W / 2 - 6.0, W / 2 - 1.0, T, T + 8.5)                              # GPIO header
    parts.append(head)
    out = parts[0]
    for q in parts[1:]:
        out = out + q
    return out


def pi5_holes():
    return [(-85.0 / 2 + 3.5 + dx, -56.0 / 2 + 3.5 + dy) for dx in (0.0, 58.0) for dy in (0.0, 49.0)]


def active_cooler():
    """Raspberry Pi 5 active cooler at envelope: finned aluminium heatsink with a 30 mm fan, underside at z = 0."""
    base = rbox(-27.0, 27.0, -20.0, 20.0, 0, 2.0, r=1.0, edge=0.3)
    fins = None
    for i in range(9):
        f = box(-27.0 + 1 + i * 3.0, -27.0 + 2.2 + i * 3.0, -20.0, 20.0, 2.0, 8.0)
        fins = f if fins is None else fins + f
    shroud = rbox(0.0, 27.0, -20.0, 20.0, 2.0, 9.0, r=2.0, edge=0.4) - Pos(13.5, 0, 1.0) * Cylinder(14.0, 10.0, align=None)
    fan = Pos(13.5, 0, 2.5) * (Cylinder(13.0, 5.0, align=None) - Cylinder(5.0, 6.0, align=None))
    return base + fins + shroud + fan


def camera_module_3():
    """Raspberry Pi Camera Module 3 (wide) at envelope: 25 x 24 x 1 mm board with four 2.2 mm holes, the lens block
    and lens barrel on the -Z face (the camera looks down -Z), and the 15-way ribbon connector. Board top at z = 0."""
    pcb = Pos(0, 0, -1.0) * extrude(RectangleRounded(25.0, 24.0, 2.0), 1.0)
    for x in (-10.5, 10.5):
        for y in (-9.5, 3.0):
            pcb = pcb - Pos(x, y, -1.2) * Cylinder(1.1, 1.4, align=None)
    block = rbox(-4.25, 4.25, -4.25 + 2.0, 4.25 + 2.0, -1.0 - 5.0, -1.0, r=0.6, edge=0.3)
    barrel = Pos(0, 2.0, -1.0 - 5.0 - 6.4) * cp.break_edges(Cylinder(4.2, 6.4, align=None), 0.4)
    glass = Pos(0, 2.0, -1.0 - 5.0 - 6.6) * Cylinder(2.6, 0.3, align=None)
    conn = rbox(-8.5, 8.5, -12.0, -7.0, 0.0, 2.6, r=0.3, edge=0.2)
    return pcb + block + barrel + glass + conn


def shutter_button(l=40.0, w=26.0, t=11.0):
    """Bluetooth camera shutter button (key-fob type, one CR2032 cell): body lying flat z 0 to t with the round
    button on top and a lanyard eye at the -X end."""
    body = rbox(-l / 2, l / 2, -w / 2, w / 2, 0, t, r=w / 2 - 1.0, edge=2.0)
    eye = Pos(-l / 2 - 2.5, 0, t / 2 - 2.0) * (Cylinder(4.5, 4.0, align=None) - Cylinder(2.0, 5.0, align=None))
    body = body + eye
    btn = cp.break_edges(Pos(3.0, 0, t) * Cylinder(8.0, 1.6, align=None), 0.6)
    return body, btn


def arcade_button(d=30.0, panel_t=2.0):
    """30 mm arcade push button: bezel ring on the panel top (z 0 to 3), plunger cap, nut and switch body below."""
    bezel = cp.break_edges(Pos(0, 0, 0) * (Cylinder(d / 2 + 3.0, 3.0, align=None) - Cylinder(d / 2 - 2.0, 4.0, align=None)), 0.6)
    cap = cp.break_edges(Pos(0, 0, 0.5) * Cylinder(d / 2 - 2.6, 5.0, align=None), 1.2)
    body = Pos(0, 0, -panel_t - 30.0) * Cylinder(d / 2 - 3.5, 30.0, align=None)
    nut = Pos(0, 0, -panel_t - 5.0) * (Cylinder(d / 2 + 4.0, 5.0, align=None) - Cylinder(d / 2 - 3.4, 6.0, align=None))
    sw = rbox(-6.0, 6.0, -10.0, 10.0, -panel_t - 30.0 - 18.0, -panel_t - 30.0, r=1.0, edge=0.3)
    return bezel + cap, body + sw, nut


def tape_roll(od=50.0, idd=38.0, w=19.0):
    """Roll of PVC insulating tape lying flat, z 0 to w."""
    return cp.break_edges(extrude(Sketch() + Circle(od / 2) - Circle(idd / 2), w), 1.0)
