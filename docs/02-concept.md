---
doc_id: WML-PRC-001
title: WasteWise-ml design precis
project: WasteWise-ml
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, data plan, first-order numbers, safety, media)
---

# WasteWise-ml design precis

WasteWise-ml is an open image classifier that runs offline on a low-cost Android phone. The user photographs one item on a light mat, and within a fraction of a second the phone shows the item's material class, its local buyer grade and a confidence value, or says "Unsure" or "Hazard". Sorted material goes to bins that match the buyer's price list; unsure plastics go to WasteWise Scan for a near-infrared (NIR) resin check; clean PET, HDPE and PP can be sold to a ReflowEconomy micro-factory. First-order numbers suggest a MobileNetV3-class model of about 5 to 6 MB answers in about 0.05 to 0.2 s and uses about 7 % of a phone battery in an 8 h shift of 500 scans. The binding constraint is data: there is no field dataset organized by buyer grade yet, and a camera alone cannot separate some resins.

![Data and material flow](../media/flow.png)

*Figure 1. Data and material flow at one sorting station. Teal: material and decisions; blue: linked WasteWise Scan and ReflowEconomy steps; red: hazards; dashed: the data loop. Percentages are estimates for a dry mixed stream.*

![Hero render](../media/hero.png)

*Figure 2. The concept in its setting: a sorting bench with a phone on a clamp stand over a light mat, sample items (PET bottle, can, carton and film), seven color-labeled bins by material class, a hazard box and a platform scale. The grey figure is a 1.75 m person for scale.*

## How it works

1. **Present.** The picker takes one item from the input sack and holds or places it on a light mat under the phone. On the floor or in the street the phone is handheld instead.
2. **Photograph.** A tap, or a foot switch in a later version, takes one photo. The app crops and resizes it to 224 x 224 pixels. The camera does not run between scans, which saves battery (see "Battery").
3. **Classify.** A mobile convolutional network with one shared backbone and two small output heads runs on the phone with no network. The first head predicts one of seven material classes; the second predicts the grade within that class (about 22 grades, listed in `ml/data/taxonomy.yaml`).
4. **Decide.** The app compares the confidence with per-class thresholds.
   - Confident: it shows an icon, a color and a bin number, and optionally speaks the grade in the local language.
   - Below threshold: it shows "Unsure: check". The item goes to the Unsure bin, and later to WasteWise Scan (for plastics) or the picker's own judgment.
   - Any hazard class above a low threshold: it shows "Hazard: do not sort" in red. The item goes to the hazard box. Hazards are never offered as a sortable grade.
5. **Map to local grades.** A per-site configuration file maps the model's grades to the buyer's grade names, bin numbers and colors, so a new city needs a new file, not a new model, unless it pays for a grade the model cannot see.
6. **Sell.** Sorted lots are weighed and sold at the grade price. Clean PET, HDPE and PP can go to a ReflowEconomy micro-factory.
7. **Learn.** With the user's consent, photos of unsure and corrected items are queued and uploaded when a network is available. The partner organization checks labels, and the project retrains, evaluates on a fixed field test set and publishes new weights with a model card.

## Main components

Numbers 1 to 7 match the exploded view (Figure 3) and `bom/bom.csv`. Items 8 to 10 are effort and compute, with no geometry.

| No. | Component | Role |
| --- | --- | --- |
| 1 | Smartphone running the model | Camera, compute and display; the user's own phone or a reference phone (about 3 GB RAM, 2019 or later chipset) |
| 2 | Phone stand with clamp arm | Holds the phone face-down about 470 mm above the mat so both hands stay free and the view is repeatable |
| 3 | Light sorting mat | Plain, matte background with a 50 mm grid for scale; assumed to help accuracy |
| 4 | Bins by material class (7) | PET; HDPE and PP; film; metal; paper and carton; glass; Unsure |
| 5 | Hazard box | Lidded steel box with a sand layer and a sharps container inside |
| 6 | Power bank and cable | Keeps the phone running through a shift |
| 7 | Platform scale | Weighs sorted lots before sale |
| 8 | Labeled field dataset | About 10,000 consented photos labeled by class and grade |
| 9 | Field evaluation set | About 2,000 photos with verified ground truth, never used for training |
| 10 | Training compute | About 40 GPU hours of fine-tuning and evaluation |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view of one sorting station with numbered callouts matching the BOM. The bench, input sack and sample items belong to the site and carry no number.*

