# This script is intended to be used after loading a scene to render it at a
# specific resolution.
# Parameters can be given after a `--` argument separator.
# They are `-w` and `-h`.

import bpy
import sys

def extract_args_after_dashdash(args):
    try:
        dashdash_index = args.index('--')
        return args[dashdash_index + 1:]
    except ValueError:
        return []

if __name__ == "__main__":
    args = extract_args_after_dashdash(sys.argv)
    if args:
        # Simulate parsing -w and -h for now. We'll probably
        # use argparse later.
        width = int(args[1])
        height = int(args[3])
    else:
        # Defaults:
        width = 1920
        height = 1080
    bpy.context.scene.render.resolution_x = width
    bpy.context.scene.render.resolution_y = height
    bpy.ops.render.render(write_still=True)
