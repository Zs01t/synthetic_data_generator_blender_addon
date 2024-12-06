import bpy
from .sdg_utils import scene_setup, object_import, data_generation
from bpy.types import Context
import os

class SDG_OT_setup_sdg_scene(bpy.types.Operator):
    bl_idname = 'sdg.setup_sdg_scene'
    bl_label = 'Setup SDG scene'
    bl_options = {'REGISTER'}
    
    

    def  execute(self, context: Context):
        plane_texture_file = context.scene.sdg_properties.plane_texture_file
        if not plane_texture_file:
            current_dir_path = os.path.dirname(os.path.realpath(__file__))
            plane_texture_path = os.path.join(current_dir_path, "sdg_utils", "misc", "plane_texture.jpeg")
            scene_setup.setup_scene(plane_texture_file=plane_texture_path)
        else:
            scene_setup.setup_scene(plane_texture_file=plane_texture_file)
        self.report({'INFO'}, "Setup scene button clicked!")
        return {'FINISHED'}


class SDG_OT_import_tools(bpy.types.Operator):
    bl_idname = 'sdg.import_tools'
    bl_label ='Import tools'
    bl_options = {'REGISTER'}

    def execute(self, context: Context):
       
        tools_dir = context.scene.sdg_properties.tools_directory
        if not tools_dir:
            #if no tools directory is specified we use the sample
            current_dir_path = os.path.dirname(os.path.realpath(__file__))
            tools_dir_path = os.path.join(current_dir_path, "sdg_utils", "misc", "tools_dir")
            object_import.import_tools(tools_dir=tools_dir_path, is_sample_tools_present=True)
        else:
            is_sample_tools_present = context.scene.sdg_properties.is_sample_models_present
            object_import.import_tools(tools_dir=tools_dir, is_sample_tools_present=is_sample_tools_present)
        self.report({'INFO'}, "Import tools button clicked!")
        return {'FINISHED'}
    


    
class SDG_OT_generate_data(bpy.types.Operator):
    bl_idname = 'sdg.generate_data'
    bl_label ='Generate data'
    bl_options = {'REGISTER'}
    
    def execute(self, context: Context):

        output_dir = context.scene.sdg_properties.output_directory
        generate_count = context.scene.sdg_properties.generate_count
        min_object_count = context.scene.sdg_properties.min_object_count
        max_object_count = context.scene.sdg_properties.min_object_count

        
        self.report({'INFO'}, "Generate data button clicked!")
        data_generation.generate_data(output=output_dir, generate_count=generate_count, min_object_count=min_object_count, max_object_count=max_object_count)
        return {'FINISHED'}



# class SDG_OT_browse_directory(bpy.types.Operator):
#     bl_idname = "sdg.browse_output_directory"
#     bl_label = "Browse Output Directory"

#     def execute(self, context):
#         # Open the file browser to choose a directory
#         context.window_manager.fileselect_add(self)
#         return {'RUNNING_MODAL'}

#     def invoke(self, context, event):
#         # Ensure the current directory is shown in the file browser (optional)
#         self.filepath = context.scene.sdg_properties.output_directory
#         return self.execute(context)

#     def execute(self, context):
#         # Save the selected directory path
#         context.scene.sdg_properties.output_directory = self.filepath
#         return {'FINISHED'}


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
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()