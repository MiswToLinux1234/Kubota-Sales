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

# ΠΛΗΡΗΣ ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ (Kubota + Manez Lozano + Niubo + ID DAVID)
database = {
    # --- Κουμπότα (Τρακτέρ & Χωματουργικά) ---
    "B1181D-EC": {"cat": "Τρακτέρ", "series": "Σειρά B1 - Stage V", "hp": 17, "price": 14500, "info": "17 HP - Σειρά B1", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα εργοστασίου κατασκευής KUBOTA Ιαπωνίας τύπου B1181D-EC."},
    "B1241D-EC": {"cat": "Τρακτέρ", "series": "Σειρά B1 - Stage V", "hp": 22, "price": 15500, "info": "22 HP - Mid ROPS", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα εργοστασίου κατασκευής KUBOTA Ιαπωνίας τύπου B1241D-EC με αψίδα προστασίας εγκεκριμένου τύπου."},
    "B2261DB-M5-S5": {"cat": "Τρακτέρ", "series": "Σειρά B2 - Stage V", "hp": 25, "price": 17500, "info": "25 HP - Σειρά B2", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα εργοστασίου κατασκευής KUBOTA Ιαπωνίας τύπου B2261DB-M5-S5."},
    "B2261 HDB-C-S5": {"cat": "Τρακτέρ", "series": "Σειρά B2 - Stage V", "hp": 25, "price": 27000, "info": "25 HP - Υδροστατικό, Καμπίνα", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA B2261 HDB-C-S5 με υδροστατικό κιβώτιο ταχυτήτων και εργοστασιακή καμπίνα."},
    "LX351-F-R": {"cat": "Τρακτέρ", "series": "Σειρά LX - Stage V", "hp": 35, "price": 33500, "info": "35 HP - Υδροστατικό κιβώτιο ταχυτήτων, ROPS", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA LX351-F-R με υδροστατικό κιβώτιο ταχυτήτων και ROPS."},
    "LX351-M": {"cat": "Τρακτέρ", "series": "Σειρά LX - Stage V", "hp": 35, "price": 29500, "info": "35 HP - 12/12 Mid ROPS", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA LX351-M 12/12."},
    "LX351-C-R": {"cat": "Τρακτέρ", "series": "Σειρά LX - Stage V", "hp": 35, "price": 40000, "info": "35 HP - Υδροστατικό κιβώτιο ταχυτήτων, Καμπίνα", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA LX351-C-R με καμπίνα."},
    "LX401-F-R": {"cat": "Τρακτέρ", "series": "Σειρά LX - Stage V", "hp": 40, "price": 43500, "info": "40 HP - Υδροστατικό κιβώτιο ταχυτήτων, ROPS", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA LX401-F-R."},
    "LX401-C-R": {"cat": "Τρακτέρ", "series": "Σειρά LX - Stage V", "hp": 40, "price": 50000, "info": "40 HP - Υδροστατικό κιβώτιο ταχυτήτων, Καμπίνα", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA LX401-C-R με καμπίνα."},
    "L2372DM": {"cat": "Τρακτέρ", "series": "Νέα Σειρά L2 - Stage V", "hp": 37, "price": 35500, "info": "37 HP - (16/16)", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA L2372DM (16/16)."},
    "L2452DM": {"cat": "Τρακτέρ", "series": "Νέα Σειρά L2 - Stage V", "hp": 45, "price": 36500, "info": "45 HP - (16/16)", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA L2452DM (16/16)."},
    "L2522DM": {"cat": "Τρακτέρ", "series": "Νέα Σειρά L2 - Stage V", "hp": 52, "price": 37500, "info": "52 HP - (16/16)", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA L2522DM (16/16)."},
    "L2452DHC": {"cat": "Τρακτέρ", "series": "Νέα Σειρά L2 - Stage V", "hp": 47, "price": 45000, "info": "47 HP - Υδροστατικό κιβώτιο ταχυτήτων, Καμπίνα", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA L2452DHC με καμπίνα."},
    "L2552DHC": {"cat": "Τρακτέρ", "series": "Νέα Σειρά L2 - Stage V", "hp": 54, "price": 50000, "info": "54 HP - Υδροστατικό κιβώτιο ταχυτήτων, Καμπίνα", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA L2552DHC με καμπίνα."},
    "L2622DHC": {"cat": "Τρακτέρ", "series": "Νέα Σειρά L2 - Stage V", "hp": 62, "price": 58000, "info": "62 HP - Υδροστατικό κιβώτιο ταχυτήτων, Καμπίνα", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA L2622DHC με καμπίνα."},
    "M5072N": {"cat": "Τρακτέρ", "series": "Σειρά M5002-NARROW - Stage V", "hp": 74, "price": 57500, "info": "74 HP - Ηλεκτρό-υδραυλική ρεβέρσα 36/36", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M5072N."},
    "M5-092N36-EC": {"cat": "Τρακτέρ", "series": "Σειρά M5002-NARROW - Stage V", "hp": 94, "price": 67500, "info": "94 HP - Ηλεκτρό-υδραυλική ρεβέρσα 36/36", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα εργοστασίου κατασκευής KUBOTA Ιαπωνίας τύπου M5092N36-EC με αψίδα προστασίας εγκεκριμένου τύπου. Διαθέτει διπλό διαφορικό, τετρακύλινδρο κινητήρα diesel κατηγορίας ρύπων φάση V, υδρόψυκτο, με ισχύ κινητήρα 94hp, σασμάν 6 ταχυτήτων με 3 ομάδες και Hi-Lo συνολικών ταχυτήτων 36/36 (εμπρός/πίσω). Ηλεκτρο-υδραυλική ρεβέρσα, ηλεκτρο-υδραυλική εμπλοκή μπροστινού διαφορικού και ηλεκτρο-υδραυλική ενεργοποίηση δυναμοδότη (PTO). 2 μνήμες στροφών και σύστημα σταθεροποίησης στροφών."},
    "M5-112NQ-EC": {"cat": "Τρακτέρ", "series": "Σειρά M5002-NARROW - Stage V", "hp": 115, "price": 78000, "info": "115 HP - Ηλεκτρό-υδραυλική ρεβέρσα 36/36", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M5-112NQ-EC."},
    "M4063 DTH": {"cat": "Τρακτέρ", "series": "Σειρά M4003 - Stage V", "hp": 66, "price": 47500, "info": "66 HP - Ηλεκτρο-υδραυλική ρεβέρσα 18/18", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M4063 DTH."},
    "M4073 DTH": {"cat": "Τρακτέρ", "series": "Σειρά M4003 - Stage V", "hp": 74, "price": 51500, "info": "74 HP - Ηλεκτρο-υδραυλική ρεβέρσα 36/36", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M4073 DTH."},
    "M5-092 DTH": {"cat": "Τρακτέρ", "series": "Σειρά M5002 - Stage V", "hp": 94, "price": 64500, "info": "94 HP - Ηλεκτρο-υδραυλική ρεβέρσα 36/36", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M5-092 DTH."},
    "M5-112 DTH": {"cat": "Τρακτέρ", "series": "Σειρά M5002 - Stage V", "hp": 107, "price": 65500, "info": "107 HP - Ηλεκτρο-υδραυλική ρεβέρσα 36/36", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M5-112 DTH."},
    "M6-121-DTC": {"cat": "Τρακτέρ", "series": "Σειρά M6 - Stage V", "hp": 131, "price": 89000, "info": "131 HP - Κιβώτιο Powershift, Καμπίνα", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M6-121-DTC."},
    "M6-141-DTC": {"cat": "Τρακτέρ", "series": "Σειρά M6 - Stage V", "hp": 142, "price": 96000, "info": "142 HP - Κιβώτιο Powershift, Καμπίνα", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M6-141-DTC."},
    "K008-5 VHG": {"cat": "Χωματουργικό", "series": "Μικροί Εκσκαφείς", "weight": "975 kg", "price": 15700, "info": "Βασική Αξία Εκσκαφέα 975 kg", "desc": "Ένα καινούριο και αμεταχειριστό χωματουργικό μηχάνημα KUBOTA K008-5."},
    "U10-5 VHG": {"cat": "Χωματουργικό", "series": "Μικροί Εκσκαφείς", "weight": "1050 kg", "price": 17600, "info": "Βασική Αξία Εκσκαφέα 1050 kg", "desc": "Ένα καινούριο και αμεταχειριστό χωματουργικό μηχάνημα KUBOTA U10-5."},
    "U27-4 HGL": {"cat": "Χωματουργικό", "series": "Εκσκαφείς Μεσαίας Κατηγορίας", "weight": "2490 kg", "price": 32800, "info": "Σκέπαστρο 2490 kg", "desc": "Ένα καινούριο και αμεταχειριστό χωματουργικό μηχάνημα KUBOTA U27-4."},
    "KX060-5": {"cat": "Χωματουργικό", "series": "Εκσκαφείς Μεσαίας Κατηγορίας", "weight": "5555 kg", "price": 62000, "info": "5555 kg - Καμπίνα, Υδραυλική Ταχυσύνδεση", "desc": "Ένα καινούριο και αμεταχειριστό χωματουργικό μηχάνημα KUBOTA KX060-5."},

    # --- Μανέζ Λοζάνο (Manez Lozano) - Ψεκαστικά & Παρελκόμενα ---
    "NTW10S/4": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S4-S5", "price": 15400, "info": "Ψεκαστικό NARROW TW S4-S5 — Φτερωτή Ø 820 — 1000 λίτρα", "desc": "Ψεκαστικό NARROW TW S4-S5 — Φτερωτή Ø 820 — 1000 λίτρα."},
    "NTW15S/5": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S4-S5", "price": 17700, "info": "Ψεκαστικό NARROW TW S4-S5 — Φτερωτή Ø 920 — 1500 λίτρα", "desc": "Ψεκαστικό NARROW TW S4-S5 — Φτερωτή Ø 920 — 1500 λίτρα."},
    "NTW20S/5": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S4-S5", "price": 18600, "info": "Ψεκαστικό NARROW TW S4-S5 — Φτερωτή Ø 920 — 2000 λίτρα", "desc": "Ψεκαστικό NARROW TW S4-S5 — Φτερωτή Ø 920 — 2000 λίτρα."},
    "NTW30S/5": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S4-S5", "price": 21900, "info": "Ψεκαστικό NARROW TW S4-S5 — Φτερωτή Ø 920 — 3000 λίτρα", "desc": "Ψεκαστικό NARROW TW S4-S5 — Φτερωτή Ø 920 — 3000 λίτρα."},
    "NTW15S/6": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S6", "price": 18600, "info": "Ψεκαστικό NARROW TW S6 (NORMAL) — Φτερωτή Ø 920 — 1500 λίτρα", "desc": "Ψεκαστικό NARROW TW S6 (NORMAL) — Φτερωτή Ø 920 — 1500 λίτρα."},
    "NTW20S/6": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S6", "price": 19600, "info": "Ψεκαστικό NARROW TW S6 (NORMAL) — Φτερωτή Ø 920 — 2000 λίτρα", "desc": "Ψεκαστικό NARROW TW S6 (NORMAL) — Φτερωτή Ø 920 — 2000 λίτρα."},
    "NTW30S/6": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S6", "price": 22800, "info": "Ψεκαστικό NARROW TW S6 (NORMAL) — Φτερωτή Ø 920 — 3000 λίτρα", "desc": "Ψεκαστικό NARROW TW S6 (NORMAL) — Φτερωτή Ø 920 — 3000 λίτρα."},
    "NTW15S/6TOP": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S6 TOP", "price": 20500, "info": "Ψεκαστικό NARROW TW S6 (TOP MANUAL) — Φτερωτή Ø 920 — 1500 λίτρα", "desc": "Ψεκαστικό NARROW TW S6 (TOP MANUAL) — Φτερωτή Ø 920 — 1500 λίτρα."},
    "NTW20S/6TOP": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S6 TOP", "price": 21300, "info": "Ψεκαστικό NARROW TW S6 (TOP MANUAL) — Φτερωτή Ø 920 — 2000 λίτρα", "desc": "Ψεκαστικό NARROW TW S6 (TOP MANUAL) — Φτερωτή Ø 920 — 2000 λίτρα."},
    "NTW30S/6TOP": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S6 TOP", "price": 24600, "info": "Ψεκαστικό NARROW TW S6 (TOP MANUAL) — Φτερωτή Ø 920 — 3000 λίτρα", "desc": "Ψεκαστικό NARROW TW S6 (TOP MANUAL) — Φτερωτή Ø 920 — 3000 λίτρα."},
    "NTW15S/6TOPH": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S6 TOPH", "price": 21200, "info": "Ψεκαστικό NARROW TW S6 (TOP ΥΔΡΑΥΛΙΚΟ) — Φτερωτή Ø 920 — 1500 λίτρα", "desc": "Ψεκαστικό NARROW TW S6 (TOP ΥΔΡΑΥΛΙΚΟ) — Φτερωτή Ø 920 — 1500 λίτρα."},
    "NTW20S/6TOPH": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S6 TOPH", "price": 22000, "info": "Ψεκαστικό NARROW TW S6 (TOP ΥΔΡΑΥΛΙΚΟ) — Φτερωτή Ø 920 — 2000 λίτρα", "desc": "Ψεκαστικό NARROW TW S6 (TOP ΥΔΡΑΥΛΙΚΟ) — Φτερωτή Ø 920 — 2000 λίτρα."},
    "NTW30S/6TOPH": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S6 TOPH", "price": 25300, "info": "Ψεκαστικό NARROW TW S6 (TOP ΥΔΡΑΥΛΙΚΟ) — Φτερωτή Ø 920 — 3000 λίτρα", "desc": "Ψεκαστικό NARROW TW S6 (TOP ΥΔΡΑΥΛΙΚΟ) — Φτερωτή Ø 920 — 3000 λίτρα."},
    "NTWESP08": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW ESPALDERA", "price": 16400, "info": "Ψεκαστικό ESPALDERA — Φτερωτή Ø 720 — 1000 λίτρα", "desc": "Ψεκαστικό ESPALDERA — Φτερωτή Ø 720 — 1000 λίτρα."},
    "NTWESP10": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW ESPALDERA", "price": 16700, "info": "Ψεκαστικό ESPALDERA — Φτερωτή Ø 820 — 1000 λίτρα", "desc": "Ψεκαστικό ESPALDERA — Φτερωτή Ø 820 — 1000 λίτρα."},
    "NTWESP15": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW ESPALDERA", "price": 18600, "info": "Ψεκαστικό ESPALDERA — Φτερωτή Ø 820 — 1500 λίτρα", "desc": "Ψεκαστικό ESPALDERA — Φτερωτή Ø 820 — 1500 λίτρα."},
    "NTWESP20": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW ESPALDERA", "price": 19500, "info": "Ψεκαστικό ESPALDERA — Φτερωτή Ø 820 — 2000 λίτρα", "desc": "Ψεκαστικό ESPALDERA — Φτερωτή Ø 820 — 2000 λίτρα."},
    "NTWESP30": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW ESPALDERA", "price": 22800, "info": "Ψεκαστικό ESPALDERA — Φτερωτή Ø 820 — 3000 λίτρα", "desc": "Ψεκαστικό ESPALDERA — Φτερωτή Ø 820 — 3000 λίτρα."},
    "NTWESP209": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW ESPALDERA", "price": 20800, "info": "Ψεκαστικό ESPALDERA — Φτερωτή Ø 920 — 2000 λίτρα", "desc": "Ψεκαστικό ESPALDERA — Φτερωτή Ø 920 — 2000 λίτρα."},
    "NTWESP309": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW ESPALDERA", "price": 24000, "info": "Ψεκαστικό ESPALDERA — Φτερωτή Ø 920 — 3000 λίτρα", "desc": "Ψεκαστικό ESPALDERA — Φτερωτή Ø 920 — 3000 λίτρα."},
    "NTWMOON10": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW MOON", "price": 15700, "info": "Ψεκαστικό MOON — Φτερωτή Ø 820 — 1000 λίτρα", "desc": "Ψεκαστικό MOON — Φτερωτή Ø 820 — 1000 λίτρα."},
    "NTWMOON15": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW MOON", "price": 17100, "info": "Ψεκαστικό MOON — Φτερωτή Ø 820 — 1500 λίτρα", "desc": "Ψεκαστικό MOON — Φτερωτή Ø 820 — 1500 λίτρα."},
    "NTWMOON20/8": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW MOON", "price": 18000, "info": "Ψεκαστικό MOON — Φτερωτή Ø 820 — 2000 λίτρα", "desc": "Ψεκαστικό MOON — Φτερωτή Ø 820 — 2000 λίτρα."},
    "NTWMOON20": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW MOON", "price": 19700, "info": "Ψεκαστικό MOON — Φτερωτή Ø 920 — 2000 λίτρα", "desc": "Ψεκαστικό MOON — Φτερωτή Ø 920 — 2000 λίτρα."},
    "NTWMOON30": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW MOON", "price": 21700, "info": "Ψεκαστικό MOON — Φτερωτή Ø 920 — 3000 λίτρα", "desc": "Ψεκαστικό MOON — Φτερωτή Ø 920 — 3000 λίτρα."},
    "NTWTOWER20": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW TOWER DF", "price": 15700, "info": "Ψεκαστικό TOWER DF — Φτερωτή 2 X 720 — 2000 λίτρα", "desc": "Ψεκαστικό TOWER DF — Φτερωτή 2 X 720 — 2000 λίτρα."},
    "NTWTOWER30": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW TOWER DF", "price": 17100, "info": "Ψεκαστικό TOWER DF — Φτερωτή 2 X 720 — 3000 λίτρα", "desc": "Ψεκαστικό TOWER DF — Φτερωτή 2 X 720 — 3000 λίτρα."},
    "NTWTOWER20-S8": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S8", "price": 35600, "info": "Ψεκαστικό S8 — Φτερωτή Ø 920 — 2000 λίτρα", "desc": "Ψεκαστικό S8 — Φτερωτή Ø 920 — 2000 λίτρα."},
    "RANT720": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 390, "info": "Πλέγμα προστασίας από D720", "desc": "Πλέγμα προστασίας από D720."},
    "RANT820": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 440, "info": "Πλέγμα προστασίας από D820", "desc": "Πλέγμα προστασίας από D820."},
    "RANT920": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 500, "info": "Πλέγμα προστασίας από D920", "desc": "Πλέγμα προστασίας από D920."},
    "FANTHO": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 180, "info": "Προστατευτικό φτερωτής (φύλλα)", "desc": "Προστατευτικό φτερωτής (φύλλα)."},
    "PTWS/5": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 270, "info": "Προστατευτικά ακροφυσίων TW S5", "desc": "Προστατευτικά ακροφυσίων TW S5."},
    "PTWS/6": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 270, "info": "Προστατευτικά ακροφυσίων TW S6", "desc": "Προστατευτικά ακροφυσίων TW S6."},
    "PTWMOON": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 290, "info": "Προστατευτικά ακροφυσίων TW Moon", "desc": "Προστατευτικά ακροφυσίων TW Moon."},
    "LARTREP": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 870, "info": "Σπαστή κοτσάνδουρα (1000-2000λ)", "desc": "Σπαστή κοτσάνδουρα (1000-2000λ)."},
    "LARTREG": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 1100, "info": "Σπαστή κοτσάνδουρα (3000-4000λ)", "desc": "Σπαστή κοτσάνδουρα (3000-4000λ)."},
    "LARTRAEP": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 870, "info": "Σπαστή κοτσάνδουρα με δαχτυλίδι (1000-2000λ)", "desc": "Σπαστή κοτσάνδουρα με δαχτυλίδι (1000-2000λ)."},
    "LARTRAEG": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 1100, "info": "Σπαστή κοτσάνδουρα με δαχτυλίδι (3000-4000λ)", "desc": "Σπαστή κοτσάνδουρα με δαχτυλίδι (3000-4000λ)."},
    "ADAPEA": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 350, "info": "Εξάρτημα / σύνδεσμος κοτσάνδουρας", "desc": "Εξάρτημα / σύνδεσμος κοτσάνδουρας."},
    "LARTVEP": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 980, "info": "Σπαστό τιμόνι στα μπράτσα του ελκυστήρα (1000-2000λ)", "desc": "Σπαστό τιμόνι στα μπράτσα του ελκυστήρα (1000-2000λ)."},
    "LARTVEG": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 1210, "info": "Σπαστό τιμόνι στα μπράτσα του ελκυστήρα (3000-4000λ)", "desc": "Σπαστό τιμόνι στα μπράτσα του ελκυστήρα (3000-4000λ)."},
    "LFA+ET": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 870, "info": "Τρίγωνο σύνδεσης 3ων σημείων ελκυστήρα", "desc": "Τρίγωνο σύνδεσης 3ων σημείων ελκυστήρα."},
    "DR261080": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 390, "info": "Χαμήλωμα με 26\"x12-12 (από 10.80/12)", "desc": "Χαμήλωμα με 26\"x12-12."},
    "DR261075": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 390, "info": "Χαμήλωμα με 26\"x12-12 (από 10.75/15)", "desc": "Χαμήλωμα με 26\"x12-12."},
    "DR341075": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 500, "info": "Ελαστικά 34/55-16\"", "desc": "Ελαστικά 34/55-16\"."},
    "DR111075": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 390, "info": "Ελαστικά 11.580/11 αντί για 10.75/15", "desc": "Ελαστικά 11.580/11."},
    "DR4001075": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 650, "info": "Ελαστικά 400/60-15.5\"", "desc": "Ελαστικά 400/60-15.5\"."},
    "PARLIGHT": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 330, "info": "Προφυλακτήρας με φώτα", "desc": "Προφυλακτήρας με φώτα."},
    "CFLIGHT": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 590, "info": "Κουτί + Φώτα", "desc": "Κουτί + Φώτα."},
    "CVLIGHT": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 650, "info": "Κατασκευή για ESPALDERA για Κουτί & Φώτα", "desc": "Κατασκευή για ESPALDERA για Κουτί & Φώτα."},
    "KITFRENR": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 770, "info": "Υδραυλικά φρένα με ρυθμιστική βαλβίδα", "desc": "Υδραυλικά φρένα με ρυθμιστική βαλβίδα."},
    "PMFRUTEP": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 650, "info": "Προμίξερ 1500-2000λ", "desc": "Προμίξερ 1500-2000λ."},
    "PMFRUTEG": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 770, "info": "Προμίξερ 3000λ", "desc": "Προμίξερ 3000λ."},
    "SUSPBPAR": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 770, "info": "Ανάρτηση με σούστα", "desc": "Ανάρτηση με σούστα."},
    "KITVALRP": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 590, "info": "Κιτ ηλεκτροβαλβίδα ρύθμισης πίεσης", "desc": "Κιτ ηλεκτροβαλβίδα ρύθμισης πίεσης."},
    "KON/OFF2+FLOW": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 1270, "info": "2-περιοχών ON-OFF ηλ.χειριστήριο με ροόμετρο", "desc": "2-περιοχών ON-OFF ηλ.χειριστήριο με ροόμετρο."},
    "KON/OFF4+FLOW": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 1500, "info": "4-περιοχών ON-OFF ηλ.χειριστήριο με ροόμετρο", "desc": "4-περιοχών ON-OFF ηλ.χειριστήριο με ροόμετρο."},
    "KITRONIC": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 2540, "info": "TRONIC-Ογκομετρικό χειριστήριο", "desc": "TRONIC-Ογκομετρικό χειριστήριο."},
    "KITSIST": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 2190, "info": "SITOMATIC χειριστήριο χωρίς ροόμετρο", "desc": "SITOMATIC χειριστήριο χωρίς ροόμετρο."},
    "FLOWMET": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 530, "info": "Ανοξείδωτο ροόμετρο", "desc": "Ανοξείδωτο ροόμετρο."},
    "4.0SCSTT": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 3690, "info": "SISTRONIC για λίτρα/στρέμμα", "desc": "SISTRONIC για λίτρα/στρέμμα."},
    "4.0SCSTTS": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 4610, "info": "SISTRONIC για λίτρα/στρέμμα + σόναρ", "desc": "SISTRONIC για λίτρα/στρέμμα + σόναρ."},
    "4.0SCSTTISO": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 5190, "info": "SISTRONIC λίτρα/στρέμμα + ISOBUS", "desc": "SISTRONIC λίτρα/στρέμμα + ISOBUS."},
    "4.0SCSTTISO+S": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 6110, "info": "SISTRONIC λίτρα/στρέμμα + ISOBUS + Σόναρ", "desc": "SISTRONIC λίτρα/στρέμμα + ISOBUS + Σόναρ."},
    "ABRBG": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": -580, "info": "Αλλαγή αντλίας ML-A1-EP σε ML-A", "desc": "Αλλαγή αντλίας ML-A1-EP σε ML-A."},
    "ABRBP": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": -980, "info": "Αλλαγή αντλίας ML-A1-EP σε ML-D", "desc": "Αλλαγή αντλίας ML-A1-EP σε ML-D."},

    # --- Νιούμπο (Niubo) - Καταστροφείς & Παρελκόμενα ---
    "TLG120": {"cat": "Νιούμπο", "series": "LIGHT", "price": 4150, "info": "Καταστροφέας LIGHT 1200mm", "desc": "Καταστροφέας LIGHT 1200mm — 320kg — 25-35 Hp."},
    "TLG140": {"cat": "Νιούμπο", "series": "LIGHT", "price": 4200, "info": "Καταστροφέας LIGHT 1400mm", "desc": "Καταστροφέας LIGHT 1400mm — 350kg — 25-35 Hp."},
    "TLG160": {"cat": "Νιούμπο", "series": "LIGHT", "price": 4300, "info": "Καταστροφέας LIGHT 1600mm", "desc": "Καταστροφέας LIGHT 1600mm — 370kg — 30-40 Hp."},
    "TLG180": {"cat": "Νιούμπο", "series": "LIGHT", "price": 4400, "info": "Καταστροφέας LIGHT 1800mm", "desc": "Καταστροφέας LIGHT 1800mm — 390kg — 35-50 Hp."},
    "NIUBO_HYD_LIGHT": {"cat": "Νιούμπο", "series": "LIGHT (Έξτρα)", "price": 310, "info": "Υδραυλική Μετατόπιση (LIGHT)", "desc": "Υδραυλική Μετατόπιση (για LIGHT)."},
    "TGD130": {"cat": "Νιούμπο", "series": "GLIDER", "price": 5100, "info": "Καταστροφέας GLIDER 1300mm", "desc": "Καταστροφέας GLIDER 1300mm — 420kg — 28-38 Hp."},
    "TGD160": {"cat": "Νιούμπο", "series": "GLIDER", "price": 5300, "info": "Καταστροφέας GLIDER 1600mm", "desc": "Καταστροφέας GLIDER 1600mm — 450kg — 48-58 Hp."},
    "TGD180": {"cat": "Νιούμπο", "series": "GLIDER", "price": 5500, "info": "Καταστροφέας GLIDER 1800mm", "desc": "Καταστροφέας GLIDER 1800mm — 480kg — 50-60 Hp."},
    "TGD200": {"cat": "Νιούμπο", "series": "GLIDER", "price": 5700, "info": "Καταστροφέας GLIDER 2000mm", "desc": "Καταστροφέας GLIDER 2000mm — 510kg — 55-65 Hp."},
    "NIUBO_HYD_GLIDER": {"cat": "Νιούμπο", "series": "GLIDER (Έξτρα)", "price": 260, "info": "Υδραυλική Μετατόπιση (GLIDER)", "desc": "Υδραυλική Μετατόπιση (για GLIDER)."},
    "TSP150": {"cat": "Νιούμπο", "series": "SPEED", "price": 5550, "info": "Καταστροφέας SPEED 1500mm", "desc": "Καταστροφέας SPEED 1500mm — 530kg — 38-48 Hp."},
    "TSP180": {"cat": "Νιούμπο", "series": "SPEED", "price": 5780, "info": "Καταστροφέας SPEED 1800mm", "desc": "Καταστροφέας SPEED 1800mm — 600kg — 55-68 Hp."},
    "TSP200": {"cat": "Νιούμπο", "series": "SPEED", "price": 5890, "info": "Καταστροφέας SPEED 2000mm", "desc": "Καταστροφέας SPEED 2000mm — 655kg — 65-70 Hp."},
    "TSP220": {"cat": "Νιούμπο", "series": "SPEED", "price": 6220, "info": "Καταστροφέας SPEED 2200mm", "desc": "Καταστροφέας SPEED 2200mm — 705kg — 75-85 Hp."},
    "TSPR150": {"cat": "Νιούμπο", "series": "SPEED REVERS", "price": 6200, "info": "Καταστροφέας SPEED REVERS 1500mm", "desc": "Καταστροφέας SPEED REVERS 1500mm."},
    "TSPR180": {"cat": "Νιούμπο", "series": "SPEED REVERS", "price": 6430, "info": "Καταστροφέας SPEED REVERS 1800mm", "desc": "Καταστροφέας SPEED REVERS 1800mm."},
    "TSPR200": {"cat": "Νιούμπο", "series": "SPEED REVERS", "price": 6540, "info": "Καταστροφέας SPEED REVERS 2000mm", "desc": "Καταστροφέας SPEED REVERS 2000mm."},
    "TSPR220": {"cat": "Νιούμπο", "series": "SPEED REVERS", "price": 6870, "info": "Καταστροφέας SPEED REVERS 2200mm", "desc": "Καταστροφέας SPEED REVERS 2200mm."},
    "NIUBO_TSR_SPEED": {"cat": "Νιούμπο", "series": "SPEED (Έξτρα)", "price": 650, "info": "Διπλή Ζεύξη (TSR)", "desc": "Διπλή Ζεύξη (TSR +40kg)."},
    "TDP140": {"cat": "Νιούμπο", "series": "DRAGON PLUS", "price": 5800, "info": "Καταστροφέας DRAGON PLUS 1400mm", "desc": "Καταστροφέας DRAGON PLUS 1400mm."},
    "TDP160": {"cat": "Νιούμπο", "series": "DRAGON PLUS", "price": 6000, "info": "Καταστροφέας DRAGON PLUS 1600mm", "desc": "Καταστροφέας DRAGON PLUS 1600mm."},
    "TDP180": {"cat": "Νιούμπο", "series": "DRAGON PLUS", "price": 6200, "info": "Καταστροφέας DRAGON PLUS 1800mm", "desc": "Καταστροφέας DRAGON PLUS 1800mm."},
    "TKM130": {"cat": "Νιούμπο", "series": "KOMPACT", "price": 7800, "info": "Καταστροφέας KOMPACT 1300mm", "desc": "Καταστροφέας KOMPACT 1300mm — 530kg — 38-48 Hp."},
    "TKM150": {"cat": "Νιούμπο", "series": "KOMPACT", "price": 7900, "info": "Καταστροφέας KOMPACT 1500mm", "desc": "Καταστροφέας KOMPACT 1500mm — 570kg — 48-58 Hp."},
    "TKM160": {"cat": "Νιούμπο", "series": "KOMPACT", "price": 7950, "info": "Καταστροφέας KOMPACT 1600mm", "desc": "Καταστροφέας KOMPACT 1600mm — 605kg — 55-68 Hp."},
    "TKM180": {"cat": "Νιούμπο", "series": "KOMPACT", "price": 8200, "info": "Καταστροφέας KOMPACT 1800mm", "desc": "Καταστροφέας KOMPACT 1800mm — 640kg — 65-70 Hp."},
    "TKM200": {"cat": "Νιούμπο", "series": "KOMPACT", "price": 8400, "info": "Καταστροφέας KOMPACT 2000mm", "desc": "Καταστροφέας KOMPACT 2000mm — 695kg — 70-85 Hp."},
    "TKM220": {"cat": "Νιούμπο", "series": "KOMPACT", "price": 8700, "info": "Καταστροφέας KOMPACT 2200mm", "desc": "Καταστροφέας KOMPACT 2200mm — 745kg — 85-90 Hp."},
    "TKM250": {"cat": "Νιούμπο", "series": "KOMPACT", "price": 8900, "info": "Καταστροφέας KOMPACT 2500mm", "desc": "Καταστροφέας KOMPACT 2500mm — 830kg — 90-95 Hp."},
    "NIUBO_KOMPACT_DOOR": {"cat": "Νιούμπο", "series": "KOMPACT (Έξτρα)", "price": 750, "info": "Υδραυλική Πόρτα", "desc": "Υδραυλική Ανοιγόμενη Πίσω Πόρτα."},
    "TXM150": {"cat": "Νιούμπο", "series": "MAX FRUIT", "price": 15200, "info": "Καταστροφέας MAX FRUIT 1460mm", "desc": "Καταστροφέας MAX FRUIT 1460mm."},
    "TXM175": {"cat": "Νιούμπο", "series": "MAX FRUIT", "price": 15900, "info": "Καταστροφέας MAX FRUIT 1730mm", "desc": "Καταστροφέας MAX FRUIT 1730mm."},
    "TXM200": {"cat": "Νιούμπο", "series": "MAX FRUIT", "price": 16600, "info": "Καταστροφέας MAX FRUIT 2000mm", "desc": "Καταστροφέας MAX FRUIT 2000mm."},
    "NIUBO_MAXFRUIT_DOUBLE": {"cat": "Νιούμπο", "series": "MAX FRUIT (Έξτρα)", "price": 1980, "info": "Διπλή Ζεύξη 540", "desc": "Διπλή Ζεύξη 540."},
    "NIUBO_MAXFRUIT_LIFT": {"cat": "Νιούμπο", "series": "MAX FRUIT (Έξτρα)", "price": 1320, "info": "Ακτίνες Ανύψωσης", "desc": "Ακτίνες Ανύψωσης."},
    "TJE160": {"cat": "Νιούμπο", "series": "JOLLY-E", "price": 8850, "info": "Καταστροφέας JOLLY-E 1600mm", "desc": "Καταστροφέας JOLLY-E 1600mm."},
    "TJE180": {"cat": "Νιούμπο", "series": "JOLLY-E", "price": 8960, "info": "Καταστροφέας JOLLY-E 1800mm", "desc": "Καταστροφέας JOLLY-E 1800mm."},
    "TJE200": {"cat": "Νιούμπο", "series": "JOLLY-E", "price": 9630, "info": "Καταστροφέας JOLLY-E 2000mm", "desc": "Καταστροφέας JOLLY-E 2000mm."},
    "NIUBO_JOLLY_VALVE": {"cat": "Νιούμπο", "series": "JOLLY-E (Έξτρα)", "price": 380, "info": "Βαλβίδα Ασφαλείας", "desc": "Βαλβίδα Ασφαλείας."},
    "NIUBO_JOLLY_SHAFT1": {"cat": "Νιούμπο", "series": "JOLLY-E (Έξτρα)", "price": 800, "info": "Ομοκινητικός Άξονας", "desc": "Ομοκινητικός Άξονας Μεγάλης Γωνίας."},
    "NIUBO_JOLLY_SHAFT2": {"cat": "Νιούμπο", "series": "JOLLY-E (Έξτρα)", "price": 1220, "info": "Άξονας Διπλής Γωνίας", "desc": "Ομοκινητικός Άξονας Διπλής Μεγάλης Γωνίας."},
    "NIUBO_JOLLY_CTRL": {"cat": "Νιούμπο", "series": "JOLLY-E (Έξτρα)", "price": 1350, "info": "Ηλεκτρικό Χειριστήριο", "desc": "Ηλεκτρικό Χειριστήριο 2 Κινήσεων."},

    # --- Κοπροδιανομείς ID DAVID (SURFEED / ECOFEED) ---
    "DES-2525-T": {"cat": "Κοπροδιανομείς ID DAVID", "series": "SURFEED", "price": 13700, "info": "Κοπροδιανομέας SURFEED 2.5m³", "desc": "Κοπροδιανομέας SURFEED 2.5m³ — Πλάτος 1.46m — 40 HP."},
    "DES-4535-T": {"cat": "Κοπροδιανομείς ID DAVID", "series": "SURFEED", "price": 15200, "info": "Κοπροδιανομέας SURFEED 3.5m³", "desc": "Κοπροδιανομέας SURFEED 3.5m³ — Πλάτος 1.50m — 50 HP."},
    "DES-5540-T": {"cat": "Κοπροδιανομείς ID DAVID", "series": "SURFEED", "price": 16800, "info": "Κοπροδιανομέας SURFEED 4.0m³", "desc": "Κοπροδιανομέας SURFEED 4.0m³ — Πλάτος 1.80m — 55 HP."},
    "DES-7560-T": {"cat": "Κοπροδιανομείς ID DAVID", "series": "SURFEED", "price": 21800, "info": "Κοπροδιανομέας SURFEED 6.0m³", "desc": "Κοπροδιανομέας SURFEED 6.0m³ — Πλάτος 2.04m — 75 HP."},
    "DES-8580-T": {"cat": "Κοπροδιανομείς ID DAVID", "series": "SURFEED", "price": 24650, "info": "Κοπροδιανομέας SURFEED 8.0m³", "desc": "Κοπροδιανομέας SURFEED 8.0m³ — Πλάτος 2.09m — 85 HP."},
    "DES-100100-T": {"cat": "Κοπροδιανομείς ID DAVID", "series": "SURFEED", "price": 32000, "info": "Κοπροδιανομέας SURFEED 10.0m³", "desc": "Κοπροδιανομέας SURFEED 10.0m³ — Πλάτος 2.09m — 100 HP."},
    "DES-130130-T": {"cat": "Κοπροδιανομείς ID DAVID", "series": "SURFEED", "price": 36700, "info": "Κοπροδιανομέας SURFEED 13.0m³", "desc": "Κοπροδιανομέας SURFEED 13.0m³ — Πλάτος 2.46m — 130 HP."},

    # Επιλογές Χειριστηρίων & Έξτρα
    "ID_CABIN_E": {"cat": "Κοπροδιανομείς ID DAVID", "series": "Εξοπλισμός / Χειριστήρια", "price": 700, "info": "Electric Cabin Χειριστήριο", "desc": "Electric Cabin Χειριστήριο."},
    "ID_TOUCHSCREEN": {"cat": "Κοπροδιανομείς ID DAVID", "series": "Εξοπλισμός / Χειριστήρια", "price": 1500, "info": "Touchscreen 7\"", "desc": "Touchscreen Οθόνη Αφής 7\" με υπολογιστή επεξεργασίας δεδομένων."},
    "ID_NARROW_VER": {"cat": "Κοπροδιανομείς ID DAVID", "series": "Εξοπλισμός / Χειριστήρια", "price": 0, "info": "Στενή Έκδοση", "desc": "Στρογγυλή \"Στενή\" Έκδοση (-18% χωρητικότητα)."},
    "ID_SONAR": {"cat": "Κοπροδιανομείς ID DAVID", "series": "Εξοπλισμός / Χειριστήρια", "price": 1650, "info": "Σόναρ δέντρων", "desc": "Σόναρ ανίχνευσης δέντρων."},
    "ID_SHREDDER": {"cat": "Κοπροδιανομείς ID DAVID", "series": "Εξοπλισμός / Χειριστήρια", "price": 2400, "info": "Τεμαχιστής κοπριάς", "desc": "Τεμαχιστής κοπριάς."},
    "ID_CAMERA_DISP": {"cat": "Κοπροδιανομείς ID DAVID", "series": "Εξοπλισμός / Χειριστήρια", "price": 1000, "info": "Κάμερα & Οθόνη", "desc": "Κάμερα & Οθόνη 7\"."},
    "ID_ANALOG_VALVE": {"cat": "Κοπροδιανομείς ID DAVID", "series": "Εξοπλισμός / Χειριστήρια", "price": 1500, "info": "Βαλβίδα αναλογική", "desc": "Κιτ Ρυθμ. βαλβίδας αναλογικές ρυθμίσεις."},
    "ID_CAMERA": {"cat": "Κοπροδιανομείς ID DAVID", "series": "Εξοπλισμός / Χειριστήρια", "price": 560, "info": "Κάμερα", "desc": "Κάμερα."},
    "ID_HITCH_EXT": {"cat": "Κοπροδιανομείς ID DAVID", "series": "Εξοπλισμός / Χειριστήρια", "price": 380, "info": "Μάτι Κοτσαδούρας", "desc": "Εξάρτημα / Μάτι Κοτσαδούρας."},

    # Εξαρτήματα Επιφανειακής Χρήσης
    "ID_DISC_GREENHOUSE": {"cat": "Κοπροδιανομείς ID DAVID", "series": "Επιφανειακή Χρήση", "price": 4800, "info": "Δίσκος θερμοκηπίου", "desc": "Δίσκος με άξονα για θερμοκήπια (Ø900 mm)."},
    "ID_DISC_NO_AXLE_1": {"cat": "Κοπροδιανομείς ID DAVID", "series": "Επιφανειακή Χρήση", "price": 6850, "info": "Δίσκος χωρίς άξονα 3.5-4m³", "desc": "Δίσκος χωρίς άξονα (Ø1100 mm)."},
    "ID_DISC_NO_AXLE_2": {"cat": "Κοπροδιανομείς ID DAVID", "series": "Επιφανειακή Χρήση", "price": 7200, "info": "Δίσκος χωρίς άξονα 6-8m³", "desc": "Δίσκος χωρίς άξονα (Ø1250 mm)."},
    "ID_DISC_NO_AXLE_3": {"cat": "Κοπροδιανομείς ID DAVID", "series": "Επιφανειακή Χρήση", "price": 8100, "info": "Δίσκος χωρίς άξονα 10m³+", "desc": "Δίσκος χωρίς άξονα (Ø1500 mm)."},
    "ID_SPECIAL_VINEYARD": {"cat": "Κοπροδιανομείς ID DAVID", "series": "Επιφανειακή Χρήση", "price": 5200, "info": "Ειδικό για αμπέλια", "desc": "Ειδικό για αμπέλια (λίπασμα ή πέλετ)."},
    "ID_VIB_RAMP_TREES": {"cat": "Κοπροδιανομείς ID DAVID", "series": "Επιφανειακή Χρήση", "price": 6600, "info": "Δονούμενη ράμπα", "desc": "Με δονούμενη ράμπα (Για δέντρα)."},
    "ID_SIMPLE_RAMP": {"cat": "Κοπροδιανομείς ID DAVID", "series": "Επιφανειακή Χρήση", "price": 900, "info": "Απλή ράμπα", "desc": "Απλή ράμπα."},
    "ID_RUBBER_RAMP": {"cat": "Κοπροδιανομείς ID DAVID", "series": "Επιφανειακή Χρήση", "price": 200, "info": "Ελαστική ράμπα", "desc": "Ελαστική ράμπα."},
    "ID_TAPE_DISC_700": {"cat": "Κοπροδιανομείς ID DAVID", "series": "Επιφανειακή Χρήση", "price": 2100, "info": "Δίσκος ταινίας Ø700", "desc": "Δίσκος για ταινία Ø700."},
    "ID_THROW_CYLINDER": {"cat": "Κοπροδιανομείς ID DAVID", "series": "Επιφανειακή Χρήση", "price": 1900, "info": "Κύλινδρος ρίψης", "desc": "Κύλινδρος ρίψης."},
    "ID_BELT_050M": {"cat": "Κοπροδιανομείς ID DAVID", "series": "Επιφανειακή Χρήση", "price": 6500, "info": "Ταινία 0.50m", "desc": "Ταινία μεταφοράς x = 0,50m."},
    "ID_BELT_075M": {"cat": "Κοπροδιανομείς ID DAVID", "series": "Επιφανειακή Χρήση", "price": 6600, "info": "Ταινία 0.75m", "desc": "Ταινία μεταφοράς x = 0,75m."},
    "ID_BELT_100M": {"cat": "Κοπροδιανομείς ID DAVID", "series": "Επιφανειακή Χρήση", "price": 7000, "info": "Ταινία 1.00m", "desc": "Ταινία μεταφοράς x = 1,00m."}
}

