---
doc_id: WML-RSK-001
title: WasteWise-ml risk register and hazard analysis
project: WasteWise-ml
doc_type: Risk register and hazard analysis
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: MIT
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: First risk register, preliminary hazard analysis and design FMEA (kit 1.8 and 1.9.1 upgrade, stage P3)
---

# WasteWise-ml risk register and hazard analysis

The top risks are a hazardous item graded as sortable (a cell crushed in a bale can start a fire) and a model that never reaches its accuracy targets because the field data are harder or scarcer than assumed. Both are controlled by design (a separate high-recall hazard output, an honest "Unsure", a hazard box) and by evaluation before use (a 2,000-image field set with 400 hazards), but neither can be closed on paper. Method: STANDARDS section 23. Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high); detection is scored 1 (almost certain to be caught) to 5 (unlikely to be caught).

> **Safety:** WasteWise-ml guides sorting; it does not make any item safe to handle and does not certify material. The station handles sharps, broken glass, lithium cells, chemical containers and biological waste, and the phone, power bank and shutter button carry lithium cells.

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | No field partner | The first candidate (SWaCH) is not approached or declines | No grade list, no field photos, no evaluation; the project stops at TRL 3 | 3 | 5 | Project lead | Approach SWaCH through the Helpful Engineering network once TRL 4 is opened; keep a second candidate cooperative |
| R2 | Accuracy or coverage short of target | Field photos harder than assumed; learning curve flatter (M4); stream differs (M5) | PR-001 to PR-004 not met; pickers lose trust | 3 | 4 | ML lead | Measure the learning curve on the first 2,000 photos before collecting more; keep "Unsure" a normal answer; publish per-class results |
| R3 | Too few hazard photos | Hazards are about 3 % of the stream; 2,400 needed for training | Hazard recall below 98 % (PR-003) | 4 | 5 | ML lead | Photograph hazards on purpose at drop-off points, by trained people; 400-item hazard evaluation (N1) |
| R4 | Consent or ownership dispute | Protocol not agreed before collection | Data withdrawn; harm to the partnership | 2 | 5 | Data lead | Written protocol with the partner before any photo (D6, PR-014); DPDP Rules timeline (REG G2) |
| R5 | Dataset license blocks published weights | TACO images under mixed licenses; non-commercial sets | Weights cannot be published under MIT (PR-013) | 3 | 3 | Data lead | ZeroWaste excluded (N2); TACO filtered image by image; field data owned with the partner |
| R6 | Phone choice changes the rig | Lens offset or focal length differs from the assumed 26 mm, centred lens | Picture off the mat (PR-019); arm and tray remade | 3 | 2 | Design lead | Buy and measure the reference phone before cutting the arm (confirm items 1 and 2) |
| R7 | Labeling pay below a fair rate | Planning figure of USD 6 an hour used as the rate | Exploits the people the project serves | 2 | 4 | Project lead | Rate set with the partner at or above the local living wage (D7) |
| R8 | Concept choice reopened | Amish chooses option B | Drawing, BOM, build plan and requirements redone | 1 | 3 | Project lead | Decision D1 in WML-DEC-001 with the scoring of WML-OPT-001 |

## Preliminary hazard analysis

Table 2. Hazards at the sorting station with the rig.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Missed hazard graded as sortable | Model error on a cell, sharp or chemical container | Fire in a bale or sack; cut or needle-stick downstream | 5 | 2 | Separate hazard output tuned for recall (PR-003); a hazard result can never be overridden into a grade; buyer's check stays final; 400-item hazard evaluation before use | Medium: depends on field recall (R3) |
| H2 | Loose cell shorts in the hazard box | Terminals touch the steel walls, other cells or cans | Heat, thermal runaway, fire | 4 | 2 | Terminals taped, cells laid in the 50 mm sand bed clear of the walls, tape roll in the box (F3, PR-018); box lidded, away from paper and film | Low |
| H3 | Cell in thermal runaway in the hazard box | Damaged or crushed cell put in the box | Fire, smoke | 4 | 2 | Steel box and sand bed contain one phone-size cell (89 K mean sand rise, WML-CAL-001 section 14); larger packs to the partner's fire guidance; box outdoors or near the door | Medium for packs larger than a phone's |
| H4 | Cuts from sharps and broken glass | Handling items; reaching under the phone | Cuts, infection | 3 | 3 | Cut-resistant gloves; the app never asks anyone to hold an item closer; items lie still on the mat; sharps container | Medium (inherent to sorting) |
| H5 | Phone or power bank overheats | Rig in direct sun (about 85 C) | Swollen or burning cell, throttled phone | 4 | 2 | Rig stands in shade (BLD safety stop S4, PR-020); power bank shaded, off hot metal; never charge a swollen pack | Low |
| H6 | Repetitive reach to the phone | Screen 1,215 mm high, above the shoulder of short users | Shoulder strain | 2 | 3 | Shutter button at the bench edge (F1, PR-015); tap only as fallback | Low |
| H7 | Coin cell swallowed | Spare CR2032 cells for the shutter button within reach of small children at the site | Internal burns | 4 | 1 | Spare cells kept out of reach, with the partner's site rules; prefer a button whose cell cover needs a tool or a twist (to confirm when bought) | Low |
| H8 | Sharp edges on the made stand | Cut aluminium edges and tray corners | Cuts during building and use | 2 | 3 | Deburr and file every edge; tray corners rounded (BLD safety stop S2) | Low |
| H9 | Wrong grade costs the picker money | Misclassification of a sortable item | Lower price or a dispute with the buyer | 2 | 3 | "Unsure" as a normal answer; grades are advice; per-class error rates in the model card | Low |
| H10 | Personal data in photos | A face or identifiable person in a field photo | Privacy harm | 3 | 2 | Frame is the mat; no faces kept; opt-in upload; protocol with the partner (PR-014, REG G2) | Low |

