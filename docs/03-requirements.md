---
doc_id: WML-REQ-001
title: WasteWise-ml requirements
project: WasteWise-ml
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
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
---

# WasteWise-ml requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with users, and will be revised after co-design sessions (see WML-PRB-001). No model has been trained, so every performance requirement is unverified; the status column gives the concept's expected position and says plainly where it is not met.

The **reference use case** is one person at a sorting bench or on the floor, holding a low-cost Android phone (or using it on a stand) over one item at a time, on a dry mixed stream, in daylight or a lit shed, with no network.

**Table 1.** Requirements, targets and status at TRL 2.

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 2 |
| --- | --- | --- | --- | --- |
| R1 | Material class accuracy | Top-1 accuracy of 90 % or more on the seven classes in `ml/data/taxonomy.yaml`, on items the model does not abstain on, on the field evaluation set (R11) | Evaluation on the held-out field set | Unverified; at risk. TrashNet's authors reported about 75 % on a clean six-class set |
| R2 | Plastic grade accuracy from a photo | 90 % or more for PET bottles and trays, 80 % or more for other rigid HDPE and PP, on non-abstained items | Field set, ground truth from NIR (WasteWise Scan) or legible resin codes | **Not met by design** for opaque HDPE versus PP and for black plastics; these go to "Unsure" and to WasteWise Scan |
| R3 | Hazard flag | Recall of 98 % or more for batteries, sharps and chemical containers; a hazard result is never offered as a sortable grade | Field set with at least 200 hazard items | Unverified; at risk because hazards are rare in training data |
| R4 | Abstain when unsure | Model says "Unsure" below a set confidence; coverage (share of items answered) 70 % or more while meeting R1 | Coverage and accuracy curve on the field set | Unverified; about 75 % coverage assumed (estimate) |
| R5 | Offline, on-device speed | Result within 0.3 s of the photo on the reference phone (R12), with no network | Timing on the reference phone | Met on paper: about 0.05 to 0.2 s for MobileNetV3-Large in 8-bit form (estimate) |
| R6 | Small download | Model file 10 MB or less; app with model 30 MB or less | File sizes of the exported models | Met on paper: about 5 to 6 MB (estimate) |
| R7 | Quick to use | 3 s or less from placing an item to seeing the result, including tap and camera focus | Timed trials with users | Unverified |
| R8 | Usable without reading | Result shown as icon, color and bin number, with optional voice in the local language; users new to the app sort correctly after a 15 min briefing | Co-design sessions and usability trials | Unverified; depends on co-design |
| R9 | Local grades | Buyer grade names and bin numbers set per site in a configuration file, without retraining, for grades the model already separates | Configuration review | Met on paper by the grade mapping layer; new visual grades still need retraining |
| R10 | Battery life | A full 8 h shift with up to 500 scans uses 30 % or less of a 4,000 mAh phone battery | Energy estimate; later measurement | Met on paper with tap-to-scan (about 7 % estimate); **not met** with a live camera preview all shift |
| R11 | Field evaluation set | 2,000 or more verified images from at least two sites, 50 or more per grade, never used for training | Dataset manifest | **Not met**: the set does not exist yet |
| R12 | Reference phone | Runs on an Android phone costing about $150 or less, 3 GB RAM, 2019 or later chipset | Device test | Unverified; assumed from published latency |
| R13 | Open and licensed | Code and weights MIT; every dataset license in `ml/data/SOURCES.md` allows training and publishing weights; a model card with per-class results and known failure modes | License review | Partly met: candidate sources listed, licenses still to confirm |
| R14 | Consent and privacy | Field photos only with informed consent; no faces or identifiable people kept; upload opt-in; pickers' organization co-owns field data (proposed) | Data protocol review with the partner | Unverified; protocol to be written with the partner |

## Requirements not met or at risk

- **R2 is not met by a camera alone** for opaque HDPE versus PP and for black plastics. The concept routes these to "Unsure" and to WasteWise Scan.
- **R11 is not met**: there is no field evaluation set yet, so R1 to R4 cannot be verified.
- **R10 is not met** if the app runs a live preview all shift; the concept therefore uses tap-to-scan.
- **R1, R3 and R4 are at risk** because public data is small, clean and not organized by grade.

## Assumptions

- Seven material classes from the taxonomy (plastic, paper, metal, glass, organic, composite and hazardous), with about 22 grades below them.
- A phone battery of 4,000 mAh at 3.85 V holds about 15 Wh; screen and camera draw about 2.5 W while scanning (estimate).
- Published MobileNetV3 speeds on a Pixel 1 large core are a fair lower bound; a low-cost 2019 or later phone is taken as 1 to 4 times slower (estimate).
- About 75 % of items are answered confidently, 22 % are "Unsure" and 3 % are hazard flags in a dry mixed stream (estimates for the flow diagram, to be replaced by field data).
