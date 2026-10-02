# Review note: WasteWise-ml

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (WML-PRB-001 v0.2): problem, scale, three gaps (knowledge, tools, data), users, operating environment, constraints, out of scope, prior work and open questions; co-design checklist kept.
- `docs/03-requirements.md` (WML-REQ-001 v0.2): 14 measurable requirements (R1 to R14) for a reference use case, each with a status at TRL 2.
- `docs/02-concept.md` (WML-PRC-001 v0.2): flow diagram near the top, how it works, numbered components, model size and speed, battery, data needed, share of items answered, pilot cost, design choices, safety, open questions and references.
- `cad/src/concept_media.py`: massing scene of a sorting station (bench, phone on a clamp stand over a light mat, bottle, can, carton and film, seven color-labeled bins, hazard box, power bank, platform scale, input sack) with a 1.75 m person standing at the bench. It also draws a custom two-lane data and material flow diagram, because the kit's linear flow diagram cannot show the linked WasteWise Scan, ReflowEconomy and data-loop branches.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `model.glb` with `viewer.html`, `exploded.png` (callouts 1 to 7 match `bom/bom.csv`) and `flow.png`. No cutaway; nothing inside the items carries the idea.
- `bom/bom.csv`: 10 lines. Lines 1 to 7 are one pilot station; lines 8 to 10 are dataset effort, evaluation set effort and training compute (no geometry). `bom/bom-notes.md` updated.
- `README.md`: hero image and links line inserted before "## Problem"; concept, key components, safety and layout updated to match the precis. Pitch and problem text unchanged.
- `ml/data/taxonomy.yaml`, `ml/data/SOURCES.md` and `ml/models/README.md`: kept and extended. All original classes and grades are kept; a `composite` class (beverage carton, multilayer pouch) and the `unsure` and `hazard` outputs were added and marked as proposed. SOURCES lists candidate datasets with license status "to confirm". The models README records the proposed export and model card. No code, training scripts or notebooks were added.
- `docs/pdf/`: branded PDFs of the three controlled documents.

The bill of materials is **indicative and outside any hardware budget**. `budget_usd` stays null because this is a software repository; the pilot costs are for planning only.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Model size, MobileNetV3-Large, 8-bit | about 5 to 6 MB | R6 met on paper (10 MB or less) |
| Time to result on a low-cost phone | about 0.05 to 0.2 s | R5 met on paper (0.3 s or less) |
| Battery, 500 tap-to-scan scans in 8 h | about 1.0 Wh, about 7 % of a 4,000 mAh battery | R10 met on paper |
| Battery, live preview all shift | about 20 Wh, more than the battery | R10 **not met**; tap-to-scan chosen |
| Items answered / unsure / hazard | about 75 % / 22 % / 3 % (placeholders) | R4 target 70 % coverage |
| Field dataset | about 10,000 photos, about 72 h of labeling | |
| Field evaluation set | about 2,000 photos, about 43 h | R11 **not met** (does not exist) |
| One pilot station (BOM 1 to 7) | about $285, indicative | |
| Dataset, evaluation set and compute (BOM 8 to 10) | about $730, indicative | |
| Two-station pilot | about $1,300, indicative | |

Requirements not met or at risk:

- **R2 not met by design:** a photo cannot reliably separate opaque HDPE from PP or identify black plastics. These route to "Unsure" and WasteWise Scan.
- **R11 not met:** there is no field evaluation set, so R1 to R4 cannot be verified.
- **R10 not met** if the app runs a live camera preview all shift.
- **R1, R3 and R4 at risk:** public data is small, mostly clean-background and not organized by grade. TrashNet's authors reported about 75 % test accuracy on a clean six-class set; hazards are rare in all public sets.
- **R13 partly met:** candidate sources are listed, but no dataset license has been confirmed for training and publishing weights.

### Proposed, awaiting Amish

