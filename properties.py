import bpy


class SDG_Properties(bpy.types.PropertyGroup):
    
    generate_count: bpy.props.IntProperty(
        name="generate_count",
        description="Number of images-mask pair to generate",
        default=3,
        min=1,
        max=2000
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