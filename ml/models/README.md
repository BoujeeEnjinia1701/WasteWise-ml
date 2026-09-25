# Models

Exported models are attached to GitHub Releases, not committed.

No model has been trained yet (TRL 2). The proposed export, awaiting Amish, is:

- 8-bit TensorFlow Lite model for Android phones, about 5 to 6 MB (estimate), plus an ONNX export for other runtimes.
- A backbone such as MobileNetV3-Large with two heads: material class and grade (see `ml/data/taxonomy.yaml`).
- A model card with each release: training data and licenses, per-class accuracy and hazard recall on the field evaluation set, coverage at the chosen confidence thresholds, and known failure modes.
