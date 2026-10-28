---
doc_id: WML-CAL-001
title: WasteWise-ml sizing calculations
project: WasteWise-ml
doc_type: Calculation note
version: "0.5"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: MIT
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First-principles sizing of dataset, model, energy and evaluation for TRL 3 against WML-REQ-001 v0.3
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-09-30'
  author: Amish Chadha
  change: Stand clearance and cost updated for the constructable scanning rig (WML-DDR-003)
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: R14 row updated for the 2026-10-02 partner decision (WML-DEC-001); no number changed
- version: "0.5"
  date: '2026-10-25'
  author: Amish Chadha
  change: "Kit 1.8 and 1.9.1 upgrade: results against PR-001 to PR-023 (WML-PRS-001); energy with fix F1 (voice and shutter button; 9 % of the battery, was 8 %); focal length range and stand tilt tolerance; bin volume from the moulded bin (60 L, was 62 L); new sections on stand stiffness, ergonomics, phone temperature, the hazard box and option B; cost USD 313.39 a station (was USD 309.00); independent review applied (preprocessing range, wake time, coverage 66 %, tray placement stack and fix F5, charging in heat)"
---

# WasteWise-ml sizing calculations

On paper, the design meets ten of the twenty-three product requirements in WML-PRS-001 (five on paper: PR-006, PR-010, PR-012, PR-020 and PR-023; five by design: PR-009, PR-015, PR-017, PR-018 and PR-021), does not meet two (PR-002 and PR-011), has six at risk (PR-001, PR-003, PR-004, PR-005, PR-013, PR-019) and five that cannot be verified at TRL 3 (PR-007, PR-008, PR-014, PR-016, PR-022). The model is small: 4.4 MB in 8-bit form; it answers in 64 to 201 ms from a preview-size frame, but up to 331 ms if the app decodes a full 12 MP frame first. The binding constraints are data and evaluation. The dataset needs about 10,000 field photos (about 72 h of labeling), coverage comes out at about 66 % against a 70 % target, and the hazard evaluation needs about 400 hazard items, not 200, to prove 98 % recall. The 2026-10-25 STEM check added three checks that changed the design (WML-DEC-001 F1 to F3): a shutter button at the bench edge and a full-screen, spoken result, because the shortest users could neither reach nor read the flat screen comfortably (section 12); a mat sealed all over (WML-STM-001 C3); and taped terminals for loose cells in the hazard box (WML-STM-001 C1).

Every number in this note is printed by `docs/04-calcs/sizing.py` (run `python docs/04-calcs/sizing.py` from the repo root). The script trains nothing and loads no images; it is arithmetic on stated assumptions. Camera geometry, the stand, the station and option B read `cad/src/model.py`; cost reads `bom/bom.csv`. Values marked "assumed" have no source and are to be replaced by measurement, which belongs to TRL 4 and is on hold.

> **Safety:** WasteWise-ml guides sorting; it does not make any item safe to handle and does not certify material. The station handles sharps, broken glass, lithium cells, chemical containers and biological waste, and the phone, power bank and shutter button carry lithium cells. A missed hazard is the worst failure, which is why this note sizes hazard recall and its evaluation separately (sections 7 and 8), and the hazard box's handling of loose cells (section 14).

## 1. Results against requirements

Table 1 lists every product requirement. Status is one of met on paper, met by design, not met, at risk, or to verify at TRL 4. Not met and at-risk items come first. The old requirement numbers of WML-REQ-001 are in brackets.

Table 1. Requirement status at TRL 3.

