"""WasteWise-ml sizing calculations for WML-CAL-001.

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number that docs/04-calcs/01-sizing.md quotes. Paper calculations only:
this script trains nothing, loads no images and runs no model. Camera geometry reads
cad/src/model.py; costs read bom/bom.csv.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))

# ================================================================ assumptions
# Model (TensorFlow Models, MobileNet README: MobileNetV3-Large 1.0, 224 px)
P_TOTAL = 5.4e6            # parameters including the 1,000-class ImageNet classifier
MACS = 217e6               # multiply-accumulates per image
T_PIXEL1_MS = 44.0         # 8-bit, Pixel 1 large core
FEAT = 1280                # penultimate feature width
N_CLASS, N_GRADE = 7, 22   # ml/data/taxonomy.yaml (plastic 7, paper 3, metal 2, glass 2, organic 2, hazardous 4, composite 2)
FILE_OVERHEAD = 0.05       # TFLite graph, quantization parameters and metadata (assumed)
APP_SHELL_MB = (8.0, 15.0) # app code, UI assets and TFLite runtime without the model (assumed range)

# Phone (reference phone R12: 2019 or later low-cost Android, Cortex-A53 class cores)
SLOWDOWN = (1.0, 4.0)      # low-cost phone relative to the Pixel 1 large core (assumed range)
GMACS_A53 = (1.2, 2.5)     # effective int8 throughput of one A53-class core, GMAC/s (assumed range)
T_PRE_MS = 20.0            # crop, resize and normalize (assumed)
P_INFER_W = 2.0            # extra SoC power while the model runs (assumed)
BATT_MAH, BATT_V = 4000.0, 3.85
P_ACTIVE_W = 2.5           # screen, camera and SoC while a scan is active (assumed)
T_ACTIVE_S = 3.0           # active time per scan in tap-to-scan use
P_SCREEN_W = 0.9           # screen on at outdoor brightness with the camera off (assumed)
P_CAM_EXTRA_W = 1.6        # camera and ISP on top of the screen during a scan (P_ACTIVE_W - P_SCREEN_W)
P_STANDBY_W = 0.03         # phone asleep between scans (assumed)
SHIFT_H, SCANS = 8.0, 500  # R10 duty
PB_MAH, PB_V = 10000.0, 3.7
PB_BOOST, PHONE_CHG = 0.85, 0.85   # power bank boost and phone charging efficiencies (assumed)

# Time to result (R7), seconds: (nominal, worst)
T_TAP = (0.3, 0.6)         # reach and tap, or foot switch
T_FOCUS = (0.4, 0.8)       # focus and exposure settle; focus can lock at the fixed stand height
T_CAPTURE = (0.13, 0.3)
T_SHOW = (0.05, 0.1)

# Learning curve for fine-tuning an ImageNet-pretrained mobile network on field photos (assumed):
#   error(n) = C_FLOOR + A * n^-B, with n images per label, anchored at error(100) = E100
C_FLOOR, B_EXP, E100 = 0.03, 0.5, 0.25
# Selective classification: abstaining on the lowest-confidence share u removes min(1, K*u) of errors (assumed)
K_ENRICH = 2.0
COV_TARGET = 0.70
MARGIN = 1.3               # margin on the calculated images per label
HARD_GRADES = 8            # film, mixed paper, newsprint, multilayer pouch and the four hazardous grades
HARD_FACTOR = 2.0
REJECT = 0.10              # share of field photos rejected in review (blur, faces, wrong label)

# Stream composition by item count for a dry mixed stream (assumed; to be replaced by field counts)
STREAM = {"PET": 0.20, "HDPE and PP, visually separable": 0.06, "HDPE and PP, opaque, not separable": 0.06,
          "Black plastics": 0.03, "Other plastics (PS, PVC)": 0.04, "Film (LDPE)": 0.14, "Metal": 0.10,
          "Paper and card": 0.20, "Composite": 0.06, "Glass": 0.06, "Organic": 0.02, "Hazardous": 0.03}
CAMERA_BLIND = ("HDPE and PP, opaque, not separable", "Black plastics")
HAZ_FPR = 0.02             # share of non-hazard items flagged as hazards at the high-recall threshold (assumed)

# Labeling and evaluation
S_LABEL, S_EVAL, REVIEW = 20.0, 60.0, 0.30   # seconds per photo, review overhead
PAY = 6.0                                    # USD per hour, planning figure (rate set with the partner)
N_TRAIN, N_EVAL = 10000, 2000
EVAL_PER_GRADE = 50
R3_TARGET, CONF = 0.98, 0.95


def line(k, v):
    print(f"  {k:58s} {v}")


def head(t):
    print(f"\n== {t}")


# ================================================================ 1. model size (R6)
head("1. Model size (R6)")
p_cls1000 = FEAT * 1000 + 1000
p_backbone = P_TOTAL - p_cls1000
p_heads = FEAT * N_CLASS + N_CLASS + FEAT * N_GRADE + N_GRADE
p_model = p_backbone + p_heads
mb = lambda nbytes: nbytes / 1e6
size_int8 = mb(p_model * 1 * (1 + FILE_OVERHEAD))
size_f16 = mb(p_model * 2 * (1 + FILE_OVERHEAD))
size_f32 = mb(p_model * 4 * (1 + FILE_OVERHEAD))
line("ImageNet 1,000-class classifier removed, parameters", f"{p_cls1000 / 1e6:.2f} M")
line("Backbone parameters", f"{p_backbone / 1e6:.2f} M")
line("Class and grade heads, parameters", f"{p_heads:,.0f}")
line("Model parameters", f"{p_model / 1e6:.2f} M")
line("File size int8 / float16 / float32", f"{size_int8:.1f} / {size_f16:.1f} / {size_f32:.1f} MB (limit 10 MB)")
app = (APP_SHELL_MB[0] + size_int8, APP_SHELL_MB[1] + size_int8)
line("App with int8 model", f"{app[0]:.0f} to {app[1]:.0f} MB (limit 30 MB)")

# ================================================================ 2. latency (R5)
head("2. Latency on a low-cost phone (R5)")
t_scaled = [T_PIXEL1_MS * s for s in SLOWDOWN]
gmacs_p1 = MACS / (T_PIXEL1_MS / 1000) / 1e9
t_mac = [MACS / (g * 1e9) * 1000 for g in reversed(GMACS_A53)]
t_res = [t_scaled[0] + T_PRE_MS, max(t_scaled[1], t_mac[1]) + T_PRE_MS]
line("Pixel 1 effective throughput", f"{gmacs_p1:.1f} GMAC/s")
line("Inference, scaled from Pixel 1 (1x to 4x)", f"{t_scaled[0]:.0f} to {t_scaled[1]:.0f} ms")
line("Inference, from A53-class throughput", f"{t_mac[0]:.0f} to {t_mac[1]:.0f} ms")
line("Photo to result incl. 20 ms preprocessing", f"{t_res[0]:.0f} to {t_res[1]:.0f} ms (limit 300 ms)")
line("Margin at the slow end", f"{300 - t_res[1]:.0f} ms")

# ================================================================ 3. time to result (R7)
head("3. Time from placing an item to the result (R7)")
t_inf = (t_res[0] / 1000, t_res[1] / 1000)
tt = [T_TAP[i] + T_FOCUS[i] + T_CAPTURE[i] + t_inf[i] + T_SHOW[i] for i in (0, 1)]
line("Nominal / worst", f"{tt[0]:.1f} / {tt[1]:.1f} s (limit 3 s)")
line("Scan interval at 500 scans in 8 h", f"{SHIFT_H * 3600 / SCANS:.0f} s")

# ================================================================ 4. energy and battery (R10)
head("4. Energy per scan and battery (R10)")
batt_wh = BATT_MAH / 1000 * BATT_V
e_inf = [P_INFER_W * t / 1000 for t in (t_scaled[0], t_scaled[1])]
e_scan = P_ACTIVE_W * T_ACTIVE_S
line("Battery energy", f"{batt_wh:.1f} Wh")
line("Energy per inference", f"{e_inf[0]:.2f} to {e_inf[1]:.2f} J")
line("Energy per scan (3 s active at 2.5 W)", f"{e_scan:.1f} J")
case_a = (SCANS * e_scan / 3600) + P_STANDBY_W * SHIFT_H
case_b = P_SCREEN_W * SHIFT_H + SCANS * P_CAM_EXTRA_W * T_ACTIVE_S / 3600
case_c = P_ACTIVE_W * SHIFT_H
for name, e in (("A tap-to-scan, screen sleeps between scans", case_a),
                ("B tap-to-scan, screen on all shift", case_b),
                ("C live camera preview all shift", case_c)):
    line(f"Case {name}", f"{e:.1f} Wh = {100 * e / batt_wh:.0f} % of battery (limit 30 %)")
pb_wh = PB_MAH / 1000 * PB_V
pb_to_phone = pb_wh * PB_BOOST * PHONE_CHG
line("Power bank nominal / into the phone battery", f"{pb_wh:.0f} / {pb_to_phone:.1f} Wh")
line("Shifts of case B per power bank charge", f"{pb_to_phone / case_b:.1f}")

# ================================================================ 5. camera geometry (from model.py)
head("5. Camera geometry at the station (from cad/src/model.py)")
import model  # noqa: E402
g = model.derived()
line("Lens height above mat / floor", f"{g['cam_h']:.0f} / {g['lens_z']:.0f} mm")
line("Field of view, horizontal x vertical", f"{g['hfov_deg']:.1f} x {g['vfov_deg']:.1f} deg")
line("Camera frame on the mat", f"{g['frame_x']:.0f} x {g['frame_y']:.0f} mm (mat {g['mat_l']:.0f} x {g['mat_d']:.0f})")
fits = g["frame_x"] <= g["mat_l"] and g["frame_y"] <= g["mat_d"]
line("Frame inside the mat", "yes" if fits else "NO")
stand_clear = g["base_y"] > g["mat_cy"] + g["frame_y"] / 2
line("Stand base outside the frame", f"{'yes' if stand_clear else 'NO'} (board front edge at Y {g['base_y']:.0f}, "
     f"frame edge {g['mat_cy'] + g['frame_y'] / 2:.1f}, margin {g['base_y'] - g['mat_cy'] - g['frame_y'] / 2:.1f} mm, "
     f"the same as the mat's own margin)")
line("Stand post / arm (WML-DDR-003)", f"{g['post_len']:.0f} / {g['arm_len']:.1f} mm of 25 x 25 x 2 mm tube; lens flush with the tray underside")
px_full = g["frame_x"] / 4000
line("Resolution, 12 MP full frame", f"{px_full:.2f} mm per pixel")
line("Resolution, full frame resized to 224 px", f"{g['frame_x'] / 224:.1f} mm per pixel")
line("Resolution, 300 mm item crop at 224 px", f"{300 / 224:.1f} mm per pixel")
line("Bin inner volume", f"{g['bin_vol_l']:.0f} L")

# ================================================================ 6. dataset size (R1, R2, R4)
head("6. Dataset size (R1, R2, R4)")
A = (E100 - C_FLOOR) * 100 ** B_EXP


def err(n, a=A, b=B_EXP, c=C_FLOOR):
    return c + a * n ** -b


def n_for(e, a=A, b=B_EXP, c=C_FLOOR):
    return (a / (e - c)) ** (1 / b)


def e_full_for(sel_err, cov=COV_TARGET, k=K_ENRICH):
    """Full-coverage error that gives sel_err on answered items at coverage cov."""
    removed = min(1.0, k * (1 - cov))
    return sel_err * cov / (1 - removed)


def coverage_for(e, sel_err, k=K_ENRICH):
    """Coverage at which answered-item error equals sel_err (1.0 if already met)."""
    if e <= sel_err:
        return 1.0
    return e * (k - 1) / (e * k - sel_err)


e90 = e_full_for(0.10); e80 = e_full_for(0.20)
line("Full-coverage error allowed for 90 % at 70 % coverage", f"{e90:.3f}")
line("Full-coverage error allowed for 80 % at 70 % coverage", f"{e80:.3f}")
n90, n80 = n_for(e90), n_for(e80)
line("Images per label for a 90 % target / 80 % target", f"{n90:.0f} / {n80:.0f}")
print("  Sensitivity, images per label for 90 % at 70 % coverage:")
for b in (0.35, 0.5, 0.65):
    for e100 in (0.20, 0.25, 0.30):
        a = (e100 - C_FLOOR) * 100 ** b
        print(f"    B = {b:.2f}, error at 100 images = {e100:.2f}: {n_for(e90, a, b):5.0f}")
n_label = math.ceil(n90 * MARGIN / 50) * 50
easy = N_GRADE - HARD_GRADES
n_total = (easy * n_label + HARD_GRADES * n_label * HARD_FACTOR) / (1 - REJECT)
line("Design images per grade (x1.3 margin, rounded)", f"{n_label}")
line("Field photos to capture (hard grades x2, 10 % rejected)", f"{n_total:,.0f}")
per_class = n_total * (1 - REJECT) / N_CLASS
line("Mean labeled photos per class", f"{per_class:,.0f}")
e_class = err(per_class); e_grade = err(n_label)
line("Expected full-coverage class error / grade error", f"{e_class:.3f} / {e_grade:.3f}")
h_train = N_TRAIN * S_LABEL * (1 + REVIEW) / 3600
line("Labeling effort, 10,000 photos", f"{h_train:.1f} h, ${h_train * PAY:,.0f} at ${PAY:.0f}/h")
haz_train = 4 * n_label * HARD_FACTOR
line("Hazard photos in the training target", f"{haz_train:,.0f} (natural stream at 3 % gives {N_TRAIN * STREAM['Hazardous']:.0f})")

# ================================================================ 7. coverage (R4)
head("7. Coverage: share of items answered (R4)")
blind = sum(STREAM[k] for k in CAMERA_BLIND)
haz = STREAM["Hazardous"]
rest = 1 - blind - haz
cov_grade = coverage_for(e_grade, 0.10)
cov_class = coverage_for(e_class, 0.10)
ans_grade = rest * cov_grade
line("Camera-blind share (opaque HDPE/PP, black)", f"{100 * blind:.0f} %")
line("Coverage on the rest for 90 % grade accuracy", f"{100 * cov_grade:.0f} %")
line("Coverage for 90 % class accuracy (R1)", f"{100 * cov_class:.0f} %")
line("Answered with a grade / Unsure / hazard flag", f"{100 * ans_grade:.0f} % / {100 * (1 - ans_grade - haz):.0f} % / {100 * haz:.0f} %")
line("Answered incl. hazard flags (R4 target 70 %)", f"{100 * (ans_grade + haz):.0f} %")
flagged = haz * R3_TARGET + (1 - haz) * HAZ_FPR
line("Items sent to the hazard box", f"{100 * flagged:.1f} % of items, {100 * (1 - haz) * HAZ_FPR / flagged:.0f} % of them false alarms")

# ================================================================ 8. evaluation plan (R1, R3, R11)
head("8. Evaluation plan (R1, R3, R11)")


def binom_cdf(k, n, p):
    return sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k + 1))


def recall_lower(n, misses, conf=CONF):
    """One-sided Clopper-Pearson lower bound on recall with `misses` misses in n items."""
    lo, hi = 0.0, 1.0
    for _ in range(60):
        r = (lo + hi) / 2
        if binom_cdf(misses, n, 1 - r) > 1 - conf:   # misses this low are still plausible at recall r
            hi = r
        else:
            lo = r
    return lo


def max_misses(n, target=R3_TARGET):
    m = -1
    while recall_lower(n, m + 1) >= target:
        m += 1
    return m


print("  One-sided 95 % lower bound on hazard recall:")
for n in (150, 200, 300, 400, 600):
    lbs = ", ".join(f"{k} miss {recall_lower(n, k):.4f}" for k in range(3))
    print(f"    n = {n:4d}: {lbs}; misses allowed for >= 98 %: {max_misses(n)}")


def n_for_power(r_true, power=0.8):
    for n in range(100, 3001, 10):
        m = max_misses(n)
        if m >= 0 and binom_cdf(m, n, 1 - r_true) >= power:
            return n, m
    return None, None


for r in (0.995, 0.99):
    n, m = n_for_power(r)
    line(f"Hazard items for 80 % chance to show 98 % (true {100 * r:.1f} %)", f"{n} (pass with {m} misses or fewer)")
line("Minimum with zero misses (rule of three)", f"{math.ceil(3 / (1 - R3_TARGET))}")
n_haz_eval = 400
n_nonhaz_min = (N_GRADE - 4) * EVAL_PER_GRADE
line("Evaluation set: hazards / non-hazard minimum / natural mix", f"{n_haz_eval} / {n_nonhaz_min} / {N_EVAL - n_haz_eval - n_nonhaz_min}")
n_ans = (N_EVAL - n_haz_eval) * (ans_grade / (1 - haz))
hw = 1.96 * math.sqrt(0.9 * 0.1 / n_ans)
line("Answered non-hazard items in the set", f"{n_ans:.0f}")
line("95 % half-width on 90 % accuracy", f"+/- {100 * hw:.1f} points")
hw50 = 1.96 * math.sqrt(0.8 * 0.2 / EVAL_PER_GRADE)
line("95 % half-width on one grade at 50 items, 80 %", f"+/- {100 * hw50:.0f} points")
h_eval = N_EVAL * S_EVAL * (1 + REVIEW) / 3600
line("Evaluation labeling effort", f"{h_eval:.1f} h, ${h_eval * PAY:,.0f}")
line("Items to sort to find 400 hazards at 3 %", f"{n_haz_eval / haz:,.0f}")

# ================================================================ 9. cost (BOM)
head("9. Cost (bom/bom.csv)")
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
ONEOFF = {8, 9, 10}          # dataset, evaluation set and compute; every other line is station hardware
num = lambda r: int(r["item"].split()[0])  # noqa: E731
station = sum(float(r["unit_cost_usd"]) * float(r["qty"]) for r in rows if num(r) not in ONEOFF)
oneoff = sum(float(r["unit_cost_usd"]) * float(r["qty"]) for r in rows if num(r) in ONEOFF)
line("BOM lines, all priced", f"{len(rows)}, {all(r['unit_cost_usd'].strip() for r in rows)}")
line("One station (lines 1 to 7 and 11)", f"${station:,.2f}")
line("Dataset, evaluation set and compute (lines 8 to 10)", f"${oneoff:,.2f}")
line("Two-station pilot", f"${2 * station + oneoff:,.2f} (budget_usd null: no hardware budget)")
