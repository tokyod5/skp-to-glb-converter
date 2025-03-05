import subprocess
import sys
import os
import logging

logging.basicConfig(level=logging.INFO)

BLENDER_PATH = r"C:\Program Files\Blender Foundation\Blender 4.3\blender.exe"
SCRIPT_PATH = os.path.abspath("convert_script.py")

def check_blender_addons():
    """Check if Blender has the required add-ons in background mode"""
    check_command = [
        BLENDER_PATH,
        "--background",
        "--python-expr",
        "import addon_utils; print(addon_utils.check('sketchup_importer'))"
    ]
    try:
        result = subprocess.run(check_command, capture_output=True, text=True, encoding='utf-8', errors='replace')
        if "True" in result.stdout:
            logging.info("✅ SketchUp Importer add-on is available.")
            return True
        else:
            logging.error("❌ SketchUp Importer add-on NOT available.")
            return False
    except Exception as e:
        logging.error(f"Error checking addons: {str(e)}")
        return False

def convert_skp_to_glb(input_path, output_path):
    """Convert SKP to GLB using Blender"""
    try:
        if not check_blender_addons():
            return False, "Addon missing in Blender."

        command = [
            BLENDER_PATH,
            "--background",
            "--python", SCRIPT_PATH,
            "--", input_path, output_path
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        # Log output for debugging
        logging.info(f"Blender stdout: {result.stdout}")
        if result.stderr:
            logging.error(f"Blender stderr: {result.stderr}")

        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, command, output=result.stdout, stderr=result.stderr)

        return True, output_path

    except subprocess.CalledProcessError as e:
        error_msg = f"Blender Error (Code {e.returncode}): {e.stderr}"
        logging.error(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"System Error: {str(e)}"
        logging.error(error_msg)
        return False, error_msg

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert.py <input_file> <output_file>")
        sys.exit(1)

    success, message = convert_skp_to_glb(sys.argv[1], sys.argv[2])
    sys.exit(0 if success else 1)