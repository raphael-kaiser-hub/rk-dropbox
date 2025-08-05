from flask import Flask, request, jsonify
import dropbox
import pdfplumber
import io
import os

# Initialisiere Flask-App
app = Flask(__name__)

# Zugriff auf Umgebungsvariable für den Dropbox-Token
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

# Route: Extrahiere Text aus allen PDFs im angegebenen Dropbox-Ordner
@app.route('/extract-folder-text', methods=['GET'])
def extract_folder_text():
    folder_path = request.args.get('folder_path')
    if not folder_path:
        return jsonify({'error': 'folder_path parameter is required'}), 400

    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    text_output = ""

    try:
        # Liste aller Dateien im angegebenen Ordner abrufen
        res = dbx.files_list_folder(folder_path)
        for entry in res.entries:
            if isinstance(entry, dropbox.files.FileMetadata) and entry.name.lower().endswith('.pdf'):
                # PDF-Datei herunterladen
                metadata, response = dbx.files_download(entry.path_lower)
                with pdfplumber.open(io.BytesIO(response.content)) as pdf:
                    for page in pdf.pages:
                        text_output += page.extract_text() or ''
                    text_output += "\n--- PDF Ende: " + entry.name + " ---\n"
    except dropbox.exceptions.ApiError as e:
        return jsonify({'error': f'Dropbox API error: {e}'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {e}'}), 500

    return jsonify({'text': text_output})

# Startpunkt (für lokale Tests – Render ignoriert das)
if __name__ == '__main__':
    app.run(debug=True)
