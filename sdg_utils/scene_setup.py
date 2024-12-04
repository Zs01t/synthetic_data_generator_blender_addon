import bpy
import os
import math

#TODO: Make this function modifiable; and make the other funtions "Plane" independent (data_generation, position objects randomizes the position based on the plane size)
def setup_scene():
    print("[Started: Setting up the scene]")
    bpy.context.scene.gravity = (0, 0, -2000)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.unit_settings.length_unit = 'MILLIMETERS'
    bpy.context.scene.unit_settings.scale_length = 0.001

    bpy.context.scene.eevee.shadow_cube_size = '4096'
    bpy.context.scene.eevee.shadow_cascade_size = '4096'
    bpy.context.scene.eevee.use_shadow_high_bitdepth = True
    bpy.context.scene.eevee.use_shadow_high_bitdepth = True
    # Delete default cube
    cube = bpy.data.objects.get("Cube")
    if cube:
        cube.select_set(True)
        bpy.ops.object.delete()
    else:
        print("Default cube not found.")
    
    # Add a plane
    plane = bpy.data.objects.get("Plane")
    if not plane:
        bpy.ops.mesh.primitive_plane_add(size=2, align='WORLD', location=(0, 0, 0))
        plane = bpy.data.objects.get("Plane")
        plane.scale = (400, 400, 400)
        # Create a new material
        plane_material = bpy.data.materials.new(name="PlaneMaterial")
        plane_material.use_nodes = True

        # Get the material's node tree
        nodes = plane_material.node_tree.nodes
        links = plane_material.node_tree.links

        # Clear default nodes
        for node in nodes:
            nodes.remove(node)

        # Add necessary nodes
        output_node = nodes.new(type="ShaderNodeOutputMaterial")
        output_node.location = (400, 0)

        principled_node = nodes.new(type="ShaderNodeBsdfPrincipled")
        principled_node.location = (0, 0)
        links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])

        texture_node = nodes.new(type="ShaderNodeTexImage")
        texture_node.location = (-400, 0)

        # Load and assign an image texture
        #TODO: Make This Dynamic
        current_dir_path = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_dir_path, "misc", "plane_texture.jpeg")
        image = bpy.data.images.load(image_path)
        texture_node.image = image
        # Connect the texture to the Principled BSDF
        links.new(texture_node.outputs['Color'], principled_node.inputs['Base Color'])
        # Assign the material to the plane
        plane.data.materials.append(plane_material)

    #Activate EEVEE effects for more photrealistic rendering
    bpy.context.scene.eevee.use_gtao = True #Ambient Occlusion aka shadow under the tools
    bpy.context.scene.eevee.taa_render_samples = 300 # increasing the sampling rate from 64 to 300 aka the shadows become smoother
    bpy.context.scene.eevee.use_ssr = True #Spacreen Space Reflection
    
    #set viewport distance (not needed but makes testing easier)
    bpy.context.space_data.clip_end = 2000

    # Set up the camera
    camera = bpy.data.objects.get("Camera")
    if camera:
        #camera.location = (730, 0, 450)
        camera.location = (0, -420, 320)
        # camera.location = (700, -700, 350)
        rotation_x = 50 * math.pi / 180
        rotation_y = 0 * math.pi / 180
        rotation_z = 0 * math.pi / 180
        camera.rotation_euler = (rotation_x, rotation_y, rotation_z)
        #camera.rotation_euler = (1.222, 0, 0.785)
        camera.data.clip_end = 2000.0
        print(f"Lens end set to {camera.data.clip_end}")
    else:
        print("Default camera not found.")

    # Set up the light
    light = bpy.data.objects.get("Light")
    if light:
        light.location = (0, 0, 150)
        light.rotation_euler = (0, 0, 0)
        light.data.energy = 3_000_000
        light.data.shadow_soft_size = 1
    else:
        print("Default light source not found.")

    setup_plane_physics()

    print("[Ended: Setting up the scene]\n")


def setup_plane_physics():
        plane = bpy.data.objects.get("Plane")
        if plane:
            bpy.context.view_layer.objects.active = plane
            bpy.ops.rigidbody.object_add()
            plane.rigid_body.type = 'PASSIVE'
            plane.rigid_body.restitution = 0.0  # No bounciness for the plane
        else:
            print("Plane not found. Please ensure the plane is named correctly.")