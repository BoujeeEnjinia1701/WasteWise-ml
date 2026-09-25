# WasteWise-ml

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![License: MIT](https://img.shields.io/badge/license-MIT-111827)

**Area:** Circular Materials · **TRL:** 3 of 9 (proof of concept on paper)

Open image-classification model that identifies waste items by material class and grade from a phone or low-cost camera. It is the software brain of the WasteWise family: WasteWise Scan adds near-infrared sensing for plastic resin type, and ReflowEconomy uses the sorted output.

![WasteWise-ml concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Problem

Recycling streams are contaminated because people and small sorting operations cannot reliably tell materials apart, and value is lost when mixed plastics, paper, metals and organics end up together. Informal waste pickers, who handle most recycling in many low-income countries, earn more only when material is sorted by type and grade.

## Concept

The user photographs one item on a light mat with a low-cost Android phone. An on-device model (MobileNetV3-Large, about 4.4 MB in 8-bit form) answers offline in 64 to 201 ms on a low-cost phone (calculated, WML-CAL-001) with the material class, the local buyer grade and a confidence value, or says "Unsure" or "Hazard". Sorted lots go to bins that match the buyer's price list; unsure plastics go to WasteWise Scan for a near-infrared resin check; clean PET, HDPE and PP can be sold to a ReflowEconomy micro-factory. Consented field photos feed a retraining loop with a fixed field evaluation set.

![Data and material flow](media/flow.png)

Full design precis: [docs/02-concept.md](docs/02-concept.md). Sizing of the dataset, model, energy and evaluation: [docs/04-calcs/01-sizing.md](docs/04-calcs/01-sizing.md). General arrangement: [cad/drawings/WML-DWG-001.pdf](cad/drawings/WML-DWG-001.pdf).

**Status at TRL 3 (on paper):** model size, speed, local grades and the reference phone are met; battery life is met if the screen sleeps between scans; class accuracy, hazard recall, coverage (about 68 % against 70 %) and dataset licenses are at risk; grading opaque HDPE versus PP from a photo and the field evaluation set are not met. Nothing has been trained; TRL 4 is on hold.

## Key components

- Open training dataset (curated from public waste image sets plus consented field photos)
- Lightweight model for phones and Raspberry Pi (MobileNetV3 or EfficientNet class), with a material class head and a grade head
- Label taxonomy aligned to resin codes and local buyer grades, mapped per site by a configuration file
- Field evaluation set from real sorting sites, never used for training
- Export to TensorFlow Lite or ONNX, with a model card
- Reference sorting station for a pilot: phone on a clamp stand, light mat, bins by material class, hazard box, power bank and scale

The pilot list with indicative costs is in [bom/bom.csv](bom/bom.csv). This repository has no hardware budget.

## Safety

> **Safety:** Classification guides sorting but does not certify material. Hazardous items (batteries, sharps, chemicals) must be flagged, never auto-sorted. Sorting stations carry cut, fire and chemical hazards; see the safety section of the [design precis](docs/02-concept.md).

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, evaluation notes and design decisions |
| `ml/data/` | Dataset manifests and label taxonomy (images are referenced, not committed) |
| `ml/notebooks/` | Training and evaluation notebooks (none yet) |
| `ml/models/` | Exported TensorFlow Lite or ONNX models (via GitHub Releases) |
| `bom/` | Reference pilot station, dataset effort and compute, with indicative costs |
| `cad/src/` | Parametric station model (`model.py`), drawing sheet (`sheets.py`) and concept media script |
| `cad/step/`, `cad/stl/`, `cad/drawings/` | STEP and STL exports and the general arrangement drawing WML-DWG-001 |
| `media/` | Concept media (hero, blueprint, 3D viewer, exploded view, flow diagram); later screenshots and sample predictions |
| `build-log/` | Dated experiment log |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (WML-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py`.

## License

MIT, see [LICENSE](LICENSE). Datasets keep their own licenses, recorded in `ml/data/SOURCES.md`.

## Related repos

- [wastewise-scan](https://github.com/BoujeeEnjinia1701/wastewise-scan): handheld NIR scanner for plastic resin type
- [refloweconomy](https://github.com/BoujeeEnjinia1701/refloweconomy): open playbook for local material recovery micro-factories

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
