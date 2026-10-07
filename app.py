import os
from datetime import datetime
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# Καταχώρηση των γραμματοσειρών Times New Roman
pdfmetrics.registerFont(TTFont('Times-Roman', 'times.ttf'))
pdfmetrics.registerFont(TTFont('Times-Bold', 'timesbd.ttf'))
pdfmetrics.registerFont(TTFont('Times-Italic', 'timesi.ttf'))
pdfmetrics.registerFont(TTFont('Times-BoldItalic', 'timesbi.ttf'))

# ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ
st.set_page_config(page_title="Σύστημα Προσφορών Kubota", page_icon="🚜", layout="centered")

# ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ (Μπορείτε να προσθέσετε όσα δεδομένα θέλετε εδώ)
database = {
    # --- Σειρά B1 - Stage V ---
    "B1181D-EC": {"cat": "Τρακτέρ", "series": "Σειρά B1 - Stage V", "hp": 17, "price": 14500, "info": "17 HP - Σειρά B1"},
    "B1241D-EC": {"cat": "Τρακτέρ", "series": "Σειρά B1 - Stage V", "hp": 22, "price": 15500, "info": "22 HP - Mid ROPS"},
    
    # --- Σειρά B2 - Stage V ---
    "B2261DB-M5-S5": {"cat": "Τρακτέρ", "series": "Σειρά B2 - Stage V", "hp": 25, "price": 17500, "info": "25 HP - Σειρά B2"},
    "B2261 HDB-C-S5": {"cat": "Τρακτέρ", "series": "Σειρά B2 - Stage V", "hp": 25,"price": 27000, "info": "25 HP - Υδροστατικό, Καμπίνα"},
    
    # --- Σειρά LX - Stage V ---
    "LX351-F-R": {"cat": "Τρακτέρ", "series": "Σειρά LX - Stage V", "hp": 35, "price": 33500, "info": "35 HP - Υδροστατικό κιβώτιο ταχυτήτων, ROPS"},
    "LX351-M": {"cat": "Τρακτέρ", "series": "Σειρά LX - Stage V", "hp": 35, "price": 29500, "info": "35 HP - 12/12 Mid ROPS"},
    "LX351-C-R": {"cat": "Τρακτέρ", "series": "Σειρά LX - Stage V", "hp": 35, "price": 40000, "info": "35 HP - Υδροστατικό κιβώτιο ταχυτήτων, Καμπίνα"},
    "LX401-F-R": {"cat": "Τρακτέρ", "series": "Σειρά LX - Stage V", "hp": 40, "price": 43500, "info": "40 HP - Υδροστατικό κιβώτιο ταχυτήτων, ROPS"},
    "LX401-C-R": {"cat": "Τρακτέρ", "series": "Σειρά LX - Stage V", "hp": 40, "price": 50000, "info": "40 HP - Υδροστατικό κιβώτιο ταχυτήτων, Καμπίνα"},
    
    # --- Νέα Σειρά L2 - Stage V ---
    "L2372DM": {"cat": "Τρακτέρ", "series": "Νέα Σειρά L2 - Stage V", "hp": 37, "price": 35500, "info": "37 HP - (16/16)"},
    "L2452DM": {"cat": "Τρακτέρ", "series": "Νέα Σειρά L2 - Stage V", "hp": 45, "price": 36500, "info": "45 HP - (16/16)"},
    "L2522DM": {"cat": "Τρακτέρ", "series": "Νέα Σειρά L2 - Stage V", "hp": 52, "price": 37500, "info": "52 HP - (16/16)"},
    "L2452DHC": {"cat": "Τρακτέρ", "series": "Νέα Σειρά L2 - Stage V", "hp": 47, "price": 45000, "info": "47 HP - Υδροστατικό κιβώτιο ταχυτήτων, Καμπίνα"},
    "L2552DHC": {"cat": "Τρακτέρ", "series": "Νέα Σειρά L2 - Stage V", "hp": 54, "price": 50000, "info": "54 HP - Υδροστατικό κιβώτιο ταχυτήτων, Καμπίνα"},
    "L2622DHC": {"cat": "Τρακτέρ", "series": "Νέα Σειρά L2 - Stage V", "hp": 62, "price": 58000, "info": "62 HP - Υδροστατικό κιβώτιο ταχυτήτων, Καμπίνα"},
    
    # --- Σειρά M5002-NARROW - Stage V ---
    "M5072N": {"cat": "Τρακτέρ", "series": "Σειρά M5002-NARROW - Stage V", "hp": 74, "price": 57500, "info": "74 HP - Ηλεκτρό-υδραυλική ρεβέρσα 36/36"},
    "M5-092N36-EC": {"cat": "Τρακτέρ", "series": "Σειρά M5002-NARROW - Stage V", "hp": 94, "price": 67500, "info": "94 HP - Ηλεκτρό-υδραυλική ρεβέρσα 36/36"},
    "M5-112NQ-EC": {"cat": "Τρακτέρ", "series": "Σειρά M5002-NARROW - Stage V", "hp": 115, "price": 78000, "info": "115 HP - Ηλεκτρό-υδραυλική ρεβέρσα 36/36"},
    
    # --- Σειρά M4003 - Stage V ---
    "M4063 DTH": {"cat": "Τρακτέρ", "series": "Σειρά M4003 - Stage V", "hp": 66, "price": 47500, "info": "66 HP - Ηλεκτρο-υδραυλική ρεβέρσα 18/18"},
    "M4073 DTH": {"cat": "Τρακτέρ", "series": "Σειρά M4003 - Stage V", "hp": 74, "price": 51500, "info": "74 HP - Ηλεκτρο-υδραυλική ρεβέρσα 36/36"},
    
    # --- Σειρά M5002 - Stage V ---
    "M5-092 DTH": {"cat": "Τρακτέρ", "series": "Σειρά M5002 - Stage V", "hp": 94, "price": 64500, "info": "94 HP - Ηλεκτρο-υδραυλική ρεβέρσα 36/36"},
    "M5-112 DTH": {"cat": "Τρακτέρ", "series": "Σειρά M5002 - Stage V", "hp": 107, "price": 65500, "info": "107 HP - Ηλεκτρο-υδραυλική ρεβέρσα 36/36"},
    
    # --- Χωματουργικά ---
    "K008-5 VHG": {"cat": "Χωματουργικό", "series": "Εκσκαφείς", "weight": "975 kg", "price": 15700, "info": "Βασική Αξία Εκσκαφέα 975 kg"},
    "U10-5 VHG": {"cat": "Χωματουργικό", "series": "Εκσκαφείς", "weight": "1050 kg", "price": 17600, "info": "Βασική Αξία Εκσκαφέα 1050 kg"},
    "U27-4 HGL": {"cat": "Χωματουργικό", "series": "Εκσκαφείς", "weight": "2490 kg", "price": 32800, "info": "Σκέπαστρο 2490 kg"}
}