1. **Task form.** Option A: single item on a mat, image classification (simpler labels, fits bench sorting). Option B: multi-item detection in a pile (TACO-style; fits floor sorting, much more labeling). Recommendation: A for TRL 3, B as a later extension.
2. **Backbone and runtime.** MobileNetV3-Large (recommended), EfficientNet-Lite0 or a small vision transformer; TensorFlow Lite as the main export with ONNX as a second export (matches the existing README).
3. **Taxonomy changes.** Add the `composite` class and the `unsure` and `hazard` outputs (already written into `taxonomy.yaml`, marked proposed). Recommendation: keep them.
4. **Grade mapping per site** in a configuration file rather than site-specific models. Recommendation: yes.
5. **Tap-to-scan rather than live preview**, for battery life. Recommendation: yes.
6. **Data ownership and consent.** Field data co-owned by the pickers' organization, opt-in upload, no faces. Recommendation: yes, written into a protocol with the partner before any collection.
7. **Pay rate for labeling** by partner members (about $6 per hour assumed). Recommendation: set with the partner at or above the local living wage.
8. **Pilot kit.** Supply a reference phone per station or use pickers' own phones. Recommendation: supply one reference phone per station for the evaluation, and support own phones in use.
9. **First partner, city and buyers** for co-design and the field set. (Still proposed, awaiting Amish: no recommendation.)
10. **Pitch.** Unchanged. The concept adds the "Unsure" route and the per-site grade mapping, which fit the current pitch.

### Safety concerns

- Sharps, broken glass, lithium cells, chemical containers and biological contamination at the sorting station. The app must never prompt users to handle items more to get a better photo.
- Hazard misclassification is the worst failure: the hazard class is tuned for recall, cannot be overridden into a grade, and hazards go to a lidded steel box with sand, away from paper and film.
- Lithium cells in the phone and power bank: shade, no hot metal, no charging of swollen packs.
- Privacy of field photos (faces, people, locations).
- Over-trust: grades are advice; the buyer's check remains final; the model card must publish per-class errors.

### Problems and notes

- **Sources.** The session's web search budget was used up before this repo, and most sites other than GitHub were blocked by the proxy. The TrashNet, TACO and MobileNetV3 figures were checked this session on GitHub (TrashNet and TACO READMEs and license files; TensorFlow Models MobileNet README). The World Bank *What a Waste 2.0* figures, the 58 % informal-sector share (Lau et al. 2020), WIEGO and the ZeroWaste, EfficientNet and MobileNetV3 paper citations come from prior knowledge and were **not re-checked**; verify them and add links at TRL 3.
- **Blueprint license.** The kit's drawing sheet defaults to "CERN-OHL-S-2.0". `concept_media.py` overrides it to MIT for this repo's sheet only; `.kit/` is unchanged. Consider a kit option for software repos.
- **CONTRIBUTING.md** still says hardware contributions are under CERN-OHL-S v2. Licenses were left as they are per instructions; Amish may want to remove that line since this repo is MIT only.
- The phone is small at scene scale, so it reads only as a dark shape in the hero and exploded views; the blueprint isometric shows it more clearly.
- The flow percentages (75 / 22 / 3 %) are placeholders, not measurements.

### Recommended next step

Review this note and the media, then decide items 1 to 3 and 9. If approved, run `/advance-trl3`: write a calculation note on latency, battery, dataset size and threshold selection; confirm dataset licenses; and draft the data consent protocol with the partner. Training and field trials belong to TRL 4 and stay out of scope until the phase cap changes.

## Session 2026-09-25: TRL 3

