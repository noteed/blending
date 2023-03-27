# This script lists shaders found in a give .blend file.

import bpy

def generate_shader_description(material):
    shader_description = []

    shader_description.append(f"Material: {material.name}\n")
    shader_description.append("Nodes:\n")

    for node in material.node_tree.nodes:
        shader_description.append(f"  - {node.name} ({node.bl_idname})\n")

    shader_description.append("Connections:\n")
    
    for link in material.node_tree.links:
        from_node = link.from_node
        from_socket = link.from_socket
        to_node = link.to_node
        to_socket = link.to_socket

        shader_description.append(f"  - {from_node.name}.{from_socket.name} -> {to_node.name}.{to_socket.name}\n")

    return ''.join(shader_description)

if __name__ == "__main__":
    for material in bpy.data.materials:
        if material.use_nodes:
            shader_description = generate_shader_description(material)
            print(shader_description)
