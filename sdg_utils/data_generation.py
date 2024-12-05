import bpy
import os
import random
import math
import glob
from . import my_common


#render related
num_renders = 0
min_num_objects = 0
max_num_objects = 0
output_dir = ""

#object positioning related
plane_size = 250
min_distance = 50
drop_height = 200

#physics related
final_frame = 50


def generate_data(output, generate_count, min_object_count, max_object_count):
    #TODO: maybe make it into a class...
    global output_dir
    output_dir = output

    global min_num_objects
    min_num_objects = min_object_count

    global max_num_objects
    max_num_objects = max_object_count

    print(output)
    print("[Started: Data generation]")
    #this is needed so I don't have to call the import_tools function everytime when i restart the script
    if not my_common.get_duplicate_holder_collections():
        my_common.get_duplicate_holder_collections([collection for collection in bpy.data.collections if collection.name.startswith("duplicate_holder_")]) 
    

    if not os.path.exists(os.path.join(output_dir, "renders")):
        os.makedirs(os.path.join(output_dir, "renders"))
        os.makedirs(os.path.join(output_dir, "annotations"))

    current_iteration = len([f for f in os.listdir(os.path.join(output_dir, "renders")) if f.startswith("render_") and f.endswith(".png")])

    for i in range(current_iteration, generate_count):
        selected_objects = select_random_objects()
        duplicated_objects = duplicate_objects(selected_objects)

        position_objects(duplicated_objects)
        setup_physics()
        simulate_physics()
        bake_to_keyframes()
        render_scene(i)
        create_annotation(i)
        remove_duplicates_from_scene(duplicated_objects)
        unbake_keyframes()
        
    print("[Ended: Data generation]")

def select_random_objects():
    tool_ref_collection = bpy.data.collections.get("Tools_reference")
    
    # Get the number of collections in the Tools_reference collection
    num_collections = len(bpy.data.collections.get("Tools_reference").children)

    # Set num_to_select to be between min_num_objects and the smaller of max_num_objects or the number of collections
    num_to_select = random.randint(min_num_objects, min(max_num_objects, num_collections))
    print(f"Number of objects selected: {num_to_select}")
    #this return the name of the sub collection, duplicates are allowed
    selected_sub_collections = random.choices(tool_ref_collection.children, k=num_to_select)

    # Now, from the selected subcollections, select a random object from each
    selected_objects = []
    for sub_collection in selected_sub_collections:
        if sub_collection.objects:
            selected_object = random.choice(list(sub_collection.objects))
            selected_objects.append(selected_object)
    return selected_objects

def duplicate_objects(
    objects):
    duplicates = []
    for obj in objects:
        duplicate = obj.copy()
        duplicate.data = obj.data.copy()
        duplicate.animation_data_clear()
        #print(f"Duplicate created: {duplicate.name}")

        #We check in which subcollection the current obj is in, and we use that collection name
        correct_collection = bpy.data.collections.get("duplicate_holder_" + obj.users_collection[0].name)
        #print(f"this object is in the {obj.users_collection[0].name} collection")
        #print(f"Correct colletion's name: {correct_collection}")
        if correct_collection:
            correct_collection.objects.link(duplicate)
            #print(f"Duplicate {duplicate.name} linked to collection {correct_collection.name}")
            duplicates.append(duplicate)
            #maybe calling this every iteration is bad for performance
            set_render_visibility(correct_collection, True)

        else:
            print(f"No collection found for object '{obj.name}'. Expected collection: 'duplicate_holder_{obj.name.split('.')[0]}'")
    
    #refreshing this value just in case...
    my_common.set_duplicate_holder_collections([collection for collection in bpy.data.collections if collection.name.startswith("duplicate_holder_")])
    return duplicates

def set_render_visibility(collection, visible):
    for obj in collection.objects:
        obj.hide_render = not visible
        obj.hide_viewport = not visible

def position_objects(objects):
    radius = 300
    placed_positions = []
    for obj in objects:
        while True:
            x, y = random.uniform(-plane_size+radius, plane_size-radius), random.uniform(-plane_size+radius, plane_size-radius)
            if all(math.sqrt((x - px) ** 2 + (y - py) ** 2) > min_distance for px, py in placed_positions):
                break
        placed_positions.append((x, y))
        obj.location = (x, y, drop_height)
        obj.rotation_euler = (0, 0, random.uniform(0, 2 * math.pi))

def setup_physics():
    #we set the physics for each object in each import_ collection
    for collection in my_common.get_duplicate_holder_collections():
        
        for obj in collection.objects:
            obj.location.z = drop_height  # Raise above the plane
            obj.rotation_euler = (random.uniform(0, math.pi), 0, random.uniform(0, math.pi))  # Random rotation
            bpy.context.view_layer.objects.active = obj
            bpy.ops.rigidbody.object_add()
            obj.rigid_body.type = 'ACTIVE'
            obj.rigid_body.restitution = 0.0  # No bounciness
            obj.rigid_body.collision_shape = 'CONVEX_HULL'  # Or 'MESH' for complex shapes

def simulate_physics():
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = final_frame
    for frame in range(1, final_frame + 1):
        bpy.context.scene.frame_set(frame)

def bake_to_keyframes():
    #TODO: check if this two lines are needed
    # Set the scene's start and end frames for baking
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = final_frame # Adjust as needed

    # Select all textured objects and bake their physics to keyframes
    
    for collection in my_common.get_duplicate_holder_collections():
        for obj in collection.objects:
            
            bpy.context.view_layer.objects.active = obj
            
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            
            # Bake physics to keyframes
            bpy.ops.rigidbody.bake_to_keyframes(frame_start=final_frame-1, frame_end=final_frame)

def render_scene(render_idx):
    bpy.context.scene.render.filepath = os.path.join(output_dir, "renders", f"render_{render_idx}.png")
    bpy.ops.render.render(write_still=True)
    #print(f"Render saved: render_{render_idx}.png")

def create_annotation(annot_idx):
    bpy.context.scene.render.filepath = os.path.join(output_dir, "")
    bpy.ops.render.bat_render_annotation() #this creates an annotations folder inside the output_dir

    # Rename annotation file based on iteration
    annotation_dir = os.path.join(bpy.context.scene.render.filepath, "annotations")
    new_annotation_path = os.path.join(annotation_dir, f"mask_exr_{annot_idx}.exr")
    annotation_files = glob.glob(os.path.join(annotation_dir, "[0-9][0-9][0-9][0-9].exr"))

    if annotation_files:
        annotation_path = annotation_files[0]
        if os.path.exists(new_annotation_path):
            os.remove(new_annotation_path)
        os.rename(annotation_path, new_annotation_path)
        print(f"Exr saved: exr_mask_{annot_idx}.exr")
    else:
        print("No 4-digit .exr file found for renaming.")

def remove_duplicates_from_scene(duplicated_objects):
    for obj in duplicated_objects:
        if obj.name in bpy.data.objects:
            #print(f"Removed duplicate: {obj.name}")
            bpy.data.objects.remove(obj)
        else:
            print(f"Object {obj.name} not found in bpy.data.objects")

def unbake_keyframes():
# Loop through textured objects and clear any baked keyframes
    for collection in my_common.get_duplicate_holder_collections():
        for obj in collection.objects:
            obj.animation_data_clear()  # Removes all keyframes and resets the object