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

# ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ (Με διπλή περιγραφή GR / EN για τα χαρακτηριστικά)
database = {
    # --- Σειρά B1 - Stage V ---
    "B1181D-EC": {
        "cat": "Τρακτέρ", 
        "series": "Σειρά B1 - Stage V", 
        "hp": 17, 
        "price": 14500, 
        "info": "17 HP - Σειρά B1",
        "info_en": "17 HP - B1 Series"
    },
    "B1241D-EC": {
        "cat": "Τρακτέρ", 
        "series": "Σειρά B1 - Stage V", 
        "hp": 22, 
        "price": 15500, 
        "info": "22 HP - Mid ROPS",
        "info_en": "22 HP - Mid ROPS"
    },
    
    # --- Σειρά B2 - Stage V ---
    "B2261DB-M5-S5": {
        "cat": "Τρακτέρ", 
        "series": "Σειρά B2 - Stage V", 
        "hp": 25, 
        "price": 17500, 
        "info": "25 HP - Σειρά B2",
        "info_en": "25 HP - B2 Series"
    },
    "B2261 HDB-C-S5": {
        "cat": "Τρακτέρ", 
        "series": "Σειρά B2 - Stage V", 
        "hp": 25, 
        "price": 27000, 
        "info": "25 HP - Υδροστατικό, Καμπίνα",
        "info_en": "25 HP - Hydrostatic, Cabin"
    },
    
    # --- Σειρά LX - Stage V ---
    "LX351-F-R": {
        "cat": "Τρακτέρ", 
        "series": "Σειρά LX - Stage V", 
        "hp": 35, 
        "price": 33500, 
        "info": "35 HP - Υδροστατικό κιβώτιο ταχυτήτων, ROPS",
        "info_en": "35 HP - Hydrostatic transmission, ROPS"
    },
    "LX351-M": {
        "cat": "Τρακτέρ", 
        "series": "Σειρά LX - Stage V", 
        "hp": 35, 
        "price": 29500, 
        "info": "35 HP - 12/12 Mid ROPS",
        "info_en": "35 HP - 12/12 Mid ROPS"
    },
    "LX351-C-R": {
        "cat": "Τρακτέρ", 
        "series": "Σειρά LX - Stage V", 
        "hp": 35, 
        "price": 40000, 
        "info": "35 HP - Υδροστατικό κιβώτιο ταχυτήτων, Καμπίνα",
        "info_en": "35 HP - Hydrostatic transmission, Cabin"
    },
    "LX401-F-R": {
        "cat": "Τρακτέρ", 
        "series": "Σειρά LX - Stage V", 
        "hp": 40, 
        "price": 43500, 
        "info": "40 HP - Υδροστατικό κιβώτιο ταχυτήτων, ROPS",
        "info_en": "40 HP - Hydrostatic transmission, ROPS"
    },
    "LX401-C-R": {
        "cat": "Τρακτέρ", 
        "series": "Σειρά LX - Stage V", 
        "hp": 40, 
        "price": 50000, 
        "info": "40 HP - Υδροστατικό κιβώτιο ταχυτήτων, Καμπίνα",
        "info_en": "40 HP - Hydrostatic transmission, Cabin"
    },
    
    # --- Νέα Σειρά L2 - Stage V ---
    "L2372DM": {
        "cat": "Τρακτέρ", 
        "series": "Νέα Σειρά L2 - Stage V", 
        "hp": 37, 
        "price": 35500, 
        "info": "37 HP - (16/16)",
        "info_en": "37 HP - (16/16)"
    },
    "L2452DM": {
        "cat": "Τρακτέρ", 
        "series": "Νέα Σειρά L2 - Stage V", 
        "hp": 45, 
        "price": 36500, 
        "info": "45 HP - (16/16)",
        "info_en": "45 HP - (16/16)"
    },
    "L2522DM": {
        "cat": "Τρακτέρ", 
        "series": "Νέα Σειρά L2 - Stage V", 
        "hp": 52, 
        "price": 37500, 
        "info": "52 HP - (16/16)",
        "info_en": "52 HP - (16/16)"
    },
    "L2452DHC": {
        "cat": "Τρακτέρ", 
        "series": "Νέα Σειρά L2 - Stage V", 
        "hp": 47, 
        "price": 45000, 
        "info": "47 HP - Υδροστατικό κιβώτιο ταχυτήτων, Καμπίνα",
        "info_en": "47 HP - Hydrostatic transmission, Cabin"
    },
    "L2552DHC": {
        "cat": "Τρακτέρ", 
        "series": "Νέα Σειρά L2 - Stage V", 
        "hp": 54, 
        "price": 50000, 
        "info": "54 HP - Υδροστατικό κιβώτιο ταχυτήτων, Καμπίνα",
        "info_en": "54 HP - Hydrostatic transmission, Cabin"
    },
    "L2622DHC": {
        "cat": "Τρακτέρ", 
        "series": "Νέα Σειρά L2 - Stage V", 
        "hp": 62, 
        "price": 58000, 
        "info": "62 HP - Υδροστατικό κιβώτιο ταχυτήτων, Καμπίνα",
        "info_en": "62 HP - Hydrostatic transmission, Cabin"
    },
    
    # --- Σειρά M5002-NARROW - Stage V ---
    "M5072N": {
        "cat": "Τρακτέρ", 
        "series": "Σειρά M5002-NARROW - Stage V", 
        "hp": 74, 
        "price": 57500, 
        "info": "74 HP - Ηλεκτρό-υδραυλική ρεβέρσα 36/36",
        "info_en": "74 HP - Electro-hydraulic reverser 36/36"
    },
    "M5-092N36-EC": {
        "cat": "Τρακτέρ", 
        "series": "Σειρά M5002-NARROW - Stage V", 
        "hp": 94, 
        "price": 67500, 
        "info": "94 HP - Ηλεκτρό-υδραυλική ρεβέρσα 36/36",
        "info_en": "94 HP - Electro-hydraulic reverser 36/36"
    },
    "M5-112NQ-EC": {
        "cat": "Τρακτέρ", 
        "series": "Σειρά M5002-NARROW - Stage V", 
        "hp": 115, 
        "price": 78000, 
        "info": "115 HP - Ηλεκτρό-υδραυλική ρεβέρσα 36/36",
        "info_en": "115 HP - Electro-hydraulic reverser 36/36"
    },
    
    # --- Σειρά M4003 - Stage V ---
    "M4063 DTH": {
        "cat": "Τρακτέρ", 
        "series": "Σειρά M4003 - Stage V", 
        "hp": 66, 
        "price": 47500, 
        "info": "66 HP - Ηλεκτρο-υδραυλική ρεβέρσα 18/18",
        "info_en": "66 HP - Electro-hydraulic reverser 18/18"
    },
    "M4073 DTH": {
        "cat": "Τρακτέρ", 
        "series": "Σειρά M4003 - Stage V", 
        "hp": 74, 
        "price": 51500, 
        "info": "74 HP - Ηλεκτρο-υδραυλική ρεβέρσα 36/36",
        "info_en": "74 HP - Electro-hydraulic reverser 36/36"
    },
    
    # --- Σειρά M5002 - Stage V ---
    "M5-092 DTH": {
        "cat": "Τρακτέρ", 
        "series": "Σειρά M5002 - Stage V", 
        "hp": 94, 
        "price": 64500, 
        "info": "94 HP - Ηλεκτρο-υδραυλική ρεβέρσα 36/36",
        "info_en": "94 HP - Electro-hydraulic reverser 36/36"
    },
    "M5-112 DTH": {
        "cat": "Τρακτέρ", 
        "series": "Σειρά M5002 - Stage V", 
        "hp": 107, 
        "price": 65500, 
        "info": "107 HP - Ηλεκτρο-υδραυλική ρεβέρσα 36/36",
        "info_en": "107 HP - Electro-hydraulic reverser 36/36"
    },
    
    # --- Χωματουργικά ---
    "K008-5 VHG": {
        "cat": "Χωματουργικό", 
        "series": "Εκσκαφείς", 
        "weight": "975 kg", 
        "price": 15700, 
        "info": "Βασική Αξία Εκσκαφέα 975 kg",
        "info_en": "Basic Excavator Value 975 kg"
    },
    "U10-5 VHG": {
        "cat": "Χωματουργικό", 
        "series": "Εκσκαφείς", 
        "weight": "1050 kg", 
        "price": 17600, 
        "info": "Βασική Αξία Εκσκαφέα 1050 kg",
        "info_en": "Basic Excavator Value 1050 kg"
    },
    "U27-4 HGL": {
        "cat": "Χωματουργικό", 
        "series": "Εκσκαφείς", 
        "weight": "2490 kg", 
        "price": 32800, 
        "info": "Σκέπαστρο 2490 kg",
        "info_en": "Canopy 2490 kg"
    }
}

