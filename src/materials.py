# Define functions to create materials. See create-scene.py for an example
# script calling such a function.

import bpy

def create_red():
    material = bpy.data.materials.new(name="material-red")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    nodes.clear()

    output_node = nodes.new(type="ShaderNodeOutputMaterial")
    diffuse_node = nodes.new(type="ShaderNodeBsdfDiffuse")
    diffuse_node.inputs["Color"].default_value = (1, 0, 0, 1)

    # Connect the nodes
    links.new(diffuse_node.outputs["BSDF"], output_node.inputs["Surface"])

    # Position the nodes in the Shader editor
    diffuse_node.location = (0, 0)
    output_node.location = (200, 0)

    return material