| ID | Target | Value from this note | Status |
| --- | --- | --- | --- |
| PR-002 (R2) | Plastic grade accuracy 90 % for PET, 80 % for other rigid HDPE and PP, on answered items | A photo cannot separate opaque HDPE from PP or identify black plastics (about 9 % of items, assumed stream); these go to "Unsure". PET needs about 230 images per grade for 90 % at 70 % coverage | Not met by design for opaque HDPE and PP and black plastics; at risk for PET |
| PR-011 (R11) | Field evaluation set of 2,000 or more images, two or more sites, 50 or more per grade | Sized at 2,000: 400 hazards, 900 non-hazard minimum (18 grades x 50), 700 natural mix; about 43 h of labeling. The set does not exist | Not met |
| PR-001 (R1) | Class accuracy 90 % or more on answered items | Expected full-coverage class error 9.1 % with about 1,290 photos per class (assumed learning curve); 90 % reached at 100 % class coverage | At risk (assumed learning curve; field data may be harder) |
| PR-003 (R3) | Hazard recall 98 % or more, never a sortable grade | Hazard is a separate output with a low threshold; 2,400 hazard training photos needed, 300 would arise naturally. Verification set of 400 hazard items (N1, decided) proves 98 % with up to 3 misses | At risk (rare class; hazard photos must be collected on purpose) |
| PR-004 (R4) | Coverage 70 % or more while meeting PR-001 | 66 % answered (63 % with a grade plus 3 % true hazard flags), 32 % "Unsure", 5 % sent to the hazard box | At risk (4 points short on assumed numbers) |
| PR-005 (R5) | Result within 0.3 s of the photo, offline | 64 to 201 ms from a preview-size frame; up to 331 ms if a full 12 MP frame is decoded first | At risk (capture path to measure) |
| PR-019 | Picture inside the 700 x 450 mm mat, placement allowed for | 586 x 439 mm at 26 mm equivalent plus a 3.3 mm placement stack a side (F5); fits lenses of 25.76 mm and longer; 420 mm proposed (D2) | At risk |
| PR-013 (R13) | MIT code and weights; every dataset license allows training and publishing weights | TrashNet repository MIT; TACO annotations CC BY 4.0, images under per-image licenses; ZeroWaste CC BY-NC 4.0 is excluded from training (N2, decided) | At risk (TACO images filtered one by one) |
| PR-010 (R10) | 8 h shift of 500 scans uses 30 % or less of a 4,000 mAh battery | 9 % if the screen sleeps between scans, with voice on and the shutter button linked (F1), 14 % with a 0.12 W standby; 52 % if the screen stays on all shift; 131 % with a live preview | Met on paper, if the screen sleeps between scans (the power-bank fallback fails above about 35 C) |
| PR-006 (R6) | Model 10 MB or less; app 30 MB or less | 4.4 MB (int8); float16 8.7 MB; float32 17.5 MB fails; app 12 to 19 MB | Met on paper (int8 or float16 only) |
| PR-009 (R9) | Local grades set per site without retraining | Per-site configuration file (D4) | Met by design |
| PR-012 (R12) | Phone about USD 150 or less, 3 GB RAM, 2019 or later chipset | USD 130 reference phone (BOM line 1); model and activations about 8 MB of memory | Met on paper (price indicative) |
| PR-015 | Scan trigger at bench height within 100 mm of the user's edge | Shutter button 45 mm in from the edge, top 773 mm above the floor (section 12) | Met by design |
| PR-016 | Bin number at least 16 arcmin at the eye of a 5th percentile user | 43 arcmin with a 40 mm digit, seen 83 degrees off the screen normal; a 10 mm icon gives 11 arcmin (section 12) | To verify at TRL 4 (trial with a short user) |
| PR-017 | Mat sealed on both faces and all edges | Build plan section 3.7 and BOM line 3 (F2) | Met by design |
| PR-018 | Loose cells go in the hazard box with taped terminals | Tape roll in the box (BOM line 5), briefing (F3); sand bed absorbs one phone-size cell's heat with an 89 K mean rise (section 14) | Met by design |
| PR-020 | Phone below 45 C in shade at a 40 C ambient | 40.7 C in tap-to-scan use; 46.9 C while charging, when the phone pauses charging, which tap-to-scan does not need; about 85 C in direct sun (section 13) | Met on paper (shade required) |
| PR-021 | Rig made from local stock with hand tools | Build plan WML-BLD-001: saw, drill stand, files, snips, vice | Met by design |
| PR-023 | Picture moves less than 1 mm under a 5 N tap | 0.30 mm (section 11) | Met on paper |
| PR-007 (R7) | 3 s or less from placing an item to the result | 0.9 s nominal, 2.1 s worst with the camera open; 1.4 and 3.6 s waking from a sleeping screen | To verify at TRL 4 (needs timed trials) |
| PR-008 (R8) | Usable without reading after a 15 min briefing | Full-screen class colour, bin number at least 40 mm, icon and voice by default (F1) | To verify at TRL 4 (needs co-design sessions) |
| PR-014 (R14) | Consent and privacy protocol with the partner | Principles decided (D6); protocol not written; first candidate partner SWaCH, Pune (decided 2026-10-02), not yet approached | To verify at TRL 4 |
| PR-022 | Phone in and out of the tray within 5 s | Nothing to undo: the phone lies on the tray, the bump in the window (BLD first checks) | To verify at TRL 4 |

