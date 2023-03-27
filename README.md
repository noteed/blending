# Scripting Blender from the command-line

This repository contains notes and exploratory scripts about using Python to
script Blender from the command-line.

I'm using Blender on NixOS, with the following shell:

```
$ nix-shell -p blender -I nixpkgs=channel:nixos-unstable
```

Blender has plenty of command line options:

```
$ blender --version
Blender 3.3.1
$ blender --help
...
```

# Rendering

Render frame 0:

```
$ blender --background --engine CYCLES --render-frame 0
```

The image is saved in `/tmp/`, e.g. as `/tmp/0000.png`. This renders the
default scene. Often you'll want to give a specific `.blend` as an argument.

# Python

It is possible to use Blender to run scripts (written in Python) from the
command-line, and without showing its graphical user interface.

```
$ blender --background --python-console
$ blender --background --python list-objects.py
```

`--python` can be given multiple times to chain scripts.

# empty.blend

Blender, even when called from the command-line to run a script as above, loads
a default scene before doing anything else. This means for instance that the
`list-objects.py` script will indeed show some content: the default scene
contains a cube mesh, a lamp, and a camera. This is also the scene being
rendered by the `--engine CYCLES --render-frame 0` line above.

It is possible to supply a specific `.blend` file as the initial scene to load,
and the script will run "on top" of it.

In some cases, such as scripts that generate a scene content, it's useful to
start with nothing. For that reason, this directory includes an `empty.blend`
file.

As an example, contrast the output of these two lines:

```
$ blender --background --python src/list-objects.py
$ blender empty.blend --background --python src/list-objects.py
```

# Command-line arguments

To have an idea of how scripts are called, here is `sys.argv`:

```
Blender 3.3.1
Read prefs: /home/thu/.config/blender/3.3/config/userpref.blend
/run/user/1000/gvfs/ non-existent directory
Arguments: ['/nix/store/d9y485naqfandxmwkf8603606wzjmmxm-blender-3.3.1/bin/blender', '--python-use-system-env', '--background', '--python', 'src/list-args.py', '--', 'dummy']

Blender quit
```

Note that a `--python-use-system-env` argument has been given. This is probably
caused by hhow Blender is packaged for NixOS. This is useful because it allows
us to set the `PYTHONPATH` environment variable to modularize our scripts and
load separate code as modules.

# Script organization

Scripts can setup a scene or modify an existing one (and save a `.blend` file
before exiting), and they can generate images. But as shown above, it is also
possible to render a scene without calling a script.

In practice I prefer to either generate an image and not save any `.blend`
file, or save a `.blend` file and leave the rendering a separate call to
Blender.

# Blender as a library

It is possible to build Blender to be a Python module and have the Python code
drive Blender instead of the other way around. I haven't tried yet.  See [this
page](https://wiki.blender.org/wiki/Building_Blender/Other/BlenderAsPyModule).

# Creating a simple scene

The script `src/create-scene.py` almost recreates the default Blender scene: a
cube, a lamp, and a camera.

The main difference is that a red material is defined and applied to the cube.

The lamp and the camera are positioned similarly to the original scene; opening
the file and hitting F12 should render the cube centered (and red).

The material is defined in a separate file, `src/materials.py`, so that it can
potentially be reused across multiple scripts. To allow `import`ing that module
in the script, we have to set the `PYTHONPATH` environement variable.

Note that allowing the usage of that environment variable seems to be done
through the `--python-use-system-env` option of Blender, which is done for use
automatically on NixOS.

See the comment in the script for how it can be run.

# Rendering 2D shaders

Inpired by this [Adam Morse
post](https://components.ai/files/pub/ntYEnMsFEpobrsSoSabY), I wanted to setup
a scene to generate images from shaders. The `.blend` file given with the post
uses a perspective camera pointed at a square plane, and a "sun" lamp is used
to uniformely light the scene.

This repository contains two alternative ways to generate images from a shader:
`src/render-checkerboard.py` and `src/bake-checkerboard.py`.

Those scripts are better run "on top" of an `empty.blend` scene: they will each
construct a scene containing a plane with an attached shader and convert it to
an image.

The first script, the `render-` one, uses a similar setup to Adam's with two
differences (in addition that it is done by a script, instead of manually): the
plane is not a square but is created to match the output aspect ratio, and the
camera is an orthographic one.

I don't know if this would actually affect the "quality" (this is subjective
anyway) of the output, but I want the ability to "zoom back" from the plane in
the case the shader is using e.g. bump maps or normal maps, or to showcase
reflections, and still see a (non-square) rectangle.

The second script, the `bake-` one, is not using a camera, nor a lamp. Instead
it bakes the shader to an image.

The resulting images are almost the same but not exactly. Although the
checkerboard patterns are placed in the same way, the "rendered" version has it
black square corners not exactly touching each others.

Note: implementing both of these scripts was a bit of a trial and error process
(I don't know much about Blender), in particular once I changed the initial
square to a plane matching the output aspect ratio: suddenly, the checkerboard
cells were no longer squares. Weirdly enough, this required to scale the plane
using two different ways.

Note: since we can give multiple `--python` arguments to Blender, in addition
of one of the above script, you can add `--python src/save-blend.py` on the
command line to save the constructed scene and have a look at it within
Blender (and even edit the shader).
