"""WasteWise-ml drawing sheets.

Run from the repo root:  python cad/src/sheets.py
Builds WML-DWG-001 (sorting station general arrangement, Rev P1) in cad/drawings/ from
cad/src/model.py. WML-DWG-010 is the concept sheet made by cad/src/concept_media.py.
This repository is MIT licensed (software only), so the sheet license label is MIT.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(ROOT / "cad" / "src"))
from drawing import Sheet, project_views  # noqa: E402
import model  # noqa: E402

p = model.derived()
work = ROOT / "cad" / "drawings" / "_views"
asm = model.station()
bb = asm.bounding_box().size
views = project_views(asm, work)
bench_views = project_views(model.bench_group(), work / "bench")

s = Sheet(project="WasteWise-ml", title="Sorting station general arrangement", dwg_no="WML-DWG-001", rev="P1",
          author="Amish Chadha", date="2026-09-25", scale=None, concept=True, license="MIT",
          material="Bought items per bom/bom.csv; bench is the site's own. PRELIMINARY, NOT FOR FABRICATION",
          revisions=[("P1", "General arrangement for TRL 3 (WML-CAL-001)", "2026-09-25", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(bench_views["iso"], 276, 32, 140, 70, label="Bench detail, isometric",
          sublabel="Not to scale; phone, stand, mat, power bank, hazard box")
s.add_notes("Main dimensions (mm)", [
    f"Station envelope {bb.X:.0f} x {bb.Y:.0f} x {bb.Z:.0f} incl. bins, scale",
    f"Bench (site's) {p['bench_l']:.0f} x {p['bench_d']:.0f}, top at {p['bench_h']:.0f}",
    f"Mat {p['mat_l']:.0f} x {p['mat_d']:.0f} x {p['mat_t']:.0f}, {p['grid']:.0f} grid",
    f"Camera lens {p['cam_h']:.0f} above mat, {p['lens_z']:.0f} above floor",
    f"Camera frame {p['frame_x']:.0f} x {p['frame_y']:.0f} on mat (26 mm eq.)",
    f"Phone {p['phone_l']:.0f} x {p['phone_w']:.0f}, landscape, screen up",
    f"Stand base {p['base_l']:.0f} x {p['base_d']:.0f} at Y {p['base_y']:.0f}, clear of frame",
    f"Hazard box {p['haz_l']:.0f} x {p['haz_d']:.0f} x {p['haz_h']:.0f}, lidded steel",
    f"Bins 7 x {p['bin_w']:.0f} x {p['bin_d']:.0f} x {p['bin_h']:.0f}, {p['bin_pitch']:.0f} pitch, {p['bin_vol_l']:.0f} L",
    f"Scale platform {p['scale_l']:.0f} x {p['scale_d']:.0f}, 60 kg",
], x=276, y=118, width=140)
s.add_notes("Parts list (items match bom/bom.csv)", [
    "1 Smartphone running the model",
    "2 Phone stand with clamp arm",
    "3 Light sorting mat",
    "4 Bins by material class (7)",
    "5 Hazard box with sand and sharps container",
], x=20, y=222, width=100)
s.add_notes("Parts list, continued", [
    "6 Power bank and cable",
    "7 Platform scale",
    "Bins left to right: PET; HDPE and PP; film;",
    "metal; paper and carton; glass; Unsure",
    "Hazards never auto-sorted (see WML-PRC-001)",
], x=124, y=222, width=100)
s.save(ROOT / "cad" / "drawings" / "WML-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("Wrote cad/drawings/WML-DWG-001.svg, .pdf and .png")
