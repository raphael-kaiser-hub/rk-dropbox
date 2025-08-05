import dropbox
import os
import fitz  # PyMuPDF

DROPBOX_TOKEN = os.getenv("DROPBOX_TOKEN")

def get_pdf_text(path):
    dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    _, res = dbx.files_download(path)
    with open("temp.pdf", "wb") as f:
        f.write(res.content)

    doc = fitz.open("temp.pdf")
    text = "\n\n".join(page.get_text() for page in doc)
    return text