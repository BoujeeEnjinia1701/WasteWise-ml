---
doc_id: WML-CAL-001
title: WasteWise-ml sizing calculations
project: WasteWise-ml
doc_type: Calculation note
version: "0.4"
status: Draft
date: '2026-10-02'
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
---

# WasteWise-ml sizing calculations

On paper, the design meets four of the fourteen requirements in WML-REQ-001 (R5, R6, R9, R12), meets R10 on one condition, does not meet two (R2 and R11), has four at risk (R1, R3, R4, R13) and three that cannot be verified at TRL 3 (R7, R8, R14). The model is small and fast enough by a wide margin: 4.4 MB in 8-bit form and 64 to 201 ms from photo to result on a low-cost phone. The binding constraints are data and evaluation. The dataset needs about 10,000 field photos (about 72 h of labeling), coverage comes out at about 68 % against a 70 % target, and the hazard evaluation needs about 400 hazard items, not 200, to prove 98 % recall.

Every number in this note is printed by `docs/04-calcs/sizing.py` (run `python docs/04-calcs/sizing.py` from the repo root). The script trains nothing and loads no images; it is arithmetic on stated assumptions. Camera geometry reads `cad/src/model.py`; cost reads `bom/bom.csv`. Values marked "assumed" have no source and are to be replaced by measurement, which belongs to TRL 4 and is on hold.

> **Safety:** WasteWise-ml guides sorting; it does not make any item safe to handle and does not certify material. The station handles sharps, broken glass, lithium cells, chemical containers and biological waste, and the phone and power bank carry lithium cells. A missed hazard is the worst failure, which is why this note sizes hazard recall and its evaluation separately (sections 7 and 8).

## 1. Results against requirements

Table 1 lists every requirement. Status is one of met, not met, at risk, or not verifiable at TRL 3. Not met and at-risk items come first.

Table 1. Requirement status at TRL 3.

| ID | Target | Value from this note | Status |
| --- | --- | --- | --- |
| R2 | Plastic grade accuracy 90 % for PET, 80 % for other rigid HDPE and PP, on answered items | A photo cannot separate opaque HDPE from PP or identify black plastics (about 9 % of items, assumed stream); these go to "Unsure". PET needs about 230 images per grade for 90 % at 70 % coverage | Not met by design for opaque HDPE and PP and black plastics; at risk for PET |
| R11 | Field evaluation set of 2,000 or more images, two or more sites, 50 or more per grade | Sized at 2,000: 400 hazards, 900 non-hazard minimum (18 grades x 50), 700 natural mix; about 43 h of labeling. The set does not exist | Not met |
| R1 | Class accuracy 90 % or more on answered items | Expected full-coverage class error 9.1 % with about 1,290 photos per class (assumed learning curve); 90 % reached at 100 % class coverage | At risk (assumed learning curve; field data may be harder) |
| R3 | Hazard recall 98 % or more, never a sortable grade | Hazard is a separate output with a low threshold; 2,400 hazard training photos needed, 300 would arise naturally. Verification set raised from 200 to 400 hazard items (N1, decided), which proves 98 % with up to 3 misses | At risk (rare class; hazard photos must be collected on purpose) |
| R4 | Coverage 70 % or more while meeting R1 | 68 % answered (65 % with a grade plus 3 % hazard flags), 32 % "Unsure" | At risk (2 points short on assumed numbers) |
| R13 | MIT code and weights; every dataset license allows training and publishing weights | TrashNet repository MIT; TACO annotations CC BY 4.0, images under per-image licenses; ZeroWaste CC BY-NC 4.0, which does not fit MIT weights, is excluded from training (N2, decided) | At risk (TACO images filtered one by one) |
| R10 | 8 h shift of 500 scans uses 30 % or less of a 4,000 mAh battery | 8 % if the screen sleeps between scans; 51 % if the screen stays on all shift; 130 % with a live preview | Met, if the screen sleeps between scans (or with the power bank) |
| R5 | Result within 0.3 s of the photo, offline | 64 to 201 ms, 99 ms margin at the slow end | Met |
| R6 | Model 10 MB or less; app 30 MB or less | 4.4 MB (int8); float16 8.7 MB; float32 17.5 MB fails; app 12 to 19 MB | Met (int8 or float16 only) |
| R9 | Local grades set per site without retraining | Per-site configuration file (D4) | Met (design review) |
| R12 | Phone about $150 or less, 3 GB RAM, 2019 or later chipset | $130 reference phone (BOM line 1); model and activations under 10 MB of RAM | Met (price indicative) |
| R7 | 3 s or less from placing an item to the result | 0.9 s nominal, 2.0 s worst on a time budget | Not verifiable at TRL 3 (needs timed trials) |
| R8 | Usable without reading after a 15 min briefing | Icon, color, bin number and optional voice (WML-PRC-001) | Not verifiable at TRL 3 (needs co-design sessions) |
| R14 | Consent and privacy protocol with the partner | Principles decided (D6); protocol not written; first candidate partner SWaCH, Pune (decided 2026-10-02), not yet approached | Not verifiable at TRL 3 |

