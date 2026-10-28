---
doc_id: WML-DDR-005
title: WasteWise-ml STEM check fixes and detailed-model findings
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
  change: Fixes F1 to F3 and F5 for the failed details of the first STEM check and its independent review, and F4 for a clash found by the detailed model, decided under Amish's standing instruction of 2026-10-23; model refinements M1 and M2 recorded; lens height D2 proposed to Amish
---

# 0005: STEM check fixes and detailed-model findings

- **Date:** 2026-10-25
- **Status:** accepted under Amish's standing instruction of 2026-10-23 ("whenever a STEM check fails propose and implement the best fix to the design and constructability"); Amish can reverse any of them.

## Context

The first STEM check (WML-STM-001, kit 1.8 upgrade) found two details that fail with a fix that keeps the working principle (C1, C3), one that fails for the shortest users (B2) and one at the edge of its screen (B1). Rebuilding the model to kit 1.9 detail (D3) found one clash the massing model had hidden (F4). The fix rule (STANDARDS section 20) asks for the best fix for the design and its constructability, implemented in the same session and recorded here and in the design decisions register (WML-DEC-001). None of the fixes changes the working principle, the pitch or what the user gets: one item, one photo, a class, grade and confidence on the phone.

## Options considered and decision

*Table 1. Fixes made.*

| # | Finding | Options weighed | Fix made | Cost |
| --- | --- | --- | --- | --- |
| F1 | B1, B2: the phone lies flat with its screen 1,215 mm above the floor. For the 5th percentile Indian woman (1,356 mm) it sits 106 mm above the shoulder: tapping it needs about 59 degrees of upper arm elevation at about one scan a minute (screen 60 degrees, ISO 11226), and her eye sees the screen 83 degrees off its normal, where a 10 mm icon subtends 11 arcmin (minimum 16, ISO 9241-303) | (a) a Bluetooth shutter button at the bench edge plus a full-screen result spoken by default; (b) lower the phone: not possible without overhanging the mat, since the 440 mm height was set by the picture (N3, decided by Amish); (c) tilt the phone or add a mirror: the camera must look straight down; (d) voice trigger: unreliable in a noisy depot and in several languages; (e) auto-capture with a live preview: 131 % of the battery and against tap-to-scan (D5, decided) | (a): a key-fob Bluetooth shutter button (BOM line 12, USD 3.39 cited) on a hook-and-loop pad at the bench edge, 45 mm in from the user's edge, takes the photo as a volume-key press; the result fills the screen in the class colour with the bin number at least 40 mm tall and an icon, and the phone says the bin number aloud by default (switchable off). The screen can still be tapped. New PR-015 and PR-016; PR-008 and PR-010 restated; battery 9 % a shift (was 8 %) | USD 3.39 a station; 0.11 Wh a shift |
| F2 | C3: the build plan primed, painted and varnished the mat's top face only. Hardboard takes up water through unsealed faces and edges (24 h thickness swelling up to 25 % at 3.2 mm, EN 317 rating) and cups when one face is coated | (a) seal both faces and all four edges; (b) a 3 mm polypropylene sheet: more costly, harder to paint matte, not tested in this design; (c) replace the mat when it swells | (a): prime, paint and varnish both faces and all four edges (BLD section 3.7, making sketch WML-DWG-107, BOM line 3). New PR-017 | None (paint and varnish of line 11) |
| F3 | C1: cells dropped into the bare steel hazard box could short across their terminals on the walls, on each other or on a can, heat and go into thermal runaway | (a) tape the terminals of every loose cell and lay it in the sand bed clear of the walls, with a tape roll kept in the box; (b) bag each cell in a plastic bag: bags burn and tear; (c) line the box with plastic: combustible and against the purpose of a steel box | (a): PVC insulating tape roll in the box (BOM line 5, USD 1.00 estimate), sand bed 50 mm deep, rule in the precis's safety section and the site briefing. New PR-018 | USD 1.00 a station (estimate) |
| F4 | Detailed model: the USB cable along the top of the arm passed through the heads and washers of the two tray tab bolts (the massing model never checked the cable against the fixings) | (a) run the cable along the arm top 8 mm to the side of the centre line, clear of the 10 mm washers, held by the two arm ties; (b) run it along the arm's side: the corner plates and their bolts are in the way; (c) countersunk bolts: the 2 mm tray tab is too thin to countersink | (a): cable 8 mm to the +X side along the arm top (`cable_arm_dx` in `cad/src/model.py`), checked clear of every bolt by `python cad/src/model.py --check` (115 of 115 pass); build plan step 8 updated | None |
| F5 | S7 (independent review): the camera bump had 2 mm of slack in its 34 mm window and the phone could turn 0.72 degrees between the lips, a possible picture shift of 5.7 mm against the 5.3 mm margin | (a) a 32 mm window and the phone pushed against the far lip; (b) a narrower tray gap: moves the arm by 0.5 mm and every drawing; (c) lower the lens for more margin: changes Amish's 440 mm decision, so proposed to him instead (D2) | (a): window 32 mm (`win` in `cad/src/model.py`), build plan step 7 and the tray making sketch; stack 3.3 mm with 0.3 degrees of tray tilt (WML-CAL-001 section 6) | None |

*Table 2. Model refinements (no design change).*

| # | Item | Was | Now | Why |
| --- | --- | --- | --- | --- |
| M1 | Bins (bought, about 60 L) | Straight-sided boxes with 12 mm walls, 62 L inside | Moulded tapered bins, 3 mm wall, 25 mm taper a side, rolled rim, 60 L inside | Real wall thickness at D3; the bought specification "about 60 L" is unchanged (WML-CAL-001 section 6) |
| M2 | Hazard box, scale, phone, power bank, G-clamps | Massing boxes | 1 mm steel box and lid with a strap handle, sand bed and sharps container; scale with pan, load cell, platform and column; phone with glass, bump and port; clamps with frame, screw, swivel pad and tommy bar; every M5 bolt, washer and nyloc nut, wood screw and cable tie | Kit 1.9 detail level D3; dimensions from the existing PARAMS |

## Consequences

- WML-STM-001 rows B1, C1 and S7 close as Within known science, each closed by its fix; B2 and C3 stay Plausible until a trial with a short user and a soak test (TRL 4), after the independent review.
- D2 (lens at 420 mm) is proposed, awaiting Amish (WML-DEC-001); it is not made.
- BOM: line 3 and line 5 specifications, line 5 USD 26.00 (was USD 25.00), new line 12 USD 3.39. One station USD 313.39 (was USD 309.00); a two-station pilot USD 1,356.78 (was USD 1,348.00). `budget_usd` stays null.
- Documents changed: WML-PRS-001 (PR-008, PR-010, PR-015 to PR-018), WML-CAL-001 v0.5, WML-PRC-001 v0.8, WML-BLD-001 v0.3, WML-DEC-001 v0.5, drawing WML-DWG-001 Rev P3, making sketch WML-DWG-107.
- The coin cell in the shutter button is a swallowing hazard for small children who may be at a sorting site: spare cells are kept out of reach (BOM line 12 notes, RSK).
