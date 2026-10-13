import os
from datetime import datetime
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ (PWA Icon & Τίτλος)
st.set_page_config(page_title="Σύστημα Προσφορών Kubota", page_icon="KUBOTA ICON.png", layout="centered")

# ΕΠΙΛΟΓΗ ΓΛΩΣΣΑΣ (UI & PDF)
lang_option = st.selectbox("Επιλογή Γλώσσας / Language", ["Ελληνικά", "English"])
is_english = (lang_option == "English")

# ΠΛΗΡΗΣ ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ (Kubota + Manez Lozano + Niubo)
database = {
    # --- Κουμπότα (Τρακτέρ & Χωματουργικά) ---
    "B1181D-EC": {"cat": "Τρακτέρ", "series": "Σειρά B1 - Stage V", "hp": 17, "price": 14500, "info": "17 HP - Σειρά B1"},
    "B1241D-EC": {"cat": "Τρακτέρ", "series": "Σειρά B1 - Stage V", "hp": 22, "price": 15500, "info": "22 HP - Mid ROPS"},
    "B2261DB-M5-S5": {"cat": "Τρακτέρ", "series": "Σειρά B2 - Stage V", "hp": 25, "price": 17500, "info": "25 HP - Σειρά B2"},
    "B2261 HDB-C-S5": {"cat": "Τρακτέρ", "series": "Σειρά B2 - Stage V", "hp": 25, "price": 27000, "info": "25 HP - Υδροστατικό, Καμπίνα"},
    "LX351-F-R": {"cat": "Τρακτέρ", "series": "Σειρά LX - Stage V", "hp": 35, "price": 33500, "info": "35 HP - Υδροστατικό κιβώτιο ταχυτήτων, ROPS"},
    "LX351-M": {"cat": "Τρακτέρ", "series": "Σειρά LX - Stage V", "hp": 35, "price": 29500, "info": "35 HP - 12/12 Mid ROPS"},
    "LX351-C-R": {"cat": "Τρακτέρ", "series": "Σειρά LX - Stage V", "hp": 35, "price": 40000, "info": "35 HP - Υδροστατικό κιβώτιο ταχυτήτων, Καμπίνα"},
    "LX401-F-R": {"cat": "Τρακτέρ", "series": "Σειρά LX - Stage V", "hp": 40, "price": 43500, "info": "40 HP - Υδροστατικό κιβώτιο ταχυτήτων, ROPS"},
    "LX401-C-R": {"cat": "Τρακτέρ", "series": "Σειρά LX - Stage V", "hp": 40, "price": 50000, "info": "40 HP - Υδροστατικό κιβώτιο ταχυτήτων, Καμπίνα"},
    "L2372DM": {"cat": "Τρακτέρ", "series": "Νέα Σειρά L2 - Stage V", "hp": 37, "price": 35500, "info": "37 HP - (16/16)"},
    "L2452DM": {"cat": "Τρακτέρ", "series": "Νέα Σειρά L2 - Stage V", "hp": 45, "price": 36500, "info": "45 HP - (16/16)"},
    "L2522DM": {"cat": "Τρακτέρ", "series": "Νέα Σειρά L2 - Stage V", "hp": 52, "price": 37500, "info": "52 HP - (16/16)"},
    "L2452DHC": {"cat": "Τρακτέρ", "series": "Νέα Σειρά L2 - Stage V", "hp": 47, "price": 45000, "info": "47 HP - Υδροστατικό κιβώτιο ταχυτήτων, Καμπίνα"},
    "L2552DHC": {"cat": "Τρακτέρ", "series": "Νέα Σειρά L2 - Stage V", "hp": 54, "price": 50000, "info": "54 HP - Υδροστατικό κιβώτιο ταχυτήτων, Καμπίνα"},
    "L2622DHC": {"cat": "Τρακτέρ", "series": "Νέα Σειρά L2 - Stage V", "hp": 62, "price": 58000, "info": "62 HP - Υδροστατικό κιβώτιο ταχυτήτων, Καμπίνα"},
    "M5072N": {"cat": "Τρακτέρ", "series": "Σειρά M5002-NARROW - Stage V", "hp": 74, "price": 57500, "info": "74 HP - Ηλεκτρό-υδραυλική ρεβέρσα 36/36"},
    "M5-092N36-EC": {"cat": "Τρακτέρ", "series": "Σειρά M5002-NARROW - Stage V", "hp": 94, "price": 67500, "info": "94 HP - Ηλεκτρό-υδραυλική ρεβέρσα 36/36"},
    "M5-112NQ-EC": {"cat": "Τρακτέρ", "series": "Σειρά M5002-NARROW - Stage V", "hp": 115, "price": 78000, "info": "115 HP - Ηλεκτρό-υδραυλική ρεβέρσα 36/36"},
    "M4063 DTH": {"cat": "Τρακτέρ", "series": "Σειρά M4003 - Stage V", "hp": 66, "price": 47500, "info": "66 HP - Ηλεκτρο-υδραυλική ρεβέρσα 18/18"},
    "M4073 DTH": {"cat": "Τρακτέρ", "series": "Σειρά M4003 - Stage V", "hp": 74, "price": 51500, "info": "74 HP - Ηλεκτρο-υδραυλική ρεβέρσα 36/36"},
    "M5-092 DTH": {"cat": "Τρακτέρ", "series": "Σειρά M5002 - Stage V", "hp": 94, "price": 64500, "info": "94 HP - Ηλεκτρο-υδραυλική ρεβέρσα 36/36"},
    "M5-112 DTH": {"cat": "Τρακτέρ", "series": "Σειρά M5002 - Stage V", "hp": 107, "price": 65500, "info": "107 HP - Ηλεκτρο-υδραυλική ρεβέρσα 36/36"},
    "M6-121-DTC": {"cat": "Τρακτέρ", "series": "Σειρά M6 - Stage V", "hp": 131, "price": 89000, "info": "131 HP - Κιβώτιο Powershift, Καμπίνα"},
    "M6-141-DTC": {"cat": "Τρακτέρ", "series": "Σειρά M6 - Stage V", "hp": 142, "price": 96000, "info": "142 HP - Κιβώτιο Powershift, Καμπίνα"},
    "K008-5 VHG": {"cat": "Χωματουργικό", "series": "Μικροί Εκσκαφείς", "weight": "975 kg", "price": 15700, "info": "Βασική Αξία Εκσκαφέα 975 kg"},
    "U10-5 VHG": {"cat": "Χωματουργικό", "series": "Μικροί Εκσκαφείς", "weight": "1050 kg", "price": 17600, "info": "Βασική Αξία Εκσκαφέα 1050 kg"},
    "U27-4 HGL": {"cat": "Χωματουργικό", "series": "Εκσκαφείς Μεσαίας Κατηγορίας", "weight": "2490 kg", "price": 32800, "info": "Σκέπαστρο 2490 kg"},
    "KX060-5": {"cat": "Χωματουργικό", "series": "Εκσκαφείς Μεσαίας Κατηγορίας", "weight": "5555 kg", "price": 62000, "info": "5555 kg - Καμπίνα, Υδραυλική Ταχυσύνδεση"},

    # --- Μανέζ Λοζάνο (Manez Lozano) - Ψεκαστικά & Παρελκόμενα ---
    "NTW10S/4": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S4-S5", "price": 15400, "info": "Ψεκαστικό NARROW TW S4-S5 — Φτερωτή Ø 820 — 1000 λίτρα"},
    "NTW15S/5": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S4-S5", "price": 17700, "info": "Ψεκαστικό NARROW TW S4-S5 — Φτερωτή Ø 920 — 1500 λίτρα"},
    "NTW20S/5": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S4-S5", "price": 18600, "info": "Ψεκαστικό NARROW TW S4-S5 — Φτερωτή Ø 920 — 2000 λίτρα"},
    "NTW30S/5": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S4-S5", "price": 21900, "info": "Ψεκαστικό NARROW TW S4-S5 — Φτερωτή Ø 920 — 3000 λίτρα"},
    "NTW15S/6": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S6", "price": 18600, "info": "Ψεκαστικό NARROW TW S6 (NORMAL) — Φτερωτή Ø 920 — 1500 λίτρα"},
    "NTW20S/6": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S6", "price": 19600, "info": "Ψεκαστικό NARROW TW S6 (NORMAL) — Φτερωτή Ø 920 — 2000 λίτρα"},
    "NTW30S/6": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S6", "price": 22800, "info": "Ψεκαστικό NARROW TW S6 (NORMAL) — Φτερωτή Ø 920 — 3000 λίτρα"},
    "NTW15S/6TOP": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S6 TOP", "price": 20500, "info": "Ψεκαστικό NARROW TW S6 (TOP MANUAL) — Φτερωτή Ø 920 — 1500 λίτρα"},
    "NTW20S/6TOP": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S6 TOP", "price": 21300, "info": "Ψεκαστικό NARROW TW S6 (TOP MANUAL) — Φτερωτή Ø 920 — 2000 λίτρα"},
    "NTW30S/6TOP": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S6 TOP", "price": 24600, "info": "Ψεκαστικό NARROW TW S6 (TOP MANUAL) — Φτερωτή Ø 920 — 3000 λίτρα"},
    "NTW15S/6TOPH": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S6 TOPH", "price": 21200, "info": "Ψεκαστικό NARROW TW S6 (TOP ΥΔΡΑΥΛΙΚΟ) — Φτερωτή Ø 920 — 1500 λίτρα"},
    "NTW20S/6TOPH": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S6 TOPH", "price": 22000, "info": "Ψεκαστικό NARROW TW S6 (TOP ΥΔΡΑΥΛΙΚΟ) — Φτερωτή Ø 920 — 2000 λίτρα"},
    "NTW30S/6TOPH": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S6 TOPH", "price": 25300, "info": "Ψεκαστικό NARROW TW S6 (TOP ΥΔΡΑΥΛΙΚΟ) — Φτερωτή Ø 920 — 3000 λίτρα"},
    "NTWESP08": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW ESPALDERA", "price": 16400, "info": "Ψεκαστικό ESPALDERA — Φτερωτή Ø 720 — 1000 λίτρα"},
    "NTWESP10": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW ESPALDERA", "price": 16700, "info": "Ψεκαστικό ESPALDERA — Φτερωτή Ø 820 — 1000 λίτρα"},
    "NTWESP15": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW ESPALDERA", "price": 18600, "info": "Ψεκαστικό ESPALDERA — Φτερωτή Ø 820 — 1500 λίτρα"},
    "NTWESP20": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW ESPALDERA", "price": 19500, "info": "Ψεκαστικό ESPALDERA — Φτερωτή Ø 820 — 2000 λίτρα"},
    "NTWESP30": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW ESPALDERA", "price": 22800, "info": "Ψεκαστικό ESPALDERA — Φτερωτή Ø 820 — 3000 λίτρα"},
    "NTWESP209": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW ESPALDERA", "price": 20800, "info": "Ψεκαστικό ESPALDERA — Φτερωτή Ø 920 — 2000 λίτρα"},
    "NTWESP309": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW ESPALDERA", "price": 24000, "info": "Ψεκαστικό ESPALDERA — Φτερωτή Ø 920 — 3000 λίτρα"},
    "NTWMOON10": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW MOON", "price": 15700, "info": "Ψεκαστικό MOON — Φτερωτή Ø 820 — 1000 λίτρα"},
    "NTWMOON15": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW MOON", "price": 17100, "info": "Ψεκαστικό MOON — Φτερωτή Ø 820 — 1500 λίτρα"},
    "NTWMOON20/8": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW MOON", "price": 18000, "info": "Ψεκαστικό MOON — Φτερωτή Ø 820 — 2000 λίτρα"},
    "NTWMOON20": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW MOON", "price": 19700, "info": "Ψεκαστικό MOON — Φτερωτή Ø 920 — 2000 λίτρα"},
    "NTWMOON30": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW MOON", "price": 21700, "info": "Ψεκαστικό MOON — Φτερωτή Ø 920 — 3000 λίτρα"},
    "NTWTOWER20": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW TOWER DF", "price": 15700, "info": "Ψεκαστικό TOWER DF — Φτερωτή 2 X 720 — 2000 λίτρα"},
    "NTWTOWER30": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW TOWER DF", "price": 17100, "info": "Ψεκαστικό TOWER DF — Φτερωτή 2 X 720 — 3000 λίτρα"},
    "NTWTOWER20-S8": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S8", "price": 35600, "info": "Ψεκαστικό S8 — Φτερωτή Ø 920 — 2000 λίτρα"},
    "RANT720": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 390, "info": "Πλέγμα προστασίας από D720"},
    "RANT820": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 440, "info": "Πλέγμα προστασίας από D820"},
    "RANT920": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 500, "info": "Πλέγμα προστασίας από D920"},
    "FANTHO": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 180, "info": "Προστατευτικό φτερωτής (φύλλα)"},
    "PTWS/5": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 270, "info": "Προστατευτικά ακροφυσίων TW S5"},
    "PTWS/6": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 270, "info": "Προστατευτικά ακροφυσίων TW S6"},
    "PTWMOON": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 290, "info": "Προστατευτικά ακροφυσίων TW Moon"},
    "LARTREP": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 870, "info": "Σπαστή κοτσάνδουρα (1000-2000λ)"},
    "LARTREG": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 1100, "info": "Σπαστή κοτσάνδουρα (3000-4000λ)"},
    "LARTRAEP": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 870, "info": "Σπαστή κοτσάνδουρα με δαχτυλίδι (1000-2000λ)"},
    "LARTRAEG": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 1100, "info": "Σπαστή κοτσάνδουρα με δαχτυλίδι (3000-4000λ)"},
    "ADAPEA": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 350, "info": "Εξάρτημα / σύνδεσμος κοτσάνδουρας"},
    "LARTVEP": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 980, "info": "Σπαστό τιμόνι στα μπράτσα του ελκυστήρα (1000-2000λ)"},
    "LARTVEG": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 1210, "info": "Σπαστό τιμόνι στα μπράτσα του ελκυστήρα (3000-4000λ)"},
    "LFA+ET": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 870, "info": "Τρίγωνο σύνδεσης 3ων σημείων ελκυστήρα"},
    "DR261080": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 390, "info": "Χαμήλωμα με 26\"x12-12 (από 10.80/12)"},
    "DR261075": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 390, "info": "Χαμήλωμα με 26\"x12-12 (από 10.75/15)"},
    "DR341075": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 500, "info": "Ελαστικά 34/55-16\""},
    "DR111075": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 390, "info": "Ελαστικά 11.580/11 αντί για 10.75/15"},
    "DR4001075": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 650, "info": "Ελαστικά 400/60-15.5\""},
    "PARLIGHT": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 330, "info": "Προφυλακτήρας με φώτα"},
    "CFLIGHT": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 590, "info": "Κουτί + Φώτα"},
    "CVLIGHT": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 650, "info": "Κατασκευή για ESPALDERA για Κουτί & Φώτα"},
    "KITFRENR": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 770, "info": "Υδραυλικά φρένα με ρυθμιστική βαλβίδα"},
    "PMFRUTEP": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 650, "info": "Προμίξερ 1500-2000λ"},
    "PMFRUTEG": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 770, "info": "Προμίξερ 3000λ"},
    "SUSPBPAR": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 770, "info": "Ανάρτηση με σούστα"},
    "KITVALRP": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 590, "info": "Κιτ ηλεκτροβαλβίδα ρύθμισης πίεσης (ρύθμιση μέσα από την καμπίνα)"},
    "KON/OFF2+FLOW": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 1270, "info": "2-περιοχών ON-OFF ηλ.χειριστήριο με ροόμετρο"},
    "KON/OFF4+FLOW": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 1500, "info": "4-περιοχών ON-OFF ηλ.χειριστήριο με ροόμετρο"},
    "KITRONIC": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 2540, "info": "TRONIC-Ογκομετρικό χειριστήριο"},
    "KITSIST": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 2190, "info": "SITOMATIC χειριστήριο χωρίς ροόμετρο"},
    "FLOWMET": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 530, "info": "Ανοξείδωτο ροόμετρο (για SISTROMATIC)"},
    "4.0SCSTT": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 3690, "info": "SISTRONIC για λίτρα/στρέμμα"},
    "4.0SCSTTS": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 4610, "info": "SISTRONIC για λίτρα/στρέμμα + ανίχνευση κόμης (σόναρ)"},
    "4.0SCSTTISO": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 5190, "info": "SISTRONIC λίτρα/στρέμμα + ISOBUS"},
    "4.0SCSTTISO+S": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 6110, "info": "SISTRONIC λίτρα/στρέμμα + ISOBUS + Σόναρ"},
    "ABRBG": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": -580, "info": "Αλλαγή αντλίας από ML-A1-EP σε ML-A (χωρίς μειωτήρα)"},
    "ABRBP": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": -980, "info": "Αλλαγή αντλίας από ML-A1-EP σε ML-D"},

    # --- Νιούμπο (Niubo) - Καταστροφείς & Παρελκόμενα ---
    "TLG120": {"cat": "Νιούμπο", "series": "LIGHT", "price": 4150, "info": "Καταστροφέας LIGHT 1200mm — 320kg — 25-35 Hp"},
    "TLG140": {"cat": "Νιούμπο", "series": "LIGHT", "price": 4200, "info": "Καταστροφέας LIGHT 1400mm — 350kg — 25-35 Hp"},
    "TLG160": {"cat": "Νιούμπο", "series": "LIGHT", "price": 4300, "info": "Καταστροφέας LIGHT 1600mm — 370kg — 30-40 Hp"},
    "TLG180": {"cat": "Νιούμπο", "series": "LIGHT", "price": 4400, "info": "Καταστροφέας LIGHT 1800mm — 390kg — 35-50 Hp"},
    "NIUBO_HYD_LIGHT": {"cat": "Νιούμπο", "series": "LIGHT (Έξτρα)", "price": 310, "info": "Υδραυλική Μετατόπιση (για LIGHT)"},

    "TGD130": {"cat": "Νιούμπο", "series": "GLIDER (Ημιβαρέου Τύπου Σταθερός)", "price": 5100, "info": "Καταστροφέας GLIDER 1300mm — 420kg — 28-38 Hp"},
    "TGD160": {"cat": "Νιούμπο", "series": "GLIDER (Ημιβαρέου Τύπου Σταθερός)", "price": 5300, "info": "Καταστροφέας GLIDER 1600mm — 450kg — 48-58 Hp"},
    "TGD180": {"cat": "Νιούμπο", "series": "GLIDER (Ημιβαρέου Τύπου Σταθερός)", "price": 5500, "info": "Καταστροφέας GLIDER 1800mm — 480kg — 50-60 Hp"},
    "TGD200": {"cat": "Νιούμπο", "series": "GLIDER (Ημιβαρέου Τύπου Σταθερός)", "price": 5700, "info": "Καταστροφέας GLIDER 2000mm — 510kg — 55-65 Hp"},
    "NIUBO_HYD_GLIDER": {"cat": "Νιούμπο", "series": "GLIDER (Έξτρα)", "price": 260, "info": "Υδραυλική Μετατόπιση (για GLIDER)"},

    "TSP150": {"cat": "Νιούμπο", "series": "SPEED (Βαρέου Τύπου Σταθερός)", "price": 5550, "info": "Καταστροφέας SPEED 1500mm — 530kg — 38-48 Hp — Υδραυλική μετατόπιση STANDART"},
    "TSP180": {"cat": "Νιούμπο", "series": "SPEED (Βαρέου Τύπου Σταθερός)", "price": 5780, "info": "Καταστροφέας SPEED 1800mm — 600kg — 55-68 Hp — Υδραυλική μετατόπιση STANDART"},
    "TSP200": {"cat": "Νιούμπο", "series": "SPEED (Βαρέου Τύπου Σταθερός)", "price": 5890, "info": "Καταστροφέας SPEED 2000mm — 655kg — 65-70 Hp — Υδραυλική μετατόπιση STANDART"},
    "TSP220": {"cat": "Νιούμπο", "series": "SPEED (Βαρέου Τύπου Σταθερός)", "price": 6220, "info": "Καταστροφέας SPEED 2200mm — 705kg — 75-85 Hp — Υδραυλική μετατόπιση STANDART"},

    "TSPR150": {"cat": "Νιούμπο", "series": "SPEED REVERS (Βαρέου Τύπου Σταθερός)", "price": 6200, "info": "Καταστροφέας SPEED REVERS 1500mm — 530kg — 38-48 Hp"},
    "TSPR180": {"cat": "Νιούμπο", "series": "SPEED REVERS (Βαρέου Τύπου Σταθερός)", "price": 6430, "info": "Καταστροφέας SPEED REVERS 1800mm — 600kg — 55-68 Hp"},
    "TSPR200": {"cat": "Νιούμπο", "series": "SPEED REVERS (Βαρέου Τύπου Σταθερός)", "price": 6540, "info": "Καταστροφέας SPEED REVERS 2000mm — 655kg — 65-70 Hp"},
    "TSPR220": {"cat": "Νιούμπο", "series": "SPEED REVERS (Βαρέου Τύπου Σταθερός)", "price": 6870, "info": "Καταστροφέας SPEED REVERS 2200mm — 705kg — 75-85 Hp"},
    "NIUBO_TSR_SPEED": {"cat": "Νιούμπο", "series": "SPEED / SPEED REVERS (Έξτρα)", "price": 650, "info": "Διπλή Ζεύξη (TSR +40kg)"},

    "TDP140": {"cat": "Νιούμπο", "series": "DRAGON PLUS", "price": 5800, "info": "Καταστροφέας DRAGON PLUS 1400mm — 525kg — 40-60 Hp — Υδραυλική μετατόπιση & πόρτα με διπλή μπουκάλα"},
    "TDP160": {"cat": "Νιούμπο", "series": "DRAGON PLUS", "price": 6000, "info": "Καταστροφέας DRAGON PLUS 1600mm — 550kg — 40-60 Hp — Υδραυλική μετατόπιση & πόρτα με διπλή μπουκάλα"},
    "TDP180": {"cat": "Νιούμπο", "series": "DRAGON PLUS", "price": 6200, "info": "Καταστροφέας DRAGON PLUS 1800mm — 575kg — 40-60 Hp — Υδραυλική μετατόπιση & πόρτα με διπλή μπουκάλα"},

    "TKM130": {"cat": "Νιούμπο", "series": "KOMPACT (Βαρέου Τύπου Υδραυλικός Χαμηλός 49cm)", "price": 7800, "info": "Καταστροφέας KOMPACT 1300mm — 530kg — 38-48 Hp"},
    "TKM150": {"cat": "Νιούμπο", "series": "KOMPACT (Βαρέου Τύπου Υδραυλικός Χαμηλός 49cm)", "price": 7900, "info": "Καταστροφέας KOMPACT 1500mm — 570kg — 48-58 Hp"},
    "TKM160": {"cat": "Νιούμπο", "series": "KOMPACT (Βαρέου Τύπου Υδραυλικός Χαμηλός 49cm)", "price": 7950, "info": "Καταστροφέας KOMPACT 1600mm — 605kg — 55-68 Hp"},
    "TKM180": {"cat": "Νιούμπο", "series": "KOMPACT (Βαρέου Τύπου Υδραυλικός Χαμηλός 49cm)", "price": 8200, "info": "Καταστροφέας KOMPACT 1800mm — 640kg — 65-70 Hp"},
    "TKM200": {"cat": "Νιούμπο", "series": "KOMPACT (Βαρέου Τύπου Υδραυλικός Χαμηλός 49cm)", "price": 8400, "info": "Καταστροφέας KOMPACT 2000mm — 695kg — 70-85 Hp"},
    "TKM220": {"cat": "Νιούμπο", "series": "KOMPACT (Βαρέου Τύπου Υδραυλικός Χαμηλός 49cm)", "price": 8700, "info": "Καταστροφέας KOMPACT 2200mm — 745kg — 85-90 Hp"},
    "TKM250": {"cat": "Νιούμπο", "series": "KOMPACT (Βαρέου Τύπου Υδραυλικός Χαμηλός 49cm)", "price": 8900, "info": "Καταστροφέας KOMPACT 2500mm — 830kg — 90-95 Hp"},
    "NIUBO_KOMPACT_DOOR": {"cat": "Νιούμπο", "series": "KOMPACT (Έξτρα)", "price": 750, "info": "Υδραυλική Ανοιγόμενη Πίσω Πόρτα"},

    "TXM150": {"cat": "Νιούμπο", "series": "MAX FRUIT", "price": 15200, "info": "Καταστροφέας MAX FRUIT 1460mm — 960kg — 70-100 Hp"},
    "TXM175": {"cat": "Νιούμπο", "series": "MAX FRUIT", "price": 15900, "info": "Καταστροφέας MAX FRUIT 1730mm — 1070kg — 90-100 Hp"},
    "TXM200": {"cat": "Νιούμπο", "series": "MAX FRUIT", "price": 16600, "info": "Καταστροφέας MAX FRUIT 2000mm — 1180kg — 90-110 Hp"},
    "NIUBO_MAXFRUIT_DOUBLE": {"cat": "Νιούμπο", "series": "MAX FRUIT (Έξτρα)", "price": 1980, "info": "Διπλή Ζεύξη 540"},
    "NIUBO_MAXFRUIT_LIFT": {"cat": "Νιούμπο", "series": "MAX FRUIT (Έξτρα)", "price": 1320, "info": "Ακτίνες Ανύψωσης"},

    "TJE160": {"cat": "Νιούμπο", "series": "JOLLY-E (Εξωτερικό Group)", "price": 8850, "info": "Καταστροφέας JOLLY-E 1600mm — 615kg — 40-90 Hp"},
    "TJE180": {"cat": "Νιούμπο", "series": "JOLLY-E (Εξωτερικό Group)", "price": 8960, "info": "Καταστροφέας JOLLY-E 1800mm — 645kg — 40-90 Hp"},
    "TJE200": {"cat": "Νιούμπο", "series": "JOLLY-E (Εξωτερικό Group)", "price": 9630, "info": "Καταστροφέας JOLLY-E 2000mm — 675kg — 50-100 Hp"},
    "NIUBO_JOLLY_VALVE": {"cat": "Νιούμπο", "series": "JOLLY-E (Προαιρετικός Εξοπλισμός)", "price": 380, "info": "Βαλβίδα Ασφαλείας"},
    "NIUBO_JOLLY_SHAFT1": {"cat": "Νιούμπο", "series": "JOLLY-E (Προαιρετικός Εξοπλισμός)", "price": 800, "info": "Ομοκινητικός Άξονας Μεγάλης Γωνίας"},
    "NIUBO_JOLLY_SHAFT2": {"cat": "Νιούμπο", "series": "JOLLY-E (Προαιρετικός Εξοπλισμός)", "price": 1220, "info": "Ομοκινητικός Άξονας Διπλής Μεγάλης Γωνίας"},
    "NIUBO_JOLLY_CTRL": {"cat": "Νιούμπο", "series": "JOLLY-E (Προαιρετικός Εξοπλισμός)", "price": 1350, "info": "Ηλεκτρικό Χειριστήριο 2 Κινήσεων"}
}

