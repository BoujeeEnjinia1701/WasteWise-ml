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
9. **First partner, city and buyers** for co-design and the field set.
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