# --- ΕΞΥΠΝΗ ΑΥΤΟΜΑΤΗ ΔΗΜΙΟΥΡΓΙΑ ΠΕΡΙΓΡΑΦΗΣ ΑΝΑ ΚΑΤΗΓΟΡΙΑ ---
def generate_auto_description(model_key, item_data):
    if "desc" in item_data and len(item_data["desc"]) > 60:
        return item_data["desc"]

    cat_name = item_data.get("cat", "Μηχάνημα")
    series_name = item_data.get("series", "")
    info_text = item_data.get("info", "")

    if cat_name == "Τρακτέρ":
        mach_desc = f"γεωργικό ελκυστήρα εργοστασίου κατασκευής KUBOTA Ιαπωνίας τύπου {model_key}"
    elif cat_name == "Χωματουργικό":
        mach_desc = f"χωματουργικό μηχάνημα KUBOTA τύπου {model_key}"
    elif cat_name == "Μανέζ Λοζάνο":
        mach_desc = f"ψεκαστικό μηχάνημα Manez Lozano τύπου {model_key} ({info_text})"
    elif cat_name == "Νιούμπο":
        mach_desc = f"καταστροφέα Niubo τύπου {model_key} ({info_text})"
    elif cat_name == "Κοπροδιανομείς ID DAVID":
        mach_desc = f"κοπροδιανομέα ID DAVID τύπου {model_key} ({info_text})"
    else:
        mach_desc = f"μηχάνημα {model_key}"

    text = f"Ένα καινούριο και αμεταχείριστο {mach_desc} με αψίδα προστασίας εγκεκριμένου τύπου. "
    text += f"Διαθέτει βασικό εξοπλισμό σειράς {series_name} και τεχνικά χαρακτηριστικά: {info_text}."

    return text

