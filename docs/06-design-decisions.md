---
doc_id: WML-DEC-001
title: WasteWise-ml design decisions register
project: WasteWise-ml
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-01'
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
---

# WasteWise-ml design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design for construction of the scanning rig: clamped base board, square tube post and arm with corner plates, foot angles, folded phone tray, cable route, mat placed by the board | Accept; change any item | Accept: each change keeps what the rig does and nothing changes the pitch or the safety case | The whole stand (build plan sections 3.1 to 3.6) | WML-DDR-003, P1 to P6 |
| 2 | How the rig suits a phone whose lens is off its centre line across the width (the mat has 5.3 mm to spare front and back) | (a) cut the arm shorter by the lens offset; (b) slot the tray tab so the tray slides; (c) a 480 mm deep mat | (a): no new part | Arm length and tray window (build plan sections 3.4 and 3.6) | WML-DDR-003, A1 |
| 3 | Lighting over the mat | (a) no lamp, site light recorded with each photo; (b) diffused 12 V LED strip under the arm; (c) a lamp chosen with the partner after the first site visit | (a) for the prototype; decide with field data, since a lamp changes the training photos | None for (a); a strip and its wiring for (b) | WML-DDR-003, A2 |
| 4 | Sites without a suitable bench (square back edge, about 600 mm deep or more) | (a) as designed, handheld use elsewhere; (b) a separate base plate for floor or table use | (a) for the prototype | None for (a) | WML-DDR-003, A3 |
| 5 | First partner organization, city and buyers | Partner, city and buyers for co-design, the field dataset and the evaluation set | None yet | Not part of the rig build; sets the reference phone, the site light and the bench | WML-DDR-001, O1 |
| 6 | The CERN-OHL-S line in `CONTRIBUTING.md` in an MIT-only repository | Remove the line; keep it | None yet | None | WML-DDR-001, O2 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The reference phone's width and thickness, the size of its camera bump and how far its lens is from the centre line across the width | They set the tray's inside width, the window and the arm's length; the model assumes 76 x 9 mm, a 30 x 30 mm bump and a centred lens | WML-DDR-003, A1 |
| 2 | The phone's main camera is a 26 mm-equivalent lens, or the picture size at 440 mm is measured | The picture's fit on the mat (586 x 439 mm on 700 x 450 mm) depends on it | WML-CAL-001, section 6 |
| 3 | The bench at the pilot site has a square back edge, a top 20 to 50 mm thick and room under it for a G-clamp's lower jaw | The board is clamped to that edge | WML-DDR-003, P1 |
| 4 | The USB cable reaches about 0.93 m with a loop to spare and fits the phone's port | The cable runs up the stand | WML-DDR-003, P5 |

## Value engineering

Value-engineering target: none set (a hypothetical control target is not defined here, because `budget_usd` is null in this software repository). Estimated cost of the constructable design: USD 309 for one station, up from USD 285 because the stand is now made and clamped to the bench (WML-DDR-003), and USD 1,348 for a two-station pilot with the dataset, evaluation set and compute. Main cost drivers and savings worth trying:

- The reference phone is the largest line (USD 130), then the seven bins (USD 70), the hazard box and platform scale (USD 25 each), the power bank and cable (USD 15) and the stand clamps and fixings (USD 14).
- The dataset and evaluation set labeling effort (USD 430 and USD 260) dominates the two-station pilot; its rate is set with the partner.
- Savings worth trying: a cheaper phone that still meets R12 (about USD 150 or less, 3 GB RAM, 2019 or later chipset), and no lamp over the mat (open decision 3, option a).

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | D1 to D8: single item on a mat; MobileNetV3-Large with TensorFlow Lite and ONNX exports; keep the composite class and the unsure and hazard outputs; per-site grade file; tap-to-scan; consent, opt-in upload, no faces and co-ownership; labeling pay set with the partner at or above the local living wage; one reference phone per station for the evaluation | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | WML-DDR-001 |
| 2026-09-25 | N1: at least 400 hazard items in the evaluation set; N2: ZeroWaste excluded from training; N3: camera 440 mm above the mat; O3: kit option for MIT labels on drawing sheets (cross-repo action) | Amish: "i accept all your recommendations, go with them across all repos." | WML-DDR-002 |
