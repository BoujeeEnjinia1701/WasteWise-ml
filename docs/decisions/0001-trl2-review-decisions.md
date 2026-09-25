---
doc_id: WML-DDR-001
title: WasteWise-ml TRL 2 review decisions
project: WasteWise-ml
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: MIT
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's 2026-09-25 decisions on the TRL 2 review points
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted (items D1 to D8); items O1 to O3 remain proposed; items N1 to N3 are new proposals raised at TRL 3

## Context

The TRL 2 review note (`docs/REVIEW.md`, session of 2026-09-25, "/populate to a strong TRL 2") listed ten items marked "Proposed, awaiting Amish". On 2026-09-25 Amish reviewed the review points for every repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." Every item that carried a recommendation is therefore decided as recommended. Items without a recommendation stay open.

## Options considered

Table 1. Items with a recommendation.

| # | Item | Options | Recommendation |
| --- | --- | --- | --- |
| D1 | Task form | A: single item on a mat, image classification; B: multi-item detection in a pile | A for TRL 3; B as a later extension |
| D2 | Backbone and runtime | MobileNetV3-Large, EfficientNet-Lite0 or a small vision transformer; TensorFlow Lite, ONNX | MobileNetV3-Large; TensorFlow Lite as the main export, ONNX as a second export |
| D3 | Taxonomy changes | Add or leave out the `composite` class and the `unsure` and `hazard` outputs | Keep them |
| D4 | Grade mapping | Per-site configuration file; site-specific models | Configuration file per site |
| D5 | Scan mode | Tap-to-scan; live camera preview | Tap-to-scan, for battery life |
| D6 | Data ownership and consent | Field data co-owned by the pickers' organization, opt-in upload, no faces; project-owned data | Co-owned, opt-in, no faces, written into a protocol with the partner before any collection |
| D7 | Pay rate for labeling | Fixed planning rate; rate set with the partner | Set with the partner at or above the local living wage |
| D8 | Pilot phones | Reference phone per station; pickers' own phones | One reference phone per station for the evaluation; support own phones in use |

## Decision

- **D1.** Decided by Amish, 2026-09-25: go with recommendation. WasteWise-ml classifies one item at a time on a light mat under a phone on a stand (handheld use also supported). Pile detection is a later extension, not part of this design.
- **D2.** Decided by Amish, 2026-09-25: go with recommendation. MobileNetV3-Large backbone with a class head and a grade head; 8-bit TensorFlow Lite as the main export and ONNX as a second export. EfficientNet-Lite0 stays a comparison candidate for later work.
- **D3.** Decided by Amish, 2026-09-25: go with recommendation. `ml/data/taxonomy.yaml` keeps the `composite` class and the `unsure` and `hazard` outputs.
- **D4.** Decided by Amish, 2026-09-25: go with recommendation. Buyer grade names, bin numbers, colors and voice prompts are set per site in a configuration file.
- **D5.** Decided by Amish, 2026-09-25: go with recommendation. The app uses tap-to-scan; the camera does not run between scans. WML-CAL-001 adds that the screen must also sleep between scans to meet R10 without the power bank.
- **D6.** Decided by Amish, 2026-09-25: go with recommendation. Field photos are collected only with informed consent, contain no faces, are uploaded only on opt-in, and are co-owned by the pickers' organization. The protocol is written with the partner before any collection.
- **D7.** Decided by Amish, 2026-09-25: go with recommendation. The labeling pay rate is set with the partner at or above the local living wage. The $6 per hour in `bom/bom.csv` remains a planning figure only.
- **D8.** Decided by Amish, 2026-09-25: go with recommendation. Each pilot station gets one reference phone (BOM line 1) for the evaluation; pickers' own phones are supported in use.

Budget and pitch: this is a software repository, licensed MIT only, and `budget_usd` stays null. The TRL 2 review recommended no pitch or problem change ("Pitch. Unchanged."), so the pitch and problem lines in `project.yaml` and `README.md` are unchanged. The kit's blueprint sheet label stays overridden to MIT for this repository.

Items that remain open (no recommendation was made, so they stay "Proposed, awaiting Amish"):

- **O1.** First partner organization, city and buyers for co-design and the field set. No recommendation; portfolio guidance is that community designs pick co-design partners per area later. Proposed, awaiting Amish.
- **O2.** `CONTRIBUTING.md` still says hardware contributions are under CERN-OHL-S v2, although this repository is MIT only. The review noted that Amish may want to remove the line but made no recommendation. Proposed, awaiting Amish.
- **O3.** A kit option for software repositories so that drawing sheets default to MIT (the review suggested it; it changes `.kit/`, which this repository does not own). Proposed, awaiting Amish.

New items raised at TRL 3 (not part of the 2026-09-25 decision):

- **N1.** Hazard evaluation size (R3). WML-CAL-001 shows that 200 hazard items prove 98 % recall only if the model misses none. Options: keep 200; raise to 400 (proves 98 % at 95 % confidence with up to 3 misses, an 80 % chance of passing if true recall is 99.5 %); raise to about 1,000 (80 % chance of passing if true recall is 99.0 %). Recommendation: 400, collected by targeted sampling. Proposed, awaiting Amish.
- **N2.** ZeroWaste is licensed CC BY-NC 4.0, which does not fit MIT model weights. Options: exclude it from training and use it only for non-commercial research comparisons; exclude it entirely; ask the authors for other terms. Recommendation: exclude it from training. Proposed, awaiting Amish.
- **N3.** Camera height. The TRL 2 concept put the phone about 470 mm above the mat; at that height a typical 26 mm-equivalent phone camera sees about 626 x 469 mm, wider than the 450 mm mat. Options: lower the lens to 440 mm (frame 586 x 439 mm, used in the model); keep 470 mm and widen the mat to 500 mm. Recommendation: 440 mm. Proposed, awaiting Amish.

## Consequences

- WML-PRB-001, WML-PRC-001 and WML-REQ-001 move to version 0.3 and state D1 to D8 as decisions rather than proposals.
- WML-CAL-001 sizes the dataset, model, energy and evaluation on these decisions.
- The build123d station model (`cad/src/model.py`) and drawing WML-DWG-001 use the 440 mm lens height of N3 pending Amish's decision; changing it is one parameter.
- Nothing here starts TRL 4 work: no training, data collection, app code or field trial.