Corrections to earlier numbers (2026-10-25): the battery share in tap-to-scan use is 9 %, not 8 %, because fix F1 adds the voice prompt (0.07 Wh a shift) and the Bluetooth link (0.04 Wh); with the screen on all shift it is 52 %, not 51 %. The bin volume is 60 L, not 62 L, because the bin is now modelled as a moulded bin with a 3 mm wall and a 25 mm taper a side, not a straight box with 12 mm walls; the "about 60 L" bought specification is unchanged. One station costs USD 313.39, not USD 309.00 (section 10). After the independent review of 2026-10-25: preprocessing is 20 to 150 ms (was 20 ms), coverage 66 % (was 68 %, because false hazard alarms leave the graded pool), and the picture's margin on the mat is set by the phone's placement in the tray, not by the stand's tilt (section 6).

## 2. Model size (PR-006, was R6)

Assumptions: MobileNetV3-Large (width 1.0, 224 px input) has 5.4 million parameters and 217 million multiply-accumulates, including its 1,000-class ImageNet classifier, with a 1,280-wide penultimate feature (TensorFlow Models, MobileNet README; Howard et al. 2019). The TensorFlow Lite file adds 5 % for the graph, quantization parameters and metadata (assumed). The app without the model is 8 to 15 MB (assumed).

- Removing the ImageNet classifier (1,280 x 1,000 weights plus 1,000 biases) leaves 4.12 million parameters.
- The class head (1,280 to 7) and grade head (1,280 to 22) add 37,149 parameters. The model has 4.16 million parameters.
- File size: 4.4 MB in 8-bit form, 8.7 MB in float16 and 17.5 MB in float32. PR-006 (10 MB) is met in 8-bit or float16 form only. The app with the 8-bit model is 12 to 19 MB, within 30 MB.

## 3. Latency and memory on a low-cost phone (PR-005, PR-012)

Assumptions: 44 ms per image in 8-bit form on a Pixel 1 large core (TensorFlow Models, MobileNet README). A 2019 or later low-cost phone is 1 to 4 times slower (assumed). One Cortex-A53-class core sustains 1.2 to 2.5 GMAC/s in 8-bit inference (assumed). Crop, resize and normalization take 20 ms from a preview-size frame, and up to 150 ms if a full 12 MP frame is decoded first (assumed; the independent review put a full decode at 100 to 300 ms on an A53-class phone).

- The Pixel 1 figure implies 4.9 GMAC/s. Scaled by 1 to 4, inference takes 44 to 176 ms. From A53-class throughput it takes 87 to 181 ms. The two estimates agree at the slow end.
- With preprocessing from a preview-size frame, the photo-to-result time is 64 to 201 ms, 99 ms inside PR-005 (300 ms). If the app decodes a full 12 MP frame first, the slow end is 331 ms, 31 ms over. PR-005 is therefore at risk until the app's capture path is measured; classifying a preview-size frame (with the full frame kept for the record) is the planned path. MobileNetV3-Small stays the fallback for older phones.
- Memory: the weights (4.4 MB) and the two largest 8-bit activation tensors (112 x 112 x 64, double-buffered) need about 8 MB; the camera's frame buffers (about 48 MB for a 12 MP RGBA frame) come on top. Both are a small share of a 3 GB phone (PR-012).

## 4. Time to result (PR-007, was R7)

Table 2 is a time budget, not a measurement.

Table 2. Time from placing an item to seeing the result, seconds.

| Step | Nominal | Worst |
| --- | --- | --- |
| Reach and press the shutter button (or tap) | 0.30 | 0.60 |
| Focus and exposure (focus can lock at the fixed stand height) | 0.40 | 0.80 |
| Capture | 0.13 | 0.30 |
| Preprocess and infer (section 3) | 0.06 | 0.20 |
| Show the result | 0.05 | 0.10 |
| Total, camera already open | 0.9 | 2.1 |
| Wake the phone and open the camera after the screen has slept | 0.50 | 1.50 |
| Total, from a sleeping screen | 1.4 | 3.6 |

The budget fits PR-007 (3 s) with the camera open, and only at the nominal case from a sleeping screen, which the 9 % battery figure relies on; only timed trials with users can verify it. Whether a Bluetooth button's key press reaches the app while the screen sleeps is unproven (WML-DEC-001 confirm item 5). The button sits beside the user's hand at the bench edge, so the reach is no longer than the tap it replaces. At 500 scans in 8 h a scan happens about every 58 s, so PR-010's duty covers only the items a picker is unsure of, not every item handled.

