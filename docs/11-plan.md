---
doc_id: WML-PLN-001
title: WasteWise-ml project plan
project: WasteWise-ml
doc_type: Project plan
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: MIT
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: First project plan (kit 1.8 and 1.9.1 upgrade), stage P3 reached; P4 to P6 on hold
---

# WasteWise-ml project plan

WasteWise-ml is at TRL 3, stage P3 (design outputs): the model is sized, the scanning rig is constructable and detailed to D3, and the pipeline documents exist. The next gate is P4 (verification), which needs a field partner, field photos and the evaluation set, and is on hold while the portfolio cap is TRL 3 and stage P3. **Decisions requested of Amish:** the concept selection D1 (option A recommended, WML-DDR-004) and the lens height D2 (420 mm recommended, WML-DEC-001). Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Requirements and pipeline | Project lead | PRB, STM, OPT, URS, PRS, RTM, REG, FEA, RSK, MKT, PLN | Done at P3 (2026-10-25); STEM check open on eight rows (S2, M2, M4, M5, B2, C3, E4, OB5) |
| Scanning rig | Design lead | Model at D3, drawing WML-DWG-001 Rev P3, making sketches WML-DWG-101 to 107, build plan WML-BLD-001 | Done on paper; arm and tray wait for the bought phone (confirm items 1 and 2) |
| Model and app | ML lead | Taxonomy, model card template, per-site grade file, app result screen and voice (F1) | Taxonomy done; app and training not started (TRL 4) |
| Data and consent | Data lead with the partner | Data protocol, consent form, labeling plan, 10,000 field photos, 2,000-image evaluation set | Not started (TRL 4, on hold) |
| Partner and co-design | Project lead | Agreement with the first candidate partner (SWaCH, Pune), co-design sessions, buyers' grade list | Not started (on hold) |
| Photoreal renders | Coordinator (Amish's Mac) | `media/options.png`, product renders from `cad/src/product_model.py`, cards | Scenes ready; renders pending |

## Resources needed

Table 2. Resources (planning figures from the BOM and WML-CAL-001; the labeling rate is set with the partner, D7).

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Partner members, labeling | 10,000 labeled field photos | About 72 h | 430 (BOM line 8) |
| Partner members and buyers, ground truth | 2,000-image evaluation set with 400 hazards | About 43 h | 260 (BOM line 9) |
| Cloud GPU | Fine-tuning and evaluation | About 40 GPU hours | 40 (BOM line 10) |
| Two pilot stations | Hardware for two sites | About a day's workshop time each | 626.78 (2 x 313.39) |
| App developer | Android app: capture, result screen, voice, shutter button, grade file, consent and upload queue | To estimate | To assess |
| Regulatory reviewer | DPDP protocol review, legal metrology, battery and bio-medical waste routes (REG G2 to G6) | To estimate | To assess |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | PRB with users and stakeholders, STM, OPT, REG, FEA, PLN | Done (2026-10-25) |
| P1 Definition | URS, PRS draft, RSK with hazard analysis, MKT, REG complete | Done (2026-10-25) |
| P2 Design inputs | PRS with targets and verification, CAL, RTM, concept selection DDR, STEM check closed, FEA closed | Done except the STEM check (eight rows open: field data, trials on bought parts, and D2) and the concept choice (D1, awaiting Amish) |
| P3 Design outputs | Model at D3, STEP, drawings, priced BOM, build plan, DEC, design FMEA, traceability complete | Done (2026-10-25) |
| P4 Verification | Field evaluation report (PR-001 to PR-004, PR-011), timed and usability trials (PR-007, PR-008, PR-016, PR-022), rig first checks | On hold (TRL 4) |
| P5 Validation | Pilot with the partner at two sites; consent protocol in use | On hold |
| P6 Commercialization | Not planned: an open, non-commercial route (WML-MKT-001) | On hold |

## Next steps and decision requested

1. **Amish:** decide the concept selection D1 (option A, the current design, recommended; WML-DDR-004) and the lens height D2 (420 mm recommended; WML-DEC-001).
2. Coordinator: render `media/options.png` and the product renders named in `cad/src/product_model.py` on the Mac.
3. When TRL 4 is opened: approach SWaCH, write the data protocol with them, buy and measure the reference phone and shutter button (confirm items 1, 2 and 5), then build one rig to WML-BLD-001.
4. Measure the learning curve on the first 2,000 field photos before collecting the rest (closes STEM M4 and M5 or changes the plan).

## References

Every source cited in this repository's documents, Chicago style.

- AZB and Partners. 2025. "India's Digital Personal Data Protection Act: Phased Rollout and Key Compliance Milestones." November 14. https://www.azbpartners.com/bank/indias-digital-personal-data-protection-act-phased-rollout-and-key-compliance-milestones/.
- Bashkirova, D., et al. 2022. "ZeroWaste Dataset: Towards Deformable Object Segmentation in Cluttered Scenes." *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition.* arXiv:2106.02740.
- Battery University. "BU-410: Charging at High and Low Temperatures." https://batteryuniversity.com/article/charging-at-high-and-low-temperatures.
- Department of Weights and Measures, Government of NCT of Delhi. "FAQs." https://weightnmeasures.delhi.gov.in/faqs.
- Drillis, R., and R. Contini. 1966. *Body Segment Parameters.* Technical Report 1166-03. New York: New York University.
- Eurostat. "Packaging Waste Statistics." https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Packaging_waste_statistics.
- filament2print. "Identificador de Plásticos Matoha PlasTell." https://filament2print.com/es/fabricacion-filamentos/4664-identificador-plasticos-matoha-plastell.html.
- Free Press Journal. 2024. "Pune: City To Hit 40 Degrees Celsius On April 1." March 30. https://www.freepressjournal.in/pune/pune-city-to-hit-40-degree-celsius-on-april-1.
- Hestness, J., et al. 2017. "Deep Learning Scaling is Predictable, Empirically." arXiv:1712.00409.
- Howard, A., et al. 2019. "Searching for MobileNetV3." *Proceedings of the IEEE/CVF International Conference on Computer Vision.* arXiv:1905.02244.
- Insights IAS. 2026. "Solid Waste Management (SWM) Rules, 2026." January 29. https://www.insightsonindia.com/2026/01/29/solid-waste-management-swm-rules-2026/.
- ISO 11226:2000. *Ergonomics: Evaluation of Static Working Postures.* Geneva: International Organization for Standardization.
- ISO 9241-303:2011. *Ergonomics of Human-System Interaction, Part 303: Requirements for Electronic Visual Displays.* Geneva: International Organization for Standardization.
- Kaza, S., L. Yao, P. Bhada-Tata and F. Van Woerden. 2018. *What a Waste 2.0: A Global Snapshot of Solid Waste Management to 2050.* Washington, DC: World Bank. https://openknowledge.worldbank.org/handle/10986/30317.
- Lau, W. W. Y., et al. 2020. "Evaluating Scenarios toward Zero Plastic Pollution." *Science* 369 (6510): 1455 to 1461. https://doi.org/10.1126/science.aba9475.
- Mitchell, M., et al. 2019. "Model Cards for Model Reporting." *Proceedings of the Conference on Fairness, Accountability, and Transparency.* arXiv:1810.03993.
- Moelven. *Hardboard H1, Betanzos.* Product data sheet. https://www.moelven.com/globalassets/inriver/documents/produktdatablad---hardboard-h1---betanzos.pdf.
- Nag, A., P. K. Nag and H. Desai. 2003. "Hand Anthropometry of Indian Women." *Indian Journal of Medical Research* 117: 260 to 269.
- NEEWER. "RT116 Wireless Bluetooth Remote Shutter Release." https://neewer.com/products/neewer-rt116-wireless-bluetooth-remote-shutter-release-66607555.
- Neo, E. R. K., et al. 2022. Review of near-infrared spectroscopy for plastic sorting. *Resources, Conservation and Recycling* 180: 106217. https://doi.org/10.1016/j.resconrec.2022.106217.
- OMG! Ubuntu. 2026. "Raspberry Pi Announce More Price Rises." February 2. https://www.omgubuntu.co.uk/2026/02/raspberry-pi-annouce-more-price-rises.
- Papadopoulos, D. P., J. R. R. Uijlings, F. Keller and V. Ferrari. 2017. "Extreme Clicking for Efficient Object Annotation." *Proceedings of the IEEE International Conference on Computer Vision.* arXiv:1708.02750.
- PiShop.us. "Raspberry Pi Foundation," page 2. https://www.pishop.us/raspberry-pi-foundation/?page=2.
- Proença, P. F., and P. Simões. 2020. "TACO: Trash Annotations in Context for Litter Detection." arXiv:2003.06975.
- Tan, M., and Q. V. Le. 2019. "EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks." *Proceedings of the 36th International Conference on Machine Learning*, PMLR 97: 6105 to 6114.
- TensorFlow Models. "MobileNet" README. https://github.com/tensorflow/models/tree/master/research/slim/nets/mobilenet.
- The Statesman. 2025. "Xiaomi Launches Redmi A5 in India, Price Starts at Rs 6,499." April 17. https://www.thestatesman.com/technology/xiaomi-launches-redmi-a5-in-india-price-starts-at-rs-6499-1503421119.html.
- Thung, G., and M. Yang. 2016. "Classification of Trash for Recyclability Status." CS 229 project report, Stanford University. https://github.com/garythung/trashnet.
- UCLA Environment, Health and Safety. "Battery Safety." https://ehs.ucla.edu/news/battery-safety.
- Ultralytics. "YOLOv8." https://docs.ultralytics.com/models/yolov8/.
- US Environmental Protection Agency. "National Overview: Facts and Figures on Materials, Wastes and Recycling." https://www.epa.gov/facts-and-figures-about-materials-waste-and-recycling/national-overview-facts-and-figures-materials.
- Walmart. "Mini Wireless Bluetooth Remote Shutter Controller Button." https://www.walmart.com/ip/Mini-Wireless-Bluetooth-Remote-Shutter-Controller-Button-Self-Timer-Camera-Stick-Shutter-F5G3/1435880459.
- WIEGO. "Waste Pickers." https://www.wiego.org/informal-economy/occupational-groups/waste-pickers/.
- Winter, D. A. 2009. *Biomechanics and Motor Control of Human Movement.* 4th ed. Hoboken, NJ: Wiley.
- World Bank. *What a Waste 3.0.* https://www.worldbank.org/en/publication/what-a-waste.
- WRAP. "Recyclability of Black Plastic Packaging." Cited through WasteWise Scan WSC-PRB-001.
