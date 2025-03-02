import bpy
import sys

# Get input arguments from command-line (from convert.py)
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # Get arguments after "--"

if len(argv) < 2:
    print("Error: Missing input and output file arguments")
    sys.exit(1)

input_file = argv[0]
output_file = argv[1]

try:
    # Clear existing scene
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # Import SKP
    bpy.ops.import_scene.skp(filepath=input_file)

    # Export GLB
    bpy.ops.export_scene.gltf(filepath=output_file, export_format='GLB')

    print(f"✅ Successfully converted {input_file} to {output_file}")

except Exception as e:
    print(f"❌ Blender conversion failed: {str(e)}")
    sys.exit(1)