# Συνάρτηση αυτόματης μετάφρασης χαρακτηριστικών και σειρών στα Αγγλικά
def translate_info(text, is_en):
    if not is_en:
        return text
    
    translations_map = {
        "Υδροστατικό κιβώτιο ταχυτήτων, Καμπίνα": "Hydrostatic transmission, Cabin",
        "Υδροστατικό κιβώτιο ταχυτήτων, ROPS": "Hydrostatic transmission, ROPS",
        "Υδροστατικό, Καμπίνα": "Hydrostatic, Cabin",
        "Ηλεκτρό-υδραυλική ρεβέρσα 36/36": "Electro-hydraulic reverser 36/36",
        "Ηλεκτρο-υδραυλική ρεβέρσα 36/36": "Electro-hydraulic reverser 36/36",
        "Ηλεκτρο-υδραυλική ρεβέρσα 18/18": "Electro-hydraulic reverser 18/18",
        "Βασική Αξία Εκσκαφέα 975 kg": "Basic Excavator Value 975 kg",
        "Βασική Αξία Εκσκαφέα 1050 kg": "Basic Excavator Value 1050 kg",
        "Σκέπαστρο 2490 kg": "Canopy 2490 kg",
        "Καμπίνα, Υδραυλική Ταχυσύνδεση": "Cabin, Hydraulic Quick Coupler",
        "Σειρά B1 - Stage V": "B1 Series - Stage V",
        "Σειρά B2 - Stage V": "B2 Series - Stage V",
        "Σειρά LX - Stage V": "LX Series - Stage V",
        "Νέα Σειρά L2 - Stage V": "New L2 Series - Stage V",
        "Σειρά M5002-NARROW - Stage V": "M5002-NARROW Series - Stage V",
        "Σειρά M4003 - Stage V": "M4003 Series - Stage V",
        "Σειρά M5002 - Stage V": "M5002 Series - Stage V",
        "Σειρά M6 - Stage V": "M6 Series - Stage V",
        "Μικροί Εκσκαφείς": "Mini Excavators",
        "Εκσκαφείς Μεσαίας Κατηγορίας": "Mid-Size Excavators",
        "Παρελκόμενα & Αξεσουάρ": "Accessories & Options",
        "Νιούμπο": "Niubo"
    }
    
    for gr_term, en_term in translations_map.items():
        text = text.replace(gr_term, en_term)
    return text

