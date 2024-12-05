import bpy


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


    generate_count: bpy.props.IntProperty(
        name="generate_count",
        description="Number of images-mask pair to generate",
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