The software itself has four parts, all MIT licensed:

- **Taxonomy** (`ml/data/taxonomy.yaml`): material class, then grade, aligned to resin identification codes and to common buyer grades.
- **Model**: an ImageNet-pretrained MobileNetV3-Large backbone (proposed, awaiting Amish) fine-tuned on public and field images, with a class head and a grade head. Exported as an 8-bit TensorFlow Lite model and as ONNX, attached to GitHub Releases (`ml/models/README.md`).
- **Site configuration**: a small file per site that maps grades to buyer names, bin numbers, colors and voice prompts.
- **Data manifests** (`ml/data/SOURCES.md`): each source with its license, use and consent basis. Images are referenced, not committed.

## First-order numbers

All values are estimates to be checked at TRL 3.

### Model size and speed

The TensorFlow model garden reports MobileNetV3-Large (width 1.0, 224 px input) at 5.4 million parameters and 217 million multiply-accumulates, with 73.9 % ImageNet top-1 accuracy in 8-bit form and about 44 ms per image on a Pixel 1 large core (TensorFlow Models, MobileNet README).

- **Size.** At one byte per weight, 5.4 million parameters is about 5.4 MB. The two heads add about 0.04 million parameters (a 1,280-wide feature into 7 plus about 22 outputs). The model file is about 5 to 6 MB, within R6.
- **Speed.** Assuming a low-cost 2019 or later phone is 1 to 4 times slower than a Pixel 1 large core, inference takes about 45 to 180 ms. Adding about 20 ms for crop and resize gives about 0.05 to 0.2 s, within R5 (0.3 s).
- **Fallback.** MobileNetV3-Small (2.9 million parameters, about 15 ms on a Pixel 1 in 8-bit form) is about three times faster at about 9 points lower ImageNet accuracy, a fallback for very old phones.

### Battery

- A 4,000 mAh battery at 3.85 V holds about 15.4 Wh.
- **Tap-to-scan.** 500 scans a shift at about 3 s of screen and camera each is about 25 min of active use. At about 2.5 W this is about 1.0 Wh, or about 7 % of the battery. R10 (30 % or less) is met on paper.
- **Live preview.** Running the camera preview for a full 8 h shift at 2.5 W needs about 20 Wh, more than the whole battery. R10 is not met this way, so the concept uses tap-to-scan and a power bank (item 6: about 37 Wh nominal, about 23 Wh delivered at an assumed 60 % to 65 % efficiency).

### Data needed

- **Training.** Transfer learning from ImageNet usually needs hundreds, not thousands, of images per class for a usable classifier. Assuming about 300 field images for each of about 22 grades plus extra for hard classes, the target is about 10,000 field photos, added to public sets such as TrashNet and TACO.
- **Labeling effort.** At about 20 s per photo to capture and label, plus 30 % for review, 10,000 photos take about 72 h. The field evaluation set of about 2,000 photos, with ground truth verified by a buyer, a legible resin code or an NIR reading at about 60 s each plus review, takes about 43 h.
- **Cost.** At an assumed $6 per hour for partner members (proposed, awaiting Amish), the dataset and evaluation set cost about $690, plus about $40 of cloud compute. See `bom/bom.csv`.

### Share of items answered

For the flow diagram, a dry mixed stream is assumed to give about 75 % confident answers, about 22 % "Unsure" and about 3 % hazard flags. These are placeholders; the real split comes from the field evaluation set and sets the confidence thresholds (R4).

### Value to the picker

The benefit is the price difference between a sorted grade and mixed material, times the mass that moves up a grade. No local price list has been collected yet, so no figure is claimed here. The first co-design sessions should record the buyer's price list and the mass a picker sorts per day, so the benefit can be estimated before any field trial.

### Pilot cost (reference only)

One station (items 1 to 7) is about $285 in indicative prices; a two-station pilot with dataset, evaluation set and compute is about $1,300. This repository has no hardware budget; these figures are for planning only.

## Key design choices

All choices below are proposed, awaiting Amish.

