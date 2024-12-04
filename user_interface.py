import bpy
from bpy.types import Context, Panel, Operator, PropertyGroup

class SDG_Panel(bpy.types.Panel):
    bl_idname = 'VIEW_3D_SDG_Panel'
    bl_label = 'SDG Panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SDG'

    def draw(self, context: Context) -> None:
        layout = self.layout
        scene = context.scene

        # Csúszka a renderek számához
        layout.prop(scene.sdg_properties, "render_count", text="Number of Renders")

        # Gomb a generálás indításához
        layout.operator("sdg.generate_data", text="Generate Data")


class SDGGenerateDataOperator(bpy.types.Operator):
    """Gomb funkció helye: adatgenerálás"""
    bl_idname = "sdg.generate_data"
    bl_label = "Generate Data"

    def execute(self, context: Context):
        self.report({'INFO'}, "Generate Data button clicked!")
        return {'FINISHED'}


class SDGProperties(PropertyGroup):
    render_count: bpy.props.IntProperty(
        name="Render Count",
        description="Number of renders to generate",
        default=10,
        min=1,
        max=100
    )

# Regisztrációs függvények
def register():
    bpy.utils.register_class(SDG_Panel)
    bpy.utils.register_class(SDGGenerateDataOperator)
    bpy.utils.register_class(SDGProperties)
    bpy.types.Scene.sdg_properties = bpy.props.PointerProperty(type=SDGProperties)


def unregister():
    bpy.utils.unregister_class(SDG_Panel)
    bpy.utils.unregister_class(SDGGenerateDataOperator)
    bpy.utils.unregister_class(SDGProperties)
    del bpy.types.Scene.sdg_properties


if __name__ == "__main__":
    register()
