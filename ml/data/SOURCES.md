# Dataset sources

Candidate sources for training and evaluation. Images are referenced, not committed. A source is used only after its license is confirmed to allow training and publishing model weights (requirement R13 in docs/03-requirements.md). Status: candidates listed 2026-09-25; no source has been downloaded or used.

| Dataset | License | Use |
| --- | --- | --- |
| TrashNet (Thung and Yang 2016), https://github.com/garythung/trashnet: 2,527 photos, six classes, items on a white posterboard | Repository under MIT; confirm that it covers the images | Pretraining and a clean-background baseline for the class head |
| TACO (Proença and Simões 2020), https://github.com/pedropro/TACO: litter in the wild, COCO-format segmentation | Repository code under MIT; images hosted on Flickr under their own licenses; confirm the annotation license and each image's license | Crops of single items for the class head; realistic backgrounds |
| ZeroWaste (Bashkirova et al. 2022): materials recovery facility conveyor images | To confirm | Candidate for cluttered, dirty items; check license before any use |
| WasteWise field set (to be collected with the partner) | Proposed: consent-based, co-owned by the pickers' organization, open release terms to be agreed | Main training data by grade; separate field evaluation set never used for training |
