import os
from flask import Flask, request, jsonify
import dropbox

app = Flask(__name__)

# Token holen und prüfen
DROPBOX_ACCESS_TOKEN = os.environ.get('DROPBOX_ACCESS_TOKEN')
print(">>> DEBUG: DROPBOX_ACCESS_TOKEN gesetzt?", bool(DROPBOX_ACCESS_TOKEN))
if not DROPBOX_ACCESS_TOKEN:
    raise Exception("DROPBOX_ACCESS_TOKEN ist nicht gesetzt!")

# Dropbox-Client initialisieren
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

@app.route('/list-root', methods=['GET'])
def list_root():
    try:
        result = dbx.files_list_folder('')
        entries = [entry.name for entry in result.entries]
        return jsonify({'entries': entries})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
@app.route('/extract-folder-text', methods=['GET'])
def extract_folder_text():
    folder_path = request.args.get('folder_path')
    if not folder_path:
        return jsonify({'error': 'folder_path fehlt'}), 400

    try:
        result_text = ""
        entries = dbx.files_list_folder(folder_path).entries

        for entry in entries:
            if isinstance(entry, dropbox.files.FileMetadata) and entry.name.endswith('.pdf'):
                _, res = dbx.files_download(entry.path_lower)
                pdf_bytes = res.content
                # Hier könnte z. B. mit pdfplumber gearbeitet werden
                result_text += f"\n--- {entry.name} ---\n[PDF-Inhalt hier extrahieren]"

        return jsonify({'text': result_text})
    
    except Exception as e:
        print(f">>> Fehler beim Verarbeiten des Ordners '{folder_path}':", repr(e))
        return jsonify({'error': str(e)}), 500