## 5. Energy per scan and battery (PR-010, was R10)

Assumptions: a 4,000 mAh battery at 3.85 V (15.4 Wh). A scan keeps the screen, camera and processor active for 3 s at 2.5 W (assumed). The model adds 2.0 W while it runs (assumed). The screen alone at outdoor brightness draws 0.9 W (assumed). A sleeping phone draws 0.03 W (assumed). Fix F1 adds the voice prompt, 0.5 W for 1 s after each scan (assumed), and the phone side of a held-open Bluetooth LE link to the shutter button, 5 mW (assumed). The 10,000 mAh power bank at 3.7 V delivers through an 85 % boost converter and an 85 % phone charger (assumed).

- Energy per inference is 0.09 to 0.35 J. Energy per scan is 7.5 J, so the model itself is under 5 % of the energy of a scan; the screen and camera dominate. The voice prompt and the Bluetooth link add 0.07 and 0.04 Wh a shift.
- Table 3 gives the shift energy for three ways of using the app.

Table 3. Energy for an 8 h shift of 500 scans, with voice on and the shutter button linked.

| Case | Energy | Share of battery | PR-010 (30 %) |
| --- | --- | --- | --- |
| A: tap-to-scan, screen sleeps between scans | 1.4 Wh | 9 % | Met |
| B: tap-to-scan, screen on all shift | 8.0 Wh | 52 % | Not met without the power bank |
| C: live camera preview all shift | 20.1 Wh | 131 % | Not met |

