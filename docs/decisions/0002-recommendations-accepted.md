---
doc_id: WML-DDR-002
title: WasteWise-ml recommendations accepted
project: WasteWise-ml
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: MIT
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: O1 and O2 decided by Amish on 2026-10-02 as recommended
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted (items O3, N1, N2 and N3); items O1 and O2 decided on 2026-10-02 as recommended (Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions.")

## Context

After the TRL 3 session, WML-DDR-001 and `docs/REVIEW.md` still listed six items as "Proposed, awaiting Amish" (O1 to O3 and N1 to N3). On 2026-09-25 Amish wrote in chat: "i accept all your recommendations, go with them across all repos." Every open item that carries a recommendation is therefore decided as recommended. Items without a recommendation stay open. Items D1 to D8 were already decided in WML-DDR-001 and are unchanged. TRL 4 remains on hold by Amish's instruction, and this repository stays at `trl: 3`, `trl_target: 3`, licensed MIT only.

## Options considered

Table 1. Items open before this decision.

| # | Item | Options | Recommendation |
| --- | --- | --- | --- |
| N1 | Hazard evaluation size (R3) | 200; 400; about 1,000 hazard items | 400, collected by targeted sampling |
| N2 | ZeroWaste dataset (CC BY-NC 4.0) | Exclude from training, research comparison only; exclude entirely; ask the authors for other terms | Exclude from training |
| N3 | Camera height above the mat | 440 mm (frame 586 x 439 mm); 470 mm with a 500 mm wide mat | 440 mm |
| O3 | Drawing sheet license for software repositories | Kit option defaulting sheets to MIT; per-repository override | Kit option (suggested in the TRL 2 review) |
| O2 | CERN-OHL-S line in `CONTRIBUTING.md` | Remove; keep | None made |
| O1 | First partner organization, city and buyers | Not listed | None made |

## Decision

- **N1.** Decided by Amish, 2026-09-25: go with recommendation. The field evaluation set holds at least 400 hazard items. Changed: WML-REQ-001 R3 verification now reads "at least 400 hazard items" (was 200); WML-CAL-001 section 1 and 8 text and WML-PRC-001 evaluation text state the decision; BOM line 9 description updated. Numbers are unchanged: 400 items prove 98 % recall at 95 % confidence with up to 3 misses (200 items allow none); the 2,000-image set (400 hazards, 900 non-hazard minimum, 700 natural mix) and its 43.3 h and $260 stay as calculated. R3 stays at risk because hazards are rare in a natural stream.
- **N2.** Decided by Amish, 2026-09-25: go with recommendation. ZeroWaste is excluded from training and kept only for non-commercial research comparison. Changed: `ml/data/SOURCES.md`, WML-REQ-001 R13 status, WML-CAL-001 R13 row and WML-PRC-001 open questions. R13 stays at risk because TACO images still need per-image license checks.
- **N3.** Decided by Amish, 2026-09-25: go with recommendation. The phone lens sits 440 mm above the mat. The model, drawing WML-DWG-001 and WML-CAL-001 already used 440 mm, so no geometry changed; the drawing keeps Rev P1 and was only re-rendered. WML-CAL-001 section 6 and WML-DDR-001 now state the decision.
- **O3.** Decided by Amish, 2026-09-25: go with recommendation. A kit option so software repositories get an MIT label on drawing sheets by default. `.kit/` belongs to the portfolio kit, not this repository, so this is recorded as a cross-repo action in `docs/REVIEW.md`; this repository keeps its own MIT override in `cad/src/sheets.py` and `cad/src/concept_media.py` until the kit changes.

No budget or pitch change was recommended: `budget_usd` stays null (software repository) and the pitch and problem lines are unchanged.

Items that stayed open ("Proposed, awaiting Amish") until Amish decided them on 2026-10-02:

- **O1.** First partner organization, city and buyers for co-design and the field set. No recommendation. Decided by Amish on 2026-10-02 (WML-DEC-001): SWaCH in Pune, India, is the first candidate to approach.
- **O2.** The CERN-OHL-S line for hardware contributions in `CONTRIBUTING.md`, although the repository is MIT only. Decided by Amish on 2026-10-02 (WML-DEC-001): the line is removed and all contributions are licensed under MIT.

## Consequences

- WML-REQ-001 moves to v0.4, WML-CAL-001 to v0.2, WML-PRC-001 to v0.4 and WML-DDR-001 to v0.2. WML-PRB-001 is unchanged at v0.3.
- Requirement status is unchanged: 4 met (R5, R6, R9, R12), 1 met on a condition (R10), 2 not met (R2, R11), 4 at risk (R1, R3, R4, R13), 3 not verifiable at TRL 3 (R7, R8, R14).
- Nothing here starts TRL 4 work. Collecting the 400 hazard items, license checks image by image and any training belong to TRL 4, which is on hold.