def translate_info(text, is_en):
    if not is_en:
        return text
    translations_map = {
        "Υδροστατικό κιβώτιο ταχυτήτων, Καμπίνα": "Hydrostatic transmission, Cabin",
        "Υδροστατικό κιβώτιο ταχυτήτων, ROPS": "Hydrostatic transmission, ROPS",
        "Υδροστατικό, Καμπίνα": "Hydrostatic, Cabin",
        "Ηλεκτρό-υδραυλική ρεβέρσα 36/36": "Electro-hydraulic reverser 36/36",
        "Μικροί Εκσκαφείς": "Mini Excavators",
        "Εκσκαφείς Μεσαίας Κατηγορίας": "Mid-Size Excavators",
        "Παρελκόμενα & Αξεσουάρ": "Accessories & Options"
    }
    for gr_term, en_term in translations_map.items():
        text = text.replace(gr_term, en_term)
    return text

def register_fonts():
    registered = pdfmetrics.getRegisteredFontNames()
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

def generate_pdf_bytes(client_data, seller_data, cart_items, company, is_english, offer_date, vat_rate, optional_equipment=""):
    pdf_filename = "temp_profora.pdf"
    font_reg, font_bld = get_company_fonts(company)

    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter
    
    comp_display = "Petropoulos" if (is_english and company == "Πετρόπουλος") else company

    # Λογότυπο (Πετρόπουλος)
    if company in ["Πετρόπουλος", "Petropoulos"]:
        logo_path = "petropoulos_logo.jpeg"
        if os.path.exists(logo_path):
            c.drawImage(logo_path, width - 180, height - 70, width=130, height=45, preserveAspectRatio=True, mask='auto')

    # Επικεφαλίδα (Αριστερά)
    c.setFont(font_bld, 14)
    c.drawString(50, height - 40, "ΠΕΤΡΟΣ ΠΕΤΡΟΠΟΥΛΟΣ ΑΕΒΕ" if not is_english else comp_display)
    
    c.setFont(font_reg, 9)
    c.drawString(50, height - 55, "Τμήμα Γεωργικών & Χωματουργικών Μηχανημάτων" if not is_english else "Machinery Department")
    
    # Στοιχεία Επικοινωνίας / Πωλητή (Δεξιά)
    c.drawRightString(width - 50, height - 40, "Τηλέφωνα : 210 - 3499333")
    c.drawRightString(width - 50, height - 55, f"E-mail : {seller_data['email']}")
    formatted_date_str = offer_date.strftime("Αθήνα, %d %B %Y") if not is_english else offer_date.strftime("Athens, %B %d, %Y")
    c.drawRightString(width - 50, height - 70, formatted_date_str)
    
    c.setStrokeColorRGB(0.2, 0.3, 0.5)
    c.setLineWidth(1)
    c.line(50, height - 80, width - 50, height - 80)
    
    # Στοιχεία Πελάτη
    c.setFont(font_bld, 11)
    c.drawString(50, height - 102, "ΣΤΟΙΧΕΙΑ ΠΕΛΑΤΗ:" if not is_english else "CLIENT DETAILS:")
    c.setFont(font_reg, 9)
    y_client = height - 116
    c.drawString(50, y_client, f"ΠΡΟΣ: {client_data['name'].upper()}")
    y_client -= 14
    c.drawString(50, y_client, f"ΔΙΕΥΘΥΝΣΗ: {client_data['address'].upper()}")
    y_client -= 14
    c.drawString(50, y_client, f"ΑΦΜ: {client_data['afm']}  |  ΤΗΛΕΦΩΝΟ: {client_data['phone']}")
    y_client -= 14
    c.drawString(50, y_client, f"ΕΠΑΓΓΕΛΜΑ: {client_data['profession'].upper()}")
        
    y_client -= 14
    c.setStrokeColorRGB(0.7, 0.7, 0.7)
    c.setLineWidth(0.5)
    c.line(50, y_client, width - 50, y_client)
    
    # Τίτλος Προσφοράς
    y = y_client - 20
    c.setFont(font_bld, 12)
    c.drawCentredString(width / 2.0, y, "ΟΙΚΟΝΟΜΙΚΗ ΠΡΟΣΦΟΡΑ" if not is_english else "COMMERCIAL OFFER")
    
    y -= 20
    c.setFont(font_reg, 9)
    c.drawString(50, y, f"Αξιότιμε/η κ. {client_data['name']},")
    y -= 14
    c.drawString(50, y, "Κατόπιν επιθυμίας σας για την αγορά εξοπλισμού από την εταιρεία μας είμαστε στην ευχάριστη θέση να σας προσφέρουμε τα εξής:")
    
    y -= 10
    total_net = 0
    
    # Εκτύπωση ειδών με πλήρη περιγραφή
    for idx, item in enumerate(cart_items, 1):
        y -= 16
        c.setFont(font_bld, 9)
        c.drawString(50, y, f"{idx})  Μοντέλο: {item['model']} — Καθαρή Αξία: {item['price']:,.2f} EUR")
        
        y -= 14
        c.setFont(font_reg, 9)
        desc_full = item.get('desc', item['info'])
        c.drawString(65, y, desc_full[:110])
        if len(desc_full) > 110:
            y -= 12
            c.drawString(65, y, desc_full[110:])
            
        total_net += item['price']
        y -= 8

    # Προαιρετικός εξοπλισμός (αν υπάρχει)
    if optional_equipment:
        y -= 12
        c.setFont(font_bld, 9)
        c.drawString(50, y, "Περιλαμβάνει τον παρακάτω προαιρετικό εξοπλισμό:")
        for line in optional_equipment.split('\n'):
            if line.strip():
                y -= 12
                c.setFont(font_reg, 9)
                c.drawString(65, y, f"- {line.strip()}")

    vat_amount = total_net * (vat_rate / 100.0)
    total_with_vat = total_net + vat_amount

    # Πίνακας Οικονομικών Στοιχείων
    y -= 28
    c.setStrokeColorRGB(0.2, 0.3, 0.5)
    c.setLineWidth(1)
    c.rect(50, y - 22, width - 100, 32)
    
    c.setFont(font_bld, 9)
    c.drawString(90, y - 4, "Αξία Προσφοράς")
    c.drawString(275, y - 4, f"ΦΠΑ {vat_rate}%")
    c.drawString(450, y - 4, "Σύνολο")
    
    c.setFont(font_reg, 10)
    c.drawString(85, y - 18, f"{total_net:,.2f} €")
    c.drawString(270, y - 18, f"{vat_amount:,.2f} €")
    c.drawString(440, y - 18, f"{total_with_vat:,.2f} €")

    # Σημειώσεις κάτω από τον πίνακα
    y -= 38
    c.setFont(font_reg, 8)
    c.drawString(50, y, "• Ο εξοπλισμός διαθέτει ελληνική και ευρωπαϊκή έγκριση τύπου & καλύπτεται από εργοστασιακή εγγύηση ενός έτους.")

    # Υπογραφή και Στοιχεία Πωλητή
    y -= 32
    c.setFont(font_bld, 9)
    c.drawString(50, y, f"{seller_data['name']} - {seller_data['title']}")

    # Footer εταιρείας κάτω-κάτω
    c.setStrokeColorRGB(0.7, 0.7, 0.7)
    c.setLineWidth(0.5)
    c.line(50, 42, width - 50, 42)
    
    c.setFont(font_reg, 7)
    c.drawString(50, 30, "Πέτρος Πετρόπουλος ΑΕΒΕ   |   Ιερά Οδός 96-104, 10447 Αθήνα   |   Τηλ: 2103499200   |   ΑΦΜ: 094043269   |   ΔΟΥ ΚΕΦΟΔΕ Αττικής")

    c.save()
    with open(pdf_filename, "rb") as f:
        pdf_data = f.read()
    return pdf_data