- A standby of 0.12 W (a foreground service and the Bluetooth link held open, the independent review's upper case) gives 2.1 Wh, 14 %, still within PR-010.
- The power bank holds 37 Wh nominal and puts about 26.7 Wh into the phone battery, enough for 3.4 shifts of case B. With the screen on and charging the phone runs about 10 K over the air, so above about 35 C in shade it pauses charging and case B fails (section 13).
- Finding: tap-to-scan (D5) is necessary but not sufficient. The app must also let the screen sleep, or dim to near zero, between scans. With the power bank on the stand, case B also works.

## 6. Camera geometry at the station (PR-019; from the model)

Assumptions: the reference phone's main camera has a 26 mm 35 mm-equivalent focal length and a 4:3, 12 MP sensor (typical of the class, assumed). The 35 mm equivalent keeps the 43.27 mm frame diagonal, so the 4:3 equivalent frame is 34.62 x 25.96 mm.

- With the lens 440 mm above the mat, the field of view is 67.3 x 53.1 degrees and the camera sees 586 x 439 mm, inside the 700 x 450 mm mat. The image's long side runs along the bench, so the phone sits landscape on the stand.
- The frame clears the mat's edges by 5.3 mm front and back. A tilt of the whole stand about its board barely moves the picture (0.24 mm a degree: the lens moves one way and its axis turns the other). The phone's own placement does: 7.7 mm a degree of axis tilt, 5.1 mm a degree of yaw, plus any slack of the camera bump in the window. With the first 34 mm window and a phone free between the lips (2.0 mm slack, 0.72 degrees of yaw) the stack was 5.7 mm, over the margin (WML-STM-001 S7, found by the independent review). Fix F5: a 32 mm window (1.0 mm slack) and the phone pushed against the far lip, so it cannot turn; with 0.3 degrees of tray tilt (assumed) the stack is 3.3 mm, leaving 2.0 mm.
- With that stack, the frame fits the mat's depth only for a main camera of 25.76 mm equivalent or longer, about 1 % under a quoted 26 mm that is itself rounded. Phones of the class quote about 24 to 28 mm. PR-019 is therefore at risk. Lowering the lens to 420 mm gives a 559 x 419 mm picture, 15.3 mm a side, for any lens of 24.2 mm or longer, at 0.14 mm a pixel; because 440 mm was Amish's decision (N3), this is proposed to him (WML-DEC-001 D2). Either way, the bought phone's picture is measured before the arm is cut (confirm item 2).
- The stand's base board meets the mat's back edge and places the mat (WML-DDR-003). Its front edge is at Y = 560 mm and the picture's edge at Y = 554.7 mm, so the board is 5.3 mm outside the picture at mat level and 12.3 mm at its top edge, the same margin the mat itself has; the post is 38 mm outside. The post (453 mm) and arm (213.5 mm) of 25 x 25 x 2 mm tube hold the lens flush with the phone tray's underside, 440 mm above the mat.
- At the TRL 2 height of 470 mm the frame would be 626 x 469 mm, wider than the mat, so the bench would show at two edges. The model uses 440 mm (N3 in WML-DDR-001, decided by Amish on 2026-09-25).
- Resolution: 0.15 mm per pixel at full 12 MP, so a molded 6 mm resin code digit spans about 41 pixels; 2.6 mm per pixel if the whole frame were shrunk to 224 px. The app therefore crops to the item before resizing: a 300 mm item at 224 px is 1.3 mm per pixel.
- Each bin holds about 60 L inside (3 mm wall, 25 mm taper a side).

## 7. Dataset size (PR-001, PR-002, PR-003, PR-004)

Assumptions (all assumed, to be replaced by a measured learning curve):

- Fine-tuning an ImageNet-pretrained mobile network on field photos follows error(n) = 0.03 + a n^-0.5, with n images per label and error 25 % at 100 images per label.
- The model ranks its own errors well enough that abstaining on the lowest-confidence share u of items removes a share 2u of the errors (up to all of them).
- 30 % margin on the calculated count; eight hard grades (film, mixed paper, newsprint, multilayer pouch and the four hazardous grades) get twice the images; 10 % of photos are rejected in review.

Results:

- To reach 90 % accuracy on answered items at 70 % coverage, the full-coverage error may be 17.5 %, which needs about 230 images per label. An 80 % target allows 35 % error and needs about 47.
- Table 4 shows how the 230 moves with the assumptions. The range is 128 to 591 images per label, so the design figure of 300 per grade covers six of the nine cases (WML-STM-001 M4, open). The independent review recalls a scaling exponent nearer 0.3 for ImageNet (Hestness et al. 2017, to check), which would need about 330. The class error uses the mean of 1,290 photos a class; classes with two grades get about 600 and an error nearer 12 %.

Table 4. Images per label for 90 % at 70 % coverage.

| Exponent | Error 20 % at 100 images | Error 25 % at 100 images | Error 30 % at 100 images |
| --- | --- | --- | --- |
| 0.35 | 158 | 329 | 591 |
| 0.50 | 137 | 230 | 347 |
| 0.65 | 128 | 190 | 260 |

- Design figure: 300 images per grade, doubled for the eight hard grades, with 10 % rejects: **10,000 field photos**. The mean is about 1,290 labeled photos per class, which gives an expected full-coverage class error of 9.1 % (PR-001) and grade error of 15.7 %.
- Labeling effort at 20 s per photo plus 30 % review: **72.2 h** (labeling only: taking the photos, and NIR or resin-code ground truth for the camera-blind grades, come on top), USD 433 at the USD 6 per hour planning rate (the real rate is set with the partner, D7).
- Hazards: the four hazardous grades need 2,400 training photos, but a natural stream at 3 % hazards gives only about 300 in 10,000 photos. Hazard photos must be collected on purpose (for example at battery drop-off points), by trained people, without extra handling of sharps (see the safety note below).
- Public sets (TrashNet, TACO) are not counted; they help pretraining but are not organized by buyer grade.

> **Safety:** Collecting hazard photos on purpose must not add handling. Photograph batteries and chemical containers where they lie, and photograph sharps only inside a rigid sharps container or with tongs, by people trained for it. Pickers are never asked to collect hazards for the dataset.

## 8. Coverage (PR-004) and hazard false alarms

Assumptions: a dry mixed stream by item count (assumed): PET 20 %; HDPE and PP visually separable 6 %; opaque HDPE and PP not separable by camera 6 %; black plastics 3 %; other plastics 4 %; film 14 %; metal 10 %; paper and card 20 %; composite 6 %; glass 6 %; organic 2 %; hazardous 3 %. At the high-recall hazard threshold, 2 % of non-hazard items are flagged (assumed).

- The camera-blind share (opaque HDPE and PP, black plastics) is 9 %; these always go to "Unsure" and then to WasteWise Scan (WML-STM-001 S3).
- On the other 88 % of items, 90 % grade accuracy on answered items needs coverage of 73 % with the grade error of section 7.
- False hazard alarms (2 % of non-hazard items) leave the graded pool (independent review, 2026-10-25). Result: **63.3 % answered with a grade, 31.9 % "Unsure", 4.9 % sent to the hazard box**, of which 2.9 % are true hazards, so about 66 % of items get a useful answer. PR-004 (70 %) is at risk by 4 points (WML-STM-001 M5, open). The calculation also takes abstention on the camera-blind items as perfect, which is not shown. At class level (PR-001) the class error is already under 10 %, so class coverage is 100 %.
- The hazard box receives 4.9 % of items, and 40 % of them are false alarms. That is the intended trade: false alarms cost a little value; misses can start a fire.

## 9. Evaluation plan (PR-001, PR-003, PR-011)

The evaluation set is never used for training and comes from at least two sites. Hazard recall is proved with a one-sided 95 % Clopper-Pearson lower bound.

Table 5. One-sided 95 % lower bound on hazard recall.

| Hazard items | 0 misses | 1 miss | 2 misses | Misses allowed for 98 % |
| --- | --- | --- | --- | --- |
| 150 | 0.9802 | 0.9688 | 0.9586 | 0 |
| 200 | 0.9851 | 0.9765 | 0.9689 | 0 |
| 300 | 0.9901 | 0.9843 | 0.9792 | 1 |
| 400 | 0.9925 | 0.9882 | 0.9843 | 3 |
| 600 | 0.9950 | 0.9921 | 0.9895 | 6 |

- A verification set of 200 hazard items (the TRL 2 figure) proves 98 % only if the model misses none. With 400 items it passes with up to 3 misses, which gives an 80 % chance of passing if true recall is 99.5 %. If true recall is 99.0 %, about 970 items are needed for the same chance. N1 in WML-DDR-001: 400 hazard items, decided by Amish on 2026-09-25; PR-003 calls for at least 400.
- Composition of the 2,000-image set: 400 hazards, at least 900 non-hazard items (18 grades x 50), and 700 in the natural mix. Finding 400 hazards at 3 % means sorting about 13,300 items, so hazards are sampled on purpose.
- Precision: about 1,044 answered non-hazard items give a 95 % interval of +/- 1.8 points on a 90 % accuracy, good enough to test PR-001; stratified and site-clustered sampling widens it, and showing at least 90 % needs an observed accuracy of about 91.5 %.
- The hazard bound holds for the evaluation population only: hazards collected on purpose are cleaner than those in the stream, so field recall can be lower, and each hazard type is reported separately. One grade at 50 items gives +/- 11 points on 80 %, so per-grade results are indicative only.
- Effort: 60 s per photo plus 30 % review for verified ground truth (buyer check, legible resin code or NIR): 43.3 h, USD 260.
- Photos from one site are correlated; the model card reports each site separately as well as pooled.

## 10. Cost (from the BOM)

All twelve BOM lines are priced. One station (lines 1 to 7, 11 and 12) is USD 313.39, up from USD 309.00 because of the shutter button (line 12, USD 3.39 cited, F1) and the tape roll in the hazard box (line 5, USD 1.00 estimate, F3); the dataset, evaluation set and compute (lines 8 to 10) are USD 730.00; a two-station pilot is USD 1,356.78. `budget_usd` is null because this is a software repository, so there is no value-engineering target and the BOM is for planning only.

## 11. Stand stiffness under a tap (PR-023)

Assumptions: a firm tap on the screen is 5 N, straight down, at the screen centre, 270 mm in front of the post's axis (assumed). The post and arm are 25 x 25 x 2 mm 6063 aluminium tube, E = 69 GPa, second moment of area 16,345 mm4 taken with square corners (the real tube's rounded corners make it a few percent less stiff); the bolted joints are taken as rigid.

