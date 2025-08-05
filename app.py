from flask import Flask, request, jsonify
import dropbox
import os

app = Flask(__name__)

# Dropbox-Token aus Umgebungsvariable (Render -> Environment)
print(">>> DEBUG: DROPBOX_ACCESS_TOKEN =", DROPBOX_ACCESS_TOKEN)
DROPBOX_ACCESS_TOKEN = os.environ.get('DROPBOX_ACCESS_TOKEN')
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
   

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
                # Extraktion z. B. mit pdfplumber oder placeholder
                result_text += f"\n--- {entry.name} ---\n[PDF-Inhalt hier extrahieren]"
        return jsonify({'text': result_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
     
