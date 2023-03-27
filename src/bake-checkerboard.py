# Instead of using rendering through a camera (and lighting) as in
# render-checkerboard.py, this script is using baking to render the material to
# an image.

import bpy
import os

import materials

if __name__ == "__main__":
    output_filepath = "/tmp/baked.png"

    material = materials.create_checkerboard()

    # Create a new mesh (plane)
    # This code is different than in render-checkerboard.py and is the only one
    # I could came up with to render the checkerboard with square cells on a
    # rectangle plane. Wierdly enough, when open in the Blender UI, the plane
    # looks square;
    # Other attempts either deformed the checkerboard pattern, of turned the
    # upper part of the image black...
    bpy.ops.mesh.primitive_plane_add(size=1, scale=(1.920, 1.080, 1.0))
    plane = bpy.context.active_object

    # Set the material (shader) to the plane
    plane.data.materials.append(material)

    # Create a new image to bake the material to
    image = bpy.data.images.new("BakedTexture", width=1920, height=1080)
    image.filepath_raw = output_filepath
    image.file_format = "PNG"

    # Set up texture bake settings
    bpy.context.scene.render.engine = "CYCLES"
    bpy.context.scene.render.bake.use_selected_to_active = False
    bpy.context.scene.render.bake.use_cage = False
    bpy.context.scene.cycles.samples = 1

    # UV unwrap the plane
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.uv.unwrap(method="ANGLE_BASED", margin=0.001)
    bpy.ops.object.mode_set(mode="OBJECT")

    # Create a new image node in the material and assign the image to it
    image_node = material.node_tree.nodes.new("ShaderNodeTexImage")
    image_node.image = image
    image_node.location=(600,0)

    # Select the image node and make it the active node
    image_node.select = True
    material.node_tree.nodes.active = image_node

    # Select the plane and make it the active object
    plane.select_set(True)
    bpy.context.view_layer.objects.active = plane

    # Bake the material to the image and save it
    bpy.ops.object.bake(type="DIFFUSE", pass_filter={'COLOR'})
    image.save()