- The tap bends the post and the arm: the screen moves down 0.17 mm, and the camera's axis turns 0.039 degrees, which moves the picture on the mat by 0.30 mm, under the 1 mm (one grid line's width) of the build plan's first check "Stand rigid".
- With the shutter button (F1) nobody needs to tap the phone at all; the check matters when someone does.

## 12. Ergonomics at the station (PR-015, PR-016)

Assumptions: Indian women's stature from Nag, Nag and Desai (2003, n = 95): 1,356 mm at the 5th percentile, 1,499 mm mean and 1,599 mm at the 95th. Body proportions after Drillis and Contini (1966) as given by Winter (2009): eye height 0.936, shoulder height 0.818, upper arm 0.186 and forearm with hand 0.254 of stature. A user standing close to the bench has the eye 100 mm and the shoulder joint 150 mm behind the bench's edge (assumed). Screens: upper arm elevation of 60 degrees (ISO 11226) and a character height of 16 arcmin minimum, 20 to 22 preferred (ISO 9241-303). The phone lies screen up with its glass 1,215 mm above the floor, 315 mm in from the user's edge of the bench.

Table 6. Reaching and reading the phone as first designed, and with fix F1.

| User | Screen against shoulder | Upper arm elevation to tap (elbow down) | Viewing angle off the screen normal | 10 mm icon | 40 mm bin number (F1) |
| --- | --- | --- | --- | --- | --- |
| Woman, 5th percentile | 106 mm above | 59 degrees | 82.6 degrees | 11 arcmin | 43 arcmin |
| Woman, mean | 11 mm below | 34 degrees | 65.6 degrees | 31 arcmin | 125 arcmin |
| Woman, 95th percentile | 93 mm below | 20 degrees | 55.8 degrees | 38 arcmin | 154 arcmin |

