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
    logger.debug(f"Full args when running script_api: {argv}")
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
    logger.debug(f"Read from input file {input_file.as_posix()}")
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

    def modify(obj, setting, schema, draw_list):
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
                    # obj will have method `find`
                    # if the object does not exist, create a new one
                    if obj.find(key) is None:
                        obj.add(key)
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
                if key not in ["draw"]:
                    setattr(obj, key, val)
                    logger.debug(f"Setting property '{key}' of {type(obj)} to {val}")
                # Monkey patch add flag for drawing
                elif key == "draw":
                    setattr(obj, "_draw", val)
                    logger.debug(f"Add flag '_draw' of {type(obj)} and set to {val}")
                    draw_list.append(obj)
                    logger.debug(f"Add {type(obj)} to drawing candidates")
                else:
                    raise NotImplementedError
            else:
                # Walk down the object tree
                sub_setting = val.copy()
                modify(sub_obj, sub_setting, sub_schema.copy(), draw_list)
        return

    draw_list = []
    modify(batoms, settings, schema, draw_list)
    return draw_list


def apply_batoms_modifications(batoms, post_modifications=[]):
    """Use plain python expressions to modify batoms"""
    for mod in post_modifications:
        # TODO: sanity check of expression?
        exec(mod, blender_globals, {"batoms": batoms, "np": np})
        logger.debug(f"Applied modification '{mod}' to {batoms}")


def save_blender_file(input_file):
    """Save the main .blend file under the same directory"""
    input_file = Path(input_file)
    blend_file = input_file.with_suffix(".blend").resolve().as_posix()
    bpy.ops.wm.save_as_mainfile(filepath=blend_file)
    logger.debug(f"Save blender file to {blend_file}")
    return


def run():
    """post_modifications are like `ase run --modify` parameters that are direct python expressions (use at your own risk!)
    format of post_modifications looks like follows:
        - batoms.<property>.<sub_property><[indices/keys]> = something
    each post-modification line is directly evaluated in sequence.
    """
    input_file = _get_input_file()
    bpy.ops.batoms.delete()
    with open(input_file, "rb") as f:
        config = pickle.load(f)
    atoms = config["atoms"]
    volume = config.get("volume", None)
    batoms_input = config.get("batoms_input", {})
    render_input = config.get("render_input", {})
    settings = config.get("settings", {})
    post_modifications = config.get("post_modifications", [])
    api_version = config.get("api_version", __version__)
    save_bl = config.get("save_blender_file", False)
    # Only allow blender api_version >= input_api_version
    _check_version(api_version)

    batoms = Batoms(from_ase=atoms, volume=volume, **batoms_input)

    draw_list = apply_batoms_settings(batoms, settings)
    for obj in draw_list:
        if hasattr(obj, "_draw") and hasattr(obj, "draw"):
            if obj._draw is True:
                obj.draw()
    apply_batoms_modifications(batoms, post_modifications)

    batoms.draw()

    batoms.get_image(**render_input)
    if save_bl:
        save_blender_file(input_file)
    return


if __name__ == "__main__":
    run()
