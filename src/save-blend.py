# Demonstrate how to save the current scene.
# `save_as_mainfile()` requires an absolute path.

import bpy
import os

filepath = os.path.abspath("./save.blend")
bpy.ops.wm.save_as_mainfile(filepath=filepath)
