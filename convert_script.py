import bpy
import sys
import traceback

def enable_addon():
    """Ensure the SketchUp Importer add-on is enabled."""
    addon_name = "sketchup_importer"  # Confirmed correct name
    if addon_name not in bpy.context.preferences.addons:
        print(f"⚠️ Enabling {addon_name} add-on...")
        bpy.ops.preferences.addon_enable(module=addon_name)
        bpy.ops.wm.save_userpref()

    if addon_name not in bpy.context.preferences.addons:
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
        # ✅ Ensure the add-on is enabled
        enable_addon()

        # ✅ Clear the scene before importing
        bpy.ops.wm.read_factory_settings(use_empty=True)
        # bpy.ops.import_scene.sketchup(filepath=input_file)
        bpy.ops.wm.obj_import(filepath=input_file)
        # ✅ Import SKP file
        # if hasattr(bpy.ops.import_scene, "skp"):
        #     bpy.ops.import_scene.skp(filepath=input_file)
        # elif hasattr(bpy.ops.import_scene, "sketchup"):
        #     bpy.ops.import_scene.sketchup(filepath=input_file)
        # else:
        #     raise Exception("❌ SketchUp import operator not found!")

        # ✅ Ensure the scene has objects (check import success)
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
