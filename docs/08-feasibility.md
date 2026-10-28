---
doc_id: WML-FEA-001
title: WasteWise-ml feasibility assessment
project: WasteWise-ml
doc_type: Feasibility assessment
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: MIT
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: First feasibility assessment (kit 1.8 upgrade), closed at stage P3 with the open items named
---

# WasteWise-ml feasibility assessment

**Verdict: feasible on paper, with the data as the one Low-rated aspect.** The hardware, the model's size, speed and energy, and the build are all well inside known limits and buildable with hand tools (WML-STM-001, WML-CAL-001, WML-BLD-001). Whether the model reaches its accuracy and coverage targets on real waste depends on about 10,000 consented field photos and a 2,000-image evaluation set that do not yet exist; building them is TRL 4 work with a partner and is on hold. The assessment is closed at stage P3 with that item open. Method: STANDARDS section 23.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | One item on a mat under a phone held 440 mm above it on a clamped stand; the picture (586 x 439 mm) falls on the 700 x 450 mm mat with the stand outside it; every rig joint face to face and bolted; 115 constructability checks pass | High | The picture has 5.3 mm to spare front and back, 3.3 mm of it taken by the phone's placement in the tray after fix F5, so only lenses of 25.76 mm equivalent or longer fit (PR-019 at risk); a 420 mm lens height is proposed to Amish (D2); measured on the bought phone before the arm is cut | WML-STM-001 S1, S2, S6, S7; WML-CAL-001 sections 6 and 11; `python cad/src/model.py --check` |
| Materials | Plywood, 6063 aluminium tube, angle and sheet, painted and sealed hardboard, stainless fixings; all common stock | High | Hardboard swells if any face or edge is unsealed (fixed by F2) | WML-STM-001 C3; BOM lines 2, 3, 11 |
| Manufacturing and assembly | Sawing, drilling, filing and folding thin sheet; no welding, machining or wiring; eight assembly steps with pictures | High | Arm length and tray window depend on the bought phone (confirm items 1 and 2) | WML-BLD-001; WML-DEC-001 confirm items 1 to 4 |
| Power and controls | Tap-to-scan with the screen asleep uses 9 % of a 4,000 mAh battery a shift, with voice and the Bluetooth button; the power bank covers the screen-on case | High | The screen must sleep between scans; in heat the phone pauses charging, which tap-to-scan does not need | WML-STM-001 S4, S5, S8; WML-CAL-001 sections 5 and 13 |
| Software and model | MobileNetV3-Large, 4.4 MB in 8-bit form, 64 to 201 ms on a low-cost phone, about 8 MB of memory; per-site grade file | High | MobileNetV3-Small stays the fallback for very old phones | WML-STM-001 M1, M2, E3; WML-CAL-001 sections 2 and 3 |
| Data and evaluation | About 10,000 field photos (72 h of labeling) and a 2,000-image evaluation set with 400 hazards (43 h) | Low | Learning curve, coverage and hazard rarity are assumptions (M4, M5 open); hazard photos must be collected on purpose by trained people; consent and co-ownership protocol not yet written | WML-STM-001 M3 to M5; WML-CAL-001 sections 7 to 9; PR-011 not met |
| Human factors | With fix F1 nobody reaches up to the phone, and the result reads at 43 arcmin or more for every user from the 5th percentile up, and is spoken | Medium | Screens only; bench heights, users' heights and the voice prompt in noise to be checked with users | WML-STM-001 B1, B2; WML-CAL-001 section 12 |
| Safety | Hazards flagged, never sorted; hazard box with sand, sharps container and taped cell terminals; rig in shade | Medium | A missed hazard is the worst failure (PR-003 at risk); larger battery packs exceed what the sand bed is sized for | WML-STM-001 C1, C2; WML-RSK-001 |
| Supply of parts | Every station item is sold locally in Pune or online; only the reference phone is above USD 100 | High | Prices are indicative except lines 12 (cited) and the option B items; the stamped scale's verification fee is to assess | BOM; WML-MKT-001 |
| Partner and people | First candidate SWaCH, Pune (decided 2026-10-02), not yet approached | Medium | Without a partner there is no field data, no grade list and no evaluation | WML-PRB-001 Table 2; WML-PLN-001 |

Ratings: High, Medium, Low.
