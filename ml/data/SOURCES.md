# Dataset sources

Candidate sources for training and evaluation. Images are referenced, not committed. A source is used only after its license is confirmed to allow training and publishing model weights (requirement R13 in docs/03-requirements.md). Status: candidates listed 2026-09-25; licenses checked on the web on 2026-09-25 (WML-CAL-001, section 11); no source has been downloaded or used.

| Dataset | License | Use |
| --- | --- | --- |
| TrashNet (Thung and Yang 2016), https://github.com/garythung/trashnet: 2,527 photos, six classes, items on a white posterboard | Repository under MIT (checked 2026-09-25); the README states no separate image license, so the repository license is taken to cover the images; cite the repository as the README asks | Pretraining and a clean-background baseline for the class head |
| TACO (Proença and Simões 2020), https://github.com/pedropro/TACO: litter in the wild, COCO-format segmentation | Repository code under MIT; annotations CC BY 4.0; images under per-image licenses recorded in the annotation file, CC BY 4.0 where none is given (tacodataset.org, checked 2026-09-25). Filter out any image whose license does not allow training and publishing weights | Crops of single items for the class head; realistic backgrounds |
| ZeroWaste (Bashkirova et al. 2022): materials recovery facility conveyor images | CC BY-NC 4.0 (dataset); code MIT (github.com/dbash/zerowaste, checked 2026-09-25). Non-commercial terms do not fit MIT weights | Proposed, awaiting Amish (WML-DDR-001 N2): exclude from training; non-commercial research comparison only |
| WasteWise field set (to be collected with the partner) | Consent-based, opt-in, no faces, co-owned by the pickers' organization (decided by Amish, 2026-09-25, WML-DDR-001 D6); open release terms to be agreed with the partner | Main training data by grade; separate field evaluation set never used for training |
