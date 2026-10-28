---
doc_id: WML-PRS-001
title: WasteWise-ml product requirements and specifications
project: WasteWise-ml
doc_type: Product requirements and specifications
version: "0.6"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: MIT
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold (as WML-REQ-001)
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
- version: "0.6"
  date: '2026-10-25'
  author: Amish Chadha
  change: "Kit 1.8 upgrade: WML-REQ-001 becomes WML-PRS-001; R1 to R14 migrated to PR-001 to PR-014 with tolerance, units and the user requirement each traces to; PR-015 to PR-023 added from the STEM check fixes (WML-DEC-001 F1 to F3, F5) and the calculation note; PR-008 and PR-010 restated for fix F1; PR-005, PR-016 and PR-019 statuses set after the independent review"
---

# WasteWise-ml product requirements and specifications

What the design must do, each traced to a user need in WML-URS-001. Targets are proposals for review with a co-design partner (first candidate SWaCH, Pune, decided 2026-10-02), not yet validated with users. No model has been trained, and at TRL 3 none will be: the status column gives the position on paper from the calculation note WML-CAL-001 and says plainly where a requirement is not met. The "Was" column gives the requirement number in WML-REQ-001, which this document replaces. Method: STANDARDS section 22.

The **reference use case** is one person at a sorting bench with a low-cost Android phone lying screen up in the tray of a clamped stand over one item at a time on a light mat (decided, D1), or holding the phone by hand on the floor, on a dry mixed stream, in daylight or a lit shed with no lamp on the rig (decided 2026-10-02; the site light is recorded with every photo), with no network. The app uses tap-to-scan (decided, D5); since 2026-10-25 the tap is a press of a Bluetooth shutter button at the bench edge, and the result fills the screen and is spoken by default (fix F1, decided under Amish's standing instruction of 2026-10-23).

Table 1. Product requirements and specifications.

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001, UR-013 | Performance | Material class accuracy | The model shall name the right one of the seven classes in `ml/data/taxonomy.yaml` on items it does not abstain on, on the field evaluation set (PR-011) | 90 | min | % top-1 | Test on the field evaluation set, TRL 4 (on hold) | At risk | R1 |
| PR-002 | UR-002 | Performance | Plastic grade accuracy from a photo | The model shall name the grade of answered plastic items, with ground truth from NIR (WasteWise Scan) or legible resin codes | 90 for PET bottles and trays; 80 for other rigid HDPE and PP | min | % | Test on the field evaluation set, TRL 4 | Not met | R2 |
| PR-003 | UR-003 | Safety | Hazard flag | The app shall flag batteries, sharps and chemical containers as hazards and shall never offer a hazard as a sortable grade | 98 recall, shown with at least 400 hazard items (up to 3 misses) | min | % | Test on the field evaluation set, TRL 4; design review of the app | At risk | R3 |
| PR-004 | UR-004 | Performance | Abstain when unsure | The model shall say "Unsure" below a set confidence and answer at least the target share of items while meeting PR-001 | 70 | min | % of items answered | Coverage and accuracy curve on the field set, TRL 4 (66 % on paper, WML-CAL-001 section 8) | At risk | R4 |
| PR-005 | UR-005, UR-008 | Performance | Offline, on-device speed | The result shall appear within the target of the photo on the reference phone (PR-012), with no network | 0.3 | max | s | Analysis (WML-CAL-001 section 3: 201 ms from a preview-size frame, up to 331 ms if a full 12 MP frame is decoded), TRL 3; timing on the reference phone, TRL 4 | At risk | R5 |
| PR-006 | UR-008 | Software | Small download | The model file and the app with the model shall stay within the targets | 10 (model); 30 (app) | max | MB | Analysis (WML-CAL-001 section 2), TRL 3; file sizes of the exports, TRL 4 | Met on paper | R6 |
| PR-007 | UR-005 | Usability | Quick to use | Placing an item to seeing the result, including the trigger and camera focus, shall take no longer than the target | 3 | max | s | Time budget (WML-CAL-001 section 4), TRL 3; timed trials with users, TRL 4 | To verify at TRL 4 | R7 |
| PR-008 | UR-006 | Usability | Usable without reading | The result shall fill the screen in the class colour with the bin number at least 40 mm tall and an icon, and the phone shall say the bin number in the local language by default (it can be switched off); users new to the app shall sort correctly after a briefing | 15 | max | min of briefing | Co-design sessions and usability trials, TRL 4 | To verify at TRL 4 | R8 |
| PR-009 | UR-010 | Software | Local grades | Buyer grade names and bin numbers shall be set per site in a configuration file, without retraining, for grades the model already separates | 1 | exact | file per site | Design review, TRL 3 | Met by design | R9 |
| PR-010 | UR-009 | Electrical | Battery life | A full 8 h shift of up to 500 scans, with voice on and the shutter button linked, shall use no more than the target share of a 4,000 mAh battery | 30 | max | % of battery | Energy estimate (WML-CAL-001 section 5), TRL 3; measurement, TRL 4 | Met on paper | R10 |
| PR-011 | UR-013 | Performance | Field evaluation set | A verified field evaluation set shall exist, from at least two sites, at least 50 images a grade, never used for training | 2,000 | min | images | Dataset manifest, TRL 4 | Not met | R11 |
| PR-012 | UR-008, UR-016 | Physical architecture | Reference phone | The app shall run on an Android phone with 3 GB RAM and a 2019 or later chipset costing no more than the target | 150 | max | USD | Analysis (BOM line 1), TRL 3; device test, TRL 4 | Met on paper | R12 |
| PR-013 | UR-012 | Software | Open and licensed | Code and weights shall be MIT; every dataset license in `ml/data/SOURCES.md` shall allow training and publishing weights; a model card shall give per-class results and known failure modes | 100 | min | % of sources cleared | License review, TRL 3 and 4 | At risk | R13 |
| PR-014 | UR-011 | Safety | Consent and privacy | Field photos shall be taken only with informed consent, keep no faces or identifiable people, be uploaded only on opt-in and be co-owned by the pickers' organization (decided, D6) | 1 | exact | protocol agreed with the partner | Data protocol review with the partner, TRL 4 | To verify at TRL 4 | R14 |
| PR-015 | UR-007 | Usability | Scan trigger at hand | The scan shall be triggered by a button at bench height within the target distance of the user's edge of the bench, so no one reaches up to the phone (fix F1) | 100 | max | mm from the bench edge | Inspection of the model (WML-CAL-001 section 12: 45 mm), TRL 3; first checks, TRL 4 | Met by design | |
| PR-016 | UR-006, UR-007 | Usability | Result legible from where users stand | The bin number shall subtend at least the target visual angle at the eye of every user from the 5th percentile Indian woman up, standing at the bench (fix F1) | 16 (20 preferred) | min | arcmin | Analysis (WML-CAL-001 section 12: 43 arcmin at the 5th percentile, but at 83 degrees off the screen normal), TRL 3; trial with a short user, TRL 4 | To verify at TRL 4 | |
| PR-017 | UR-015 | Materials | Mat sealed all over | The sorting mat shall be primed, painted and varnished on both faces and all four edges, so wet items cannot swell or cup it (fix F2) | 0 | max | unsealed faces or edges | Inspection (WML-BLD-001 section 3.7), TRL 3 and 4 | Met by design | |
| PR-018 | UR-003 | Safety | Loose cells cannot short | Loose cells shall go into the hazard box with their terminals taped, laid in the sand bed clear of the steel walls; the box shall carry a tape roll (fix F3) | 0 | max | bare terminals in the box | Inspection; site briefing, TRL 4 | Met by design | |
| PR-019 | UR-001 | Performance | Picture on the mat | The camera's picture, with the phone's placement in the tray allowed for, shall fall inside the 700 x 450 mm mat with the stand outside it | 450 | max | mm picture depth plus placement stack | Analysis (WML-CAL-001 section 6: 439 mm at 26 mm plus 3.3 mm a side of stack; fits lenses of 25.76 mm and longer), TRL 3; first check "Picture on the mat", TRL 4 | At risk | |
| PR-020 | UR-015 | Environment and durability | Phone temperature | In shade at a 40 C ambient the phone, used tap-to-scan, shall stay below the Li-ion charge limit; the rig shall stand in shade | 45 | max | C | Analysis (WML-CAL-001 section 13: 40.7 C), TRL 3; site temperature log, TRL 4 | Met on paper | |
| PR-021 | UR-014, UR-016 | Physical architecture | Built locally with hand tools | Every made part of the scanning rig shall be makeable from local stock with hand tools and a drill stand, and fit a bench with a square back edge | 0 | max | parts needing a machine shop | Inspection of the build plan (WML-BLD-001), TRL 3 | Met by design | |
| PR-022 | UR-017 | Usability | Phone lifts out | The phone shall lift out of the tray and go back in within the target, with nothing to undo | 5 | max | s | First check "Phone in and out" (WML-BLD-001), TRL 4 | To verify at TRL 4 | |
| PR-023 | UR-001 | Physical architecture | Stand rigid | A firm 5 N tap on the screen shall move the picture on the mat by less than the target | 1 | max | mm | Analysis (WML-CAL-001 section 11: 0.30 mm), TRL 3; first check "Stand rigid", TRL 4 | Met on paper | |

## Requirements not met or at risk

- **PR-002 is not met by a camera alone** for opaque HDPE versus PP and for black plastics (about 9 % of items on the assumed stream). The design routes these to "Unsure" and to WasteWise Scan. PET is at risk.
- **PR-011 is not met**: there is no field evaluation set, so PR-001 to PR-004 cannot be verified. Building it is TRL 4 work, on hold.
- **PR-001, PR-003, PR-004 and PR-013 are at risk**: public data is small, clean and not organized by grade; hazards are rare; coverage is estimated at 66 %, 4 points under PR-004; one candidate dataset has a non-commercial license, and the license of the ImageNet pretraining weights is still to review.
- **PR-005 is at risk**: 201 ms at the slow end if the app classifies a preview-size frame, up to 331 ms if it decodes a full 12 MP frame first.
- **PR-010 is met on paper only if the screen sleeps between scans** (9 % of the battery; 14 % with a 0.12 W standby). With the screen on all shift (52 %) it needs the power bank, and in shade above about 35 C the phone then pauses charging (PR-020).
- **PR-019 is at risk**: 5.3 mm of margin front and back, of which the phone's placement in the tray takes 3.3 mm after fix F5, so only lenses of 25.76 mm equivalent or longer fit. Lowering the lens to 420 mm is proposed to Amish (WML-DEC-001 D2); the bought phone's picture is measured before the arm is cut (confirm item 2).
- **PR-016 is to verify**: the 40 mm bin number subtends 43 arcmin for a 5th percentile user, but seen 83 degrees off the screen normal; a trial with a short user confirms it.

## Assumptions

- Seven material classes from the taxonomy (plastic, paper, metal, glass, organic, composite and hazardous), with 22 grades below them.
- A phone battery of 4,000 mAh at 3.85 V holds 15.4 Wh; screen, camera and processor draw about 2.5 W while scanning and the screen alone about 0.9 W; the voice prompt about 0.5 W for 1 s; the Bluetooth link about 5 mW (estimates, WML-CAL-001 section 5).
- Published MobileNetV3 speeds on a Pixel 1 large core are a fair lower bound; a low-cost 2019 or later phone is taken as 1 to 4 times slower (estimate).
- The stream composition, learning curve and error ranking in WML-CAL-001 sections 7 and 8 are assumptions to be replaced by field data.
- Body sizes for the ergonomic checks are Indian women's stature from Nag, Nag and Desai (2003) with standard body proportions; they are to be replaced by measurements with the partner.