# Καταχώρηση Γραμματοσειρών με υποστήριξη πεζών/κεφαλαίων για Streamlit Cloud
def register_fonts():
    registered = pdfmetrics.getRegisteredFontNames()

    # 1. Times New Roman (Πετρόπουλος)
    if 'WinTimes' not in registered:
        for f, fb in [("times.ttf", "timesbd.ttf"), ("TIMES.TTF", "TIMESBD.TTF"), ("Times.ttf", "Timesbd.ttf")]:
            if os.path.exists(f) and os.path.exists(fb):
                pdfmetrics.registerFont(TTFont('WinTimes', f))
                pdfmetrics.registerFont(TTFont('WinTimes-Bold', fb))
                break
        else:
            if os.path.exists("C:/Windows/Fonts/times.ttf"):
                pdfmetrics.registerFont(TTFont('WinTimes', 'C:/Windows/Fonts/times.ttf'))
                pdfmetrics.registerFont(TTFont('WinTimes-Bold', 'C:/Windows/Fonts/timesbd.ttf'))

    # 2. Arial (Φίλης)
    if 'WinArial' not in registered:
        for f, fb in [("arial.ttf", "arialbd.ttf"), ("ARIAL.TTF", "ARIALBD.TTF"), ("Arial.ttf", "Arialbd.ttf")]:
            if os.path.exists(f) and os.path.exists(fb):
                pdfmetrics.registerFont(TTFont('WinArial', f))
                pdfmetrics.registerFont(TTFont('WinArial-Bold', fb))
                break
        else:
            if os.path.exists("C:/Windows/Fonts/arial.ttf"):
                pdfmetrics.registerFont(TTFont('WinArial', 'C:/Windows/Fonts/arial.ttf'))
                pdfmetrics.registerFont(TTFont('WinArial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))

    # 3. Verdana (Κάμπος)
    if 'WinVerdana' not in registered:
        for f, fb in [("verdana.ttf", "verdanab.ttf"), ("VERDANA.TTF", "VERDANAB.TTF"), ("Verdana.ttf", "Verdanab.ttf")]:
            if os.path.exists(f) and os.path.exists(fb):
                pdfmetrics.registerFont(TTFont('WinVerdana', f))
                pdfmetrics.registerFont(TTFont('WinVerdana-Bold', fb))
                break
        else:
            if os.path.exists("C:/Windows/Fonts/verdana.ttf"):
                pdfmetrics.registerFont(TTFont('WinVerdana', 'C:/Windows/Fonts/verdana.ttf'))
                pdfmetrics.registerFont(TTFont('WinVerdana-Bold', 'C:/Windows/Fonts/verdanab.ttf'))

# Επιλογή γραμματοσειράς βάσει εταιρείας
def get_company_fonts(company):
    register_fonts()
    registered = pdfmetrics.getRegisteredFontNames()
    
    if company in ["Πετρόπουλος", "Petropoulos"]:
        reg = 'WinTimes' if 'WinTimes' in registered else 'WinArial'
        bld = 'WinTimes-Bold' if 'WinTimes-Bold' in registered else 'WinArial-Bold'
    elif company in ["Φίλης", "Filis"]:
        reg = 'WinArial' if 'WinArial' in registered else 'WinTimes'
        bld = 'WinArial-Bold' if 'WinArial-Bold' in registered else 'WinTimes-Bold'
    else:
        reg = 'WinVerdana' if 'WinVerdana' in registered else ('WinArial' if 'WinArial' in registered else 'WinTimes')
        bld = 'WinVerdana-Bold' if 'WinVerdana-Bold' in registered else ('WinArial-Bold' if 'WinArial-Bold' in registered else 'WinTimes-Bold')
        
    return reg, bld

if "cart" not in st.session_state:
    st.session_state.cart = []

def generate_pdf_bytes(client_data, cart_items, company, is_english):
    pdf_filename = "temp_profora.pdf"
    
    font_reg, font_bld = get_company_fonts(company)

    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter
    
    if is_english:
        comp_display = "Petropoulos" if company == "Πετρόπουλος" else ("Filis" if company == "Φίλης" else "Kampos")
    else:
        comp_display = company

    if company in ["Πετρόπουλος", "Petropoulos"]:
        logo_path = "petropoulos_logo.jpeg"
        if os.path.exists(logo_path):
            c.drawImage(logo_path, width - 180, height - 70, width=130, height=45, preserveAspectRatio=True, mask='auto')

    # Επικεφαλίδα Εταιρείας (Χωρίς τη λέξη "ΕΤΑΙΡΕΙΑ:")
    c.setFont(font_bld, 16)
    c.drawString(50, height - 50, comp_display)
    
    c.setFont(font_reg, 10)
    dept_label = "Agricultural & Construction Machinery Department" if is_english else "Τμήμα Γεωργικών & Χωματουργικών Μηχανημάτων Kubota"
    c.drawString(50, height - 65, dept_label)
    
    c.setStrokeColorRGB(0.2, 0.3, 0.5)
    c.setLineWidth(1)
    c.line(50, height - 75, width - 50, height - 75)
    
    # Στοιχεία Πελάτη
    c.setFont(font_bld, 12)
    c.drawString(50, height - 100, "CLIENT DETAILS:" if is_english else "ΣΤΟΙΧΕΙΑ ΠΕΛΑΤΗ:")
    c.setFont(font_reg, 10)
    y_client = height - 118
    c.drawString(50, y_client, f"{'Name' if is_english else 'Ονοματεπώνυμο / Επωνυμία'}: {client_data['name']}")
    y_client -= 16
    c.drawString(50, y_client, f"{'Profession' if is_english else 'Επάγγελμα'}: {client_data['profession']}")
    y_client -= 16
    c.drawString(50, y_client, f"{'VAT No' if is_english else 'ΑΦΜ'}: {client_data['afm']}")
    y_client -= 16
    c.drawString(50, y_client, f"{'Phone' if is_english else 'Τηλέφωνο'}: {client_data['phone']}")
    y_client -= 16
    c.drawString(50, y_client, f"{'Address' if is_english else 'Διεύθυνση'}: {client_data['address']}")
        
    y_client -= 12
    c.setStrokeColorRGB(0.7, 0.7, 0.7)
    c.setLineWidth(0.5)
    c.line(50, y_client, width - 50, y_client)
    
    # Τίτλος Προσφοράς
    y = y_client - 25
    c.setFont(font_bld, 13)
    c.drawString(50, y, "COMMERCIAL OFFER" if is_english else "ΟΙΚΟΝΟΜΙΚΗ ΠΡΟΣΦΟΡΑ")
    
    y -= 22
    c.setFont(font_reg, 10)
    greet_text = f"Dear {client_data['name']}," if is_english else f"Αξιότιμε/η κ. {client_data['name']}, σας αποστέλλουμε την προσφορά μας:"
    c.drawString(50, y, greet_text)
    
    y -= 15
    total_net = 0
    
    for idx, item in enumerate(cart_items, 1):
        translated_info = translate_info(item['info'], is_english)
        if is_english:
            if item["cat"] == "Τρακτέρ":
                noun = "KUBOTA tractor"
                cat_display = "Tractor"
            elif item["cat"] == "Χωματουργικό":
                noun = "KUBOTA excavator"
                cat_display = "Excavator"
            elif item["cat"] == "Μανέζ Λοζάνο":
                noun = "MANEZ LOZANO equipment"
                cat_display = "Manez Lozano"
            else:
                noun = "NIUBO equipment"
                cat_display = "Niubo"
            desc_text = f"A brand new and unused {noun} ({translated_info})"
        else:
            if item["cat"] == "Τρακτέρ":
                noun = "ελκυστήρα KUBOTA"
            elif item["cat"] == "Χωματουργικό":
                noun = "εκσκαφέα KUBOTA"
            elif item["cat"] == "Μανέζ Λοζάνο":
                noun = "εξοπλισμού MANEZ LOZANO"
            else:
                noun = "μηχανήματος NIUBO"
            
            if "Έξτρα" in item['series'] or "Προαιρετικός" in item['series'] or item['series'] == "Παρελκόμενα & Αξεσουάρ":
                desc_text = f"Εξάρτημα / Παρελκόμενο {item['cat']}: {translated_info}"
            else:
                desc_text = f"Ένα καινούριο και αμεταχειριστό {noun} ({translated_info})"
            cat_display = item["cat"]
        
        y -= 20
        c.setFont(font_bld, 10)
        net_lbl = "Net Value" if is_english else "Καθαρή Αξία"
        c.drawString(50, y, f"{idx}. {cat_display} | Model: {item['model']} — {net_lbl}: {item['price']:,.2f} EUR")
        
        y -= 15
        c.setFont(font_reg, 10)
        c.drawString(70, y, desc_text)
        
        total_net += item['price']
        
        if y < 120:
            c.showPage()
            y = height - 50

    vat = total_net * 0.24
    total_with_vat = total_net + vat
    
    y -= 25
    c.setStrokeColorRGB(0.2, 0.3, 0.5)
    c.setLineWidth(1)
    c.line(50, y + 15, width - 50, y + 15)
    
    c.setFont(font_reg, 10)
    c.drawString(50, y, f"{'Total Net Value' if is_english else 'Συνολική Καθαρή Αξία'}: {total_net:,.2f} EUR")
    y -= 18
    c.drawString(50, y, f"{'VAT (24%)' if is_english else 'ΦΠΑ (24%)'}: {vat:,.2f} EUR")
    y -= 20
    c.setFont(font_bld, 12)
    c.drawString(50, y, f"{'GRAND TOTAL WITH VAT' if is_english else 'ΓΕΝΙΚΟ ΣΥΝΟΛΟ ΜΕ ΦΠΑ'}: {total_with_vat:,.2f} EUR")
    
    y -= 35
    c.setFont(font_reg, 10)
    close_text = f"At your disposal for any clarification from {comp_display}!" if is_english else f"Στη διάθεσή σας για οποιαδήποτε διευκρίνιση από την εταιρεία {comp_display}!"
    c.drawString(50, y, close_text)
    
    c.save()
    
    with open(pdf_filename, "rb") as f:
        pdf_data = f.read()
    return pdf_data

# ΕΜΦΑΝΙΣΗ ΣΤΟ UI
st.title("🚜 " + ("Kubota Quotation System" if is_english else "Σύστημα Προσφορών Kubota"))
st.markdown("Create commercial quotes easily!" if is_english else "Δημιουργήστε οικονομικές προσφορές εύκολα από το PC ή το κινητό σας!")

# 1. Στοιχεία Πελάτη
with st.expander("👤 " + ("1. Client Details (All Mandatory)" if is_english else "1. Στοιχεία Πελάτη (Υποχρεωτικά Όλα)"), expanded=True):
    company_options = ["Πετρόπουλος", "Φίλης", "Κάμπος"]
    if is_english:
        company_ui = st.selectbox("Company / Εταιρεία", ["Petropoulos", "Filis", "Kampos"])
        company = "Πετρόπουλος" if company_ui == "Petropoulos" else ("Φίλης" if company_ui == "Filis" else "Κάμπος")
    else:
        company = st.selectbox("Company / Εταιρεία", company_options)

    client_name = st.text_input("Client Name / Όνομα Πελάτη")
    client_profession = st.text_input("Profession / Επάγγελμα")
    col1, col2 = st.columns(2)
    with col1:
        client_afm = st.text_input("VAT No / ΑΦΜ")
    with col2:
        client_phone = st.text_input("Phone / Τηλέφωνο")
    client_address = st.text_input("Address / Διεύθυνση")

# 2. Επιλογή Προϊόντος & Χαρακτηριστικά
with st.expander("⚙️ " + ("2. Product Selection & Features" if is_english else "2. Επιλογή Προϊόντος & Χαρακτηριστικά"), expanded=True):
    raw_categories = sorted(list(set(item["cat"] for item in database.values())))
    if is_english:
        cat_map = {"Τρακτέρ": "Tractor", "Χωματουργικό": "Excavator", "Μανέζ Λοζάνο": "Manez Lozano", "Νιούμπο": "Niubo"}
        categories = [cat_map.get(c, c) for c in raw_categories]
    else:
        categories = raw_categories
        
    selected_cat_ui = st.selectbox("Category / Κατηγορία", categories)
    
    if is_english:
        inv_cat_map = {"Tractor": "Τρακτέρ", "Excavator": "Χωματουργικό", "Manez Lozano": "Μανέζ Λοζάνο", "Niubo": "Νιούμπο"}
        selected_cat = inv_cat_map.get(selected_cat_ui, selected_cat_ui)
    else:
        selected_cat = selected_cat_ui
    
    series_list = sorted(list(set(item["series"] for item in database.values() if item["cat"] == selected_cat)))
    if is_english:
        display_series_list = [translate_info(s, True) for s in series_list]
    else:
        display_series_list = series_list
        
    selected_series_ui = st.selectbox("Series / Σειρά", display_series_list)
    selected_series = series_list[display_series_list.index(selected_series_ui)]
    
    model_list = [model for model, item in database.items() if item["cat"] == selected_cat and item["series"] == selected_series]
    selected_model = st.selectbox("Model / Μοντέλο", model_list)
    
    if selected_model:
        current_item = database[selected_model]
        default_info = translate_info(current_item["info"], is_english)
        st.markdown(f"**{'Model Price' if is_english else 'Τιμή Μοντέλου'}:** :red[{current_item['price']:,.2f} EUR]")
        custom_info = st.text_input("Description / Info / Περιγραφή", value=default_info)
    else:
        custom_info = ""

    if st.button("➕ " + ("Add to Quote" if is_english else "Προσθήκη στην Προσφορά")):
        if selected_model:
            st.session_state.cart.append({
                "model": selected_model,
                "cat": current_item["cat"],
                "series": current_item["series"],
                "price": current_item["price"],
                "info": custom_info if custom_info else current_item["info"]
            })
            st.success("Product added!" if is_english else f"Το προϊόν {selected_model} προστέθηκε στην προσφορά!")
        else:
            st.error("Select valid model." if is_english else "Επιλέξτε έγκυρο μοντέλο.")

# 3. Επιλεγμένα Είδη Προσφοράς
with st.expander("🛒 " + ("3. Selected Quote Items" if is_english else "3. Επιλεγμένα Είδη Προσφοράς"), expanded=True):
    if st.session_state.cart:
        for idx, cart_item in enumerate(st.session_state.cart):
            if is_english:
                display_cat = "Tractor" if cart_item['cat'] == "Τρακτέρ" else ("Excavator" if cart_item['cat'] == "Χωματουργικό" else ("Manez Lozano" if cart_item['cat'] == "Μανέζ Λοζάνο" else "Niubo"))
            else:
                display_cat = cart_item['cat']
                
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.write(f"**{idx+1}. {display_cat} | {cart_item['model']}** — {cart_item['price']:,.2f} EUR")
            with col_b:
                if st.button("❌", key=f"del_{idx}"):
                    st.session_state.cart.pop(idx)
                    st.rerun()
        
        if st.button("🗑️ " + ("Clear Cart" if is_english else "Εκκαθάριση Καλαθιού")):
            st.session_state.cart = []
            st.rerun()
    else:
        st.info("Cart is empty." if is_english else "Το καλάθι είναι κενό.")

# Δημιουργία PDF
st.markdown("---")
if st.button("📄 " + ("Generate Summary PDF" if is_english else "Δημιουργία Συγκεντρωτικού PDF"), type="primary", use_container_width=True):
    if not client_name:
        st.warning("Please fill in the client's name!" if is_english else "Παρακαλώ συμπληρώστε το όνομα του πελάτη!")
    elif not client_profession:
        st.warning("Please fill in the profession!" if is_english else "Παρακαλώ συμπληρώστε το επάγγελμα του πελάτη!")
    elif not client_afm:
        st.warning("Please fill in the VAT No!" if is_english else "Παρακαλώ συμπληρώστε το ΑΦΜ του πελάτη!")
    elif not client_phone:
        st.warning("Please fill in the phone!" if is_english else "Παρακαλώ συμπληρώστε το τηλέφωνο του πελάτη!")
    elif not client_address:
        st.warning("Please fill in the address!" if is_english else "Παρακαλώ συμπληρώστε τη διεύθυνση του πελάτη!")
    elif not st.session_state.cart:
        st.warning("The cart is empty!" if is_english else "Το καλάθι προσφοράς είναι κενό! Προσθέστε τουλάχιστον ένα προϊόν.")
    else:
        client_data = {
            "name": client_name,
            "profession": client_profession,
            "afm": client_afm,
            "phone": client_phone,
            "address": client_address
        }
        pdf_data = generate_pdf_bytes(client_data, st.session_state.cart, company, is_english)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_company = (company if not is_english else ("Petropoulos" if company == "Πετρόπουλος" else ("Filis" if company == "Φίλης" else "Kampos"))).replace(" ", "_")
        safe_client = client_name.replace(" ", "_")
        pdf_filename = f"Profora_{safe_company}_{safe_client}_{timestamp}.pdf"
        
        st.download_button(
            label="📥 " + ("Download PDF File" if is_english else "Λήψη Αρχείου PDF"),
            data=pdf_data,
            file_name=pdf_filename,
            mime="application/pdf",
            use_container_width=True
        )
        