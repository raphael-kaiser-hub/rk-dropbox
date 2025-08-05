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
    print(f">>> extract-folder-text aufgerufen mit folder_path={folder_path}")
    if not folder_path:
        return jsonify({'error': 'folder_path fehlt'}), 400

    try:
        entries = dbx.files_list_folder(folder_path).entries
        print(f">>> Dateien im Ordner '{folder_path}': {[e.name for e in entries]}")

        pdf_files = [e for e in entries if isinstance(e, dropbox.files.FileMetadata) and e.name.endswith('.pdf')]
        print(f">>> PDF-Dateien im Ordner: {[e.name for e in pdf_files]}")

        result_text = ""
        for entry in pdf_files:
            _, res = dbx.files_download(entry.path_lower)
            pdf_bytes = res.content
            # PDF-Inhalt extrahieren hier einbauen (z.B. pdfplumber)
            result_text += f"\n--- {entry.name} ---\n[PDF-Inhalt hier extrahieren]"

        return jsonify({'text': result_text})

    except Exception as e:
        print(f">>> Fehler beim Verarbeiten des Ordners '{folder_path}': {repr(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