Corrections to TRL 2 numbers: the model file is about 4.4 MB, not 5 to 6 MB, because the 1.28 million-parameter ImageNet classifier is replaced by two small heads; latency is 64 to 201 ms, not 0.05 to 0.2 s, once preprocessing is added at the slow end; tap-to-scan uses about 8 %, not 7 %, of the battery once standby is counted; and the flow split is about 65 % answered with a grade, 32 % "Unsure" and 3 % hazard, not 75 %, 22 % and 3 %.

## 2. Model size (R6)

Assumptions: MobileNetV3-Large (width 1.0, 224 px input) has 5.4 million parameters and 217 million multiply-accumulates, including its 1,000-class ImageNet classifier, with a 1,280-wide penultimate feature (TensorFlow Models, MobileNet README; Howard et al. 2019). The TensorFlow Lite file adds 5 % for the graph, quantization parameters and metadata (assumed). The app without the model is 8 to 15 MB (assumed).

- Removing the ImageNet classifier (1,280 x 1,000 weights plus 1,000 biases) leaves 4.12 million parameters.
- The class head (1,280 to 7) and grade head (1,280 to 22) add 37,149 parameters. The model has 4.16 million parameters.
- File size: 4.4 MB in 8-bit form, 8.7 MB in float16 and 17.5 MB in float32. R6 (10 MB) is met in 8-bit or float16 form only. The app with the 8-bit model is 12 to 19 MB, within 30 MB.

## 3. Latency on a low-cost phone (R5)

Assumptions: 44 ms per image in 8-bit form on a Pixel 1 large core (TensorFlow Models, MobileNet README). A 2019 or later low-cost phone is 1 to 4 times slower (assumed). One Cortex-A53-class core sustains 1.2 to 2.5 GMAC/s in 8-bit inference (assumed). Crop, resize and normalization take 20 ms (assumed).

- The Pixel 1 figure implies 4.9 GMAC/s. Scaled by 1 to 4, inference takes 44 to 176 ms. From A53-class throughput it takes 87 to 181 ms. The two estimates agree at the slow end.
- With preprocessing, the photo-to-result time is 64 to 201 ms. R5 (300 ms) is met with 99 ms margin at the slow end. MobileNetV3-Small stays the fallback for older phones.

## 4. Time to result (R7)

Table 2 is a time budget, not a measurement.

Table 2. Time from placing an item to seeing the result, seconds.

| Step | Nominal | Worst |
| --- | --- | --- |
| Reach and tap (or foot switch) | 0.30 | 0.60 |
| Focus and exposure (focus can lock at the fixed stand height) | 0.40 | 0.80 |
| Capture | 0.13 | 0.30 |
| Preprocess and infer (section 3) | 0.06 | 0.20 |
| Show the result | 0.05 | 0.10 |
| Total | 0.9 | 2.0 |

The budget fits R7 (3 s), but only timed trials with users can verify it. At 500 scans in 8 h a scan happens about every 58 s, so R10's duty covers only the items a picker is unsure of, not every item handled.

## 5. Energy per scan and battery (R10)

Assumptions: a 4,000 mAh battery at 3.85 V (15.4 Wh). A scan keeps the screen, camera and processor active for 3 s at 2.5 W (assumed). The model adds 2.0 W while it runs (assumed). The screen alone at outdoor brightness draws 0.9 W (assumed). A sleeping phone draws 0.03 W (assumed). The 10,000 mAh power bank at 3.7 V delivers through an 85 % boost converter and an 85 % phone charger (assumed).

- Energy per inference is 0.09 to 0.35 J. Energy per scan is 7.5 J, so the model itself is under 5 % of the energy of a scan; the screen and camera dominate.
- Table 3 gives the shift energy for three ways of using the app.

Table 3. Energy for an 8 h shift of 500 scans.

