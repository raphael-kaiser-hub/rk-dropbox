from flask import Flask, request, jsonify
from dropbox_access import get_pdf_text

app = Flask(__name__)

@app.route("/pdf-text", methods=["GET"])
def pdf_text():
    path = request.args.get("path")
    if not path:
        return jsonify({"error": "Pfad zur Datei fehlt."}), 400

    try:
        text = get_pdf_text(path)
        return jsonify({"text": text, "path": path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500