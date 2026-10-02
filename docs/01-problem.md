---
doc_id: WML-PRB-001
title: WasteWise-ml problem statement
project: WasteWise-ml
doc_type: Problem statement
version: "0.4"
status: Draft
date: '2026-10-02'
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
  change: Populate to TRL 2 (users, context, constraints, prior work, open questions)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Apply WML-DDR-001 decisions (consent and ownership, task form, pilot phones); sources checked and linked
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: First candidate partner, city and buyers (SWaCH in Pune), as decided by Amish on 2026-10-02
---

# WasteWise-ml problem statement

Recycling streams are contaminated because people and small sorting operations cannot reliably tell materials apart, and value is lost when mixed plastics, paper, metals and organics end up together. Informal waste pickers, who handle most recycling in many low-income countries, earn more only when material is sorted by type and grade. Design with, not for: requirements must come from co-design sessions with waste pickers, their organizations and the buyers they sell to.

## The problem

Sorting quality sets the price of recovered material. A buyer pays a grade price for clean, single-material lots (for example clear PET bottles, natural HDPE, aluminum cans or baled cardboard) and much less, or nothing, for mixed or contaminated material. The person who can tell PET from PP, a multilayer pouch from a film bag, or a coated carton from plain board captures that difference. The person who cannot either sells mixed material at the lowest price or spends time and trust arguing grades with the buyer.

The scale is large. The World Bank's *What a Waste 2.0* estimates that the world generated about 2.01 billion tonnes of municipal solid waste in 2016, 242 million tonnes (12 %) of it plastic, and projects about 3.40 billion tonnes by 2050 (Kaza et al. 2018). In many low- and middle-income cities most of the material that is recycled at all is collected and sorted by informal waste pickers. A global model of plastic flows estimated that the informal sector collected about 58 % of the plastic waste collected for recycling in 2016 (Lau et al. 2020, *Science* 369: 1455 to 1461). WIEGO, the global research and policy network for informal workers, estimates that 15 to 20 million people work as informal waste pickers; in some regions, such as Latin America, they work collectively in cooperatives, and the International Alliance of Waste Pickers represents about 460,000 organized waste pickers in 34 countries (WIEGO, "Waste Pickers" occupational group page).

Three gaps keep sorting quality low:

1. **Knowledge.** Resin codes are often missing, molded illegibly or wrong. New packaging formats (multilayer pouches, coated cartons, compostable films) appear faster than informal know-how spreads. New entrants, often women and young people, learn grades slowly and on the job.
2. **Tools.** Industrial plants identify materials with near-infrared (NIR) spectroscopy, eddy-current separators and optical sorters that cost far more than a small operation can pay. The only tool most pickers carry is a phone.
3. **Data.** Public waste-image datasets are small or taken in clean conditions. TrashNet, a widely used benchmark, has 2,527 photos in six classes, each item shot on a white posterboard (Thung and Yang 2016, TrashNet repository). TACO has litter photographed in the wild, labeled for detection in COCO format, but it is sized and labeled for litter, not for buyer grades (Proença and Simões 2020, arXiv:2003.06975). Neither maps to the grades a local buyer pays for.

WasteWise-ml is an open image-classification model that runs offline on a low-cost phone and tells the user an item's material class and local grade, with a confidence value, and says "unsure" when it does not know. It is the software core of the WasteWise family: WasteWise Scan adds a handheld NIR reading for plastic resin type, and ReflowEconomy micro-factories buy the sorted output.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Informal waste picker | Sort faster and to a higher grade, sell at a better price, learn new packaging types | Street, dump site or depot; hands full; gloves; bright sun or dim shed; shared or low-cost Android phone |
| Waste picker cooperative or depot operator | Consistent grades across members, fewer disputes with buyers, training for new members | Sorting benches or floor sorting; weighing and sale records; some members with limited literacy |
| Scrap buyer or aggregator | Fewer rejected lots, clear grade names, quicker weighing and pricing | Buys by grade and weight; sets the price list that the grades must match |
| ReflowEconomy micro-factory | Clean feedstock of one resin, for washing, shredding and remanufacture | Downstream customer; defines what "clean PET, HDPE, PP" means locally |
| Researchers and NGOs | An open model, dataset licenses and evaluation that they can inspect and extend | Universities, city programs, open-source contributors |

