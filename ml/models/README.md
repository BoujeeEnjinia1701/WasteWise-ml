# Models

Exported models are attached to GitHub Releases, not committed.

No model has been trained yet (TRL 3 is a paper step; training is TRL 4 work and on hold). The export, decided by Amish on 2026-09-25 (WML-DDR-001 D2), is:

- 8-bit TensorFlow Lite model for Android phones, about 4.4 MB (calculated in WML-CAL-001; the TRL 2 estimate was 5 to 6 MB), plus an ONNX export for other runtimes.
- A MobileNetV3-Large backbone with two heads: material class and grade (see `ml/data/taxonomy.yaml`).
- A model card with each release: training data and licenses, per-class accuracy and hazard recall on the field evaluation set, coverage at the chosen confidence thresholds, and known failure modes.
