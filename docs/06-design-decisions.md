---
doc_id: WML-DEC-001
title: WasteWise-ml design decisions register
project: WasteWise-ml
doc_type: Design decisions register
version: "0.5"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: MIT
revisions:
  - version: "0.1"
    date: '2026-09-30'
    author: Amish Chadha
    change: Register opened with the build plan; open items from WML-DDR-001 to WML-DDR-003 and the review note
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Budget treated as a value-engineering target
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: Amish approved the recommendations for open items 1 to 6 on 2026-10-02 (WML-DDR-003 accepted, lens offset, no lamp, bench-clamped rig, SWaCH in Pune as first candidate partner, MIT-only contributing guide); moved to decisions made
  - version: "0.4"
    date: '2026-10-02'
    author: Amish Chadha
    change: Approved follow-ups carried out; value engineering savings corrected (the reference phone is already under USD 150)
  - version: "0.5"
    date: '2026-10-25'
    author: Amish Chadha
    change: "Kit 1.8 and 1.9.1 upgrade: concept selection D1 opened (option A recommended, proposed, awaiting Amish); STEM check fixes F1 to F3 and the cable route F4 recorded as decided under Amish's standing instruction of 2026-10-23 (WML-DDR-005); confirm items 5 and 6; value engineering updated to USD 313.39 a station; after the independent review, F5 (phone placement in the tray) made and D2 (lens at 420 mm) opened"
---

# WasteWise-ml design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | To be decided | Options | Recommendation | What it affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| D1 | Concept selection | (A) phone stand over a mat, the current design, 205 of 255; (B) tray detector, 152 of 255 | **Proposed, awaiting Amish: option A** (26 % ahead, outside the 10 % band). Graft from B: the bench-edge trigger (already in A as F1); a multi-item mode on A's stand later, once field data exist | Nothing if A; if B, the drawing, BOM, build plan and requirements are redone for the tray detector and the phone is no longer the computer | WML-OPT-001, WML-DDR-004 |
| D2 | Lens height above the mat | (a) keep 440 mm (decided by Amish, N3, 2026-09-25): 2.0 mm of margin left for the lens after the placement stack, so only lenses of 25.76 mm equivalent or longer fit; (b) 420 mm: picture 559 x 419 mm, 15.3 mm a side, lenses of 24.2 mm and longer fit, a little less resolution (0.14 mm a pixel); (c) a 480 mm deep mat (option c of A1, not chosen in 2026-10-02) | **Proposed, awaiting Amish: (b) 420 mm**, because a quoted 26 mm lens is rounded and the 440 mm margin is inside that rounding (WML-STM-001 S2, independent review 2026-10-25) | Post 20 mm shorter (433 mm); drawing, making sketch WML-DWG-103, build plan and CAL section 6 redone; nothing else | WML-STM-001 S2; WML-CAL-001 section 6 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The reference phone's width and thickness, the size of its camera bump and how far its lens is from the centre line across the width | They set the tray's inside width, the window and the arm's length; the model assumes 76 x 9 mm, a 30 x 30 mm bump and a centred lens | WML-DDR-003, A1 |
| 2 | The phone's main camera is a 26 mm-equivalent lens, or the picture size at 440 mm is measured | The picture's fit on the mat (586 x 439 mm on 700 x 450 mm) depends on it | WML-CAL-001, section 6 |
| 3 | The bench at the pilot site (first candidate: SWaCH, Pune) has a square back edge, a top 20 to 50 mm thick and room under it for a G-clamp's lower jaw | The board is clamped to that edge | WML-DDR-003, P1 |
| 4 | The USB cable reaches about 0.93 m with a loop to spare and fits the phone's port | The cable runs up the stand | WML-DDR-003, P5 |
| 5 | The shutter button pairs with the reference phone and the app receives its key press as the scan trigger | Fix F1 depends on it; the screen tap stays as the fallback | WML-DDR-005, F1 |
| 6 | The pilot site's bench height and the heights of the people who will use it | The reach and viewing checks of WML-CAL-001 section 12 assume a 760 mm bench and Indian women's stature from a published survey | WML-DDR-005, F1 |

## Value engineering

