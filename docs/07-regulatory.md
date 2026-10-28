---
doc_id: WML-REG-001
title: WasteWise-ml regulatory and standards register
project: WasteWise-ml
doc_type: Regulatory and standards register
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: MIT
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: First regulatory and standards register (kit 1.8 upgrade), for a first pilot with a waste picker cooperative in Pune, India
---

# WasteWise-ml regulatory and standards register

Which standards and regulations apply, where, and what is needed, for a first pilot in Pune, India (first candidate partner SWaCH, decided 2026-10-02). WasteWise-ml is software and a sorting station built from bought items and a small made stand; it advises and never certifies material, so most rules apply to the site and the partner rather than to the product. Not legal advice; anything marked "to assess" needs a qualified reviewer before any product claim. Rules marked "not checked in this session" are named from general knowledge and are to be read and cited before they are relied on. Method: STANDARDS section 23.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | Solid Waste Management Rules, 2026 (supersede the 2016 rules; in full effect from 2026-04-01) | India | Segregation at source into wet, dry, sanitary and special care waste; dry recyclables to material recovery facilities | The station sorts dry recyclables; batteries, paint cans and similar items are special care waste that goes to designated collection points, which matches the hazard route | Partner (site operator) | Applies (site); to assess how the rules recognise and integrate waste pickers |
| G2 | Digital Personal Data Protection Act, 2023, and Digital Personal Data Protection Rules, 2025 (notified 2025-11-13; notice and consent duties apply 18 months after notification, from about 2027-05-12) | India | Notice, consent and duties of data fiduciaries for digital personal data | Field photos are taken with consent, keep no faces and are uploaded only on opt-in (D6, PR-014); a photo of a hand or a voice prompt record could still be personal data | Data lead with the partner | To assess (met by design in principle; protocol to be written with the partner and reviewed) |
| G3 | Legal Metrology Act, 2009, and state enforcement rules | India | Weights and measures used in any transaction must be verified and stamped; electronic and platform scales are re-verified every year | The platform scale (BOM line 7) weighs sorted lots for sale | Partner (site operator) | Applies: buy a verified and stamped scale and re-verify it yearly (BOM line 7 specification) |
| G4 | Battery Waste Management Rules, 2022 | India | Collection and handling of waste batteries | Cells and battery-powered items go to the hazard box, then to a collection route the partner and municipality agree | Partner; municipality | To assess (not checked in this session) |
| G5 | E-Waste (Management) Rules, 2022 | India | Electrical and electronic waste | Devices with batteries found in the stream; end-of-life phones and power banks of the station | Partner | To assess (not checked in this session) |
| G6 | Bio-Medical Waste Management Rules, 2016 | India | Sharps and medical waste | Syringes and other medical waste found in the stream go to the sharps container; the app flags them, never sorts them | Partner; municipality | To assess (not checked in this session) |
| G7 | Plastic Waste Management Rules, 2016, as amended (extended producer responsibility) | India | Producers' obligations and recycler registration | Context for the buyers of sorted plastics; no obligation on the app | Partner; buyers | Does not apply to the design; to assess as market context (not checked in this session) |
| G8 | BIS Compulsory Registration Scheme for electronics | India | Safety registration of listed electronic products sold in India | The bought phone, power bank and shutter button | Procurement (partner) | To assess: buy registered products where the category is listed (scheme page https://www.bis.gov.in/product-certification/products-under-compulsory-certification/scheme-ii-registration-scheme, not read in this session) |
| G9 | Radio equipment approval for the Bluetooth shutter button | India | Approval of short-range radio devices | BOM line 12 | Procurement | To assess (not checked in this session) |
| G10 | Dataset licenses: TrashNet (MIT), TACO (annotations CC BY 4.0, images per image), ZeroWaste (CC BY-NC 4.0) | International | Use of third-party images for training and publishing weights | ZeroWaste excluded from training (N2, decided); TACO filtered image by image (PR-013) | Data lead | Applies; at risk until the TACO image check is done |
| G11 | Model cards for model reporting (Mitchell et al. 2019, practice) | International | Published per-class results, intended use and known failure modes | Required by PR-013 | ML lead | Met by design (planned with the first released weights) |
| G12 | ISO 11226:2000 (static working postures) and ISO 9241-303:2011 (display legibility) | International | Upper arm elevation screen; minimum character height | Used as screens in WML-CAL-001 section 12 (fix F1) | Design lead | Met on paper (standards not purchased; values to confirm against the texts) |
| G13 | Resin identification codes (ASTM D7611) | International | The numbered marks on plastic items | Read by the camera where legible; ground truth for PR-002 | ML lead | Applies (reference; cited through WasteWise Scan) |
| G14 | EU Artificial Intelligence Act | European Union | Obligations by risk class of an AI system | Only if the app is deployed in the EU; not for the Pune pilot | Project lead | Does not apply to the pilot; risk class to assess before any EU use |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

- AZB and Partners. "India's Digital Personal Data Protection Act: Phased Rollout and Key Compliance Milestones." 2025-11-14 (DPDP Rules notified 2025-11-13; consent obligations after 18 months, about 2027-05-12). https://www.azbpartners.com/bank/indias-digital-personal-data-protection-act-phased-rollout-and-key-compliance-milestones/. Checked 2026-10-25.
- Department of Weights and Measures, Government of NCT of Delhi. Frequently asked questions (verification and stamping; re-verification intervals). https://weightnmeasures.delhi.gov.in/faqs. Checked 2026-10-25. Legal Metrology Act, 2009: https://www.indiacode.nic.in/bitstream/123456789/6927/1/legal_metrology_act_2009.pdf (not read in this session).
- Insights IAS. "Solid Waste Management (SWM) Rules, 2026." 2026-01-29 (from PIB; in full effect from 2026-04-01; four segregation streams). https://www.insightsonindia.com/2026/01/29/solid-waste-management-swm-rules-2026/. Checked 2026-10-25.
- Mitchell, M., et al. 2019. "Model Cards for Model Reporting." *Proceedings of FAT\* 2019*. arXiv:1810.03993.
- Dataset licenses as recorded in `ml/data/SOURCES.md` and WML-CAL-001 section 16 (checked 2026-09-25).
- ASTM D7611 as cited in WasteWise Scan WSC-PRB-001.
