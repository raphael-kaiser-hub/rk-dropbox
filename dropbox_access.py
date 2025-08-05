import dropbox
import os
import pdfplumber
import io

DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")

ALLOWED_FOLDER = "/Raphael Kaiser/RK IMMOBILIEN/LEB-Leistungserbringung/7- Kundenordner/LEB7-08SN - Schadensregulierung NRW/00_Rechnungen, Hilfsmittel, Vorlagen, etc/App, RC NRW"

def get_pdf_text(path):
    if not path.startswith(ALLOWED_FOLDER):
        raise Exception("Zugriff verweigert: Nur Zugriff auf den definierten Ordner erlaubt.")

    dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    _, res = dbx.files_download(path)
    pdf_file = io.BytesIO(res.content)

    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n\n"

    return text.strip()
