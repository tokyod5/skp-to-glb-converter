from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import subprocess
import traceback

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
CONVERTED_FOLDER = "converted"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

@app.route("/convert", methods=["POST"])
def convert_file():
    """Handle file upload and conversion"""
    try:
        if "file" not in request.files:
            return jsonify({"success": False, "error": "No file provided"}), 400

        uploaded_file = request.files["file"]
        if uploaded_file.filename == "":
            return jsonify({"success": False, "error": "No selected file"}), 400

        # Validate file extension
        if not uploaded_file.filename.lower().endswith('.skp'):
            return jsonify({"success": False, "error": "Only .skp files are allowed"}), 400

        # Prepare paths
        input_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        output_filename = os.path.splitext(uploaded_file.filename)[0] + ".glb"
        output_path = os.path.join(CONVERTED_FOLDER, output_filename)

        # Cleanup previous files
        for path in [input_path, output_path]:
            if os.path.exists(path):
                os.remove(path)

        uploaded_file.save(input_path)

        # Run conversion
        result = subprocess.run(
            ["python", "convert.py", input_path, output_path],
            check=True,
            capture_output=True,
            text=True
        )

        # Verify output file was created
        if not os.path.exists(output_path):
            return jsonify({"success": False, "error": "Conversion failed - no output file"}), 500

        return jsonify({
            "success": True,
            "download_url": f"/download/{output_filename}"
        })

    except subprocess.CalledProcessError as e:
        error_msg = f"Conversion failed: {e.stderr}"
        print(f"ERROR: {error_msg}")
        return jsonify({"success": False, "error": error_msg}), 500
        
    except Exception as e:
        error_msg = f"Server error: {str(e)}"
        print(f"CRITICAL ERROR: {traceback.format_exc()}")
        return jsonify({"success": False, "error": error_msg}), 500

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(CONVERTED_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)