| Case | Energy | Share of battery | R10 (30 %) |
| --- | --- | --- | --- |
| A: tap-to-scan, screen sleeps between scans | 1.3 Wh | 8 % | Met |
| B: tap-to-scan, screen on all shift | 7.9 Wh | 51 % | Not met without the power bank |
| C: live camera preview all shift | 20.0 Wh | 130 % | Not met |

- The power bank holds 37 Wh nominal and puts about 26.7 Wh into the phone battery, enough for 3.4 shifts of case B.
- Finding: tap-to-scan (D5) is necessary but not sufficient. The app must also let the screen sleep, or dim to near zero, between scans. With the power bank on the stand, case B also works.

## 6. Camera geometry at the station (from the model)

Assumptions: the reference phone's main camera has a 26 mm 35 mm-equivalent focal length and a 4:3, 12 MP sensor (typical of the class, assumed). The 35 mm equivalent keeps the 43.27 mm frame diagonal, so the 4:3 equivalent frame is 34.62 x 25.96 mm.

- With the lens 440 mm above the mat, the field of view is 67.3 x 53.1 degrees and the camera sees 586 x 439 mm, inside the 700 x 450 mm mat. The image's long side runs along the bench, so the phone sits landscape on the stand.
- The stand's base board now meets the mat's back edge and places the mat (WML-DDR-003). Its front edge is at Y = 560 mm and the picture's edge at Y = 554.7 mm, so the board is 5.3 mm outside the picture at mat level and 12.3 mm at its top edge, the same margin the mat itself has; the post is 38 mm outside. The post (453 mm) and arm (213.5 mm) of 25 x 25 x 2 mm tube hold the lens flush with the phone tray's underside, 440 mm above the mat.
- At the TRL 2 height of 470 mm the frame would be 626 x 469 mm, wider than the mat, so the bench would show at two edges. The model uses 440 mm (N3 in WML-DDR-001, decided by Amish on 2026-09-25).
- Resolution: 0.15 mm per pixel at full 12 MP, enough to read a molded resin code; 2.6 mm per pixel if the whole frame were shrunk to 224 px. The app therefore crops to the item before resizing: a 300 mm item at 224 px is 1.3 mm per pixel.
- Each bin holds about 62 L inside.

## 7. Dataset size (R1, R2, R3, R4)

Assumptions (all assumed, to be replaced by a measured learning curve):

- Fine-tuning an ImageNet-pretrained mobile network on field photos follows error(n) = 0.03 + a n^-0.5, with n images per label and error 25 % at 100 images per label.
- The model ranks its own errors well enough that abstaining on the lowest-confidence share u of items removes a share 2u of the errors (up to all of them).
- 30 % margin on the calculated count; eight hard grades (film, mixed paper, newsprint, multilayer pouch and the four hazardous grades) get twice the images; 10 % of photos are rejected in review.

Results:

- To reach 90 % accuracy on answered items at 70 % coverage, the full-coverage error may be 17.5 %, which needs about 230 images per label. An 80 % target allows 35 % error and needs about 47.
- Table 4 shows how the 230 moves with the assumptions. The range is 128 to 591 images per label, so the design figure of 300 per grade covers the central cases but not the most pessimistic one.

Table 4. Images per label for 90 % at 70 % coverage.

| Exponent | Error 20 % at 100 images | Error 25 % at 100 images | Error 30 % at 100 images |
| --- | --- | --- | --- |
| 0.35 | 158 | 329 | 591 |
| 0.50 | 137 | 230 | 347 |
| 0.65 | 128 | 190 | 260 |

- Design figure: 300 images per grade, doubled for the eight hard grades, with 10 % rejects: **10,000 field photos**. The mean is about 1,290 labeled photos per class, which gives an expected full-coverage class error of 9.1 % (R1) and grade error of 15.7 %.
- Labeling effort at 20 s per photo plus 30 % review: **72.2 h**, $433 at the $6 per hour planning rate (the real rate is set with the partner, D7).
- Hazards: the four hazardous grades need 2,400 training photos, but a natural stream at 3 % hazards gives only about 300 in 10,000 photos. Hazard photos must be collected on purpose (for example at battery drop-off points), by trained people, without extra handling of sharps (see the safety note below).
- Public sets (TrashNet, TACO) are not counted; they help pretraining but are not organized by buyer grade.

> **Safety:** Collecting hazard photos on purpose must not add handling. Photograph batteries and chemical containers where they lie, and photograph sharps only inside a rigid sharps container or with tongs, by people trained for it. Pickers are never asked to collect hazards for the dataset.