# Διαχείριση καλαθιού στη μνήμη της εφαρμογής
if "cart" not in st.session_state:
    st.session_state.cart = []

def register_windows_fonts():
    # Χρησιμοποιούμε τα αρχεία που βρίσκονται απευθείας στον φάκελο του project μας
    font_path = "times.ttf"       # ή times.ttf ανάλογα ποια θες να χρησιμοποιήσεις
    font_bold_path = "timesbd.ttf" # ή timesbd.ttf

    if os.path.exists(font_path) and os.path.exists(font_bold_path):
        pdfmetrics.registerFont(TTFont('WinArial', font_path))
        pdfmetrics.registerFont(TTFont('WinArial-Bold', font_bold_path))
        return True
    
    return False

def generate_pdf_bytes(client_data, cart_items, company):
    pdf_filename = "temp_profora.pdf"
    has_font = register_windows_fonts()
    font_reg = 'WinArial' if has_font else 'Helvetica'
    font_bld = 'WinArial-Bold' if has_font else 'Helvetica-Bold'

    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter
    
    if company == "Πετρόπουλος":
        logo_path = "petropoulos_logo.jpeg"
        if os.path.exists(logo_path):
            c.drawImage(logo_path, width - 180, height - 70, width=130, height=45, preserveAspectRatio=True, mask='auto')

    # Επικεφαλίδα Εταιρείας
    c.setFont(font_bld, 16)
    c.drawString(50, height - 50, f"ΕΤΑΙΡΕΙΑ: {company}")
    c.setFont(font_reg, 10)
    c.drawString(50, height - 65, "Τμήμα Γεωργικών & Χωματουργικών Μηχανημάτων Kubota")
    
    c.setStrokeColorRGB(0.2, 0.3, 0.5)
    c.setLineWidth(1)
    c.line(50, height - 75, width - 50, height - 75)
    
    # Στοιχεία Πελάτη
    c.setFont(font_bld, 12)
    c.drawString(50, height - 100, "ΣΤΟΙΧΕΙΑ ΠΕΛΑΤΗ:")
    c.setFont(font_reg, 10)
    y_client = height - 118
    c.drawString(50, y_client, f"Ονοματεπώνυμο / Επωνυμία: {client_data['name']}")
    y_client -= 16
    c.drawString(50, y_client, f"Επάγγελμα: {client_data['profession']}")
    y_client -= 16
    c.drawString(50, y_client, f"ΑΦΜ: {client_data['afm']}")
    y_client -= 16
    c.drawString(50, y_client, f"Τηλέφωνο: {client_data['phone']}")
    y_client -= 16
    c.drawString(50, y_client, f"Διεύθυνση: {client_data['address']}")
        
    y_client -= 12
    c.setStrokeColorRGB(0.7, 0.7, 0.7)
    c.setLineWidth(0.5)
    c.line(50, y_client, width - 50, y_client)
    
    # Τίτλος Προσφοράς
    y = y_client - 25
    c.setFont(font_bld, 13)
    c.drawString(50, y, "ΟΙΚΟΝΟΜΙΚΗ ΠΡΟΣΦΟΡΑ")
    
    y -= 22
    c.setFont(font_reg, 10)
    c.drawString(50, y, f"Αξιότιμε/η κ. {client_data['name']}, σας αποστέλλουμε την προσφορά μας:")
    
    y -= 15
    total_net = 0
    
    for idx, item in enumerate(cart_items, 1):
        noun = "ελκυστήρα KUBOTA" if item["cat"] == "Τρακτέρ" else "εκσκαφέα KUBOTA"
        
        y -= 20
        c.setFont(font_bld, 10)
        c.drawString(50, y, f"{idx}. Μοντέλο: {item['model']} — Καθαρή Αξία: {item['price']:,.2f} EUR")
        
        y -= 15
        c.setFont(font_reg, 10)
        c.drawString(70, y, f"Ένα καινούριο και αμεταχειριστό {noun} ({item['info']})")
        
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
    c.drawString(50, y, f"Συνολική Καθαρή Αξία: {total_net:,.2f} EUR")
    y -= 18
    c.drawString(50, y, f"ΦΠΑ (24%): {vat:,.2f} EUR")
    y -= 20
    c.setFont(font_bld, 12)
    c.drawString(50, y, f"ΓΕΝΙΚΟ ΣΥΝΟΛΟ ΜΕ ΦΠΑ: {total_with_vat:,.2f} EUR")
    
    y -= 35
    c.setFont(font_reg, 10)
    c.drawString(50, y, f"Στη διάθεσή σας για οποιαδήποτε διευκρίνιση από την εταιρεία {company}!")
    
    c.save()
    
    with open(pdf_filename, "rb") as f:
        pdf_data = f.read()
    return pdf_data

