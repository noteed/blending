# Define functions to create materials. See create-scene.py for an example
# script calling such a function.

import bpy

def create_checkerboard():
    material = bpy.data.materials.new("material-checkerboard")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links

    nodes.clear()

    # Note: both rendering and baking works with "object" or "uv" coordinates
    # (linked to checkerboard's vector), but "uv" gives exatly the same
    # results.
    # The mapping node inserted between the coordinates and the checker is
    # only needed for baking.
    output_node = nodes.new("ShaderNodeOutputMaterial")
    diffuse_node = nodes.new("ShaderNodeBsdfDiffuse")
    checker_node = nodes.new("ShaderNodeTexChecker")
    mapping_node = nodes.new(type="ShaderNodeMapping")
    mapping_node.inputs["Scale"].default_value = (1.920, 1.080, 1)
    coord_node = nodes.new(type="ShaderNodeTexCoord")

    # Set the checker colors and scale
    checker_node.inputs["Color1"].default_value = (1, 1, 1, 1)
    checker_node.inputs["Color2"].default_value = (0, 0, 0, 1)
    checker_node.inputs["Scale"].default_value = 10

    # Connect the nodes
    links.new(coord_node.outputs["UV"], mapping_node.inputs["Vector"])
    links.new(mapping_node.outputs["Vector"], checker_node.inputs["Vector"])
    links.new(checker_node.outputs["Color"], diffuse_node.inputs["Color"])
    links.new(diffuse_node.outputs["BSDF"], output_node.inputs["Surface"])

    # Position the nodes in the Shader editor
    coord_node.location = (-400,0)
    mapping_node.location = (-200,0)
    checker_node.location = (0, 0)
    diffuse_node.location = (200, 0)
    output_node.location = (400, 0)

    return material

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
