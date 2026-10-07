import os
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

# 1. Βασική διαμόρφωση σελίδας και PWA Icon με το σωστό όνομα αρχείου
st.set_page_config(
    page_title="Kubota Sales Quotes",
    page_icon="KUBOTA ICON.png",  
    layout="wide"
)

# 2. Εγγραφή γραμματοσειρών Times New Roman τοπικά (συμβατότητα με Cloud/Linux & Windows)
def register_local_fonts():
    font_path = "times.ttf"
    font_bold_path = "timesbd.ttf"
    
    if os.path.exists(font_path) and os.path.exists(font_bold_path):
        pdfmetrics.registerFont(TTFont('WinTimes', font_path))
        pdfmetrics.registerFont(TTFont('WinTimes-Bold', font_bold_path))
        return True
    return False

register_local_fonts()

# 3. Πλαϊνό μενού για επιλογή γλώσσας
st.sidebar.header("⚙️ Ρυθμίσεις / Settings")
lang_option = st.sidebar.selectbox("Γλώσσα Εκτύπωσης / PDF Language", ["Ελληνικά", "English"])

# Ορισμός μεταφράσεων ανάλογα με τη γλώσσα
if lang_option == "English":
    t_title = "COMMERCIAL QUOTATION"
    t_client = "Client Name:"
    t_model = "Select Model:"
    t_btn = "Generate PDF Offer"
    t_success = "PDF successfully generated!"
    t_col_model = "Model"
    t_col_series = "Series"
    t_col_hp = "HP"
    t_col_price = "Price (€)"
else:
    t_title = "ΟΙΚΟΝΟΜΙΚΗ ΠΡΟΣΦΟΡΑ KUBOTA"
    t_client = "Όνομα Πελάτη:"
    t_model = "Επιλογή Μοντέλου:"
    t_btn = "Δημιουργία PDF Προσφοράς"
    t_success = "Η προσφορά δημιουργήθηκε με επιτυχία!"
    t_col_model = "Μοντέλο"
    t_col_series = "Σειρά"
    t_col_hp = "HP"
    t_col_price = "Τιμή (€)"

st.title("🚜 Kubota Sales Quote Generator")

# Ενδεικτική βάση δεδομένων τρακτέρ
tractors_db = {
    "B2261DB-M5-S5": {"cat": "Τρακτέρ", "series": "Σειρά B2 - Stage V", "hp": 25, "price": 17000},
    "B2261 HDB-C-S5": {"cat": "Τρακτέρ", "series": "Σειρά B2 - Stage V", "hp": 25, "price": 27000},
    "LX4510": {"cat": "Τρακτέρ", "series": "Σειρά LX - Stage V", "hp": 45, "price": 34000}
}

# Φόρμα εισαγωγής στοιχείων
client_name = st.text_input(t_client, "Γιώργος Παπαδόπουλος")
selected_model = st.selectbox(t_model, list(tractors_db.keys()))

item = tractors_db[selected_model]

if st.button(t_btn):
    # Δημιουργία PDF στη μνήμη
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    
    # Στυλ με χρήση της γραμματοσειράς WinTimes για σωστή εμφάνιση ελληνικών
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        fontName='WinTimes-Bold',
        fontSize=18,
        leading=22,
        alignment=1, # Κέντρο
        textColor=colors.HexColor("#1b4d3e")
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        fontName='WinTimes',
        fontSize=12,
        leading=16
    )

    # Προσθήκη τίτλου στο PDF
    story.append(Paragraph(t_title, title_style))
    story.append(Spacer(1, 20))
    
    # Στοιχεία πελάτη
    story.append(Paragraph(f"<b>{t_client}</b> {client_name}", body_style))
    story.append(Spacer(1, 15))
    
    # Πίνακας προσφοράς
    table_data = [
        [Paragraph(f"<b>{t_col_model}</b>", body_style), Paragraph(f"<b>{t_col_series}</b>", body_style), Paragraph(f"<b>{t_col_hp}</b>", body_style), Paragraph(f"<b>{t_col_price}</b>", body_style)],
        [Paragraph(selected_model, body_style), Paragraph(item['series'], body_style), Paragraph(str(item['hp']), body_style), Paragraph(f"{item['price']:,} €", body_style)]
    ]
    
    t = Table(table_data, colWidths=[150, 150, 80, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ]))
    
    story.append(t)
    doc.build(story)
    
    buffer.seek(0)
    
    st.success(t_success)
    
    # Κουμπί λήψης PDF
    st.download_button(
        label="📥 Download PDF Offer",
        data=buffer,
        file_name=f"Kubota_Offer_{selected_model}.pdf",
        mime="application/pdf"
    )
    