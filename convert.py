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
        "import bpy; print(bpy.context.preferences.addons.keys())"
    ]

    try:
        result = subprocess.run(check_command, capture_output=True, text=True, encoding='utf-8', errors='replace')
        if "sketchup_importer" in result.stdout:
            logging.info("✅ SketchUp Importer add-on is available in background mode.")
            return True
        else:
            logging.error("❌ SketchUp Importer add-on NOT available in background mode.")
            return False
    except Exception as e:
        logging.error(f"Error checking Blender add-ons: {str(e)}")
        return False

def convert_skp_to_glb(input_path, output_path):
    """Convert an SKP file to GLB using Blender with error handling."""
    try:
        # ✅ Check if the add-on is available in background mode
        if not check_blender_addons():
            return False, "SketchUp Importer Add-on is missing in Blender background mode."

        command = [
            BLENDER_PATH,
            "--background",
            "--python", SCRIPT_PATH,
            "--", input_path, output_path
        ]

        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        # Debug logs
        logging.info(f"✅ Blender stdout: {result.stdout}")
        if result.stderr:
            logging.error(f"❌ Blender stderr: {result.stderr}")

        return True, output_path

    except subprocess.CalledProcessError as e:
        error_msg = f"❌ Blender Error (Code {e.returncode}): {e.stderr}"
        logging.error(error_msg)
        return False, error_msg
        
    except Exception as e:
        error_msg = f"❌ Conversion System Error: {str(e)}"
        logging.error(error_msg)
        return False, error_msg

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    success, message = convert_skp_to_glb(input_file, output_file)
    sys.exit(0 if success else 1)
