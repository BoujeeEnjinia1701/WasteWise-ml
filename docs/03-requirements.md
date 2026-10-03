---
doc_id: WML-REQ-001
title: WasteWise-ml requirements
project: WasteWise-ml
doc_type: Requirements
version: "0.5"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: MIT
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from WML-CAL-001; decisions of WML-DDR-001 applied (R9, R10, R12, R14); R3 verification size flagged
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: Decisions of 2026-10-02 (WML-DEC-001) carried in; no lamp, site light recorded with every photo; first candidate partner named in R14; no status change
---

# WasteWise-ml requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with users, and will be revised after co-design sessions (see WML-PRB-001). No model has been trained, and at TRL 3 none will be: the status column gives the position on paper from the calculation note WML-CAL-001 and says plainly where a requirement is not met. No target was relaxed or redefined by the 2026-09-25 decisions (WML-DDR-001); they fix the design choices that the status depends on.

The **reference use case** is one person at a sorting bench with a low-cost Android phone on a stand over one item at a time on a light mat (decided, D1), or holding the phone by hand on the floor, on a dry mixed stream, in daylight or a lit shed with no lamp on the rig (decided 2026-10-02; the site light is recorded with every photo), with no network. The app uses tap-to-scan (decided, D5).

**Table 1.** Requirements, targets and status at TRL 3.

| ID | Requirement | Target | Verification (TRL 4 or later, on hold) | Status at TRL 3 (WML-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Material class accuracy | Top-1 accuracy of 90 % or more on the seven classes in `ml/data/taxonomy.yaml`, on items the model does not abstain on, on the field evaluation set (R11) | Evaluation on the held-out field set | At risk: expected full-coverage class error 9.1 % with about 1,290 photos per class, on an assumed learning curve |
| R2 | Plastic grade accuracy from a photo | 90 % or more for PET bottles and trays, 80 % or more for other rigid HDPE and PP, on non-abstained items | Field set, ground truth from NIR (WasteWise Scan) or legible resin codes | **Not met by design** for opaque HDPE versus PP and for black plastics (about 9 % of items); these go to "Unsure" and to WasteWise Scan. At risk for PET |
| R3 | Hazard flag | Recall of 98 % or more for batteries, sharps and chemical containers; a hazard result is never offered as a sortable grade | Field set with at least 400 hazard items (decided, N1; 400 items prove 98 % with up to 3 misses, where 200 would allow none, WML-CAL-001) | At risk: hazards are rare (about 300 in 10,000 natural photos against 2,400 needed) |
| R4 | Abstain when unsure | Model says "Unsure" below a set confidence; coverage (share of items answered) 70 % or more while meeting R1 | Coverage and accuracy curve on the field set | At risk: about 68 % answered (65 % with a grade, 3 % hazard flags), 32 % "Unsure" |
| R5 | Offline, on-device speed | Result within 0.3 s of the photo on the reference phone (R12), with no network | Timing on the reference phone | Met on paper: 64 to 201 ms for MobileNetV3-Large in 8-bit form (decided, D2) |
| R6 | Small download | Model file 10 MB or less; app with model 30 MB or less | File sizes of the exported models | Met on paper: 4.4 MB in 8-bit form; app 12 to 19 MB. Float32 (17.5 MB) would not meet it |
| R7 | Quick to use | 3 s or less from placing an item to seeing the result, including tap and camera focus | Timed trials with users | Not verifiable at TRL 3: time budget 0.9 s nominal, 2.0 s worst |
| R8 | Usable without reading | Result shown as icon, color and bin number, with optional voice in the local language; users new to the app sort correctly after a 15 min briefing | Co-design sessions and usability trials | Not verifiable at TRL 3; depends on co-design |
| R9 | Local grades | Buyer grade names and bin numbers set per site in a configuration file, without retraining, for grades the model already separates | Configuration review | Met by design review (per-site file decided, D4); new visual grades still need retraining |
| R10 | Battery life | A full 8 h shift with up to 500 scans uses 30 % or less of a 4,000 mAh phone battery | Energy estimate; later measurement | Met on condition: 8 % with tap-to-scan and the screen sleeping between scans; 51 % with the screen on all shift (met only with the power bank); 130 % with a live preview |
| R11 | Field evaluation set | 2,000 or more verified images from at least two sites, 50 or more per grade, never used for training | Dataset manifest | **Not met**: the set does not exist. Sized at 2,000 (400 hazards, 900 non-hazard minimum, 700 natural mix), about 43 h of labeling |
| R12 | Reference phone | Runs on an Android phone costing about $150 or less, 3 GB RAM, 2019 or later chipset | Device test | Met on paper: $130 indicative reference phone, one per pilot station (decided, D8) |
| R13 | Open and licensed | Code and weights MIT; every dataset license in `ml/data/SOURCES.md` allows training and publishing weights; a model card with per-class results and known failure modes | License review | At risk: TrashNet (MIT) and TACO (annotations CC BY 4.0, images per image) usable with checks; ZeroWaste (CC BY-NC 4.0) is excluded from training (decided, N2); TACO images still need per-image license checks |
| R14 | Consent and privacy | Field photos only with informed consent; no faces or identifiable people kept; upload opt-in; pickers' organization co-owns field data (decided, D6) | Data protocol review with the partner | Not verifiable at TRL 3: protocol to be written with the partner; first candidate SWaCH, Pune (decided 2026-10-02), not yet approached; the protocol will include the site light record |

## Requirements not met or at risk

- **R2 is not met by a camera alone** for opaque HDPE versus PP and for black plastics. The design routes these to "Unsure" and to WasteWise Scan.
- **R11 is not met**: there is no field evaluation set, so R1 to R4 cannot be verified. Building it is TRL 4 work, on hold.
- **R10 is met only if the screen sleeps between scans** (or with the power bank); tap-to-scan alone is not enough.
- **R1, R3, R4 and R13 are at risk**: public data is small, clean and not organized by grade; hazards are rare; coverage is estimated at 68 %; one candidate dataset has a non-commercial license.

## Assumptions

- Seven material classes from the taxonomy (plastic, paper, metal, glass, organic, composite and hazardous), with 22 grades below them.
- A phone battery of 4,000 mAh at 3.85 V holds 15.4 Wh; screen, camera and processor draw about 2.5 W while scanning and the screen alone about 0.9 W (estimates, WML-CAL-001 section 5).
- Published MobileNetV3 speeds on a Pixel 1 large core are a fair lower bound; a low-cost 2019 or later phone is taken as 1 to 4 times slower (estimate).
- The stream composition, learning curve and error ranking in WML-CAL-001 sections 7 and 8 are assumptions to be replaced by field data.