# ΕΜΦΑΝΙΣΗ ΣΤΟ UI
st.title("🚜 Σύστημα Προσφορών Kubota")
st.markdown("Δημιουργήστε οικονομικές προσφορές εύκολα από το PC ή το κινητό σας!")

# 1. Στοιχεία Πελάτη
with st.expander("👤 1. Στοιχεία Πελάτη (Υποχρεωτικά Όλα)", expanded=True):
    company = st.selectbox("Εταιρεία", ["Πετρόπουλος", "Φίλης", "Κάμπος"])
    client_name = st.text_input("Όνομα Πελάτη")
    client_profession = st.text_input("Επάγγελμα")
    col1, col2 = st.columns(2)
    with col1:
        client_afm = st.text_input("ΑΦΜ")
    with col2:
        client_phone = st.text_input("Τηλέφωνο")
    client_address = st.text_input("Διεύθυνση")

# 2. Επιλογή Προϊόντος & Χαρακτηριστικά
with st.expander("⚙️ 2. Επιλογή Προϊόντος & Χαρακτηριστικά", expanded=True):
    categories = sorted(list(set(item["cat"] for item in database.values())))
    selected_cat = st.selectbox("Κατηγορία", categories)
    
    series_list = sorted(list(set(item["series"] for item in database.values() if item["cat"] == selected_cat)))
    selected_series = st.selectbox("Σειρά", series_list)
    
    model_list = [model for model, item in database.items() if item["cat"] == selected_cat and item["series"] == selected_series]
    selected_model = st.selectbox("Μοντέλο", model_list)
    
    if selected_model:
        current_item = database[selected_model]
        st.markdown(f"**Τιμή Μοντέλου:** :red[{current_item['price']:,.2f} EUR]")
        custom_info = st.text_input("Περιγραφή / Info", value=current_item["info"])
    else:
        custom_info = ""

    if st.button("➕ Προσθήκη στην Προσφορά"):
        if selected_model:
            st.session_state.cart.append({
                "model": selected_model,
                "cat": current_item["cat"],
                "price": current_item["price"],
                "info": custom_info
            })
            st.success(f"Το προϊόν {selected_model} προστέθηκε στην προσφορά!")
        else:
            st.error("Επιλέξτε έγκυρο μοντέλο.")