- Tapping the screen about once a minute puts the shortest users at the 60 degree screen, with the hand above the shoulder. The shutter button removes the reach: it lies on the bench 45 mm in from the user's edge, its key 773 mm above the floor, beside the hand (PR-015).
- The flat screen is seen nearly edge-on by the shortest users, so a normal-size icon falls under the 16 arcmin minimum. A full-screen class colour with a bin number at least 40 mm tall reads at 43 arcmin or more for every user from the 5th percentile up, and the spoken bin number does not depend on the angle at all (PR-008, PR-016).
- These are screens, not an assessment. ISO 11226 is written for static postures, and the 59 degrees moves to 51 or 68 degrees with the shoulder 100 or 200 mm behind the bench edge. At 83 degrees off the normal the digit is squashed about 7.7 to 1 and glare is likely, so legibility is confirmed with a short user (PR-016 to verify). The back 100 mm of the mat is beyond the 5th percentile user's reach without leaning; items are placed near the middle. Posture, frequency and the partner's bench heights are measured with users at TRL 4.

## 13. Phone temperature at the station (PR-020)

Assumptions: a 40 C afternoon in Pune before the monsoon (IMD Pune forecast as reported on 2024-03-30); heat leaves the phone from both faces at 10 W/(m2 K), natural convection plus radiation (assumed); charging from the power bank adds about 1.5 W of heat (assumed); sun 1,000 W/m2 at 0.9 absorptance on the top face; Li-ion charge window 0 to 45 C (Battery University BU-410).

- In tap-to-scan use the phone dissipates 0.17 W on average and sits 0.7 K above the shade air, at 40.7 C, below the 45 C charge limit.
- While charging it would reach about 46.9 C, so the phone pauses charging on the hottest afternoons. Tap-to-scan needs only 9 % of the battery a shift (section 5), so the shift does not depend on charging.
- With the screen on all shift and charging (case B with the power bank), the phone runs about 10.3 K over the air, so charging holds only below about 35 C ambient.
- In direct sun the phone would reach about 85 C and throttle or shut down: the rig stands in shade, as the build plan's safety stop S4 says.

## 14. Hazard box and shutter button cell (PR-018, PR-015)

Assumptions: dry sand at 1,600 kg/m3 and 830 J/(kg K) (typical); a phone-size cell stores 15.4 Wh, and its total heat in thermal runaway is taken as up to 8 times that (assumed upper bound); a CR2032 cell holds 225 mAh and a linked Bluetooth LE button draws 0.05 mA on average (assumed).

- The 50 mm sand bed holds 6.0 kg of sand. One phone-size cell in runaway would raise its mean temperature by about 89 K. That is bulk heat capacity only; the sand near the cell gets far hotter, and venting and spread to other cells are not assessed: the bed and the steel box contain one such cell and keep it from paper and film, but sand does not stop a cell in runaway, and larger packs need the partner's fire guidance (RSK H3).
- Loose cells go in with their terminals taped (F3), so they are much less likely to short on the steel walls or on each other (WML-STM-001 C1).
- The shutter button's cell lasts about 4,500 h, about 560 shifts, against a three-month screen of 78 shifts, if the button draws 0.05 mA; at 0.45 mA it would last only about 62 shifts, so the bought button's current is measured (WML-STM-001 E4, open).

## 15. Option B, tray detector: first-order numbers (WML-OPT-001)

