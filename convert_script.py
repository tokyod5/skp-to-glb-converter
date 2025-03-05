import bpy
import sys
import traceback
import addon_utils

def enable_addon():
    """Ensure the SketchUp Importer add-on is enabled."""
    addon_name = "sketchup_importer"
    # Check if addon is enabled
    loaded_default, loaded_state = addon_utils.check(addon_name)
    if not loaded_state:
        print(f"⚠️ Enabling {addon_name} add-on...")
        addon_utils.enable(addon_name, default_set=True, persistent=True)
        bpy.ops.wm.save_userpref()  # Save preferences

    # Verify
    loaded_default, loaded_state = addon_utils.check(addon_name)
    if not loaded_state:
        raise Exception(f"❌ SketchUp Importer add-on could not be enabled.")

def main():
    """Handles the SKP to GLB conversion inside Blender"""
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]

    if len(argv) < 2:
        print("❌ Error: Missing input/output paths")
        sys.exit(1)

    input_file, output_file = argv[0], argv[1]
    try:
        # ✅ Clear the scene before importing
        bpy.ops.wm.read_factory_settings(use_empty=True)
        
        # ✅ Ensure the add-on is enabled after reset
        enable_addon()

        # ✅ Import SKP file using the correct operator
        if hasattr(bpy.ops.import_scene, "skp"):
            bpy.ops.import_scene.skp(filepath=input_file)
        elif hasattr(bpy.ops.import_scene, "sketchup"):
            bpy.ops.import_scene.sketchup(filepath=input_file)
        else:
            raise Exception("❌ SketchUp import operator not found!")

        # ✅ Check if import succeeded
        if not bpy.data.objects:
            raise Exception("❌ Imported scene is empty. Import failed.")

        # ✅ Export to GLB
        bpy.ops.export_scene.gltf(
            filepath=output_file,
            export_format='GLB',
            export_yup=True,
            export_apply=True
        )

        print(f"✅ Success: Converted {input_file} to {output_file}")

    except Exception as e:
        print(f"❌ Blender conversion failed: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()