# 3. Επιλεγμένα Είδη Προσφοράς
with st.expander("🛒 3. Επιλεγμένα Είδη Προσφοράς", expanded=True):
    if st.session_state.cart:
        for idx, cart_item in enumerate(st.session_state.cart):
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.write(f"**{idx+1}. {cart_item['cat']} | {cart_item['model']}** — {cart_item['price']:,.2f} EUR")
            with col_b:
                if st.button("❌", key=f"del_{idx}"):
                    st.session_state.cart.pop(idx)
                    st.rerun()
        
        if st.button("🗑️ Εκκαθάριση Καλαθιού"):
            st.session_state.cart = []
            st.rerun()
    else:
        st.info("Το καλάθι είναι κενό.")

# Δημιουργία PDF
st.markdown("---")
if st.button("📄 Δημιουργία Συγκεντρωτικού PDF", type="primary", use_container_width=True):
    if not client_name:
        st.warning("Παρακαλώ συμπληρώστε το όνομα του πελάτη!")
    elif not client_profession:
        st.warning("Παρακαλώ συμπληρώστε το επάγγελμα του πελάτη!")
    elif not client_afm:
        st.warning("Παρακαλώ συμπληρώστε το ΑΦΜ του πελάτη!")
    elif not client_phone:
        st.warning("Παρακαλώ συμπληρώστε το τηλέφωνο του πελάτη!")
    elif not client_address:
        st.warning("Παρακαλώ συμπληρώστε τη διεύθυνση του πελάτη!")
    elif not st.session_state.cart:
        st.warning("Το καλάθι προσφοράς είναι κενό! Προσθέστε τουλάχιστον ένα προϊόν.")
    else:
        client_data = {
            "name": client_name,
            "profession": client_profession,
            "afm": client_afm,
            "phone": client_phone,
            "address": client_address
        }
        pdf_data = generate_pdf_bytes(client_data, st.session_state.cart, company)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_company = company.replace(" ", "_")
        safe_client = client_name.replace(" ", "_")
        pdf_filename = f"Profora_{safe_company}_{safe_client}_{timestamp}.pdf"
        
        st.download_button(
            label="📥 Λήψη Αρχείου PDF",
            data=pdf_data,
            file_name=pdf_filename,
            mime="application/pdf",
            use_container_width=True
        )