Assumptions: Raspberry Pi Camera Module 3 Wide, 102 x 67 degrees and 4,608 x 2,592 pixels (datasheet values); lens 450 mm over the tray floor; Pi 5 idle 2.7 W, 6 W while the detector runs for 3 s a photo, 5 inch display 1.5 W (assumed); 3,000 items a shift at 15 a photo (assumed); a YOLOv8n-class detector at 8.7 GFLOP for a 640 px input (Ultralytics), four times that at 1,280 px, at 20 to 40 GFLOP/s on the Pi 5 (assumed); a box drawn by extreme clicking in about 7 s (Papadopoulos et al. 2017).

- The camera sees 1,111 x 596 mm, the whole 600 x 400 mm tray. Resolution is 0.24 mm per pixel at full size and 0.87 mm per pixel at a 1,280 px detector input, where a 40 mm bottle cap spans 46 pixels.
- The Pi 5 and display use about 34.1 Wh a shift, 54 % of the 62.9 Wh a 20,000 mAh power bank delivers.
- The detector needs 0.9 to 1.7 s a photo, at worst about 116 ms an item.
- Labeling 10,000 item instances with a class, a grade and a box takes about 98 h (USD 585), against 72 h for option A.
- One option B station costs about USD 418.90 without a phone, from cited prices for the Pi 5 (USD 100 after the February 2026 rise), the Camera Module 3 Wide (USD 35.95) and the 5 inch Touch Display 2 (USD 54.95), estimates for the rest, and the shared bins, hazard box and scale (USD 121.00).

## 16. Sources

- Battery University. "BU-410: Charging at High and Low Temperatures." https://batteryuniversity.com/article/charging-at-high-and-low-temperatures. Checked 2026-10-25.
- Bashkirova, D., et al. 2022. ZeroWaste dataset (CC BY-NC 4.0; code MIT). https://github.com/dbash/zerowaste. Checked 2026-09-25.
- Drillis, R., and R. Contini. 1966. *Body Segment Parameters.* Technical Report 1166-03, New York University; as given in Winter, D. A. 2009. *Biomechanics and Motor Control of Human Movement.* 4th ed. Wiley.
- Free Press Journal. "Pune: City To Hit 40 Degrees Celsius On April 1." 2024-03-30 (IMD Pune forecast). https://www.freepressjournal.in/pune/pune-city-to-hit-40-degree-celsius-on-april-1. Checked 2026-10-25.
- Howard, A., et al. 2019. "Searching for MobileNetV3." ICCV 2019. arXiv:1905.02244. Checked 2026-09-25 at https://arxiv.org/abs/1905.02244.
- ISO 11226:2000 and ISO 9241-303:2011 screening values as widely reported; standards not purchased (to confirm).
- Nag, A., P. K. Nag and H. Desai. 2003. "Hand Anthropometry of Indian Women." *Indian Journal of Medical Research* 117: 260 to 269. Checked 2026-10-25.
- OMG! Ubuntu. "Raspberry Pi Announce More Price Rises." 2026-02-02 (Pi 5 4 GB from USD 85 to USD 100). https://www.omgubuntu.co.uk/2026/02/raspberry-pi-annouce-more-price-rises. Checked 2026-10-25.
- Papadopoulos, D. P., et al. 2017. "Extreme Clicking for Efficient Object Annotation." ICCV 2017. arXiv:1708.02750.
- PiShop.us. Raspberry Pi category, page 2 (Camera Module 3 assemblies USD 21.95 to 35.95; 5 inch Touch Display 2 USD 54.95). https://www.pishop.us/raspberry-pi-foundation/?page=2. Checked 2026-10-25.
- Proença, P. F., and P. Simões. 2020. TACO. Annotations CC BY 4.0; images under per-image licenses. http://tacodataset.org. Checked 2026-09-25.
- TensorFlow Models. "MobileNet" README, MobileNetV3 checkpoint table (5.4 M parameters, 217 M MACs, 44 ms on a Pixel 1 in 8-bit form). https://github.com/tensorflow/models/tree/master/research/slim/nets/mobilenet. Checked at TRL 2.
- Thung, G., and M. Yang. 2016. TrashNet repository (MIT license; 2,527 images on a white posterboard). https://github.com/garythung/trashnet. Checked 2026-09-25.
- Walmart. "Mini Wireless Bluetooth Remote Shutter Controller Button" (USD 3.39, CR2032). https://www.walmart.com/ip/Mini-Wireless-Bluetooth-Remote-Shutter-Controller-Button-Self-Timer-Camera-Stick-Shutter-F5G3/1435880459. Checked 2026-10-25.
- Values marked "assumed" in this note have no source.