# Διαχείριση καλαθιού στη μνήμη της εφαρμογής
if "cart" not in st.session_state:
    st.session_state.cart = []

def register_local_fonts():
    font_path = "times.ttf"
    font_bold_path = "timesbd.ttf"
    win_font_path = "C:/Windows/Fonts/times.ttf"
    win_bold_path = "C:/Windows/Fonts/timesbd.ttf"
    if os.path.exists(font_path) and os.path.exists(font_bold_path):
        pdfmetrics.registerFont(TTFont('WinTimes', font_path))
        pdfmetrics.registerFont(TTFont('WinTimes-Bold', font_bold_path))
        return True
    elif os.path.exists(win_font_path) and os.path.exists(win_bold_path):
        pdfmetrics.registerFont(TTFont('WinTimes', win_font_path))
        pdfmetrics.registerFont(TTFont('WinTimes-Bold', win_bold_path))
        return True
    return False

def generate_pdf_bytes(client_data, cart_items, company, is_english):
    pdf_filename = "temp_profora.pdf"
    has_font = register_local_fonts()
    font_reg = 'WinTimes' if has_font else 'Helvetica'
    font_bld = 'WinTimes-Bold' if has_font else 'Helvetica-Bold'

    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter
    
    # Μετάφραση ονόματος εταιρείας για το PDF/Logo
    if is_english:
        comp_display = "Petropoulos" if company == "Πετρόπουλος" else ("Filis" if company == "Φίλης" else "Kampos")
    else:
        comp_display = company

    if company == "Πετρόπουλος":
        logo_path = "petropoulos_logo.jpeg"
        if os.path.exists(logo_path):
            c.drawImage(logo_path, width - 180, height - 70, width=130, height=45, preserveAspectRatio=True, mask='auto')

    # Επικεφαλίδα Εταιρείας
    c.setFont(font_bld, 16)
    comp_label = f"COMPANY: {comp_display}" if is_english else f"ΕΤΑΙΡΕΙΑ: {comp_display}"
    c.drawString(50, height - 50, comp_label)
    
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
        item_info = item['info_en'] if is_english and 'info_en' in item else item['info']
        if is_english:
            noun = "KUBOTA tractor" if item["cat"] == "Τρακτέρ" else "KUBOTA excavator"
            desc_text = f"A brand new and unused {noun} ({item_info})"
            cat_display = "Tractor" if item["cat"] == "Τρακτέρ" else "Excavator"
        else:
            noun = "ελκυστήρα KUBOTA" if item["cat"] == "Τρακτέρ" else "εκσκαφέα KUBOTA"
            desc_text = f"Ένα καινούριο και αμεταχειριστό {noun} ({item_info})"
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
        categories = ["Tractor" if c == "Τρακτέρ" else "Excavator" for c in raw_categories]
    else:
        categories = raw_categories
        
    selected_cat_ui = st.selectbox("Category / Κατηγορία", categories)
    
    selected_cat = "Τρακτέρ" if (is_english and selected_cat_ui == "Tractor") or (not is_english and selected_cat_ui == "Τρακτέρ") else "Χωματουργικό"
    
    series_list = sorted(list(set(item["series"] for item in database.values() if item["cat"] == selected_cat)))
    selected_series = st.selectbox("Series / Σειρά", series_list)
    
    model_list = [model for model, item in database.items() if item["cat"] == selected_cat and item["series"] == selected_series]
    selected_model = st.selectbox("Model / Μοντέλο", model_list)
    
    if selected_model:
        current_item = database[selected_model]
        default_info = current_item["info_en"] if is_english else current_item["info"]
        st.markdown(f"**{'Model Price' if is_english else 'Τιμή Μοντέλου'}:** :red[{current_item['price']:,.2f} EUR]")
        custom_info = st.text_input("Description / Info / Περιγραφή", value=default_info)
    else:
        custom_info = ""

    if st.button("➕ " + ("Add to Quote" if is_english else "Προσθήκη στην Προσφορά")):
        if selected_model:
            st.session_state.cart.append({
                "model": selected_model,
                "cat": current_item["cat"],
                "price": current_item["price"],
                "info": custom_info,
                "info_en": custom_info if is_english else current_item.get("info_en", custom_info)
            })
            st.success("Product added!" if is_english else f"Το προϊόν {selected_model} προστέθηκε στην προσφορά!")
        else:
            st.error("Select valid model." if is_english else "Επιλέξτε έγκυρο μοντέλο.")

# 3. Επιλεγμένα Είδη Προσφοράς
with st.expander("🛒 " + ("3. Selected Quote Items" if is_english else "3. Επιλεγμένα Είδη Προσφοράς"), expanded=True):
    if st.session_state.cart:
        for idx, cart_item in enumerate(st.session_state.cart):
            display_cat = "Tractor" if (is_english and cart_item['cat'] == "Τρακτέρ") else ("Excavator" if is_english else cart_item['cat'])
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
        safe_company = company.replace(" ", "_")
        safe_client = client_name.replace(" ", "_")
        pdf_filename = f"Profora_{safe_company}_{safe_client}_{timestamp}.pdf"
        
        st.download_button(
            label="📥 " + ("Download PDF File" if is_english else "Λήψη Αρχείου PDF"),
            data=pdf_data,
            file_name=pdf_filename,
            mime="application/pdf",
            use_container_width=True
        )
        