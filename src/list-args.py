# This script is used to show how Blender invokes Python code from the
# command-line.

import bpy
import sys

if __name__ == "__main__":
  print(f"Arguments: {sys.argv}")
