import os
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io
import datetime

# 1. Βασική διαμόρφωση σελίδας και PWA Icon
st.set_page_config(
    page_title="Εφαρμογή Προσφορών Τρακτέρ", 
    page_icon="KUBOTA ICON.png",  
    layout="centered"
)

# 2. Εγγραφή γραμματοσειρών Times New Roman τοπικά (για υποστήριξη ελληνικών σε Cloud/Linux & Windows)
def register_local_fonts():
    font_path = "times.ttf"
    font_bold_path = "timesbd.ttf"
    
    if os.path.exists(font_path) and os.path.exists(font_bold_path):
        pdfmetrics.registerFont(TTFont('WinTimes', font_path))
        pdfmetrics.registerFont(TTFont('WinTimes-Bold', font_bold_path))
        return True
    return False

register_local_fonts()

st.title("🚜 Γεννήτρια Προσφορών Τρακτέρ & Μηχανημάτων")
st.write("Επιλέξτε εταιρεία και συμπληρώστε τα στοιχεία της νέας προσφοράς!")

# 1. Επιλογή Εταιρείας
company = st.selectbox(
    "Επιλέξτε Εταιρεία:",
    ["Φίλης Βασίλειος", "Πέτρος Πετρόπουλος ΑΕΒΕ", "Κάμπος Α.Ε."]
)

st.divider()

# 2. Στοιχεία Πελάτη
st.subheader("Στοιχεία Πελάτη")
col1, col2 = st.columns(2)
with col1:
    client_name = st.text_input("Ονοματεπώνυμο Πελάτη", "")
    client_address = st.text_input("Διεύθυνση", "")
    client_job = st.text_input("Επάγγελμα", "")
with col2:
    client_afm = st.text_input("ΑΦΜ / ΔΟΥ", "")
    client_tel = st.text_input("Τηλέφωνο", "")
    offer_date = st.text_input("Ημερομηνία", f"Αθήνα, {datetime.date.today().strftime('%d/%m/%Y')}")

st.divider()

# 3. Εισαγωγικό Κείμενο
st.subheader("Εισαγωγικό Κείμενο")
editable_text = st.text_area(
    "Κείμενο προσφώνησης / εισαγωγής:", 
    value="", 
    height=80, 
    key="intro_text", 
    placeholder="Π.χ. Κατόπιν επιθυμίας σας για την αγορά γεωργικού εξοπλισμού..."
)

st.divider()

# 4. Δυναμική Επιλογή Πλήθους Προσφορών / Ειδών
st.subheader("Αναλυτικά Είδη / Προσφορές")
num_offers = st.number_input(
    "Πόσες προσφορές/είδη θέλετε να προσθέσετε;", 
    min_value=1, 
    max_value=10, 
    value=1, 
    step=1
)

offers_list = []
for i in range(1, int(num_offers) + 1):
    st.markdown("---")
    st.markdown(f"**Προσφορά {i}**")
    desc = st.text_area(
        f"Περιγραφή {i}", 
        value="", 
        height=100, 
        key=f"desc_{i}", 
        placeholder="Γράψτε την περιγραφή του είδους..."
    )
    price = st.text_input(
        f"Αξία Προσφοράς {i}", 
        value="", 
        key=f"price_{i}", 
        placeholder="Π.χ. 45.600€ + Φ.Π.Α."
    )
    offers_list.append({"desc": desc, "price": price})

st.divider()

# 5. Δημιουργία PDF με ReportLab
if st.button("Δημιουργία & Λήψη Οικονομικής Προσφοράς PDF", type="primary"):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    
    styles = getSampleStyleSheet()
    
    # Ορισμός στυλ με τις τοπικές γραμματοσειρές Times
    title_style = ParagraphStyle(
        'TitleStyle',
        fontName='WinTimes-Bold',
        fontSize=14,
        leading=18,
        alignment=1, # Κέντρο
        textColor=colors.HexColor("#1b4d3e")
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        fontName='WinTimes',
        fontSize=10,
        leading=14
    )
    
    body_bold_style = ParagraphStyle(
        'BodyBoldStyle',
        fontName='WinTimes-Bold',
        fontSize=10,
        leading=14
    )

    # Ημερομηνία δεξιά πάνω
    date_style = ParagraphStyle(
        'DateStyle',
        fontName='WinTimes',
        fontSize=10,
        alignment=2 # Δεξιά
    )
    story.append(Paragraph(offer_date, date_style))
    story.append(Spacer(1, 10))
    
    # Τίτλος Εγγράφου
    story.append(Paragraph("ΟΙΚΟΝΟΜΙΚΗ ΠΡΟΣΦΟΡΑ", title_style))
    story.append(Spacer(1, 15))
    
    # Στοιχεία πελάτη
    client_text = f"""
    <b>ΠΡΟΣ:</b> {client_name}<br/>
    <b>ΔΙΕΥΘΥΝΣΗ:</b> {client_address}<br/>
    <b>ΑΦΜ / ΔΟΥ:</b> {client_afm}<br/>
    <b>ΕΠΑΓΓΕΛΜΑ:</b> {client_job}<br/>
    <b>ΤΗΛ:</b> {client_tel}
    """
    story.append(Paragraph(client_text, body_style))
    story.append(Spacer(1, 12))
    
    # Προσφώνηση
    story.append(Paragraph("Αγαπητέ κύριε,", body_style))
    story.append(Spacer(1, 8))
    
    # Εισαγωγικό κείμενο (αν έχει συμπληρωθεί)
    if editable_text.strip():
        story.append(Paragraph(editable_text, body_style))
        story.append(Spacer(1, 12))
        
    # Εκτύπωση προσφορών δυναμικά
    for idx, offer in enumerate(offers_list, start=1):
        if offer["desc"].strip():
            offer_block = f"<b>{idx})</b> {offer['desc']}<br/><b>Αξία προσφοράς:</b> {offer['price']}"
            story.append(Paragraph(offer_block, body_style))
            story.append(Spacer(1, 10))
            
    # Χτισίμο PDF
    doc.build(story)
    buffer.seek(0)
    
    st.success("Η οικονομική προσφορά δημιουργήθηκε με επιτυχία!")
    
    st.download_button(
        label="📥 Κατεβάστε το PDF τώρα",
        data=buffer,
        file_name="oikonomiki_prosfora.pdf",
        mime="application/pdf"
    )
    