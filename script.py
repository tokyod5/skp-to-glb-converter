import bpy
import os

# Enable SketchUp Importer add-on if disabled
addon_name = "sketchup_importer"
if addon_name not in bpy.context.preferences.addons:
    bpy.ops.preferences.addon_enable(module=addon_name)

# Define folders
input_dir = "C:/Users/MARWAN/Downloads/SKP"  # Change this to your SKP folder
output_dir = "C:/Users/MARWAN/Downloads/GLTF"  # Change this to where you want GLB files

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through all SKP files
for filename in os.listdir(input_dir):
    if filename.endswith(".skp"):
        skp_path = os.path.join(input_dir, filename)
        glb_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".glb")

        # Import the SKP file
        bpy.ops.import_scene.skp(filepath=skp_path)

        # Export to GLB (single binary file, no extra files)
        bpy.ops.export_scene.gltf(filepath=glb_path, export_format="GLB")

        # Remove all objects from the scene to reset
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

# Save preferences so the add-on stays enabled
bpy.ops.wm.save_userpref()

print("✅ All SKP files converted to GLB successfully!")
