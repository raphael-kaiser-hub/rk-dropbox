@app.route('/extract-folder-text', methods=['GET'])
def extract_folder_text():
    folder_path = request.args.get('folder_path')
    result_texts = []

    try:
        files = dbx.files_list_folder(folder_path).entries
        pdf_files = [f for f in files if isinstance(f, dropbox.files.FileMetadata) and f.name.endswith('.pdf')]

        for file in pdf_files:
            metadata, res = dbx.files_download(file.path_lower)
            with BytesIO(res.content) as f:
                pdf = PdfReader(f)
                text = '\n'.join([page.extract_text() for page in pdf.pages if page.extract_text()])
                result_texts.append(f"--- {file.name} ---\n{text}")

        return jsonify({"text": "\n\n".join(result_texts)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
