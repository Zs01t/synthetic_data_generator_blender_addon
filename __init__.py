import logging
import importlib

bl_info = {
    "name": "SDG (Synthetic Data Generator)",
    "description": "Automated image-mask pair generator",
    "author": "Zsolt Bekeffy",
    "blender": (3, 1, 2),
    "version": (1, 0, 0),
    "category": "Object",
    "location": "3D View > N panel > SDG",
    "warning": "Blender Annotation Tool is required"
}

# List of modules making up the addon
module_names = ("operators", "user_interface", "properties")
modules = []

for mod in module_names:
    try:
        modules.append(importlib.import_module('.' + mod, __name__))
    except Exception as e:
        logging.error(e)

def register() -> None:
    for mod in modules:
        try:
            mod.register()
        except Exception as e:
            logging.error(e)
    
def unregister() -> None:
    for mod in modules:
        try:
            mod.unregister()
        except Exception as e:
            logging.error(e)