# --- UI ΕΦΑΡΜΟΓΗΣ STREAMLIT ---
st.title("🚜 " + ("Kubota Quotation System" if is_english else "Σύστημα Προσφορών Kubota"))
st.markdown("Δημιουργήστε οικονομικές προσφορές εύκολα από το PC ή το κινητό σας!")

# 1. Στοιχεία Συντάκτη / Πωλητή (Sidebar)
with st.sidebar:
    st.header("👤 Στοιχεία Πωλητή / Συντάκτη")
    seller_name = st.text_input("Ονοματεπώνυμο Πωλητή", value="Νικήτας Μπάρλας")
    seller_title = st.text_input("Τίτλος Θέσης", value="Επιθεωρητής Πωλήσεων")
    seller_email = st.text_input("Email Πωλητή", value="nikitasb@petropoulos.com")
    offer_date = st.date_input("Ημερομηνία Προσφοράς", value=datetime.today())
    vat_rate = st.selectbox("Ποσοστό ΦΠΑ (%)", [13, 24], index=0)

# 2. Στοιχεία Πελάτη (ΚΕΝΑ για εύκολη συμπλήρωση)
with st.expander("👤 1. Στοιχεία Πελάτη (Συμπληρώστε τα στοιχεία)", expanded=True):
    company_options = ["Πετρόπουλος", "Φίλης", "Κάμπος"]
    if is_english:
        company_ui = st.selectbox("Company / Εταιρεία", ["Petropoulos", "Filis", "Kampos"])
        company = "Πετρόπουλος" if company_ui == "Petropoulos" else ("Φίλης" if company_ui == "Filis" else "Κάμπος")
    else:
        company = st.selectbox("Company / Εταιρεία", company_options)

    client_name = st.text_input("Client Name / Όνομα Πελάτη", value="")
    client_profession = st.text_input("Profession / Επάγγελμα", value="")
    col1, col2 = st.columns(2)
    with col1:
        client_afm = st.text_input("VAT No / ΑΦΜ", value="")
    with col2:
        client_phone = st.text_input("Phone / Τηλέφωνο", value="")
    client_address = st.text_input("Address / Διεύθυνση", value="")

