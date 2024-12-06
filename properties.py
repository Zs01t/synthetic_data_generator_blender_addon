import bpy
import os

class SDG_Properties(bpy.types.PropertyGroup):
    
    def update_max_object_count(self, context):

        if self.max_object_count < self.min_object_count:
            self.max_object_count = self.min_object_count

        tools_collection = bpy.data.collections.get("Tools_reference")  
        if tools_collection:
            collection_count = len(tools_collection.children)
            self.max_object_count = min(self.max_object_count, collection_count)
        else:
            self.max_object_count = 0

    def update_min_object_count(self, context):

        if self.min_object_count > self.max_object_count:
            self.min_object_count = self.max_object_count
        
        tools_collection = bpy.data.collections.get("Tools_reference") 
        if tools_collection:
            collection_count = len(tools_collection.children)
            self.max_object_count = min(self.max_object_count, collection_count)
        else:
            self.max_object_count = 0

    def browse_directory(self, context):
        context.window_manager.fileselect_add(self)

    def validate_directory(self, context):
        if not os.path.isdir(self.output_directory):
            self.report({'ERROR'}, "Invalid directory path. Please choose a valid folder.")
            return False
        return True

    generate_count: bpy.props.IntProperty(
        name="generate_count",
        description="Number of image-mask pair to generate",
        default=3,
        min=1,
        max=2000
    )
    min_object_count: bpy.props.IntProperty(
        name ="min_object_count",
        description="Minimum number of objects on the render",
        default=0,
        min=0,
        max=2000,
        update=update_min_object_count
    )
    max_object_count: bpy.props.IntProperty(
        name ="max_object_count",
        description="Maximum number of objects on the render",
        default=1,
        min=1,
        max=2000,
        update=update_max_object_count
    )
    output_directory: bpy.props.StringProperty(
        name="output_dir",
        description="The output where the image-mask pair will be saved",
        default="",
        subtype='DIR_PATH'
    )
    tools_directory: bpy.props.StringProperty(
        name="tools_dir",
        description="The folder which contains the models for automatic data generation",
        default="",
        subtype='DIR_PATH'
    )
    is_sample_models_present: bpy.props.BoolProperty(
        name="is_sample_models_present",
        description="If True, the it will generate texure nodes for the sample model set",
        default=False
    )

    plane_texture_file: bpy.props.StringProperty(
        name = "plane_texture_file",
        description="The Plane's texture on which the object will be",
        subtype= 'FILE_PATH',   
    )

    


# ==============================================================================
# SECTION: Register/Unregister
# ==============================================================================
# Description: Make defined classes available in Blender

classes = [SDG_Properties,]

def register() -> None:
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.sdg_properties = bpy.props.PointerProperty(type=SDG_Properties)

def unregister() -> None:
    del bpy.types.Scene.sdg_properties
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()