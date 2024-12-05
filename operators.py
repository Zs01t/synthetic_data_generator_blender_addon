import bpy
from .sdg_utils import scene_setup, object_import, data_generation
from bpy.types import Context
import os

class SDG_OT_setup_sdg_scene(bpy.types.Operator):
    bl_idname = 'sdg.setup_sdg_scene'
    bl_label = 'Setup SDG scene'
    bl_options = {'REGISTER'}

    def  execute(self, context: Context):
        scene_setup.setup_scene()
        self.report({'INFO'}, "Setup scene button clicked!")
        return {'FINISHED'}


class SDG_OT_import_tools(bpy.types.Operator):
    bl_idname = 'sdg.import_tools'
    bl_label ='Import tools'
    bl_options = {'REGISTER'}

    def execute(self, contect: Context):
        current_dir_path = os.path.dirname(os.path.realpath(__file__))
        tools_dir_path = os.path.join(current_dir_path, "sdg_utils", "misc", "tools_dir")
        object_import.import_tools(tools_dir=tools_dir_path)
        self.report({'INFO'}, "Import tools button clicked!")
        return {'FINISHED'}
    
class SDG_OT_generate_data(bpy.types.Operator):
    bl_idname = 'sdg.generate_data'
    bl_label ='Generate data'
    bl_options = {'REGISTER'}

    def execute(self, contect: Context):
        self.report({'INFO'}, "Generate data button clicked!")
        return {'FINISHED'}

# ==============================================================================
# SECTION: Register/Unregister
# ==============================================================================
# Description: Make defined classes available in Blender

classes = [
    SDG_OT_setup_sdg_scene, SDG_OT_import_tools, SDG_OT_generate_data
]

def register() -> None:
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister() -> None:
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()