## Design FMEA (first pass, P3)

Table 3. Failure modes of option A. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Hazard output of the model | Flag every hazard | Hazard missed | Fire or injury downstream (H1) | Rare class, too few training photos | 5 | 3 | 4 | 60 | Hazard photos collected on purpose; 400-item evaluation; threshold set for recall; buyer's check |
| F2 | Class and grade heads | Name the class and grade | Confident wrong grade | Lost value, dispute | Grades not visible in a photo; field shift | 3 | 3 | 3 | 27 | Per-class thresholds; "Unsure"; model card; retraining loop |
| F3 | Camera picture | Fall on the mat | Picture runs off the mat | Bench shows at the edges; lower accuracy | Lens shorter than 25.76 mm equivalent; phone tilted or turned in the tray; bump loose in the window; lens off centre | 2 | 3 | 2 | 12 | F5 (32 mm window, phone against the far lip); measure the phone; lens at 420 mm proposed (D2); first check "Picture on the mat"; arm cut to the lens offset |
| F4 | Phone tray | Hold the phone level, bump in the window | Phone slides or tilts | Picture shifts; phone falls on the mat | Phone wider or thicker than the tray; bump larger than the window | 3 | 2 | 2 | 12 | Confirm item 1; tray made after the phone is bought |
| F5 | Post and arm joints | Keep the camera still | Joint loosens | Picture drifts | Nyloc nuts not tightened; wood screws strip in the plywood | 2 | 2 | 2 | 8 | Hold point in step 5; nyloc nuts; check at the start of each shift |
| F6 | G-clamps | Hold the board to the bench | Clamp slips | Stand moves; picture shifts | Bench top thicker or thinner than the clamp's range; bench edge not square | 3 | 2 | 2 | 12 | Confirm item 3; clamps hand tight plus a quarter turn |
| F7 | USB cable | Power the phone | Cable pulled or chafed | Phone stops charging; plug damage | Cable caught by the user; rubbing on a bolt head | 2 | 2 | 2 | 8 | Cable along one edge of the arm top, clear of the bolts (F4); ties; 1.5 m with slack |
| F8 | Shutter button | Trigger the scan | Button does not trigger | User falls back to tapping the screen | Cell flat; pairing lost; app does not get the key press | 2 | 3 | 1 | 6 | Confirm item 5; cell life about 560 shifts; screen tap as fallback |
| F9 | Result screen and voice | Tell the user the bin | Result misread | Item in the wrong bin | Grazing view of the flat screen; noise drowns the voice | 3 | 2 | 3 | 18 | Full-screen colour and 40 mm bin number (F1, PR-016); voice by default; trials at TRL 4 |
| F10 | Sorting mat | Plain, flat background | Mat swells or cups | Uneven background, glare | Water through an unsealed face or edge | 2 | 2 | 2 | 8 | Sealed all over (F2, PR-017) |
| F11 | Hazard box | Contain hazards | Short or fire in the box | Fire at the station (H2, H3) | Bare terminals; large pack | 5 | 2 | 3 | 30 | Taped terminals and sand bed (F3); lid on; box away from combustibles; fire guidance for large packs |
| F12 | Phone | Run the model all shift | Overheats or flat battery | Scans stop | Direct sun; screen left on | 3 | 2 | 2 | 12 | Shade (S4, PR-020); screen sleeps between scans (PR-010); power bank |

The highest RPNs (F1, hazards missed, 60; F11, hazard box fire, 30; F2, confident wrong grade, 27) belong to the model and the hazard route, not the made rig. They are tested at TRL 4 with the field evaluation set and the site briefing; nothing in this table is verified yet.
