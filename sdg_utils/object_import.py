import bpy
import os
import re

def import_tools(tools_dir):
    print("[Started: Importing the tools]")

    tool_ref_collection_name = "Tools_reference"
    #This will contain collections of the tools. So for example Tools_reference will contain a collection nambed Combination Pliers
    #and inside this collection will be the Combination Pliers objects. These objects are the same classID wise, but they are open in different angles
    tool_ref_collection = get_or_create_collection(tool_ref_collection_name)
    
    if tool_ref_collection.name not in bpy.context.scene.collection.children.keys():
        bpy.context.scene.collection.children.link(tool_ref_collection)

    if not os.path.exists(tools_dir):
        print("Error: Hand tools directory does not exist.")
        return

    #This will give us all the tool folders (only the names and not the full path, which is ideal)
    #Inside the Tools_reference collection we will create subcollections that will contain the different states of the same object e.g. Combination Pliers with different angles of opening
    hand_tool_dirs = [dir for dir in os.listdir(tools_dir)]

    #We iterate through all the folders
    for dir in hand_tool_dirs:

        #we create a subcollection inside the Tools_reference collection
        sub_collection = get_or_create_collection(dir) #this function links the the sub collection to the main one, which is not ideal, we need to unlink it
        if sub_collection.name in  bpy.context.scene.collection.children:
            bpy.context.scene.collection.children.unlink(sub_collection)
        if sub_collection.name not in tool_ref_collection.children:
            #We link this sub collection to the Tools_reference collection
            tool_ref_collection.children.link(sub_collection)

        #We get the current folder's obj files
        hand_tool_files = [f for f in os.listdir(os.path.join(tools_dir, dir)) if f.endswith(".obj")]

        for obj_file in hand_tool_files:
            full_path = os.path.join(tools_dir, dir, obj_file)
            base_name = os.path.splitext(obj_file)[0] #we only want its name
            
            #we check if it is already imported
            if is_object_imported(base_name, sub_collection.name):
                print(f"Skipping '{base_name}': already imported.")
                continue

            #We simply import it into the scene
            bpy.ops.import_scene.obj(filepath=full_path)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

            #we change the materials' values because obj files are limited in storing these informations
            for slot in bpy.context.selected_objects[0].material_slots:
                material = slot.material
                if material and material.name.lower().split(".")[0] == "steel":
                    # Set the metallic property to 1
                    if material.node_tree:  # Ensure the material uses nodes
                        for node in material.node_tree.nodes:
                            if node.type == 'BSDF_PRINCIPLED':  # Find the Principled BSDF node
                                node.inputs['Metallic'].default_value = 1.0
                elif material and material.name.lower().split(".")[0] == "yellow_rubber" or material.name.lower().split(".")[0] == "black_rubber":

                    if material.node_tree:  
                        for node in material.node_tree.nodes:
                            if node.type == 'BSDF_PRINCIPLED':
                                #I'm lazy to do it manually...
                                if material.name.lower().split(".")[0] == "yellow_rubber":
                                    node.inputs['Base Color'].default_value = (1, 0.379, 0.008, 1)
                                elif material.name.lower().split(".")[0] == "black_rubber":
                                    node.inputs['Base Color'].default_value = (0.003, 0.003, 0.003, 1)

                                node.inputs['Specular'].default_value = 0.5
                                node.inputs['Roughness'].default_value = 0.6
                                node.inputs['Sheen'].default_value = 0.4
                                node.inputs['Sheen Tint'].default_value = 0.5
                                node.inputs['Clearcoat'].default_value = 0.3
                                # Create and connect Bump and Musgrave Texture nodes
                                nodes = material.node_tree.nodes
                                links = material.node_tree.links

                                # Create Musgrave Texture
                                musgrave_node = nodes.new(type='ShaderNodeTexMusgrave')
                                musgrave_node.location = (-400, 300)
                                musgrave_node.inputs['Scale'].default_value = 6

                                # Create Bump Node
                                bump_node = nodes.new(type='ShaderNodeBump')
                                bump_node.location = (-200, 300)
                                bump_node.inputs['Strength'].default_value = 0.1
                                # Connect Musgrave Texture to Bump Height input
                                links.new(musgrave_node.outputs['Fac'], bump_node.inputs['Height'])
                                # Connect Bump Node to Principled BSDF Normal input
                                links.new(bump_node.outputs['Normal'], node.inputs['Normal'])

            #in terms of blender context, it is currently inside the selected objects. We iterate over all the selected objects because it may contain multiple parts, but my models are one part only
            for obj in bpy.context.selected_objects:
                for col in obj.users_collection:
                    #we unlink these objects (wherever they are)
                    col.objects.unlink(obj)
                #the relink them into the sub collection
                sub_collection.objects.link(obj)
                obj.hide_render = True
                
                #then, for good measure we move it outside of the camera's view
                obj.location = (obj.location.x + 1000, obj.location.y, obj.location.z)

        #then, just to make it sure that everything is imported correctly, we list the the sub collection's items 
        # print(f"\nObjects inside of {sub_collection.name}:")
        # for obj in sub_collection.objects:
        #     print("-----", obj.name)


        #Now, here we create the collections where put the choosen duplicates from the Tools_reference collection
        for sub_coll in tool_ref_collection.children:
    
            #Adding the "duplicate_holder_" tag will help find these collections more easily
            formatted_collection_name = "duplicate_holder_" + sub_coll.name

            #We create separate collection for BAT as it only separates classID this way
            get_or_create_collection(formatted_collection_name) 
            
            #We link the created collection to the Scene collection 
            if formatted_collection_name not in bpy.context.scene.collection.children:
                # print(f"Linking '{formatted_collection_name}' collection to the scene collection.")
                bpy.context.scene.collection.children.link(get_or_create_collection(formatted_collection_name))
            
            #we create the BAT class
            bpy.ops.bat.add_class(new_class_name=sub_coll.name)
            #we set it to active to handle its properties
            bpy.context.scene.bat_properties.current_class = sub_coll.name
            #we assign the correct collection to this class
            bpy.context.scene.bat_properties.current_class_objects = formatted_collection_name
            
            #we set the necessary properties 
            bpy.context.scene.bat_properties.current_class_is_instances = True
            bpy.context.scene.bat_properties.depth_map_generation = True
            bpy.context.scene.bat_properties.surface_normal_generation = True
            bpy.context.scene.bat_properties.optical_flow_generation = True
    
    duplicate_holder_collections = [collection for collection in bpy.data.collections if collection.name.startswith("duplicate_holder_")]
    
    print("[Ended: Importing the tools]\n")

def get_or_create_collection(name):
        if name in bpy.data.collections:
            return bpy.data.collections[name]
        new_collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(new_collection)
        return new_collection

def is_object_imported(self, base_name, collection_name):

    # Function to strip Blender's numeric suffix (.001, .002)
    def strip_blender_suffix(name):
        match = re.match(r"(.*?)(\.\d+)?$", name)
        return match.group(1) if match else name

    # Get the collection
    collection = bpy.data.collections.get(collection_name)
    if not collection:
        return False

    # Check if any object's base name matches
    return any(strip_blender_suffix(obj.name) == base_name for obj in collection.objects)