1. **Single item on a mat, not detection in a pile.** Classifying one centered item is simpler, needs image-level labels only and fits a sorting bench. Detecting many items in a pile (a TACO-style detector) is kept as a later option.
2. **Mobile classifier on the phone, not a cloud service.** Works offline, costs nothing per scan and keeps photos on the device unless the user shares them.
3. **Two heads: class, then grade.** A wrong grade within the right class costs less than a wrong class, and the class head can be trusted when the grade head is not.
4. **Abstain rather than guess.** "Unsure" is a normal answer with its own bin. It protects the picker's reputation with the buyer.
5. **Camera for shape and label; NIR for resin.** A photo sees shape, color, print and texture, which identify PET bottles, cans, cartons and cardboard well. It cannot reliably separate opaque HDPE from PP or identify black plastics. Those go to WasteWise Scan.
6. **Grades set per site in a file.** Buyers' grade names and prices differ by city.
7. **Hazards are flagged, never sorted.** The hazard class is tuned for high recall even at the cost of false alarms.
8. **Data owned with the pickers.** Field photos are collected with consent, and the pickers' organization co-owns the field dataset (proposed).

## Safety

> **Safety:** WasteWise-ml guides sorting; it does not make any item safe to handle and does not certify material. The sorting station has sharp, chemical, biological and fire hazards, and a wrong answer can put a hazardous item in the wrong place.

- **Sharps and broken glass.** Cut-resistant gloves are the norm at the station. The app must never ask the user to hold an item closer or turn it by hand for a better photo; the mat and stand let the item lie still.
- **Lithium cells.** Loose cells and devices with batteries can ignite when crushed, punctured or baled. Any battery or electronic item goes to the lidded steel hazard box with a sand layer, away from paper and film. The hazard class is tuned for high recall (R3), and a hazard result can never be overridden into a sortable grade in the app.
- **Chemical and medical waste.** Containers with residues, aerosol cans, syringes and medical waste are flagged as hazards. Disposal routes are agreed with the partner and the municipality; the app does not advise on disposal.
- **Misclassification.** The model will be wrong on some items. Grades are advice, the "Unsure" route is normal, and the buyer's check remains the final grade. The model card will publish per-class error rates.
- **Power bank and phone.** Both contain lithium cells: keep them shaded, off hot metal and away from the hazard box; do not charge a swollen or damaged pack.
- **Privacy.** Photos must not include faces or identify people; upload is opt-in; the data protocol is agreed with the partner before any collection.
- **Heat and ergonomics.** A phone in direct sun overheats and throttles; the stand should sit in shade. Bench height and bin placement should be set with the users to avoid repeated bending.

## Open questions for TRL 3

- Which backbone gives the best accuracy per millisecond on the reference phone: MobileNetV3-Large, EfficientNet-Lite0 or a small vision transformer?
- How much does the light mat help versus a handheld photo on a mixed background?
- Which grades matter most to the first buyer, and which are visible in a photo at all?
- What confidence thresholds give 70 % or more coverage while meeting R1 and R3?
- How should the app handle crushed, wet or dirty items, and labels that lie about the contents?
- Which public datasets allow training and publishing weights? Licenses must be confirmed one by one.
- How are contributors paid or credited, and who holds the field dataset?

## References

- Bashkirova, D., et al. 2022. "ZeroWaste Dataset: Towards Deformable Object Segmentation in Cluttered Scenes." *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*.
- Howard, A., et al. 2019. "Searching for MobileNetV3." *Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)*. arXiv:1905.02244.
- Kaza, S., L. Yao, P. Bhada-Tata and F. Van Woerden. 2018. *What a Waste 2.0: A Global Snapshot of Solid Waste Management to 2050.* Washington, DC: World Bank.
- Lau, W. W. Y., et al. 2020. "Evaluating Scenarios toward Zero Plastic Pollution." *Science* 369 (6510): 1455 to 1461.
- Proença, P. F., and P. Simões. 2020. "TACO: Trash Annotations in Context for Litter Detection." arXiv:2003.06975. Dataset and code: https://github.com/pedropro/TACO.
- Tan, M., and Q. V. Le. 2019. "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks." *Proceedings of the 36th International Conference on Machine Learning (ICML)*.
- TensorFlow Models. "MobileNet" README, MobileNetV3 checkpoint table. https://github.com/tensorflow/models/tree/master/research/slim/nets/mobilenet.
- Thung, G., and M. Yang. 2016. "Classification of Trash for Recyclability Status." CS 229 project report, Stanford University. Dataset: https://github.com/garythung/trashnet.
- WIEGO (Women in Informal Employment: Globalizing and Organizing). "Waste Pickers." Occupational group pages. https://www.wiego.org.
