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

# ΠΛΗΡΗΣ ΚΑΙ ΕΝΙΑΙΑ ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ (ΟΛﺎ ΤΑ ΜΗΧΑΝΗΜΑΤΑ ΧΩΡΙΣ ΚΑΜΙΑ ΠΑΡΑΛΕΙΨΗ)
database = {
    # --- 1. ΝΕΑ ΤΡΑΚΤΕΡ & ΟΧΗΜΑΤΑ (από τις φωτογραφίες σου) ---
    "B1181": {"cat": "Τρακτέρ", "series": "Σειρά B1 - T2a", "hp": 17.00, "price": 14500, "info": "17.00 HP - T2a", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα εργοστασίου κατασκευής KUBOTA Ιαπωνίας τύπου B1181."},
    "B1241": {"cat": "Τρακτέρ", "series": "Σειρά B1 - T2a", "hp": 21.35, "price": 15500, "info": "21.35 HP - T2a", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα εργοστασίου κατασκευής KUBOTA Ιαπωνίας τύπου B1241."},
    "B2261": {"cat": "Τρακτέρ", "series": "Σειρά B2 - T2a", "hp": 24.75, "price": 17500, "info": "24.75 HP - T2a", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα εργοστασίου κατασκευής KUBOTA Ιαπωνίας τύπου B2261."},
    "LX351": {"cat": "Τρακτέρ", "series": "Σειρά LX - T2a", "hp": 34.82, "price": 33500, "info": "34.82 HP - T2a", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA LX351."},
    "LX401": {"cat": "Τρακτέρ", "series": "Σειρά LX - T2a", "hp": 39.85, "price": 43500, "info": "39.85 HP - T2a", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA LX401."},
    "L2372": {"cat": "Τρακτέρ", "series": "Σειρά L2 - T2a", "hp": 36.58, "price": 35500, "info": "36.58 HP - T2a", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA L2372."},
    "L2452": {"cat": "Τρακτέρ", "series": "Σειρά L2 - T2a", "hp": 44.88, "price": 36500, "info": "44.88 HP - T2a", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA L2452."},
    "L2522": {"cat": "Τρακτέρ", "series": "Σειρά L2 - T2a", "hp": 50.86, "price": 37500, "info": "50.86 HP - T2a", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA L2522."},
    "L2552": {"cat": "Τρακτέρ", "series": "Σειρά L2 - T2a", "hp": 54.54, "price": 50000, "info": "54.54 HP - T2a", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA L2552."},
    "L2622": {"cat": "Τρακτέρ", "series": "Σειρά L2 - T2a", "hp": 61.34, "price": 58000, "info": "61.34 HP - T2a", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA L2622."},
    
    "M4063R": {"cat": "Τρακτέρ", "series": "Σειρά M4 - T1a", "hp": 66.37, "price": 47500, "info": "66.37 HP - T1a (ROPS)", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M4063 R."},
    "M4063C": {"cat": "Τρακτέρ", "series": "Σειρά M4 - T1a", "hp": 66.37, "price": 50500, "info": "66.37 HP - T1a (Cab)", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M4063 C."},
    "M4073R": {"cat": "Τρακτέρ", "series": "Σειρά M4 - T1a", "hp": 74.26, "price": 51500, "info": "74.26 HP - T1a (ROPS)", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M4073 R."},
    "M4073C": {"cat": "Τρακτέρ", "series": "Σειρά M4 - T1a", "hp": 74.26, "price": 54500, "info": "74.26 HP - T1a (Cab)", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M4073 C."},
    
    "M5072NR": {"cat": "Τρακτέρ", "series": "Σειρά M5 Narrow - T2a", "hp": 73.58, "price": 57500, "info": "73.58 HP - T2a (ROPS)", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M5072N R."},
    "M5072NC": {"cat": "Τρακτέρ", "series": "Σειρά M5 Narrow - T2a", "hp": 73.58, "price": 60500, "info": "73.58 HP - T2a (Cab)", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M5072N C."},
    "M5082NC": {"cat": "Τρακτέρ", "series": "Σειρά M5 Narrow - T2a", "hp": 87.45, "price": 63500, "info": "87.45 HP - T2a (Cab)", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M5082N C."},
    "M5092NR": {"cat": "Τρακτέρ", "series": "Σειρά M5 Narrow - T2a", "hp": 93.30, "price": 67500, "info": "93.30 HP - T2a (ROPS)", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M5092N R."},
    "M5092NC": {"cat": "Τρακτέρ", "series": "Σειρά M5 Narrow - T2a", "hp": 94.38, "price": 70500, "info": "94.38 HP - T2a (Cab)", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M5092N C."},
    "M5010NR": {"cat": "Τρακτέρ", "series": "Σειρά M5 Narrow - T2a", "hp": 104.31, "price": 74000, "info": "104.31 HP - T2a (ROPS)", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M5010N R."},
    "M5010NC": {"cat": "Τρακτέρ", "series": "Σειρά M5 Narrow - T2a", "hp": 105.94, "price": 77000, "info": "105.94 HP - T2a (Cab)", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M5010N C."},
    "M5112NC": {"cat": "Τρακτέρ", "series": "Σειρά M5 Narrow - T2a", "hp": 114.78, "price": 80000, "info": "114.78 HP - T2a (Cab)", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M5112N C."},

    "M5092R": {"cat": "Τρακτέρ", "series": "Σειρά M5 - T1a", "hp": 93.84, "price": 64500, "info": "93.84 HP - T1a (ROPS)", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M5092 R."},
    "M5092C": {"cat": "Τρακτέρ", "series": "Σειρά M5 - T1a", "hp": 96.42, "price": 67500, "info": "96.42 HP - T1a (Cab)", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M5092 C."},
    "M5112R": {"cat": "Τρακτέρ", "series": "Σειρά M5 - T1a", "hp": 107.17, "price": 68500, "info": "107.17 HP - T1a (ROPS)", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M5112 R."},
    "M5112C": {"cat": "Τρακτέρ", "series": "Σειρά M5 - T1a", "hp": 114.78, "price": 72000, "info": "114.78 HP - T1a (Cab)", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M5112 C."},
    
    "M6121U": {"cat": "Τρακτέρ", "series": "Σειρά M6 - T1a", "hp": 123.49, "price": 89000, "info": "123.49 HP - T1a", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M6121 U."},
    "M6131U": {"cat": "Τρακτέρ", "series": "Σειρά M6 - T1a", "hp": 133.42, "price": 93000, "info": "133.42 HP - T1a", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M6131 U."},
    "M6141U": {"cat": "Τρακτέρ", "series": "Σειρά M6 - T1a", "hp": 143.48, "price": 97000, "info": "143.48 HP - T1a", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M6141 U."},
    
    "M6122": {"cat": "Τρακτέρ", "series": "Σειρά M6 - T1a", "hp": 123.50, "price": 90000, "info": "123.50 HP - T1a", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M6122."},
    "M6132": {"cat": "Τρακτέρ", "series": "Σειρά M6 - T1a", "hp": 133.40, "price": 94000, "info": "133.40 HP - T1a", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M6132."},
    "M6142": {"cat": "Τρακτέρ", "series": "Σειρά M6 - T1a", "hp": 143.40, "price": 98000, "info": "143.40 HP - T1a", "desc": "Ένα καινούριο και αμεταχειριστό γεωργικό ελκυστήρα KUBOTA M6142."},
    
    "RTV-X1110": {"cat": "Τρακτέρ", "series": "Utility - T1a", "hp": 21.62, "price": 22000, "info": "21.62 HP - T1a Utility", "desc": "Ένα καινούριο και αμεταχειριστό μηχάνημα KUBOTA RTV-X1110."},

    # --- 2. ΥΠΟΛΟΙΠΑ ΚΛΑΣΙΚΑ ΜΟΝΤΕΛΑ KUBOTA ---
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

    # --- 3. ΧΩΜΑΤΟΥΡΓΙΚΑ ---
    "K008-5 VHG": {"cat": "Χωματουργικό", "series": "Μικροί Εκσκαφείς", "weight": "975 kg", "price": 15700, "info": "Βασική Αξία Εκσκαφέα 975 kg", "desc": "Ένα καινούριο και αμεταχειριστό χωματουργικό μηχάνημα KUBOTA K008-5."},
    "U10-5 VHG": {"cat": "Χωματουργικό", "series": "Μικροί Εκσκαφείς", "weight": "1050 kg", "price": 17600, "info": "Βασική Αξία Εκσκαφέα 1050 kg", "desc": "Ένα καινούριο και αμεταχειριστό χωματουργικό μηχάνημα KUBOTA U10-5."},
    "U27-4 HGL": {"cat": "Χωματουργικό", "series": "Εκσκαφείς Μεσαίας Κατηγορίας", "weight": "2490 kg", "price": 32800, "info": "Σκέπαστρο 2490 kg", "desc": "Ένα καινούριο και αμεταχειριστό χωματουργικό μηχάνημα KUBOTA U27-4."},
    "KX060-5": {"cat": "Χωματουργικό", "series": "Εκσκαφείς Μεσαίας Κατηγορίας", "weight": "5555 kg", "price": 62000, "info": "5555 kg - Καμπίνα, Υδραυλική Ταχυσύνδεση", "desc": "Ένα καινούριο και αμεταχειριστό χωματουργικό μηχάνημα KUBOTA KX060-5."},

    # --- 4. ΜΑΝΕΖ ΛΟΖΑΝΟ (Ψεκαστικά & Παρελκόμενα) ---
    "NTW10S/4": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S4-S5", "price": 15400, "info": "Ψεκαστικό NARROW TW S4-S5 — Φτερωτή Ø 820 — 1000 λίτρα", "desc": "Ψεκαστικό NARROW TW S4-S5 — Φτερωτή Ø 820 — 1000 λίτρα."},
    "NTW15S/5": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S4-S5", "price": 17700, "info": "Ψεκαστικό NARROW TW S4-S5 — Φτερωτή Ø 920 — 1500 λίτρα", "desc": "Ψεκαστικό NARROW TW S4-S5 — Φτερωτή Ø 920 — 1500 λίτρα."},
    "NTW20S/5": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S4-S5", "price": 18600, "info": "Ψεκαστικό NARROW TW S4-S5 — Φτερωτή Ø 920 — 2000 λίτρα", "desc": "Ψεκαστικό NARROW TW S4-S5 — Φτερωτή Ø 920 — 2000 λίτρα."},
    "NTW30S/5": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S4-S5", "price": 21900, "info": "Ψεκαστικό NARROW TW S4-S5 — Φτερωτή Ø 920 — 3000 λίτρα", "desc": "Ψεκαστικό NARROW TW S4-S5 — Φτερωτή Ø 920 — 3000 λίτρα."},
    "NTW15S/6": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S6", "price": 18600, "info": "Ψεκαστικό NARROW TW S6 (NORMAL) — Φτερωτή Ø 920 — 1500 λίτρα", "desc": "Ψεκαστικό NARROW TW S6 (NORMAL) — Φτερωτή Ø 920 — 1500 λίτρα."},
    "NTW20S/6": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S6", "price": 19600, "info": "Ψεκαστικό NARROW TW S6 (NORMAL) — Φτερωτή Ø 920 — 2000 λίτρα", "desc": "Ψεκαστικό NARROW TW S6 (NORMAL) — Φτερωτή Ø 920 — 2000 λίτρα."},
    "NTW30S/6": {"cat": "Μανέζ Λοζάνο", "series": "NARROW TW S6", "price": 22800, "info": "Ψεκαστικό NARROW TW S6 (NORMAL) — Φτερωτή Ø 920 — 3000 λίτρα", "desc": "Ψεκαστικό NARROW TW S6 (NORMAL) — Φτερωτή Ø 920 — 3000 λίτρα."},
    "RANT720": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 390, "info": "Πλέγμα προστασίας από D720", "desc": "Πλέγμα προστασίας από D720."},
    "KITFRENR": {"cat": "Μανέζ Λοζάνο", "series": "Παρελκόμενα & Αξεσουάρ", "price": 770, "info": "Υδραυλικά φρένα με ρυθμιστική βαλβίδα", "desc": "Υδραυλικά φρένα με ρυθμιστική βαλβίδα."},

    # --- 5. ΝΙΟΥΜΠΟ (Καταστροφείς) ---
    "TLG120": {"cat": "Νιούμπο", "series": "LIGHT", "price": 4150, "info": "Καταστροφέας LIGHT 1200mm", "desc": "Καταστροφέας LIGHT 1200mm — 320kg — 25-35 Hp."},
    "TLG140": {"cat": "Νιούμπο", "series": "LIGHT", "price": 4200, "info": "Καταστροφέας LIGHT 1400mm", "desc": "Καταστροφέας LIGHT 1400mm — 350kg — 25-35 Hp."},
    "TLG160": {"cat": "Νιούμπο", "series": "LIGHT", "price": 4300, "info": "Καταστροφέας LIGHT 1600mm", "desc": "Καταστροφέας LIGHT 1600mm — 370kg — 30-40 Hp."},
    "TLG180": {"cat": "Νιούμπο", "series": "LIGHT", "price": 4400, "info": "Καταστροφέας LIGHT 1800mm", "desc": "Καταστροφέας LIGHT 1800mm — 390kg — 35-50 Hp."},
    "TGD130": {"cat": "Νιούμπο", "series": "GLIDER", "price": 5100, "info": "Καταστροφέας GLIDER 1300mm", "desc": "Καταστροφέας GLIDER 1300mm — 420kg — 28-38 Hp."},
    "TGD160": {"cat": "Νιούμπο", "series": "GLIDER", "price": 5300, "info": "Καταστροφέας GLIDER 1600mm", "desc": "Καταστροφέας GLIDER 1600mm — 450kg — 48-58 Hp."},

    # --- 6. ΚΟΠΡΟΔΙΑΝΟΜΕΙΣ ID DAVID ---
    "DES-2525-T": {"cat": "Κοπροδιανομείς ID DAVID", "series": "SURFEED", "price": 13700, "info": "Κοπροδιανομέας SURFEED 2.5m³", "desc": "Κοπροδιανομέας SURFEED 2.5m³ — Πλάτος 1.46m — 40 HP."},
    "DES-4535-T": {"cat": "Κοπροδιανομείς ID DAVID", "series": "SURFEED", "price": 15200, "info": "Κοπροδιανομέας SURFEED 3.5m³", "desc": "Κοπροδιανομέας SURFEED 3.5m³ — Πλάτος 1.50m — 50 HP."},
    "DES-5540-T": {"cat": "Κοπροδιανομείς ID DAVID", "series": "SURFEED", "price": 16800, "info": "Κοπροδιανομέας SURFEED 4.0m³", "desc": "Κοπροδιανομέας SURFEED 4.0m³ — Πλάτος 1.80m — 55 HP."},
    "DES-7560-T": {"cat": "Κοπροδιανομείς ID DAVID", "series": "SURFEED", "price": 21800, "info": "Κοπροδιανομέας SURFEED 6.0m³", "desc": "Κοπροδιανομέας SURFEED 6.0m³ — Πλάτος 2.04m — 75 HP."},
    "ID_TOUCHSCREEN": {"cat": "Κοπροδιανομείς ID DAVID", "series": "Εξοπλισμός / Χειριστήρια", "price": 1500, "info": "Touchscreen 7\"", "desc": "Touchscreen Οθόνη Αφής 7\" με υπολογιστή επεξεργασίας δεδομένων."}
}

# --- ΕΞΥΠΝΗ ΑΥΤΟΜΑΤΗ ΔΗΜΙΟΥΡΓΙΑ ΠΕΡΙΓΡΑΦΗΣ (Υποστηρίζει Ελληνικά & Αγγλικά) ---
def generate_auto_description(model_key, item_data, is_en=False):
    cat_name = item_data.get("cat", "Μηχάνημα")
    series_name = item_data.get("series", "")
    info_text = item_data.get("info", "")

    if is_en:
        if cat_name == "Τρακτέρ":
            mach_desc = f"brand new and unused KUBOTA agricultural tractor type {model_key}"
        elif cat_name == "Χωματουργικό":
            mach_desc = f"brand new and unused KUBOTA excavation machine type {model_key}"
        elif cat_name == "Μανέζ Λοζάνο":
            mach_desc = f"brand new and unused Manez Lozano sprayer type {model_key} ({info_text})"
        elif cat_name == "Νιούμπο":
            mach_desc = f"brand new and unused Niubo shredder type {model_key} ({info_text})"
        elif cat_name == "Κοπροδιανομείς ID DAVID":
            mach_desc = f"brand new and unused ID DAVID manure spreader type {model_key} ({info_text})"
        else:
            mach_desc = f"machine {model_key}"

        text = f"A {mach_desc} equipped with an approved safety roll-bar/cab. "
        text += f"It features standard equipment of series {series_name} and technical specifications: {info_text}."
    else:
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

        text = f"Ένα καινούριο και αμεταχείριστό {mach_desc} με αψίδα προστασίας εγκεκριμένου τύπου. "
        text += f"Διαθέτει βασικό εξοπλισμό σειράς {series_name} και τεχνικά χαρακτηριστικά: {info_text}."

    return text

# Λεξικό μετάφρασης προαιρετικού εξοπλισμού
optional_equipment_translations = {
    "Υδραυλική τιράντα": "Hydraulic top link",
    "Υδραυλικό ραντάρ": "Hydraulic radar",
    "Αντίβαρα στους πίσω τροχούς": "Rear wheel ballast weights",
    "Εμπρόσθια Υδραυλικά": "Front linkage",
    "Αεροκάθισμα": "Air suspension seat"
}

def translate_optional_equipment(text, is_en):
    if not is_en:
        return text
    lines = text.split('\n')
    translated_lines = []
    for line in lines:
        clean_line = line.strip()
        if clean_line in optional_equipment_translations:
            translated_lines.append(optional_equipment_translations[clean_line])
        else:
            translated_lines.append(clean_line)
    return '\n'.join(translated_lines)

def translate_info(text, is_en):
    if not is_en:
        return text
    translations_map = {
        "Υδροστατικό κιβώτιο ταχυτήτων, Καμπίνα": "Hydrostatic transmission, Cabin",
        "Υδροστατικό κιβώτιο ταχυτήτων, ROPS": "Hydrostatic transmission, ROPS",
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

    if company in ["Πετρόπουλος", "Petropoulos"]:
        logo_path = "petropoulos_logo.jpeg"
        if os.path.exists(logo_path):
            c.drawImage(logo_path, width - 180, height - 70, width=130, height=45, preserveAspectRatio=True, mask='auto')

    c.setFont(font_bld, 14)
    c.drawString(50, height - 40, "ΠΕΤΡΟΣ ΠΕΤΡΟΠΟΥΛΟΣ ΑΕΒΕ" if not is_english else comp_display)
    
    c.setFont(font_reg, 9)
    c.drawString(50, height - 55, "Τμήμα Γεωργικών & Χωματουργικών Μηχανημάτων" if not is_english else "Machinery Department")
    
    c.drawRightString(width - 50, height - 40, "Τηλέφωνα : 210 - 3499333")
    c.drawRightString(width - 50, height - 55, f"E-mail : {seller_data['email']}")
    formatted_date_str = offer_date.strftime("Αθήνα, %d %B %Y") if not is_english else offer_date.strftime("Athens, %B %d, %Y")
    c.drawRightString(width - 50, height - 70, formatted_date_str)
    
    c.setStrokeColorRGB(0.2, 0.3, 0.5)
    c.setLineWidth(1)
    c.line(50, height - 80, width - 50, height - 80)
    
    c.setFont(font_bld, 11)
    c.drawString(50, height - 102, "ΣΤΟΙΧΕΙΑ ΠΕΛΑΤΗ:" if not is_english else "CLIENT DETAILS:")
    c.setFont(font_reg, 9)
    y_client = height - 116
    c.drawString(50, y_client, f"ΠΡΟΣ: {client_data['name'].upper()}" if not is_english else f"TO: {client_data['name'].upper()}")
    y_client -= 14
    c.drawString(50, y_client, f"ΔΙΕΥΘΥΝΣΗ: {client_data['address'].upper()}" if not is_english else f"ADDRESS: {client_data['address'].upper()}")
    y_client -= 14
    c.drawString(50, y_client, f"ΑΦΜ: {client_data['afm']}  |  ΤΗΛΕΦΩΝΟ: {client_data['phone']}" if not is_english else f"VAT: {client_data['afm']}  |  PHONE: {client_data['phone']}")
    y_client -= 14
    c.drawString(50, y_client, f"ΕΠΑΓΓΕΛΜΑ: {client_data['profession'].upper()}" if not is_english else f"PROFESSION: {client_data['profession'].upper()}")
        
    y_client -= 14
    c.setStrokeColorRGB(0.7, 0.7, 0.7)
    c.setLineWidth(0.5)
    c.line(50, y_client, width - 50, y_client)
    
    y = y_client - 20
    c.setFont(font_bld, 12)
    c.drawCentredString(width / 2.0, y, "ΟΙΚΟΝΟΜΙΚΗ ΠΡΟΣΦΟΡΑ" if not is_english else "COMMERCIAL OFFER")
    
    y -= 20
    c.setFont(font_reg, 9)
    c.drawString(50, y, f"Αξιότιμε/η κ. {client_data['name']}," if not is_english else f"Dear {client_data['name']},")
    y -= 14
    c.drawString(50, y, "Κατόπιν επιθυμίας σας για την αγορά εξοπλισμού από την εταιρεία μας είμαστε στην ευχάριστη θέση να σας προσφέρουμε τα εξής:" if not is_english else "Following your request for equipment purchase, we are pleased to offer you the following:")
    
    y -= 10
    total_net = 0
    
    for idx, item in enumerate(cart_items, 1):
        y -= 16
        c.setFont(font_bld, 9)
        model_label = f"{idx})  Μοντέλο: {item['model']} — Καθαρή Αξία: {item['price']:,.2f} EUR" if not is_english else f"{idx})  Model: {item['model']} — Net Value: {item['price']:,.2f} EUR"
        c.drawString(50, y, model_label)
        
        y -= 14
        c.setFont(font_reg, 9)
        desc_full = item.get('desc', item['info'])
        c.drawString(65, y, desc_full[:110])
        if len(desc_full) > 110:
            y -= 12
            c.drawString(65, y, desc_full[110:])
            
        total_net += item['price']
        y -= 8

    if optional_equipment:
        y -= 12
        c.setFont(font_bld, 9)
        c.drawString(50, y, "Περιλαμβάνει τον παρακάτω προαιρετικό εξοπλισμό:" if not is_english else "Includes the following optional equipment:")
        for line in optional_equipment.split('\n'):
            if line.strip():
                y -= 12
                c.setFont(font_reg, 9)
                c.drawString(65, y, f"- {line.strip()}")

    vat_amount = total_net * (vat_rate / 100.0)
    total_with_vat = total_net + vat_amount

    y -= 28
    c.setStrokeColorRGB(0.2, 0.3, 0.5)
    c.setLineWidth(1)
    c.rect(50, y - 22, width - 100, 32)
    
    c.setFont(font_bld, 9)
    c.drawString(90, y - 4, "Αξία Προσφοράς" if not is_english else "Offer Value")
    c.drawString(275, y - 4, f"ΦΠΑ {vat_rate}%" if not is_english else f"VAT {vat_rate}%")
    c.drawString(450, y - 4, "Σύνολο" if not is_english else "Total")
    
    c.setFont(font_reg, 10)
    c.drawString(85, y - 18, f"{total_net:,.2f} €")
    c.drawString(270, y - 18, f"{vat_amount:,.2f} €")
    c.drawString(440, y - 18, f"{total_with_vat:,.2f} €")

    y -= 38
    c.setFont(font_reg, 8)
    note_text = "• Ο εξοπλισμός διαθέτει ελληνική και ευρωπαϊκή έγκριση τύπου & καλύπτεται από εργοστασιακή εγγύηση ενός έτους." if not is_english else "• The equipment has Greek and European type approval & is covered by a one-year factory warranty."
    c.drawString(50, y, note_text)

    y -= 32
    c.setFont(font_bld, 9)
    c.drawString(50, y, f"{seller_data['name']} - {seller_data['title']}")

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
st.markdown("Δημιουργήστε οικονομικές προσφορές εύκολα από το PC ή το κινητό σας!" if not is_english else "Easily create commercial offers from your PC or mobile!")

with st.sidebar:
    st.header("👤 Στοιχεία Πωλητή / Συντάκτη" if not is_english else "👤 Salesperson Details")
    seller_name = st.text_input("Ονοματεπώνυμο Πωλητή" if not is_english else "Salesperson Name", value="Νικήτας Μπάρλας")
    seller_title = st.text_input("Τίτλος Θέσης" if not is_english else "Job Title", value="Επιθεωρητής Πωλήσεων" if not is_english else "Sales Inspector")
    seller_email = st.text_input("Email Πωλητή" if not is_english else "Salesperson Email", value="nikitasb@petropoulos.com")
    offer_date = st.date_input("Ημερομηνία Προσφοράς" if not is_english else "Offer Date", value=datetime.today())
    vat_rate = st.selectbox("Ποσοστό ΦΠΑ (%)" if not is_english else "VAT Rate (%)", [13, 24], index=0)

with st.expander("👤 1. Στοιχεία Πελάτη (Συμπληρώστε τα στοιχεία)" if not is_english else "👤 1. Client Details (Fill in details)", expanded=True):
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

with st.expander("⚙️ 2. Επιλογή Προϊόντος & Χαρακτηριστικά" if not is_english else "⚙️ 2. Product Selection & Features", expanded=True):
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
        auto_desc = generate_auto_description(selected_model, current_item, is_english)
        
        st.markdown(f"**{'Model Price' if is_english else 'Τιμή Μοντέλου'}:** :red[{current_item['price']:,.2f} EUR]")
        custom_desc = st.text_area("Αναλυτική Περιγραφή Μηχανήματος στο PDF (Προσαρμόζεται αυτόματα)" if not is_english else "Detailed Machine Description in PDF (Auto-adapts)", value=auto_desc, height=120)
    else:
        custom_desc = ""

    default_opt_eq = "Υδραυλική τιράντα\nΥδραυλικό ραντάρ\nΑντίβαρα στους πίσω τροχούς\nΕμπρόσθια Υδραυλικά\nΑεροκάθισμα"
    optional_equipment = st.text_area("Προαιρετικός Εξοπλισμός (ένα σε κάθε γραμμή)" if not is_english else "Optional Equipment (one per line)", value=default_opt_eq)

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
        
        final_optional_eq = translate_optional_equipment(optional_equipment, is_english)

        pdf_data = generate_pdf_bytes(client_data, seller_data, st.session_state.cart, company, is_english, offer_date, vat_rate, final_optional_eq)
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
        