## 8. Coverage (R4) and hazard false alarms

Assumptions: a dry mixed stream by item count (assumed): PET 20 %; HDPE and PP visually separable 6 %; opaque HDPE and PP not separable by camera 6 %; black plastics 3 %; other plastics 4 %; film 14 %; metal 10 %; paper and card 20 %; composite 6 %; glass 6 %; organic 2 %; hazardous 3 %. At the high-recall hazard threshold, 2 % of non-hazard items are flagged (assumed).

- The camera-blind share (opaque HDPE and PP, black plastics) is 9 %; these always go to "Unsure" and then to WasteWise Scan.
- On the other 88 % of items, 90 % grade accuracy on answered items needs coverage of 73 % with the grade error of section 7.
- Result: **65 % answered with a grade, 32 % "Unsure", 3 % hazard flags**, so 68 % of items get an answer. R4 (70 %) is at risk by 2 points. At class level (R1) the class error is already under 10 %, so class coverage is 100 %.
- The hazard box receives 4.9 % of items, and 40 % of them are false alarms. That is the intended trade: false alarms cost a little value; misses can start a fire.

## 9. Evaluation plan (R1, R3, R11)

The evaluation set is never used for training and comes from at least two sites. Hazard recall is proved with a one-sided 95 % Clopper-Pearson lower bound.

Table 5. One-sided 95 % lower bound on hazard recall.

| Hazard items | 0 misses | 1 miss | 2 misses | Misses allowed for 98 % |
| --- | --- | --- | --- | --- |
| 150 | 0.9802 | 0.9688 | 0.9586 | 0 |
| 200 | 0.9851 | 0.9765 | 0.9689 | 0 |
| 300 | 0.9901 | 0.9843 | 0.9792 | 1 |
| 400 | 0.9925 | 0.9882 | 0.9843 | 3 |
| 600 | 0.9950 | 0.9921 | 0.9895 | 6 |

- A verification set of 200 hazard items (the TRL 2 figure) proves 98 % only if the model misses none. With 400 items it passes with up to 3 misses, which gives an 80 % chance of passing if true recall is 99.5 %. If true recall is 99.0 %, about 970 items are needed for the same chance. N1 in WML-DDR-001: 400 hazard items, decided by Amish on 2026-09-25; R3 in WML-REQ-001 v0.4 now calls for at least 400.
- Composition of the 2,000-image set: 400 hazards, at least 900 non-hazard items (18 grades x 50), and 700 in the natural mix. Finding 400 hazards at 3 % means sorting about 13,300 items, so hazards are sampled on purpose.
- Precision: about 1,065 answered non-hazard items give a 95 % interval of +/- 1.8 points on a 90 % accuracy, good enough to test R1. One grade at 50 items gives +/- 11 points on 80 %, so per-grade results are indicative only.
- Effort: 60 s per photo plus 30 % review for verified ground truth (buyer check, legible resin code or NIR): 43.3 h, $260.
- Photos from one site are correlated; the model card reports each site separately as well as pooled.

## 10. Cost (from the BOM)

All eleven BOM lines are priced. One station (lines 1 to 7 and 11) is $309.00, up from $285.00 because the stand is now made and clamped to the bench (WML-DDR-003); the dataset, evaluation set and compute (lines 8 to 10) are $730.00; a two-station pilot is $1,348.00. `budget_usd` is null because this is a software repository, so the BOM is for planning only.

## 11. Sources

- Howard, A., et al. 2019. "Searching for MobileNetV3." ICCV 2019. arXiv:1905.02244. Checked 2026-09-25 at https://arxiv.org/abs/1905.02244.
- TensorFlow Models. "MobileNet" README, MobileNetV3 checkpoint table (5.4 M parameters, 217 M MACs, 44 ms on a Pixel 1 in 8-bit form). https://github.com/tensorflow/models/tree/master/research/slim/nets/mobilenet. Checked at TRL 2.
- Thung, G., and M. Yang. 2016. TrashNet repository (MIT license; 2,527 images on a white posterboard). https://github.com/garythung/trashnet. Checked 2026-09-25.
- Proença, P. F., and P. Simões. 2020. TACO. Annotations CC BY 4.0; images under per-image licenses, CC BY 4.0 where none is given. http://tacodataset.org. Checked 2026-09-25.
- Bashkirova, D., et al. 2022. ZeroWaste dataset (CC BY-NC 4.0; code MIT). https://github.com/dbash/zerowaste. Checked 2026-09-25.
- Values marked "assumed" in this note have no source.
