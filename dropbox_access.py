import dropbox
import os
import pdfplumber
import io

DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")

def get_pdf_text(path):
    dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    _, res = dbx.files_download(path)
    pdf_file = io.BytesIO(res.content)

    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n\n"

    return text.strip()