Value-engineering target: none set (a hypothetical control target is not defined here, because `budget_usd` is null in this software repository). Estimated cost of the constructable design: USD 313.39 for one station (USD 309.00 before the STEM check fixes of 2026-10-25 added the shutter button, USD 3.39, and the hazard box's tape roll, USD 1.00; USD 285 before the stand was made and clamped to the bench, WML-DDR-003), and USD 1,356.78 for a two-station pilot with the dataset, evaluation set and compute. Main cost drivers and savings worth trying:

- The reference phone is the largest line (USD 130), then the seven bins (USD 70), the hazard box (USD 26) and platform scale (USD 25), the power bank and cable (USD 15), the stand clamps and fixings (USD 14) and the shutter button (USD 3.39).
- The dataset and evaluation set labeling effort (USD 430 and USD 260) dominates the two-station pilot; its rate is set with the partner.
- Savings worth trying: the user's own phone, where it meets R12, in place of the USD 130 reference phone (the reference phone is already priced under the USD 150 ceiling of R12, so a cheaper phone is not counted as a saving). No lamp over the mat was decided on 2026-10-02 (option a), so the estimate already carries no lamp.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | D1 to D8: single item on a mat; MobileNetV3-Large with TensorFlow Lite and ONNX exports; keep the composite class and the unsure and hazard outputs; per-site grade file; tap-to-scan; consent, opt-in upload, no faces and co-ownership; labeling pay set with the partner at or above the local living wage; one reference phone per station for the evaluation | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | WML-DDR-001 |
| 2026-09-25 | N1: at least 400 hazard items in the evaluation set; N2: ZeroWaste excluded from training; N3: camera 440 mm above the mat; O3: kit option for MIT labels on drawing sheets (cross-repo action) | Amish: "i accept all your recommendations, go with them across all repos." | WML-DDR-002 |
| 2026-10-02 | Design for construction of the scanning rig accepted: clamped base board, square tube post and arm with corner plates, foot angles, folded phone tray, cable route and mat placed by the board (P1 to P6), as made | Amish: "i approve your recommendations for all 555 open decisions." | WML-DDR-003, P1 to P6 |
| 2026-10-02 | Phone lens off the centre line: option (a), lay the phone with its lens on the side away from the post and cut the arm shorter by the measured lens offset, only after the reference phone is bought and measured | Amish: "i approve your recommendations for all 555 open decisions." | WML-DDR-003, A1 |
| 2026-10-02 | Lighting: option (a) for the prototype, no lamp; the site light is recorded with every photo (a light reading or a gray card in a corner of the frame); a lamp is decided only after the first site visit | Amish: "i approve your recommendations for all 555 open decisions." | WML-DDR-003, A2 |
| 2026-10-02 | Sites without a suitable bench: option (a) for the prototype, the bench-clamped rig, with handheld use at sites without a square-edged bench about 600 mm deep | Amish: "i approve your recommendations for all 555 open decisions." | WML-DDR-003, A3 |
| 2026-10-02 | First partner, city and buyers: a member-owned waste picker cooperative that already sorts dry waste for scrap buyers; first candidate to approach SWaCH in Pune, India, with its existing scrap dealers as the buyers and Pune as the city | Amish: "i approve your recommendations for all 555 open decisions." | WML-DDR-001, O1 |
| 2026-10-02 | Contributing guide: remove the CERN-OHL-S sentence from `CONTRIBUTING.md` and state that all contributions are licensed under MIT | Amish: "i approve your recommendations for all 555 open decisions." | WML-DDR-001, O2 |
| 2026-10-25 | F1: a Bluetooth shutter button at the bench edge takes the photo; the result fills the screen in the class colour with a bin number at least 40 mm tall and is spoken by default (STEM rows B1, B2) | Decided under Amish's standing instruction of 2026-10-23: "whenever a STEM check fails propose and implement the best fix to the design and constructability" | WML-DDR-005, F1 |
| 2026-10-25 | F2: the mat is primed, painted and varnished on both faces and all four edges (STEM row C3) | Decided under the standing instruction of 2026-10-23 | WML-DDR-005, F2 |
| 2026-10-25 | F3: loose cells go into the hazard box with their terminals taped, in the sand bed clear of the walls; a tape roll lives in the box (STEM row C1) | Decided under the standing instruction of 2026-10-23 | WML-DDR-005, F3 |
| 2026-10-25 | F4: the USB cable runs along the arm top 8 mm to one side, clear of the tray tab bolts (found by the detailed model) | Decided under Amish's instructions of 2026-09-30 ("fix the design assumptions to match and be physically feasible") and 2026-10-23 | WML-DDR-005, F4 |
| 2026-10-25 | F5: the camera window is 32 mm (was 34) and the phone is pushed against the far lip of the tray, so it cannot turn; picture placement stack 3.3 mm against the 5.3 mm margin (STEM row S7, found by the independent review) | Decided under the standing instruction of 2026-10-23 | WML-DDR-005, F5 |
