from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import subprocess

app = Flask(__name__)
CORS(app)  # Allow front-end to connect

UPLOAD_FOLDER = "uploads"
CONVERTED_FOLDER = "converted"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

@app.route("/convert", methods=["POST"])
def convert():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    # Save uploaded file
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(CONVERTED_FOLDER, file.filename.replace(".skp", ".glb"))

    file.save(input_path)

    # Run conversion
    try:
        result = subprocess.run(["python", "convert.py", input_path, output_path], check=True, capture_output=True, text=True)
        print(result.stdout)  # Debugging output
        print(result.stderr)

        return jsonify({"message": "Conversion successful!", "download_url": f"/download/{file.filename.replace('.skp', '.glb')}"}), 200
    
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Conversion failed: {e.stderr}"}), 500

@app.route("/download/<filename>")
def download(filename):
    filepath = os.path.join(CONVERTED_FOLDER, filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404

@app.route('/')
def home():
    return "Flask API is running on Railway!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)