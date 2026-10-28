---
doc_id: WML-MKT-001
title: WasteWise-ml market and viability
project: WasteWise-ml
doc_type: Market and viability
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: MIT
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: First market and viability note (kit 1.8 upgrade)
---

# WasteWise-ml market and viability

WasteWise-ml is for waste picker cooperatives and the people in them, who sort by hand and earn by grade, with nothing between their own judgment and a plastics identifier that costs about EUR 4,930. It competes on being free software on a phone users already own, at about USD 183 for the rest of a station, and it is open so the cooperatives that co-own its data can keep and change it. Prices and benchmarks are cited with the date they were checked. Method: STANDARDS section 23.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Waste picker cooperatives and depots | Member-owned cooperatives that sort dry waste for scrap dealers; first candidate SWaCH, Pune, India | Handheld NIR plastic identifier: Matoha PlasTell Handheld, EUR 4,930 (filament2print, checked 2026-10-25); identifies resin, not buyer grade or non-plastics | 313.39 a station with a USD 130 reference phone; about 183 with members' own phones (BOM lines 2 to 7, 11, 12) | Class, local grade and hazard flag on a phone, offline; "Unsure" rather than a guess; grade names set by the cooperative |
| Individual waste pickers | Pickers in the street or at depots who already carry a low-cost Android phone | Low-cost phone of the class: Redmi A5, 3 GB and 64 GB, INR 6,499 at launch (The Statesman, 2025-04-17; checked 2026-10-25) | 0 for the app on their own phone (handheld use) | Learn new packaging and grades; fewer disputes with buyers |
| Municipal drop-off points and material recovery facilities | Hand-sorting lines and drop-off staff in Indian cities | Industrial NIR sorters (price not published; hundreds of thousands of dollars per WasteWise Scan WSC-PRB-001, an estimate) | 313.39 a station | A quality check on hand-sorted lines and a battery flag before baling |
| Schools, campuses and events | Teaching which bin an item belongs in | No paid benchmark checked | 0 to 183 | Teaching tool with the "Unsure" route shown openly |
| Researchers and NGOs | Universities and programs extending the model to new regions | Public datasets, free (TrashNet MIT; TACO CC BY 4.0 annotations) | Labeling effort: USD 690 for the dataset and evaluation set at the planning rate | Open model, taxonomy, evaluation method and consent protocol to reuse |

Option B, the tray detector, would cost about USD 419 a station without a phone, from a Raspberry Pi 5 4 GB at USD 100 (after the February 2026 rise, OMG! Ubuntu, 2026-02-02), a Camera Module 3 Wide at USD 35.95 and a 5 inch Touch Display 2 at USD 54.95 (PiShop.us, checked 2026-10-25), plus estimates (WML-CAL-001 section 15). The reference phone of option A, priced at USD 130 in the BOM as an indicative figure, sits above the Redmi A5's launch price, so a cheaper qualifying phone may exist; the price is confirmed when the phone is bought (WML-DEC-001 confirm item 1).

The benefit to a picker is the price difference between a sorted grade and mixed material, times the mass moved up a grade. No local price list has been collected yet, so no figure is claimed; the first co-design sessions should record the buyer's price list and the mass a picker sorts a day.

## Open route

- **Who builds it.** The cooperative's own members or a local workshop build the stand from the build plan (saw, drill, files); every other station item is bought locally. The app installs on members' phones.
- **How it spreads.** Through waste picker networks (WIEGO and the International Alliance of Waste Pickers), the Helpful Engineering volunteer network, universities and city programs; a new city needs a new grade file, not a new model, unless it pays for a grade the model cannot see.
- **What keeps it open.** Code and weights are MIT; every dataset license is recorded; field data is co-owned by the pickers' organization (D6); the evaluation method and model card are published with every release. No paid cloud service is needed at the point of use.
- **Non-commercial by intent.** The project sells nothing; any income from sorted material stays with the pickers.

## Sources

- filament2print. "Identificador de Plásticos Matoha PlasTell" (PlasTell Handheld EUR 4,930.00). https://filament2print.com/es/fabricacion-filamentos/4664-identificador-plasticos-matoha-plastell.html. Checked 2026-10-25.
- OMG! Ubuntu. "Raspberry Pi Announce More Price Rises." 2026-02-02. https://www.omgubuntu.co.uk/2026/02/raspberry-pi-annouce-more-price-rises. Checked 2026-10-25.
- PiShop.us. Raspberry Pi category, page 2. https://www.pishop.us/raspberry-pi-foundation/?page=2. Checked 2026-10-25.
- The Statesman. "Xiaomi Launches Redmi A5 in India, Price Starts at Rs 6,499." 2025-04-17. https://www.thestatesman.com/technology/xiaomi-launches-redmi-a5-in-india-price-starts-at-rs-6499-1503421119.html. Checked 2026-10-25.
- WasteWise Scan, WSC-PRB-001 (industrial NIR sorter cost, an estimate there).
- BOM `bom/bom.csv` and WML-CAL-001 sections 10 and 15 for every cost of this design.
