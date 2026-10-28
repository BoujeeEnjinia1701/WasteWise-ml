---
doc_id: WML-DDR-004
title: WasteWise-ml concept selection
project: WasteWise-ml
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: MIT
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: Concept selection between option A (phone stand over a mat) and option B (tray detector); option A recommended; proposed, awaiting Amish
---

# 0004: Concept selection

- **Date:** 2026-10-25
- **Status:** proposed, awaiting Amish. Recommendation: option A, the current design.

## Context

Kit 1.8 asks every repository for at least two concept options with different working principles, scored against the user requirements, with the choice left to Amish (STANDARDS section 21). WasteWise-ml was designed before kit 1.8, so its current design is option A and is not redesigned without Amish's go. Kit 1.9 asks every option to be modelled to the repository's detail level (D3 at stage P3; Amish, 2026-10-24: "Detail every option"). Both options are in `cad/src/model.py` and pass `.kit/cad_check.py` at D3 (`cad/fidelity.json`: option A 101 parts, 38.5 kg; option B 116 parts, 39.2 kg, each with the station's bins, hazard box and scale).

## Options considered

1. **Option A, phone stand over a mat (current design).** One item at a time on a light mat under the user's own phone, held screen up 440 mm above it; a shutter button at the bench edge takes one photo; an on-device classifier answers with class, grade and confidence, or "Unsure" or "Hazard". About USD 313 a station including a USD 130 reference phone.
2. **Option B, tray detector.** Ten to twenty items spread in a tray under a Raspberry Pi wide camera on a mast; an on-device object detector boxes and labels every item at once on a touch display at eye level; an arcade button at the bench edge takes the photo. About USD 419 a station without a phone.

A third principle, reading the resin by near-infrared spectroscopy, is WasteWise Scan, a separate repository, and is out of scope here (WML-PRB-001). Handheld use of option A's phone without the stand is already supported and is not a separate working principle.

## Decision

Proposed, awaiting Amish: **option A**. In the weighted scoring of WML-OPT-001 Table 2 it scores 205 of 255 against 152 for option B, 26 % ahead, outside the 10 % band in which both options would go to Amish without a pick. Option A runs on the user's own phone (UR-008), sees each item alone and close, which matters most for hazards (UR-003) and grades (UR-002), keeps faces out of a narrow frame (UR-011), stays MIT-compatible (UR-012) and costs less (UR-016). Option B wins on throughput (UR-005) and on a display that faces the user (UR-006).

Grafted from option B: the bench-edge trigger, already in option A as the shutter button of fix F1 (WML-DEC-001). Proposed for later, not part of this decision: a multi-item mode on option A's phone stand, once field data exist and with a detector whose license fits MIT.

## Consequences

- If Amish chooses option A, nothing in the repository changes: the drawing, BOM, build plan and calculations already describe it. `concept_chosen` in `project.yaml` becomes `A`.
- If Amish chooses option B, the drawing set, priced BOM, build plan and requirements status are redone for the tray detector, the phone is no longer the computer (a change to the pitch, which names "a phone or low-cost camera"), and PR-008, PR-012 and PR-014 need new targets.
- Until Amish decides, `concept_chosen` reads "A (proposed)" and option A stays `CHOSEN` in the model, as the current design.
