import bpy
from bpy.types import Context, PropertyGroup

class SDG_PT_Panel(bpy.types.Panel):
    bl_idname = 'VIEW_3D_PT_SDG_Panel'
    bl_label = 'SDG Panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SDG'

    def draw(self, context: Context) -> None:
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.operator('sdg.setup_sdg_scene', text='Setup scene')


# class SDGProperties(PropertyGroup):
#     render_count: bpy.props.IntProperty(
#         name="Render Count",
#         description="Number of renders to generate",
#         default=10,
#         min=1,
#         max=100
#     )


# ==============================================================================
# SECTION: Register/Unregister
# ==============================================================================
# Description: Make defined classes available in Blender


classes = [SDG_PT_Panel,]
def register() -> None:
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister() -> None:
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
