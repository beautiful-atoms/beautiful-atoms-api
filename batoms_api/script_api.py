"""
Usage:
```
from batoms_api import script_api
script_api.run()
```
Function `run()` will get the path of input file (`.batoms.inp`) from `sys.argv`
"""
try:
    from batoms import Batoms
except ImportError as e:
    raise ImportError(
        ("batoms_api.script_api must be run within the blender environment!")
    ) from e
try:
    import bpy
except ImportError as e:
    raise ImportError(
        ("batoms_api.script_api must be run within the blender environment!")
    ) from e
import os
import sys
import pickle
from packaging.version import Version
from warnings import warn
from multiprocessing.sharedctypes import Value
import numpy as np
from pathlib import Path
from copy import copy

from .metadata import __version__
from .batoms_api import default_schema

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

blender_globals = globals().copy()


def _handle_argv_extras():
    """Special to blender usage. Parse the extra argv after '--' symbols
    If no extra options provided, return None
    """
    argv = copy(sys.argv)
    if "--" not in argv:
        return None
    else:
        ind = argv.index("--")
        if ind == len(argv) - 1:
            raise ValueError("No arguments provided after the '--' symbols!")
        elif len(argv) - ind > 2:
            raise ValueError("batoms_api.script_api only accepts 1 positional argument")
        else:
            return argv[ind + 1]


def _get_input_file():
    """Get the input file as PosixPath from argv.
    If no defined, use environment variable $BATOMS_INPUT_FILE
    """
    argv_extras = _handle_argv_extras()
    if argv_extras:
        input_file = Path(argv_extras).resolve()
    elif "BATOMS_INPUT_FILE" in os.environ.keys():
        input_file = Path(os.environ["BATOMS_INPUT_FILE"])
    else:
        raise ValueError("Cannot find input file!")
    return input_file


def _check_version(input_api_version):
    if Version(input_api_version) > Version(__version__):
        raise ValueError(
            f"Input file api version {input_api_version} is newer than current api version {__version__}!"
        )
    elif Version(input_api_version) < Version(__version__):
        warn(
            f"Input file api version {input_api_version} is older than current api version {__version__}. There might be some incompatibilities."
        )
    else:
        pass


def apply_batoms_settings(batoms, settings={}, schema=default_schema["settings"]):
    """Apply settings to batoms instances"""

    def modify(obj, setting, schema):
        """Follow the same algorithm as batoms_api.set_dict"""
        for key, val in setting.items():
            # breakpoint()
            if key not in schema.keys():
                if "_any" not in schema.keys():
                    warn(f"Key {key} not in schema, skip")
                    continue
                else:
                    # This subschema accepts any key value
                    sub_schema = schema["_any"]
                    sub_obj = obj[key]
            else:
                sub_schema = schema[key]
                sub_obj = getattr(obj, key)

            # breakpoint()
            # Determine if we have eached the leaf node
            if "_disabled" in sub_schema.keys():
                warn(f"Key {key} is disabled in current scope, ignore.")
            elif "_type" in sub_schema.keys():
                # Reached a leaf node
                setattr(obj, key, val)
            else:
                # Walk down the object tree
                sub_setting = val.copy()
                modify(sub_obj, sub_setting, sub_schema.copy())
        return

    modify(batoms, settings, schema)
    return


def apply_batoms_modifications(batoms, post_modifications=[]):
    """Use plain python expressions to modify batoms"""
    for mod in post_modifications:
        # TODO: sanity check of expression?
        exec(mod, blender_globals, {"batoms": batoms, "np": np})


def run():
    """post_modifications are like `ase run --modify` parameters that are direct python expressions (use at your own risk!)
    format of post_modifications looks like follows:
        - batoms.<property>.<sub_property><[indices/keys]> = something
    each post-modification line is directly evaluated in sequence.
    """
    input_file = _get_input_file()

    with open(input_file, "rb") as f:
        config = pickle.load(f)
    atoms = config["atoms"]
    volume = config.get("volume", None)
    batoms_input = config.get("batoms_input", {})
    render_input = config.get("render_input", {})
    settings = config.get("settings", {})
    post_modifications = config.get("post_modifications", [])
    api_version = config.get("api_version", __version__)
    # Only allow blender api_version >= input_api_version
    _check_version(api_version)

    batoms = Batoms(from_ase=atoms, volume=volume, **batoms_input)

    apply_batoms_settings(batoms, settings)
    apply_batoms_modifications(batoms, post_modifications)

    # Do extras update
    batoms.species.update()
    batoms.polyhedras.update()
    batoms.draw()

    batoms.get_image(**render_input)
    # TODO: add option to save .blend file
    bpy.ops.wm.save_as_mainfile(
        filepath=input_file.with_suffix(".blend").resolve().as_posix()
    )
    return


# def main():
#     # run()
#     print(sys.argv)
#     extra_arg = _handle_argv_extras()
#     print(extra_arg)


if __name__ == "__main__":
    run()


##################
# Old functions
# Handle the setting parts, may be a little tricky
# There are two types of parameters:
# 1. batoms itself, direct intialization
# 2. initializable objects: render, boundary. invoke as batoms.<obj> = ObjClass(param=param)
# 3. requiring special treatment: species. Has "update" section
# 4. objects need setting: polyhedras, bonds, lattice_plane, crystal_shape, isosurfaces, cavity, ms, magres etc
#    an ObjectSetting instance needs to be updated. Usage batoms.<obj>.setting[key] = setting_dict
# YAML parser need to distinguish between the levels that are used
# TODO: add global lighting / plane setting
# TODO: add file io settings
# for prop_name, prop_setting in settings.items():
#     # TODO prototype API check
#     print(prop_name, prop_setting)
#     if prop_name == "batoms":
#         prop_obj = batoms
#         # do not change label after creation
#         prop_setting.pop("label", None)
#         for key, value in prop_setting.items():
#             print(key, value, type(value))
#             setattr(prop_obj, key, value)
#         print(prop_obj)
#         # setattr(prop_obj, key, type_convert({}, value))
#     elif prop_name in ["render", "boundary"]:
#         prop_obj = getattr(batoms, prop_name)
#         for key, value in prop_setting.items():
#             setattr(prop_obj, key, value)
#     else:
#         # TODO: check if prop_name is valid
#         prop_obj = getattr(batoms, prop_name)
#         draw_params = {}
#         for sub_prop_name, sub_prop_setting in prop_setting.items():
#             if sub_prop_name == "setting":
#                 sub_prop_obj = prop_obj.setting
#                 # sub_prop_setting is by default a dict
#                 for key, value in sub_prop_setting.items():
#                     sub_prop_obj[key] = value
#             elif sub_prop_name == "draw":
#                 if sub_prop_setting is not False:
#                     draw_params = sub_prop_setting
#                 else:
#                     draw_params = False
#             else:
#                 raise ValueError(f"Unknown sub_prop_setting {sub_prop_setting}")
#         if draw_params is not False:
#             if hasattr(prop_obj, "draw"):
#                 prop_obj.draw(**draw_params)
#             else:
#                 batoms.draw()
#         print(prop_obj)

# for prop_name, setting in settings.items():
#     # TODO: catch AttributeError
#     prop_obj = getattr(batoms, prop_name)
#     for key, value in setting.items():
#         val_string = f"_obj.{key}"
#         handle = eval(val_string, {}, {"_obj": prop_obj})
#         handle = value
# post_modifications = preferences.get("post_modifications", [])

# render_input = preferences.get("render_input", {})
# Force run self
##################
