---
doc_id: WML-DDR-003
title: WasteWise-ml scanning rig design for construction
project: WasteWise-ml
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: MIT
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Changes that make the scanning rig physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction and open for his review
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: Accepted by Amish on 2026-10-02, including the recommendations for A1 to A3
---

# 0003: Scanning rig design for construction

- **Date:** 2026-09-30
- **Status:** accepted. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Tables 1 and 2 and the recommendations in Table 3 (A1 to A3), which are now decided as recommended and recorded in the design decisions register (WML-DEC-001).

## Context

On 2026-09-30 Amish asked for an illustrated prototype build plan for every repository and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." WasteWise-ml is mainly software. Its prototype hardware is the scanning rig: the phone, the stand that holds it over the sorting mat, the mat itself, and the power bank and cable. The bins, hazard box and scale of the sorting station are bought and are not changed here.

The TRL 3 model (`cad/src/model.py`) drew the stand as a massing shape: a 180 x 65 mm base behind the mat, a round post, a round arm and a box-shaped clamp over the phone. Checking it with build123d found six problems (P1 to P6 below). The changes keep what the rig does: the phone lies landscape, screen up, with its main camera 440 mm straight above the centre of a 700 x 450 mm light mat (decided, WML-DDR-002 N3), and nothing of the stand appears in the picture. Nothing here changes the pitch, the software, the requirements or the safety case.

Every change is in `cad/src/model.py`, which now also runs 99 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, no two parts overlap, the cable clears every part it passes, the clamps clear the bench frame, the lens is 440 mm above the mat and the board stays outside the camera's picture. All 99 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The stand would tip. The phone sat about 240 mm in front of the base's front edge, and the base was 65 mm deep, so a base of about 2 kg was needed just to balance the phone, arm and clamp, before anyone touched the phone. | The base is a plywood board 240 x 90 x 18 mm whose back edge is flush with the bench's back edge, held by two bought 100 mm G-clamps (BOM line 11). | A clamped board cannot tip, needs no weight and fits any bench with a square back edge. The board's front edge cannot move forward without entering the picture, so it was made deeper backward, not forward. |
| P2 | The clamp did not hold the phone. Its two jaws were cut away by the phone's own shape and were left as loose slivers, and its bar ran across the middle of the screen the user reads. | A phone tray folded from 2 mm aluminium sheet: the phone lies screen up on it with lips along both long edges, and its camera bump sits in a 34 x 34 mm window that locates it. The lens is flush with the tray's underside. | Nothing covers the screen, nothing grips the phone (no spring to wear, no pressure on buttons), and the phone lifts out in one move to charge or swap. The window doubles as the locator. |
| P3 | The round arm met the round post with no fixing, and the arm ran over the centre of the screen to the clamp. | Post and arm are both 25 x 25 x 2 mm square aluminium tube. The arm's square end butts the post's front face and two 3 mm aluminium corner plates, one each side, bolt through both tubes (four M5 bolts). The arm stops 3 mm short of the tray's lip and holds the tray by a tab under its end (two M5 bolts). | Every joint is face to face and bolted with hand tools. The square tube gives flat faces to bolt to; the plates make the corner rigid. The arm now ends beside the phone, not over it. |
| P4 | The post had no fixing to its base. | Two foot angles (50 x 50 x 3 mm aluminium angle, 60 mm long), one each side of the post, each bolted through the post and screwed to the board with two wood screws. | The bolts carry the post's bending into the angles; the screws, 40 mm apart front to back, carry it into the board. |
| P5 | The power bank's cable ran through the stand. | The cable runs from the power bank over the board, up the post's back face, along the top of the arm and down to the phone's charging end, held by four cable ties. The run is about 0.93 m, so the cable is now 1.5 m (BOM line 6). | Clear of every part (checked), out of the picture and out of the user's hands. |
| P6 | The stand base stood 15 mm behind the mat with nothing to place the mat, so the picture could drift off the mat. | The board's front edge meets the mat's back edge; a centre mark on each lines them up. The board's front edge is 5.3 mm outside the picture at mat level (12.3 mm at its top edge), the same margin the mat itself has, and the post 38 mm. | One push places the mat for every session, with no fixing. The board can show in the picture only if the mat's own edge would too. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Camera geometry | Unchanged: lens 440 mm above the mat, picture 586 x 439 mm. The stand's clearance from the picture is now 5.3 mm (it was 20 mm, with the base 15 mm behind the mat) [WML-CAL-001 section 6]. | The board now places the mat. |
| BOM | Line 2 is now a made stand ($22.00 of stock, was a $12.00 bought stand); line 3 spells out the mat as painted 4 mm hardboard; line 6 cable 1.5 m; new line 11, stand clamps and fixings ($14.00). One station is $309.00 (was $285.00); a two-station pilot is $1,348.00 (was $1,300.00). `budget_usd` stays null. | Parts added for construction. |
| Calculation script | `docs/04-calcs/sizing.py` now counts lines 1 to 7 and 11 as one station, and prints the stand's clearance and post and arm lengths. WML-CAL-001 v0.3. | Follows the BOM and the model. |
| Drawings | WML-DWG-001 Rev P2; making sketches WML-DWG-101 to 107 added. | Follows the model. |
| Concept media | Hero, blueprint, exploded view and 3D viewer regenerated from the model. | Follows the model. |
| Requirements | No change of status. R12 (reference phone) is unaffected; the stand works with a phone whose camera bump fits the window. | |

*Table 3. Items proposed, then accepted by Amish as recommended on 2026-10-02.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | Real phones do not have the lens on the centre line across their width, and the mat has only 5.3 mm to spare front and back, so the picture can run off the mat. | (a) cut the arm to suit the phone: lay the phone with its lens on the side away from the post and shorten the arm by the lens's offset, as the build plan says; (b) slot the tray tab so the tray slides along the arm; (c) a deeper mat, 480 mm. | (a) for the prototype: no new part. Choose the reference phone (D8) before the arm is cut. Accepted 2026-10-02: the arm is cut only after the reference phone is bought and its lens offset measured. |
| A2 | Light on the mat. The concept assumes daylight or a lit shed; the rig has no lamp. The 2026-09-26 review note calls the rendered rig a "lit mat". | (a) no lamp: rely on site light and record it with each photo; (b) a diffused 12 V LED strip on the arm's underside, powered from the bench; (c) a lamp chosen with the partner after the first site visit. | (a) for the prototype, because a lamp changes the photos the model is trained on and should be decided with field data. Accepted 2026-10-02: the site light is recorded with every photo (a light reading or a gray card in a corner of the frame); a lamp is decided only after the first site visit. |
| A3 | The rig needs a bench with a square back edge at least about 600 mm deep (mat plus board), which not every site has. | (a) as designed; (b) a separate base plate for floor or table use. | (a) for the prototype; handheld use remains for sites without a bench. Accepted 2026-10-02. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan WML-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status is unchanged (WML-CAL-001 v0.3).
- The photoreal renders `media/render-hero.png` and `media/render-station.png`, `media/card.png` and `media/social-preview.png` show the concept stand (round post and arm, clamp over the phone). They are stale and need regenerating on Amish's Mac, where Blender is.
- The phone tray's window and the arm's length depend on the reference phone, which is chosen at TRL 4.
- With A1 to A3 accepted (2026-10-02): the arm is cut to the measured lens offset of the bought reference phone; the prototype has no lamp and every photo carries a record of the site light; the rig is clamped to a bench, with handheld use where there is none.