Authority: on 2026-09-25 Amish wrote "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." This session advanced WasteWise-ml from TRL 2 to TRL 3 and stopped there. It wrote no training code, no notebooks and no app code.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (WML-DDR-001 v0.1): decisions D1 to D8, open items O1 to O3 and new proposals N1 to N3.
- `docs/04-calcs/01-sizing.md` (WML-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: model size, latency, time to result, energy per scan and battery, camera geometry (read from the model), dataset size with a sensitivity table, coverage and hazard false alarms, evaluation plan with hazard recall bounds, and cost (read from the BOM). The script is arithmetic only; it trains and loads nothing.
- `cad/src/model.py`: parametric build123d model of the sorting station (bench, mat, phone, stand, power bank, hazard box, seven bins, platform scale). Exports `cad/step/wastewise-{station-assembly,phone-stand,sorting-mat,hazard-box,bin}.step` and matching `cad/stl/*.stl`.
- `cad/src/sheets.py` and `cad/drawings/WML-DWG-001.{svg,pdf,png}`: station general arrangement at Rev P1, 1:50, license label MIT, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept sheet keeps its number WML-DWG-010, so DWG-001 was the next free number.
- `cad/src/concept_media.py` now takes the station geometry from `model.py`; all media regenerated and inspected (hero, blueprint WML-DWG-010, exploded view with items 1 to 7, flow with the calculated split, `model.glb` and `viewer.html`). No `_views` folders are left.
- `bom/bom.csv` (10 lines, every line priced, supplier or supplier type on each) and `bom/bom-notes.md`: notes updated for the decisions; totals unchanged.
- WML-PRB-001, WML-PRC-001 and WML-REQ-001 moved to v0.3. `ml/data/SOURCES.md`, `ml/data/taxonomy.yaml` (comment only) and `ml/models/README.md` updated for the checked licenses, the decisions and the 4.4 MB size; all existing `ml/` content kept.
- `project.yaml`: `trl: 3`, `trl_target: 3`, evidence listed; `budget_usd` stays null and the license stays MIT only. `README.md`: TRL 3 badge and status line; pitch and problem unchanged.

### Requirement status (WML-CAL-001)

Counts: 4 met, 1 met on a condition, 2 not met, 4 at risk, 3 not verifiable at TRL 3.

| ID | Status | Value |
| --- | --- | --- |
| R2 | Not met by design | Opaque HDPE versus PP and black plastics (about 9 % of items) cannot be graded from a photo; they go to "Unsure" and WasteWise Scan. PET at risk |
| R11 | Not met | Field evaluation set does not exist; sized at 2,000 (400 hazards, 900 non-hazard minimum, 700 natural mix), about 43 h |
| R1 | At risk | Expected class error 9.1 % on an assumed learning curve |
| R3 | At risk | Hazards rare (300 of 10,000 natural photos against 2,400 needed); a 200-item test proves 98 % only with zero misses |
| R4 | At risk | About 68 % answered against 70 % (65 % graded, 32 % "Unsure", 3 % hazard) |
| R13 | At risk | ZeroWaste is CC BY-NC 4.0; TACO images need per-image checks |
| R10 | Met, conditional | 8 % if the screen sleeps between scans; 51 % with the screen on all shift; 130 % with live preview |
| R5, R6, R9, R12 | Met | 64 to 201 ms; 4.4 MB int8; per-site file; $130 phone |
| R7, R8, R14 | Not verifiable at TRL 3 | Time budget 0.9 to 2.0 s; co-design; consent protocol not written |

Key numbers: 4.16 million parameters; 0.09 to 0.35 J per inference and 7.5 J per scan; about 230 images per label for 90 % at 70 % coverage (128 to 591 across the sensitivity cases), design figure 300 per grade and 10,000 field photos, 72.2 h of labeling; camera frame 586 x 439 mm at 440 mm lens height; one station $285, two-station pilot $1,300.

Corrections to TRL 2 numbers: model 4.4 MB, not 5 to 6 MB (the ImageNet classifier is replaced); latency 64 to 201 ms including preprocessing; tap-to-scan 8 %, not 7 %, of the battery; flow split 65 / 32 / 3 %, not 75 / 22 / 3 %; camera height 440 mm, not 470 mm, so the frame fits the mat; bins modeled at 62 L inside.

Findings: tap-to-scan alone does not meet R10; the screen must also sleep between scans (or the power bank must be used). R3's verification size of 200 hazard items is too small unless the model misses none.

### Decisions recorded (WML-DDR-001)

Decided by Amish, 2026-09-25, going with the recommendation: D1 single item on a mat; D2 MobileNetV3-Large, TensorFlow Lite plus ONNX; D3 keep the `composite` class and the `unsure` and `hazard` outputs; D4 per-site grade file; D5 tap-to-scan; D6 consent, opt-in, no faces, co-ownership, protocol before collection; D7 pay rate set with the partner at or above the local living wage; D8 one reference phone per station for the evaluation. No pitch or budget change was recommended: pitch unchanged, `budget_usd` null, MIT only.

### Still awaiting Amish

1. O1: first partner organization, city and buyers. No recommendation.
2. O2: the CERN-OHL-S line in `CONTRIBUTING.md` in an MIT-only repository. No recommendation was made; left unchanged.
3. O3: a kit option so software repositories get an MIT sheet label by default. `.kit/` unchanged; this repository overrides the label in its own scripts. (Decided by Amish, 2026-09-25: go with recommendation; see WML-DDR-002.)
4. New, N1: hazard evaluation size 400 items (recommended), 200 or about 1,000. (Decided by Amish, 2026-09-25: go with recommendation.)
5. New, N2: exclude ZeroWaste (CC BY-NC 4.0) from training (recommended). (Decided by Amish, 2026-09-25: go with recommendation.)
6. New, N3: camera height 440 mm (recommended, used in the model) or 470 mm with a wider mat. (Decided by Amish, 2026-09-25: go with recommendation.)

### Safety concerns

- A missed hazard is the worst failure. The design sends about 4.9 % of items to the hazard box, 40 % of them false alarms, by choice. Hazard results can never be overridden into a grade.
- The dataset needs about 2,400 hazard photos, far more than a natural stream gives. Collecting them on purpose must not add handling: photograph where items lie, sharps only in a rigid container or with tongs, by trained people; pickers are never asked to collect hazards.
- Lithium cells in the phone and power bank; privacy of field photos; over-trust in grades. These are unchanged from TRL 2 and remain in WML-PRC-001.

### Citations

The TRL 2 note listed unchecked citations. This session checked on the web: World Bank *What a Waste 2.0* (2.01 billion tonnes in 2016, 242 million tonnes or 12 % plastic, 3.40 billion tonnes by 2050); Lau et al. 2020 (*Science* 369 (6510): 1455 to 1461; the 58 % informal-sector share, in the accepted manuscript); WIEGO (15 to 20 million waste pickers); ZeroWaste (CVPR 2022, dataset CC BY-NC 4.0); MobileNetV3 (ICCV 2019, arXiv:1905.02244); EfficientNet (ICML 2019, PMLR 97: 6105 to 6114); TrashNet and TACO licenses. All are cited with links in WML-PRC-001 or WML-CAL-001. Values marked "assumed" in WML-CAL-001 have no source.

### TRL 4 material

None found. `build-log/` holds only its README; `ml/notebooks/` holds only `.gitkeep`.

### Recommended next step

TRL 4 is on hold by Amish's instruction; do not start it. Paper work that remains within TRL 3: decide O1 to O3 and N1 to N3, and with the partner (once chosen) draft the consent and data protocol and collect the first buyer price list and stream composition, which would replace the assumed stream in WML-CAL-001.

For reference only, TRL 4 would need: the consent protocol signed with a partner, the field dataset and field evaluation set collected, a trained and exported model, a measured learning curve, coverage and hazard recall on the evaluation set, timing and battery measured on the reference phone, a lab test report (TST with `environment: lab`) and build log entries.

## Session 2026-09-25: recommendations accepted

Authority: on 2026-09-25 Amish wrote in chat: "i accept all your recommendations, go with them across all repos." Every open item with a recommendation is now "Decided by Amish, 2026-09-25: go with recommendation", recorded in `docs/decisions/0002-recommendations-accepted.md` (WML-DDR-002 v0.1). Items without a recommendation stay open.

### Decisions applied and what changed

| Item | Decision | Before | After |
| --- | --- | --- | --- |
| N1 | Hazard evaluation size | R3 verification: at least 200 hazard items (400 proposed) | At least 400 hazard items; proves 98 % recall with up to 3 misses (200 allowed none). Field set stays 2,000 images, 43.3 h, $260 |
| N2 | ZeroWaste (CC BY-NC 4.0) | Proposed exclusion | Excluded from training; research comparison only (`ml/data/SOURCES.md`, R13) |
| N3 | Camera height | 440 mm used, pending decision | 440 mm decided; frame 586 x 439 mm on the 700 x 450 mm mat. No geometry change, so WML-DWG-001 stays Rev P1 (re-rendered only) |
| O3 | Kit option for MIT drawing labels | Proposed | Decided; cross-repo action for the kit owner. This repository keeps its own MIT override |

Documents changed: WML-REQ-001 0.3 to 0.4 (R3 and R13 text), WML-CAL-001 0.1 to 0.2 (R3 and R13 rows, sections 6 and 8 text; `sizing.py` re-run, numbers unchanged), WML-PRC-001 0.3 to 0.4 (evaluation and open questions), WML-DDR-001 0.1 to 0.2 (status wording), new WML-DDR-002 0.1. Also `ml/data/SOURCES.md` and BOM line 9 description (prices unchanged: one station $285, two-station pilot $1,300). `budget_usd` stays null and the pitch and problem are unchanged, as no change was recommended.

README: added "Concept rationale", "Burning platform" (World Bank *What a Waste 3.0*, Lau et al. 2020, WIEGO, US EPA), "Where it could be used" and "What sparked the idea" (TrashNet, the 2016 Stanford CS 229 dataset of items photographed with phones on a white posterboard). All generated drawings, media and PDFs were re-rendered so the lab site reads designmolecule.com.

### Requirement status (unchanged in count)

- Not met: R2 (opaque HDPE versus PP and black plastics cannot be graded from a photo; by design they go to "Unsure"), R11 (field evaluation set does not exist).
- At risk: R1 (class error 9.1 % on an assumed curve), R3 (hazards rare; verification now sized at 400), R4 (68 % answered against 70 %), R13 (TACO per-image checks remain; ZeroWaste excluded).
- Met on a condition: R10 (8 % of the battery if the screen sleeps between scans).
- Met: R5, R6, R9, R12.
- Not verifiable at TRL 3: R7, R8, R14.

### Still awaiting Amish

1. O1: first partner organization, city and buyers. No recommendation.
2. O2: the CERN-OHL-S line in `CONTRIBUTING.md` in an MIT-only repository. No recommendation; unchanged.

### Cross-repo actions

- O3: add a kit option in `.kit/` so software repositories (license MIT only) get an MIT label on drawing and blueprint sheets by default. For the kit owner; `.kit/` was not edited here.

### TRL 4

TRL 4 remains on hold by Amish's instruction. No training, data collection, app code, purchasing or field work was started. `trl: 3`, `trl_target: 3`.

## Session 2026-09-26: photoreal renders

Amish asked on 2026-09-26 for photoreal renders across the portfolio, starting with the software and playbook repos (Group C). This repo has no new product model: the existing concept scene from `cad/src/concept_media.py` was rendered with Blender Cycles (`.kit/scene_export.py`, `.kit/photoreal.py`) on Amish's Mac and captioned with the project, repository and viewing direction.

- New: `media/render-hero.png`, `media/render-station.png`. The README now leads with `media/render-hero.png`.
- Geometry, BOM, calculations and drawings are unchanged. `trl` stays 3; TRL 4 remains on hold.
- `cad/src/render_detail.py` (new): cosmetic detail for renders only (lit phone screen, mat grid print, bin rims and label text, hazard sticker and handle, scale display). The hero is a close-up of the scanning rig (phone, clamp stand and lit mat), which is the hardware this model runs on; the station view shows the whole sorting station.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-09-30: kit 1.7.0, constructable scanning rig and build plan

Authority: Amish's 2026-09-30 instructions to write an illustrated prototype build plan in the approved format for every repository, to "fix the design assumptions to match and be physically feasible" where the concept cannot be built, and to keep outstanding decisions out of the build plan in a separate design decisions register. WasteWise-ml is mainly software; its prototype hardware is the scanning rig (phone, stand and mat), so the build plan covers that rig. The bins, hazard box and scale stay bought and unchanged.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`, including `/build-plan`); `CLAUDE.md` replaced with `.kit/CLAUDE.md`.
- `cad/src/model.py`: the stand rebuilt as made parts (`build_components()`), with 99 constructability checks (`python cad/src/model.py --check`, all pass). STEP and STL regenerated, including single parts of the stand.
- `docs/decisions/0003-design-for-construction.md` (WML-DDR-003 v0.1, Draft): every change, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `docs/05-build-plan.md` (WML-BLD-001 v0.1) and `docs/06-design-decisions.md` (WML-DEC-001 v0.1).
- `cad/src/build_plan_media.py`: overview, 7 making sketches (`cad/drawings/WML-DWG-101` to `107`), 2 layout pictures (tray blank, camera picture on the mat), 6 joint close-ups and 8 assembly step pictures in `docs/05-build-plan/`.
- `cad/drawings/WML-DWG-001` Rev P2; concept media regenerated (`hero.png`, `concept-blueprint`, `exploded.png`, `flow.png`, `model.glb`).
- `bom/bom.csv`: line 2 now a made stand, line 3 and line 6 specs, new line 11 (G-clamps and fixings); `bom/bom-notes.md`; `docs/04-calcs/sizing.py` counts lines 1 to 7 and 11 as the station. WML-CAL-001 v0.3, WML-PRC-001 v0.5.
- `project.yaml`: `design_state: constructable`, the three new documents in `trl_evidence`. `README.md`: links line and a "Building the prototype" section.

### Design changes made for construction (WML-DDR-003)

| # | Concept | Constructable design |
| --- | --- | --- |
| P1 | Free-standing 180 x 65 mm base; would tip under the phone | Plywood board 240 x 90 x 18 mm clamped to the bench's back edge with two G-clamps |
| P2 | Clamp whose jaws were cut away by the phone, bar across the screen | Folded 2 mm aluminium tray; the camera bump sits in a 34 x 34 mm window; screen clear |
| P3 | Round arm meeting a round post with no fixing; arm over the screen | 25 x 25 x 2 mm square tube post (453 mm) and arm (213.5 mm), two bolted 3 mm corner plates; arm ends beside the phone and holds the tray by a tab |
| P4 | Post not fixed to its base | Two 50 x 50 x 3 mm foot angles, bolted through the post and screwed to the board |
| P5 | Power bank cable ran through the stand | Cable up the post's back and along the arm top; 1.5 m cable (run about 0.93 m) |
| P6 | Base 15 mm behind the mat, nothing placed the mat | The mat's back edge meets the board's front edge, centre mark to centre mark; board 5.3 mm outside the picture (was 20 mm), the mat's own margin |

Knock-on: one station $309.00 (was $285.00), two-station pilot $1,348.00 (was $1,300.00); `budget_usd` stays null. No requirement changed status; no change to the pitch, software or safety case.

### Proposed, awaiting Amish (in WML-DEC-001)

1. Accept the design for construction (WML-DDR-003). Recommendation: accept.
2. A1, lens offset on real phones (mat has 5.3 mm to spare front and back). Recommendation: cut the arm shorter by the offset.
3. A2, lighting over the mat. Recommendation: no lamp for the prototype; decide with field data.
4. A3, sites without a suitable bench. Recommendation: as designed, handheld elsewhere.
5. O1 (partner, city, buyers) and O2 (CERN-OHL-S line in `CONTRIBUTING.md`) remain open, no recommendation.

### Safety

The rig adds sharp cut aluminium edges (deburr, gloves) and keeps the phone and power bank's lithium cells on the bench (shade, away from hot metal and the hazard box). The build plan's safety stops S1 to S5 cover these, and repeat that hazards are never held under the phone.

### Stale media (made on Amish's Mac, not regenerated here)

`media/render-hero.png`, `media/render-station.png`, `media/card.png` and `media/social-preview.png` show the concept stand (round post and arm, clamp over the phone) and are stale. `cad/src/render_detail.py` still adds the lit screen and mat grid and needs no change; regenerate the renders on the Mac with `/render-product`.

### Recommended next step

Amish reviews WML-DDR-003 and the register. TRL 4 (building the rig to this plan and running the first checks) stays on hold.

## Session 2026-10-02: open decisions decided

Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This approves the recommendation written for each open decision in the design decisions register (WML-DEC-001 v0.2). trl stays 3; no build or test work was done, and the model, BOM quantities and prices, and pictures are unchanged.

### Decisions recorded

Six decisions, all moved to Decisions made in WML-DEC-001, dated 2026-10-02:

1. WML-DDR-003 accepted: the design for construction of the scanning rig, P1 to P6, as made.
2. Lens off the centre line: option (a), cut the arm shorter by the measured lens offset, only after the reference phone is bought and measured.
3. Lighting: option (a) for the prototype, no lamp; the site light is recorded with every photo (a light reading or a gray card in a corner of the frame); a lamp is decided after the first site visit.
4. Benches: option (a), the bench-clamped rig, with handheld use at sites without a suitable bench.
5. First partner: a member-owned waste picker cooperative that sorts dry waste for scrap buyers; SWaCH in Pune, India, is the first candidate to approach, with its scrap dealers as buyers.
6. `CONTRIBUTING.md`: the CERN-OHL-S sentence is removed; all contributions are licensed under MIT.

### Documents changed

- `docs/06-design-decisions.md` (WML-DEC-001 v0.3): open decisions moved to Decisions made; the "no lamp" saving and confirm item 3 updated.
- `docs/decisions/0003-design-for-construction.md` (WML-DDR-003 v0.2, status Draft): accepted, with A1 to A3 accepted as recommended.
- `docs/decisions/0001-trl2-review-decisions.md` (WML-DDR-001 v0.3) and `docs/decisions/0002-recommendations-accepted.md` (WML-DDR-002 v0.2): O1 and O2 recorded as decided.
- `docs/02-concept.md` (WML-PRC-001 v0.6): handheld use at sites without a bench, no lamp with the site light recorded, partner question answered.
- `docs/01-problem.md` (WML-PRB-001 v0.4): partner question answered.
- `CONTRIBUTING.md`: MIT only.

### Follow-up actions to carry approved decisions into the design

1. Decision 1 (pictures): regenerate `media/render-hero.png`, `media/render-station.png`, `media/card.png` and `media/social-preview.png` on Amish's Mac from the constructable rig (clamped board, square post and arm, folded tray, no lamp).
2. Decision 2 (model and drawings): once the reference phone is bought and measured, set the arm length and tray window in `cad/src/model.py` and drawing WML-DWG-001 to its lens offset and size, and update the build plan pictures.
3. Decision 3 (docs): add the site light record (light reading or gray card) to the data protocol and the app's capture step.
4. Decision 6 (docs): tidy the `REUSE.toml` comments, which still name CERN-OHL-S-2.0 above MIT identifiers, and run `reuse lint`.

### Points found in the review

- The `REUSE.toml` comments still say CERN-OHL-S-2.0 for hardware, documentation and CAD, although every license identifier beneath them is MIT (follow-up 4).
- Value engineering listed "a cheaper phone that still meets R12 (about USD 150 or less)" as a saving, but the reference phone is already priced at USD 130, so it is not a saving against the current estimate.
- The renders, card and social preview still show the concept stand (round post, clamp over the screen), and the 2026-09-26 note calls the rig a "lit mat" although it has no lamp (follow-up 1).
