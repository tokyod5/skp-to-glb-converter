import subprocess
import sys
import os

def convert_skp_to_glb(input_path, output_path):
    """
    Converts an SKP file to GLB using Blender.
    """

    # Ensure directories exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Construct Blender command
    blender_path = r"C:\Program Files\Blender Foundation\Blender 4.3\blender.exe"  # Update if needed
    script_path = os.path.abspath("convert_script.py")  # This will handle the conversion inside Blender
    
    command = [
        blender_path,
        "--background",
        "--python", script_path,
        "--", input_path, output_path  # Passing arguments to the Blender script
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Blender Output:", result.stdout)
        print("Blender Error:", result.stderr)

        if result.returncode == 0:
            return True, output_path
        else:
            return False, f"Blender failed: {result.stderr}"
    
    except subprocess.CalledProcessError as e:
        return False, f"Conversion error: {e.stderr}"

# If run directly from terminal
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert.py <input_file> <output_file>")
        sys.exit(1)
    
    input_file = os.path.abspath(sys.argv[1])
    output_file = os.path.abspath(sys.argv[2])

    success, message = convert_skp_to_glb(input_file, output_file)
    if success:
        print(f"Conversion successful: {output_file}")
    else:
        print(f"Error: {message}")
