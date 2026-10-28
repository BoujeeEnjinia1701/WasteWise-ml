# BOM notes

WasteWise-ml is software, licensed MIT only. It has no hardware budget (`budget_usd` is null in `project.yaml`), so there is no value-engineering target to report the total against.

`bom.csv` lists what a two-station pilot would need, for reference only. Every line is priced. Costs are indicative USD prices from typical retail ranges or supplier types, not supplier quotes, except line 12, which is a cited retail price (walmart.com, checked 2026-10-25), and the USD 1.00 tape roll in line 5, which is an estimate.

- Lines 1 to 7, 11 and 12 are the items at one sorting station (numbered as in `media/exploded.png` and drawing WML-DWG-001 Rev P3). One station is $313.39. Line 2, the phone stand, is made from stock to the build plan WML-BLD-001; line 11 holds its G-clamps, bolts, screws, cable ties and the mat's paint and varnish (added for construction, WML-DDR-003).
- 2026-10-25 STEM check fixes (WML-DDR-005): line 12, a Bluetooth shutter button at the bench edge (F1); line 3, the mat sealed on both faces and all edges (F2, no price change); line 5, a tape roll for loose cell terminals (F3, +$1.00). Line 7 now asks for a scale verified and stamped for trade (WML-REG-001 G3); the stamping fee is to assess.
- Lines 8 to 10 are one-off effort and compute for the dataset, evaluation set and training. They have no geometry. Together they are $730.00. WML-CAL-001 calculates the labeling effort at $433 and $260 (entered as $430 and $260).
- A two-station pilot is $1,356.78 (2 x $313.39 + $730), excluding partner coordination, travel and the phones of pickers who use their own.
- The labeling pay rate of $6 per hour is a planning figure; the real rate is set with the partner at or above the local living wage (WML-DDR-001 D7).
- The sorting bench, input sacks and sample items in the render belong to the site and are not costed.
- Option B (tray detector, WML-OPT-001) is not in this BOM; its first-order cost, about $418.90 a station, is in WML-CAL-001 section 15.
- WasteWise Scan is costed in its own repository.

`docs/04-calcs/sizing.py` reads this file and prints the totals; every made or bought part of option A in `cad/src/model.py` carries one of these line numbers (`python .kit/cad_check.py`).
