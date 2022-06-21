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
from distutils.version import StrictVersion
from logging import warning
from multiprocessing.sharedctypes import Value
import numpy as np
import pickle
import sys
from pathlib import Path
import os


from .metadata import __version__
from copy import copy

blender_globals = globals().copy()


def _handle_argv_extras():
    """Special to blender usage. Parse the extra argv after '--' symbols
    If no extra options provided, return None
    """
    argv = copy(sys.argv)
    print(argv)
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
    if StrictVersion(input_api_version) > StrictVersion(__version__):
        raise ValueError(
            f"Input file api version {input_api_version} does newer than current api version {__version__}!"
        )
    elif StrictVersion(input_api_version) > StrictVersion(__version__):
        warning(
            f"Input file api version {input_api_version} does older than current api version {__version__}. There might be some incompatibilities."
        )
    else:
        pass


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
    settings = (config.get("settings", {}),)
    post_modifications = config.get("post_modifications", [])
    api_version = config.get("api_version", __version__)
    _check_version(api_version)

    batoms = Batoms(from_ase=atoms, volume=volume, **batoms_input)
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
    for prop_name, prop_setting in settings.items():
        # TODO prototype API check
        print(prop_name, prop_setting)
        if prop_name == "batoms":
            prop_obj = batoms
            # do not change label after creation
            prop_setting.pop("label", None)
            for key, value in prop_setting.items():
                print(key, value, type(value))
                setattr(prop_obj, key, value)
            print(prop_obj)
            # setattr(prop_obj, key, type_convert({}, value))
        elif prop_name in ["render", "boundary"]:
            prop_obj = getattr(batoms, prop_name)
            for key, value in prop_setting.items():
                setattr(prop_obj, key, value)
        else:
            # TODO: check if prop_name is valid
            prop_obj = getattr(batoms, prop_name)
            draw_params = {}
            for sub_prop_name, sub_prop_setting in prop_setting.items():
                if sub_prop_name == "setting":
                    sub_prop_obj = prop_obj.setting
                    # sub_prop_setting is by default a dict
                    for key, value in sub_prop_setting.items():
                        sub_prop_obj[key] = value
                elif sub_prop_name == "draw":
                    if sub_prop_setting is not False:
                        draw_params = sub_prop_setting
                    else:
                        draw_params = False
                else:
                    raise ValueError(f"Unknown sub_prop_setting {sub_prop_setting}")
            if draw_params is not False:
                if hasattr(prop_obj, "draw"):
                    prop_obj.draw(**draw_params)
                else:
                    batoms.draw()
            print(prop_obj)

    # for prop_name, setting in settings.items():
    #     # TODO: catch AttributeError
    #     prop_obj = getattr(batoms, prop_name)
    #     for key, value in setting.items():
    #         val_string = f"_obj.{key}"
    #         handle = eval(val_string, {}, {"_obj": prop_obj})
    #         handle = value
    # post_modifications = preferences.get("post_modifications", [])
    for mod in post_modifications:
        # TODO: sanity check of expression?
        blender_globals.update({"batoms": batoms, "np": np})
        exec(mod, blender_globals)
    # render_input = preferences.get("render_input", {})
    # Force run self
    print(batoms.bonds)
    print(batoms.bonds.setting)
    batoms.draw()

    # batoms.render.run(batoms)
    batoms.get_image(**render_input)
    return


def main():
    # run()
    print(sys.argv)
    extra_arg = _handle_argv_extras()
    print(extra_arg)


if __name__ == "__main__":
    main()
