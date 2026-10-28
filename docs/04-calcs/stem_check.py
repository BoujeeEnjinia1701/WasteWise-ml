"""WasteWise-ml STEM check calculations (WML-STM-001, STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv, which fills Table 1 of docs/01b-stem-check.md. Design values come from
cad/src/model.py (PARAMS, derived()) and from WML-CAL-001 (docs/04-calcs/sizing.py); each check here is a
first-order screen of a claim, not the sizing itself. Rows whose first verdict was "Fails, fix proposed" are
recorded with the verdict after the fix and the decision that closed them (fix rule, WML-DEC-001 F1 to F3);
the first verdicts are listed in the document.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from stem_check import Check, WITHIN, PLAUSIBLE, FIX, FAILS  # noqa: E402,F401
import model  # noqa: E402

g = model.derived()
c = Check(out=ROOT / "docs/04-calcs/stem_results.csv")

# ---------------------------------------------------------------- Physics: optics and radiation (option A)
diag = math.hypot(36.0, 24.0)
c.order_of_magnitude("S1", "Lens 440 mm above the mat with a 26 mm-equivalent lens sees a 586 x 439 mm frame", "Physics",
                     "Optics and radiation", claimed=439, estimate=g["cam_h"] * diag * 0.6 / g["focal_eq"], unit="mm (frame depth)",
                     law="Pinhole camera: frame = height x sensor size / focal length, on the 35 mm-equivalent 4:3 frame (34.62 x 25.96 mm)",
                     factor=1.05, closed_by="WML-CAL-001 section 6")
c.claim("S2", "The frame stays on the 450 mm deep mat with the phone's placement in the tray allowed for", "Physics",
        "Optics and radiation", "Pinhole camera: frame depth 439 mm at 26 mm; with 3.3 mm of placement stack (S7) the lens must be 25.76 mm "
        "equivalent or longer, 1 % under a quoted 26 mm that is itself rounded (independent review 2026-10-25). Lowering the lens to 420 mm "
        "gives 15.3 mm a side and fits lenses of 24.2 mm and longer: proposed to Amish as D2, since 440 mm was his decision (N3)",
        g["focal_eq"], 25.76, "mm (35 mm-equivalent focal length)", rule="above", margin=0.05, closed_by="")
c.cited("S3", "A visible-light camera does not reliably separate opaque HDPE from PP or identify carbon-black plastics; these go to Unsure",
        "Physics", "Optics and radiation",
        "Polymers are told apart by C-H overtone absorption in the short-wave infrared (Neo et al. 2022, as cited in WasteWise Scan WSC-PRB-001), "
        "not by visible colour; carbon black pigment prevents NIR sorting of black packaging (WRAP)",
        "The design claims a limit, not a capability: 9 % of items (assumed stream) are routed to Unsure (WML-CAL-001 section 8)",
        WITHIN, "WML-CAL-001 section 8; PR-002 not met by design")

# ---------------------------------------------------------------- Physics: electromagnetism and circuits
batt = 4000 / 1000 * 3.85
e_a = 500 * 7.5 / 3600 + 0.03 * 8 + 500 * 0.5 * 1.0 / 3600 + 0.005 * 8
c.claim("S4", "An 8 h shift of 500 scans (tap-to-scan, screen asleep between scans, voice on, button linked) uses 30 % or less of a 4,000 mAh battery",
        "Physics", "Electromagnetism and circuits", "Energy balance: 7.5 J a scan, 0.03 W asleep, 0.5 W for 1 s of voice, 0.005 W Bluetooth link; battery 15.4 Wh",
        round(100 * e_a / batt, 1), 30.0, "% of battery", closed_by="WML-CAL-001 section 5 (PR-010)")
c.order_of_magnitude("S5", "The 10,000 mAh power bank puts about 26.7 Wh into the phone battery", "Physics", "Electromagnetism and circuits",
                     claimed=26.7, estimate=37.0 * 0.85 * 0.85, unit="Wh", factor=1.05,
                     law="Conservation of energy: 37 Wh x 0.85 boost x 0.85 charger", closed_by="WML-CAL-001 section 5")

# ---------------------------------------------------------------- Physics: mechanics and statics
E_AL, F_TAP = 69000.0, 5.0
I_SHS = (g["tube"] ** 4 - (g["tube"] - 2 * g["tube_t"]) ** 4) / 12
a_tap = g["post_y"] - g["mat_cy"]
th = F_TAP * a_tap * g["post_len"] / (E_AL * I_SHS) + F_TAP * (a_tap - g["tube"] / 2) ** 2 / (2 * E_AL * I_SHS)
c.claim("S6", "A firm 5 N tap on the screen moves the picture on the mat by less than 1 mm (one grid line's width)", "Physics",
        "Mechanics and statics", "Cantilever bending of the 25 x 25 x 2 aluminium post and arm, E = 69 GPa (6063); bolted joints and clamps taken as rigid; the lens's "
        "own 0.12 mm drop is left out, which opposes the axis turn, so the figure is conservative",
        round(g["cam_h"] * th, 2), 1.0, "mm", closed_by="WML-CAL-001 section 11; WML-BLD-001 first check 'Stand rigid'")
c.claim("S7", "The phone's placement in the tray keeps the picture within the 5.3 mm margin", "Engineering and technology",
        "Manufacturing tolerances", "A whole-stand tilt barely moves the picture (0.24 mm a degree: the lens moves one way, the axis turns the other); "
        "the phone does: 7.7 mm a degree of axis tilt, 5.1 mm a degree of yaw, plus bump slack in the window. First verdict: Fails, fix proposed "
        "(34 mm window and a free phone: 2.0 mm slack plus 0.72 deg yaw, 5.7 mm). Fix F5: 32 mm window (1 mm slack) and the phone pushed "
        "against the far lip (no yaw); with 0.3 deg of tray tilt (assumed) the stack is 3.3 mm",
        3.3, (g["mat_d"] - g["frame_y"]) / 2, "mm", closed_by="WML-DEC-001 F5 (fix implemented: tray window, BLD step 7, first check)")

# ---------------------------------------------------------------- Physics: heat transfer
A_PHONE = 2 * g["phone_l"] * g["phone_w"] / 1e6
p_avg = e_a / 8
c.claim("S8", "In shade on a 40 C Pune afternoon the phone, used tap-to-scan, stays below the 45 C Li-ion charge limit", "Physics", "Heat transfer",
        "Steady heat balance, h = 10 W/(m2 K) over both faces (0.024 m2); Li-ion charge window 0 to 45 C (Battery University BU-410). In direct sun "
        "(about 10 W absorbed) the phone would reach about 85 C, so the rig stands in shade. With the screen on and charging (case B) the phone runs "
        "about 10 K over the air, so that fallback holds only below about 35 C (independent review 2026-10-25)",
        round(40.0 + p_avg / (10.0 * A_PHONE), 1), 45.0, "C", closed_by="WML-CAL-001 section 13; WML-BLD-001 safety stop S4 (shade); PR-020")

# ---------------------------------------------------------------- Chemistry
c.cited("C1", "Loose cells put in the steel hazard box are much less likely to short across their terminals", "Chemistry", "Electrochemistry and batteries",
        "A cell whose terminals touch a conductor (the steel walls, another cell, a can) discharges through it and heats; lithium cells can then go "
        "into thermal runaway. Taping terminals is the standard control (UCLA EHS, battery safety)",
        "First verdict: Fails, fix proposed (a bare steel box with a sand floor; terminals could touch the walls or each other). Fix F3: the terminals "
        "of every loose cell are covered with PVC tape before it goes in, and cells are laid in the 50 mm sand bed clear of the walls; a tape roll lives in the box",
        WITHIN, "WML-DEC-001 F3 (fix implemented: BOM line 5, PRC safety, PR-018)")
sand_kg = (g["haz_l"] - 2 * g["haz_sheet"] - 1) * (g["haz_d"] - 2 * g["haz_sheet"] - 1) * g["haz_sand"] * 1e-9 * 1600
c.claim("C2", "The 50 mm sand bed absorbs the heat of one phone-size cell in thermal runaway with a mean rise under 100 K", "Chemistry",
        "Physical chemistry", "Heat balance: 15.4 Wh x 8 (assumed upper bound on total heat release against stored electrical energy) into "
        f"{sand_kg:.1f} kg of sand at 830 J/(kg K): bulk heat capacity only; local temperature near the cell (hundreds of C), venting and spread "
        "to other cells are not assessed. The steel box keeps the fire from paper and film; sand does not stop a cell in runaway",
        round(15.4 * 3600 * 8 / (sand_kg * 830), 0), 100.0, "K", closed_by="WML-CAL-001 section 14")
c.cited("C3", "The painted hardboard mat stays flat when wet, dirty items lie on it", "Chemistry", "Materials and polymer chemistry",
        "Hardboard takes up water through unsealed faces and edges: 24 h thickness swelling up to 25 % for 3.2 mm board (EN 317 rating, Moelven hardboard "
        "datasheet); a coating on one face only also cups the board as the other face swells",
        "First verdict: Fails, fix proposed (the build plan painted and varnished the top face only). Fix F2: prime, paint and varnish both faces and "
        "all four edges, so the board is sealed all over and the coatings balance. That it then stays flat is not shown: chips and scratches "
        "let water in (independent review 2026-10-25); a 24 h wet-cloth soak and cup measurement at TRL 4 confirms it",
        PLAUSIBLE, "")
c.cited("C4", "The model never certifies chemical content, food-contact suitability or hazardous-waste status", "Chemistry", "Analytical",
        "A photo records reflected visible light; it carries no chemical analysis", "Scope claim (PRB out of scope; PRC safety)", WITHIN,
        "WML-PRB-001 out of scope")

# ---------------------------------------------------------------- Biology: ergonomics and toxicology
H5 = 1356.0
sh, U, Fh = 0.818 * H5, 0.186 * H5, 0.254 * H5
dx, dz = g["bench_d"] - g["mat_cy"] + 150.0, g["screen_z"] - sh
D = math.hypot(dx, dz)
elev = 90.0 - (math.degrees(math.acos((U * U + D * D - Fh * Fh) / (2 * U * D))) - math.degrees(math.atan2(dz, dx)))
c.cited("B1", "The user triggers each scan without repeated reaching at shoulder height", "Biology", "Ergonomics",
        "Two-link arm (Drillis and Contini proportions, Winter 2009) for the 5th percentile Indian woman (stature 1,356 mm, Nag, Nag and Desai 2003); "
        "ISO 11226 screens upper arm elevation above 60 deg for static postures (a tap a minute is not static; the 59 deg moves to 51 or 68 deg "
        "with the shoulder 100 or 200 mm behind the bench edge)",
        f"First verdict: Plausible (tapping the screen needs {elev:.0f} deg upper arm elevation at about one scan a minute, at the 60 deg screen). "
        "Fix F1: a Bluetooth shutter button on the bench edge, 45 mm in from the user's edge at bench height, takes the photo; no reach to the phone",
        WITHIN, "WML-DEC-001 F1 (fix implemented: BOM line 12, model, BLD, PR-015)")
ex, ez = g["bench_d"] - g["mat_cy"] + 100.0, 0.936 * H5 - g["screen_z"]
theta = math.degrees(math.atan2(ex, ez)); De = math.hypot(ex, ez)
arc = lambda h: math.degrees(math.atan(h * math.cos(math.radians(theta)) / De)) * 60  # noqa: E731
c.claim("B2", "A user at the 5th percentile can read the result (a 40 mm bin number) on the screen lying flat at 1,215 mm", "Biology", "Ergonomics",
        f"Visual angle of the foreshortened symbol: the 5th percentile user's eye is {ez:.0f} mm above the screen and {ex:.0f} mm back, {theta:.1f} deg off "
        f"the screen normal; a 10 mm icon subtends {arc(10):.0f} arcmin against the 16 arcmin minimum of ISO 9241-303 (first verdict: Fails, fix proposed). "
        "Fix F1: the result fills the screen in the class colour with the bin number at least 40 mm tall, and the phone says the bin number aloud by default. "
        "ISO 9241-303 assumes a near-normal view; at 83 deg the digit is squashed about 7.7 to 1 and glare and contrast loss are likely, so legibility "
        "is confirmed by a trial with a short user (independent review 2026-10-25); colour and voice do not depend on it",
        round(arc(40.0)), 16.0, "arcmin", rule="above", margin=10.0, closed_by="")
c.cited("B3", "The rig adds little exposure beyond the existing handling of sharps and dirty items, apart from the stored cells of C1 and C2", "Biology",
        "Toxicology", "Cut-resistant gloves, no handling of items closer to the camera, hazards to the box (PRC safety)", "Safety claim only",
        WITHIN, "WML-PRC-001 safety; WML-BLD-001 safety stops")

# ---------------------------------------------------------------- Mathematics
p_model = 5.4e6 - (1280 * 1000 + 1000) + (1280 * 7 + 7 + 1280 * 22 + 22)
c.order_of_magnitude("M1", "The 8-bit model file is about 4.4 MB", "Mathematics", "Units and dimensional analysis", claimed=4.4,
                     estimate=p_model * 1.05 / 1e6, unit="MB", law="Parameters x 1 byte + 5 % file overhead (MobileNetV3-Large, 5.4 M parameters less the "
                     "ImageNet classifier plus two heads)", factor=1.1, closed_by="WML-CAL-001 section 2 (PR-006)")
c.cited("M2", "Photo to result in 300 ms or less on a low-cost phone", "Mathematics", "Orders of magnitude",
        "217 M multiply-accumulates at 1.2 to 4.9 GMAC/s (TensorFlow Models, MobileNet README: 44 ms on a Pixel 1) plus preprocessing",
        "201 ms at the slow end from a preview-size frame (20 ms preprocessing); 331 ms if a full 12 MP frame is decoded first, which the "
        "independent review (2026-10-25) put at 100 to 300 ms on an A53-class phone. Met only if the app classifies a preview-size frame; to measure",
        PLAUSIBLE, "")


def binom_cdf(k, n, p):
    return sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k + 1))


def lower(n, m, conf=0.95):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        r = (lo + hi) / 2
        if binom_cdf(m, n, 1 - r) > 1 - conf:
            hi = r
        else:
            lo = r
    return lo


c.claim("M3", "400 hazard items with 3 misses or fewer show hazard recall of at least 98 % at 95 % confidence, for the evaluation population", "Mathematics",
        "Statistics and uncertainty", "One-sided Clopper-Pearson lower bound; valid for an independent sample of the evaluation population only: hazards "
        "collected on purpose and photos from one site are not that, so field recall can be lower; report each hazard type separately", round(lower(400, 3), 4), 0.98, "recall", rule="above",
        closed_by="WML-CAL-001 section 9 (PR-003, PR-011)")
c.cited("M4", "About 230 field images per label give 90 % accuracy on answered items at 70 % coverage", "Mathematics", "Statistics and uncertainty",
        "Power-law learning curve, error = 0.03 + a n^-0.5 anchored at 25 % for 100 images (assumed); power laws fit deep-learning learning curves "
        "(Hestness et al. 2017), but the constants for field waste photos are unknown",
        "128 to 591 images per label across the sensitivity cases; the design figure of 300 covers six of the nine cases. The review recalls a scaling "
        "exponent nearer 0.3 for ImageNet (Hestness et al. 2017, to check), which would need about 330", PLAUSIBLE,
        "")
c.cited("M5", "About 66 % of items get an answer (63 % graded, 3 % true hazard flags) at 90 % grade accuracy", "Mathematics", "Statistics and uncertainty",
        "Selective classification: abstaining on the least-confident share u removes 2u of the errors (assumed); stream composition assumed",
        "Corrected after the independent review (false hazard alarms leave the graded pool): 66 %, 4 points under PR-004; rests on the assumed "
        "stream, enrichment factor and perfect abstention on camera-blind items", PLAUSIBLE, "")
c.claim("M6", "About 1,065 answered items estimate a 90 % accuracy to within 2 points (95 %)", "Mathematics", "Statistics and uncertainty",
        "Normal approximation to the binomial, half-width 1.96 sqrt(p(1-p)/n)", round(100 * 1.96 * math.sqrt(0.09 / 1065), 1), 2.0,
        "points", closed_by="WML-CAL-001 section 9")
c.order_of_magnitude("M7", "Labeling 10,000 photos takes about 72 h (labeling only; capture and NIR ground truth for camera-blind grades excluded)", "Mathematics", "Orders of magnitude", claimed=72.2,
                     estimate=10000 * 20 * 1.3 / 3600, unit="h", law="Photos x 20 s x 1.3 review", factor=1.1, closed_by="WML-CAL-001 section 7")

# ---------------------------------------------------------------- Engineering and technology
c.cited("E1", "A phone image classifier can tell broad material classes apart from one photo", "Engineering and technology", "Sensing resolution",
        "TrashNet: six classes of single items photographed with phones on a plain board were told apart (Thung and Yang 2016; the reported accuracy "
        "is to recheck against the CS 229 report, independent review 2026-10-25); a clean board is a weak proxy for the field",
        "The principle is shown on clean photos; field accuracy by grade is PR-001 and PR-002 (at risk) and M4", WITHIN, "WML-PRB-001 prior work")
c.claim("E2", "At full resolution a molded 6 mm resin code digit spans at least 20 pixels (pixel count only)", "Engineering and technology", "Sensing resolution",
        "Pixel pitch on the mat = frame width / 4,000 px; 20 px a character is the design figure (assumed). Legibility of embossed, same-colour "
        "codes also depends on lens sharpness and light, not shown here",
        round(6.0 / (g["frame_x"] / 4000)), 20.0, "px", rule="above", closed_by="WML-CAL-001 section 6")
c.order_of_magnitude("E3", "The model and its activations need about 8 MB of the phone's 3 GB of memory (camera frame buffers, about 48 MB at 12 MP, come on top)", "Engineering and technology",
                     "Power and link budgets", claimed=8.0, estimate=4.4 + 112 * 112 * 64 * 2 / 1e6 * 2, unit="MB",
                     law="Weights plus the two largest activation tensors (112 x 112 x 64, 8-bit, double-buffered)", closed_by="WML-CAL-001 section 3")
c.cited("E4", "The shutter button's CR2032 cell lasts at least three months of shifts", "Engineering and technology", "Power and link budgets",
        "225 mAh at 0.05 mA mean while linked (assumed, no datasheet); cheap buttons may draw 0.1 to 0.5 mA, and above about 0.45 mA the cell "
        "fails the 78-shift screen (independent review 2026-10-25)", "562 shifts at 0.05 mA; 62 at 0.45 mA. The screen tap stays as the fallback; measure the bought button",
        PLAUSIBLE, "")

# ---------------------------------------------------------------- Option B: tray detector (WML-OPT-001)
c.claim("OB1", "Option B: the wide camera 450 mm over the tray floor sees the whole 600 x 400 mm tray", "Physics", "Optics and radiation",
        "Frame = 2 h tan(FOV / 2), 102 x 67 deg (Camera Module 3 Wide)", round(g["b_frame_y"]), g["b_tray_d"], "mm (frame depth)", rule="above",
        closed_by="WML-CAL-001 section 15")
c.claim("OB2", "Option B: a 40 mm bottle cap spans at least 16 px at a 1,280 px detector input", "Engineering and technology", "Sensing resolution",
        "Pixel pitch = frame width / 1,280 px; small-object detectors need about 16 to 32 px (assumed); an 11 mm button cell is only about 13 px", round(40 / (g["b_frame_x"] / 1280)), 16.0, "px",
        rule="above", closed_by="WML-CAL-001 section 15")
c.claim("OB3", "Option B: a 20,000 mAh power bank runs the Pi 5 and display for an 8 h shift", "Physics", "Electromagnetism and circuits",
        "Energy balance: Pi 5 idle 2.7 W, display 1.5 W, detector bursts 6 W for 3 s (assumed); 74 Wh x 0.85 boost", 34.1, 62.9, "Wh",
        closed_by="WML-CAL-001 section 15")
c.order_of_magnitude("OB4", "Option B: the detector answers a 1,280 px tray photo in about 1 s on the Pi 5", "Mathematics", "Orders of magnitude",
                     claimed=1.0, estimate=8.7 * 4 / 30.0, unit="s", law="YOLOv8n at 640 px is 8.7 GFLOP (Ultralytics); x4 at 1,280 px; 20 to 40 GFLOP/s effective on the Pi 5 (assumed)",
                     closed_by="WML-CAL-001 section 15")
c.cited("OB5", "Option B: hazard recall of 98 % holds for items at least half visible in a tray of 10 to 20", "Mathematics", "Statistics and uncertainty",
        "Detection recall falls for occluded objects; no field data for waste trays", "Untested; would need its own field evaluation set", PLAUSIBLE, "")

state = c.write()
