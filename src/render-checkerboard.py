# This generates a material, assign it to a plane and render it using an
# orthographic camera. This doens't remove the default camera or cube.
#
# Usage:
#   PYTHONPATH=./src blender empty.blend --background --python src/render-checkerboard.py
#
# (Modifying the PYTHONPATH is necessary to load materials.py.)

import bpy
from math import radians
import os

import materials

def add_lamp(
        location=(4.0, 1.0, 6.0),
        rotation=(radians(37.0), radians(3.0), radians(107)),
        lamp_type='SUN'):
    bpy.ops.object.light_add(type=lamp_type, location=location, rotation=rotation)
    lamp = bpy.context.active_object

    lamp.data.energy = 1000

    return lamp

if __name__ == "__main__":
    output_filepath = "/tmp/rendered.png"

    add_lamp()
    material = materials.create_checkerboard()

    # Create a new mesh (plane)
    bpy.ops.mesh.primitive_plane_add(size=1)
    plane = bpy.context.active_object
    plane.scale.x = 1.920
    plane.scale.y = 1.080
    # Apply the scale
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Set the material (shader) to the plane
    plane.data.materials.append(material)

    # Create an orthographic camera
    bpy.ops.object.camera_add(location=(0, 0, 2))
    camera = bpy.context.active_object
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = 1.920
    bpy.context.scene.camera = camera

    # Configure render settings
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.resolution_percentage = 100
    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.render.filepath = output_filepath

    # Render the image
    bpy.ops.render.render(write_still=True)
