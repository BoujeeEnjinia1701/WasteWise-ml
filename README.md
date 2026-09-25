# WasteWise-ml

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![License: MIT](https://img.shields.io/badge/license-MIT-111827)

**Area:** Circular Materials · **TRL:** 2 of 9 (concept formulated)

Open image-classification model that identifies waste items by material class and grade from a phone or low-cost camera. It is the software brain of the WasteWise family: WasteWise Scan adds near-infrared sensing for plastic resin type, and ReflowEconomy uses the sorted output.

## Problem

Recycling streams are contaminated because people and small sorting operations cannot reliably tell materials apart, and value is lost when mixed plastics, paper, metals and organics end up together. Informal waste pickers, who handle most recycling in many low-income countries, earn more only when material is sorted by type and grade.

## Concept

Open image-classification model that identifies waste items by material class and grade from a phone or low-cost camera. It is the software brain of the WasteWise family: WasteWise Scan adds near-infrared sensing for plastic resin type, and ReflowEconomy uses the sorted output.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Open training dataset (curated from public waste image sets plus field photos)
- Lightweight model for phones and Raspberry Pi (e.g. MobileNet or EfficientNet class)
- Label taxonomy aligned to resin codes and local buyer grades
- Evaluation set from real field conditions
- Export to TensorFlow Lite or ONNX

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Classification guides sorting but does not certify material. Hazardous items (batteries, sharps, chemicals) must be flagged, never auto-sorted.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, evaluation notes and design decisions |
| `ml/data/` | Dataset manifests and label taxonomy (images are referenced, not committed) |
| `ml/notebooks/` | Training and evaluation notebooks |
| `ml/models/` | Exported TensorFlow Lite or ONNX models (via GitHub Releases) |
| `bom/` | Compute and camera hardware for field deployment |
| `media/` | Screenshots and sample predictions |
| `build-log/` | Dated experiment log |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (WML-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py`.

## License

MIT, see [LICENSE](LICENSE). Datasets keep their own licenses, recorded in `ml/data/SOURCES.md`.

## Related repos

- [wastewise-scan](https://github.com/BoujeeEnjinia1701/wastewise-scan): handheld NIR scanner for plastic resin type
- [refloweconomy](https://github.com/BoujeeEnjinia1701/refloweconomy): open playbook for local material recovery micro-factories

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
