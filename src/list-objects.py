# Show the object names of a .blend scene.

import bpy

print("Objects:")
for obj in bpy.context.scene.objects:
  print("  " + obj.data.name)