### Operating environment

- **Stream:** dry mixed recyclables, often dirty, crushed, wet, labeled or partly burned; organics and hazardous items mixed in.
- **Lighting:** direct sun to dim indoor light; glare from film and metal.
- **Devices:** Android phones in the low-cost class (estimate: 2 to 4 GB RAM, 2019 or later chipset), often shared, with limited data plans and intermittent network.
- **People:** multilingual users, a range of literacy, gloved hands, and work paid by weight so every second counts.
- **Hazards at the station:** sharps, broken glass, lithium cells, chemical containers and biological contamination (see the safety section in WML-PRC-001).

## Constraints

- Runs on phones users already own or that cost about $100 to $150; no special camera.
- Works offline; no paid cloud service is needed at the point of use.
- Open: code and model weights under MIT; every dataset's license recorded in `ml/data/SOURCES.md`; only data whose license allows training and publishing weights.
- Grades follow the local buyer's price list, which differs by city, so grade names are configurable per site without retraining the model where possible.
- Photos taken in the field are collected only with informed consent, contain no faces, are uploaded only on opt-in and are co-owned by the pickers' organization (decided by Amish, 2026-09-25, WML-DDR-001 D6). Labelers are paid at or above the local living wage, with the rate set with the partner (D7).
- The model advises; it never certifies material and never auto-sorts hazardous items.
- This repository is software and a playbook for data; it has no hardware budget (`budget_usd` is null). A pilot kit is costed in `bom/bom.csv` for reference only.

## Out of scope

- Robotic or conveyor sorting systems.
- Resin identification by spectroscopy (that is WasteWise Scan).
- Recycling processes after sale (that is ReflowEconomy).
- Price setting, payments or a marketplace app.
- Certifying food-contact suitability, chemical content or hazardous-waste status of any item.

## Prior work

- **Public waste-image datasets.** TrashNet (Thung and Yang 2016; 2,527 images, six classes: glass, paper, cardboard, plastic, metal and trash; about 75 % test accuracy reported by its authors for their network) and TACO (Proença and Simões 2020; litter in the wild with segmentation labels) are the most used. ZeroWaste (Bashkirova et al. 2022, CVPR) adds images from a materials recovery facility conveyor. None is organized by buyer grade or by resin code, and most are photographed in conditions unlike a picker's sorting bench.
- **Mobile vision models.** MobileNetV3 (Howard et al. 2019) and EfficientNet (Tan and Le 2019) are designed for phones. The TensorFlow model garden reports MobileNetV3-Large at 5.4 million parameters, 217 million multiply-accumulates and 73.9 % ImageNet top-1 accuracy in 8-bit form, running in about 44 ms on a Pixel 1 phone's large core (TensorFlow Models, MobileNet README).
- **Industrial sorting.** NIR optical sorters in materials recovery facilities identify resin type at belt speed. They show what spectroscopy can do, but their cost and scale do not fit a street or depot. WasteWise Scan takes the same principle to a handheld device.
- **Waste picker organizations.** Cooperatives and associations supported by networks such as WIEGO already run training, collective sales and weighing records. They are the natural partners for co-design, data collection and ownership.

Named sources are listed in WML-PRC-001, section "References". The World Bank, Lau et al., WIEGO, TrashNet, TACO, ZeroWaste, MobileNetV3 and EfficientNet citations were checked on the web on 2026-09-25.

## Open questions

- Which partner organization, city and buyers first? Decided by Amish on 2026-10-02: a member-owned waste picker cooperative that already sorts dry waste for scrap buyers; SWaCH in Pune, India, is the first candidate to approach, with its scrap dealers as the buyers (WML-DEC-001).
- Which grades change the price most at the first site, and are they visible in a photo at all?
- How do pickers want the answer shown: icon and color, voice, local language text, or a mix?
- Who owns field photos and the resulting model, and how are contributors credited or paid?
- The design classifies one item at a time on a mat under a phone on a stand, with handheld use supported (decided, D1). Does that fit the partner's floor and street sorting, or will pile detection be needed later?

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design
