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
