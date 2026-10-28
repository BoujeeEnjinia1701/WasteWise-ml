---
doc_id: WML-URS-001
title: WasteWise-ml user requirements
project: WasteWise-ml
doc_type: User requirements
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: MIT
revisions:
  - version: "0.1"
    date: '2026-10-25'
    author: Amish Chadha
    change: First user requirements (kit 1.8 upgrade), drawn from the users and stakeholders in WML-PRB-001 v0.5
---

# WasteWise-ml user requirements

What users need, written from their side. Product requirements that meet these needs are in WML-PRS-001 (`03-requirements.md`) and the links are in the traceability matrix WML-RTM-001 (`03b-traceability.md`). The needs are drawn from the users and stakeholders in WML-PRB-001 Tables 1 and 2; none has yet been confirmed in a co-design session with the first candidate partner (SWaCH, Pune, decided 2026-10-02), so every priority is a proposal. Method: STANDARDS section 22.

Table 1. User requirements.

| ID | Category | Title | Need | Priority | Source |
| --- | --- | --- | --- | --- | --- |
| UR-001 | Performance | Right material class | When I show an item, I am told its material class correctly almost every time it gives an answer | High | Informal waste picker; cooperative operator (PRB Table 1) |
| UR-002 | Performance | Buyer's grade | For plastics and other graded material, I am told the grade my buyer pays for, where a photo can tell it | High | Waste picker; scrap buyer (PRB Table 1) |
| UR-003 | Safety | Hazards flagged | Batteries, sharps and chemical containers are flagged as hazards and never offered as something to sort, and the station does not add a fire or cut risk | High | Waste picker; cooperative; municipality (PRB Tables 1 and 2) |
| UR-004 | Performance | Honest unsure | When it is not sure it says so rather than guessing, and it still answers most items | High | Waste picker; scrap buyer (PRB Table 1) |
| UR-005 | Performance | Fast | The answer comes quickly enough not to slow work that is paid by weight | High | Waste picker (PRB operating environment) |
| UR-006 | Usability | No reading needed | I can use it without reading, in my own language, after a short briefing, and see or hear the answer from where I stand | High | Waste picker; cooperative (PRB Table 1, literacy) |
| UR-007 | Usability | Hands free, no stretching | My hands stay free, the item lies still, and I can trigger a scan without reaching up or leaning in | High | Waste picker in gloves (PRB operating environment) |
| UR-008 | Logistics | My own phone, offline | It runs on a phone I own or one costing about USD 150, with no network and a small download | High | Waste picker; cooperative (PRB constraints) |
| UR-009 | Performance | Lasts a shift | The phone lasts a full shift of scanning | Medium | Waste picker (PRB operating environment) |
| UR-010 | Usability | Our grade names | Grade names and bin numbers match our buyer's price list, and the cooperative can change them | High | Cooperative; scrap buyer (PRB Table 1) |
| UR-011 | Regulatory | Our data, our consent | Photos are taken only with consent, show no faces, are uploaded only if we agree, and the field data is co-owned by our organization | High | Cooperative; waste pickers (PRB constraints, D6) |
| UR-012 | Regulatory | Open and licensed | Code, model weights and dataset licenses are open and checked, so others can inspect and extend them | Medium | Researchers and NGOs (PRB Table 1) |
| UR-013 | Performance | Proven on real waste | The accuracy is shown on real field photos from our kind of site before we rely on it | Medium | Scrap buyer; researchers; cooperative (PRB Table 2) |
| UR-014 | Deployment and assembly | Build it locally | The station can be built from local parts with hand tools and sits on a bench we already have | Medium | Cooperative operator (PRB Table 1) |
| UR-015 | Environment and durability | Works in our shed | The station copes with wet and dirty items, heat and dust in a sorting shed | Medium | Cooperative operator (PRB operating environment) |
| UR-016 | Cost | Low cost | The station costs little enough for a cooperative to buy or build | Medium | Cooperative; NGOs (PRB constraints) |
| UR-017 | Maintenance | Easy to keep going | The phone lifts out to charge or swap, and parts can be replaced locally | Low | Cooperative operator (PRB Table 1) |

Categories: deployment and assembly, performance, usability, safety, environment and durability, logistics, maintenance, cost, regulatory. Priorities: High, Medium, Low.
