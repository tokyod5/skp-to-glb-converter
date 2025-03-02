from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import subprocess

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with API

UPLOAD_FOLDER = "uploads"
CONVERTED_FOLDER = "converted"

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

@app.route("/convert", methods=["POST"])
def convert_file():
    """Handle file upload and conversion"""
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    input_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    output_filename = os.path.splitext(uploaded_file.filename)[0] + ".glb"
    output_path = os.path.join(CONVERTED_FOLDER, output_filename)

    uploaded_file.save(input_path)  # Save the uploaded file

    try:
        # Run conversion script
        subprocess.run(["python", "convert.py", input_path, output_path], check=True)

        # Get download URL
        download_url = f"/download/{output_filename}"
        return jsonify({"message": "Conversion successful!", "download_url": download_url})

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Conversion error: {str(e)}"}), 500


@app.route("/download/<filename>")
def download_file(filename):
    """Allow users to download converted files"""
    return send_from_directory(CONVERTED_FOLDER, filename, as_attachment=True)


# 🚀 Run with Railway PORT support
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Railway port or default 5000
    app.run(host="0.0.0.0", port=port)