# 3. Επιλογή Προϊόντος & Χαρακτηριστικά
with st.expander("⚙️ 2. Επιλογή Προϊόντος & Χαρακτηριστικά", expanded=True):
    raw_categories = sorted(list(set(item["cat"] for item in database.values())))
    if is_english:
        cat_map = {"Τρακτέρ": "Tractor", "Χωματουργικό": "Excavator", "Μανέζ Λοζάνο": "Manez Lozano", "Νιούμπο": "Niubo", "Κοπροδιανομείς ID DAVID": "ID DAVID Manure Spreaders"}
        categories = [cat_map.get(c, c) for c in raw_categories]
    else:
        categories = raw_categories
        
    selected_cat_ui = st.selectbox("Category / Κατηγορία", categories)
    
    if is_english:
        inv_cat_map = {"Tractor": "Τρακτέρ", "Excavator": "Χωματουργικό", "Manez Lozano": "Μανέζ Λοζάνο", "Niubo": "Νιούμπο", "ID DAVID Manure Spreaders": "Κοπροδιανομείς ID DAVID"}
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
        auto_desc = generate_auto_description(selected_model, current_item)
        
        st.markdown(f"**{'Model Price' if is_english else 'Τιμή Μοντέλου'}:** :red[{current_item['price']:,.2f} EUR]")
        custom_desc = st.text_area("Αναλυτική Περιγραφή Μηχανήματος στο PDF (Προσαρμόζεται αυτόματα)", value=auto_desc, height=120)
    else:
        custom_desc = ""

    optional_equipment = st.text_area("Προαιρετικός Εξοπλισμός (ένα σε κάθε γραμμή)", value="Υδραυλική τιράντα\nΥδραυλικό ραντάρ\nΑντίβαρα στους πίσω τροχούς\nΕμπρόσθια Υδραυλικά\nΑεροκάθισμα")

    if st.button("➕ " + ("Add to Quote" if is_english else "Προσθήκη στην Προσφορά")):
        if selected_model:
            st.session_state.cart.append({
                "model": selected_model,
                "cat": current_item["cat"],
                "series": current_item["series"],
                "price": current_item["price"],
                "info": current_item["info"],
                "desc": custom_desc
            })
            st.success("Product added!" if is_english else f"Το προϊόν {selected_model} προστέθηκε στην προσφορά!")
        else:
            st.error("Select valid model." if is_english else "Επιλέξτε έγκυρο μοντέλο.")

# 4. Επιλεγμένα Είδη Προσφοράς
with st.expander("🛒 " + ("3. Selected Quote Items" if is_english else "3. Επιλεγμένα Είδη Προσφοράς"), expanded=True):
    if st.session_state.cart:
        for idx, cart_item in enumerate(st.session_state.cart):
            if is_english:
                display_cat = "Tractor" if cart_item['cat'] == "Τρακτέρ" else ("Excavator" if cart_item['cat'] == "Χωματουργικό" else ("Manez Lozano" if cart_item['cat'] == "Μανέζ Λοζάνο" else ("Niubo" if cart_item['cat'] == "Νιούμπο" else "ID David Spreader")))
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
if st.button("📄 " + ("Generate Summary PDF" if is_english else "Δημιουργία Επαγγελματικού PDF Προσφοράς"), type="primary", use_container_width=True):
    if not client_name:
        st.warning("Please fill in the client's name!" if is_english else "Παρακαλώ συμπληρώστε το όνομα του πελάτη!")
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
        seller_data = {
            "name": seller_name, "title": seller_title, "email": seller_email
        }
        pdf_data = generate_pdf_bytes(client_data, seller_data, st.session_state.cart, company, is_english, offer_date, vat_rate, optional_equipment)
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
        