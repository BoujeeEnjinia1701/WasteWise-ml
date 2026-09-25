# BOM notes

WasteWise-ml is software. It has no hardware budget (`budget_usd` is null in `project.yaml`).

`bom.csv` lists what a two-station pilot would need, for reference only. All costs are indicative USD prices from typical retail ranges, not supplier quotes, and sit outside any hardware budget.

- Lines 1 to 7 are the items at one sorting station (numbered as in `media/exploded.png`). One station is about $285.
- Lines 8 to 10 are one-off effort and compute for the dataset, evaluation set and training. They have no geometry. Together they are about $730.
- A two-station pilot is about $1,300 (2 x $285 + $730), excluding partner coordination, travel and the phones of pickers who use their own.
- The sorting bench, input sacks and sample items in the render belong to the site and are not costed.
- WasteWise Scan is costed in its own repository.
