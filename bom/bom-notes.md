# BOM notes

WasteWise-ml is software, licensed MIT only. It has no hardware budget (`budget_usd` is null in `project.yaml`), so there is no budget to check the total against.

`bom.csv` lists what a two-station pilot would need, for reference only. Every line is priced. All costs are indicative USD prices from typical retail ranges or supplier types, not supplier quotes, and sit outside any hardware budget.

- Lines 1 to 7 are the items at one sorting station (numbered as in `media/exploded.png` and drawing WML-DWG-001). One station is $285.00.
- Lines 8 to 10 are one-off effort and compute for the dataset, evaluation set and training. They have no geometry. Together they are $730.00. WML-CAL-001 calculates the labeling effort at $433 and $260 (entered as $430 and $260).
- A two-station pilot is $1,300.00 (2 x $285 + $730), excluding partner coordination, travel and the phones of pickers who use their own.
- The labeling pay rate of $6 per hour is a planning figure; the real rate is set with the partner at or above the local living wage (WML-DDR-001 D7).
- The sorting bench, input sacks and sample items in the render belong to the site and are not costed.
- WasteWise Scan is costed in its own repository.

`docs/04-calcs/sizing.py` reads this file and prints the totals.
