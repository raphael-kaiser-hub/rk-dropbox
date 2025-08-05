import os
print(">>> DEBUG: DROPBOX_ACCESS_TOKEN vorhanden?", bool(os.environ.get('DROPBOX_ACCESS_TOKEN')))

from flask import Flask, request, jsonify
import dropbox

app = Flask(__name__)

# Token holen
DROPBOX_ACCESS_TOKEN = os.environ.get('DROPBOX_ACCESS_TOKEN')
print(">>> DEBUG: DROPBOX_ACCESS_TOKEN gesetzt?", bool(DROPBOX_ACCESS_TOKEN))

# Token prüfen
if not DROPBOX_ACCESS_TOKEN:
    raise Exception("DROPBOX_ACCESS_TOKEN ist nicht gesetzt!")

# Dropbox-Client initialisieren
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

@app.route('/extract-folder-text', methods=['GET'])
def extract_folder_text():
    folder_path = request.args.get('folder_path')
    if not folder_path:
        return jsonify({'error': 'folder_path fehlt'}), 400

    result_text = ""
    try:
        entries = dbx.files_list_folder(folder_path).entries
    except Exception as list_error:
        print(">>> Fehler bei files_list_folder:", list_error)
        raise list_error

    try:
        for entry in entries:
            if isinstance(entry, dropbox.files.FileMetadata) and entry.name.endswith('.pdf'):
                _, res = dbx.files_download(entry.path_lower)
                pdf_bytes = res.content
                # Hier müsste die PDF-Extraktion eingebaut werden, z. B. mit pdfplumber
                result_text += f"\n--- {entry.name} ---\n[PDF-Inhalt hier extrahieren]"
        return jsonify({'text': result_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
