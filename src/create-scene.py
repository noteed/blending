# This script generate a .blend file containing a scene similar to the default
# scene. A red shader is assigned to a cube.
#
# Usage:
#   PYTHONPATH=./src blender empty.blend --background --python src/create-scene.py

import bpy
from math import radians
import sys

import materials

def add_camera(
        location=(7.3, -6.9, 4.9),
        rotation=(radians(63.6), radians(0.0), radians(46.7))):
    bpy.ops.object.camera_add(location=location, rotation=rotation)
    camera = bpy.context.active_object

    # Set the camera as the active camera for the scene
    bpy.context.scene.camera = camera

    return camera

def add_lamp(
        location=(4.0, 1.0, 6.0),
        rotation=(radians(37.0), radians(3.0), radians(107)),
        lamp_type='POINT'):
    bpy.ops.object.light_add(type=lamp_type, location=location, rotation=rotation)
    lamp = bpy.context.active_object

    lamp.data.energy = 1000

    return lamp

def add_cube(material=None):    
    # Create a new mesh cube object
    bpy.ops.mesh.primitive_cube_add(size=2)
    cube = bpy.context.active_object

    # Assign the material to the cube
    if material is not None:
        cube.data.materials.append(material)

    return cube

def save_blend(filepath):    
    bpy.ops.wm.save_as_mainfile(filepath=filepath)

if __name__ == "__main__":
    add_camera()
    add_lamp()

    material = materials.create_red()
    add_cube(material)

    save_blend("/tmp/output.blend")
