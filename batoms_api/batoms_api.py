import os
import pickle
from warnings import warn
from pathlib import Path
from subprocess import run
from collections import OrderedDict
from ruamel_yaml import YAML
from mergedeep import merge, Strategy
from .metadata import SCHEMA_DIR, __version__

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


DEFAULT_SCHEMA = SCHEMA_DIR / "schema.yaml"

default_schema = YAML(pure=True).load(DEFAULT_SCHEMA)

TYPE_MAPPING = {
    "_int": int,
    "_float": float,
    "_list": list,
    "_dict": dict,
    "_str": str,
    "_bool": bool,
}


def type_check(value, allowed_type):
    """Check if value is in allowed_type
    0. map between string --> python type
    1. if allowed_type is a list, match any
    2. if allowed_type is single instance, try convert
    if all pass, return the value, or raise Exception
    """
    python_types = []
    if isinstance(allowed_type, str):
        allowed_type = [allowed_type]
    for typ in allowed_type:
        python_types.append(TYPE_MAPPING[typ])
    if isinstance(value, tuple(python_types)):
        return value
    elif len(python_types) == 1:
        try:
            return python_types[0](value)
        except ValueError as e:
            raise Exception(f"Cannot convert {value} to type {python_types[0]}") from e
    else:
        raise ValueError("Cannot perform type conversion for multiple types!")


def set_dict(raw_dict, output_dict, schema):
    """Recursively set dict according to schema"""
    # Avoid change of root level schema
    schema = schema.copy()
    raw_dict = raw_dict.copy()
    for key, value in raw_dict.items():
        # "_any" in schema key can accept any entry
        # 1. evaluate the key is necessary
        # 2. test if new key is valid in schema
        # 3. create new entries and walk the dict tree
        if key not in schema.keys():
            if "_any" not in schema.keys():
                warn(f"Key {key} not in schema, skip")
                continue
            else:
                # Evaluate the key like "('C', 'H')" --> ('C', 'H')
                if schema["_any"].get("_eval_key", False):
                    key = eval(str(key))
                # This subschema accepts any key value
                sub_schema = schema["_any"]
        else:
            sub_schema = schema[key]
        # breakpoint()
        # Determine if we have eached the leaf node
        if "_disabled" in sub_schema.keys():
            warn(f"Key {key} is disabled in current scope, ignore.")
        elif "_type" in sub_schema.keys():
            allowed_type = sub_schema["_type"]
            # Reached a leaf node
            output_dict[key] = type_check(value, allowed_type)
        else:
            # Walk the dictionary
            sub_raw_dict = value
            output_dict[key] = {}
            sub_output_dict = output_dict[key]
            set_dict(sub_raw_dict, sub_output_dict, sub_schema)
    return


def load_yaml_config(custom_yaml, schema=default_schema):
    """Load yaml from a custom yaml file and validate using schema"""
    content = YAML(pure=True).load(custom_yaml)
    output_dict = {}
    set_dict(content, output_dict, schema)
    return output_dict


def merge_dicts(origin_dict, update_dict, schema=default_schema):
    """Recursively merge two dicts with update_dict overwrites values in origin_dict.
    Both dicts will be passed through schema checker
    """
    sane_origin_dict, sane_update_dict = {}, {}
    set_dict(origin_dict.copy(), sane_origin_dict, schema)
    set_dict(update_dict.copy(), sane_update_dict, schema)
    merged = merge({}, sane_origin_dict, sane_update_dict)
    return merged


def blender_run(input_file, blender_command=None, args_prefix=(), args_extras=("-b",), dryrun=False):
    """Run the blender file using given input file
    Basic usage
    blender -b batoms_api.script_api -- input_file_path
    args_prefix: series of args to put before blender, e.g. wrapper of docker command
    args_extras: series of args to put in between blender main command and sub commands, e.g. to control display
    """
    input_file = Path(input_file).resolve()
    bl_sub_commands = [
        "--python-exit-code",
        "1",
        "--python-expr",
        "from batoms_api import script_api; script_api.run()",
        "--",
        input_file.as_posix(),
    ]
    if blender_command is None:
        if "BLENDER_COMMAND" in os.environ.keys():
            blender_command = os.environ["BLENDER_COMMAND"]
        else:
            blender_command = "blender"
        bl_main_command = [str(blender_command)]

    full_args = (
        list(args_prefix) + bl_main_command + list(args_extras) + bl_sub_commands
    )
    if dryrun:
        logger.debug(("Dryrun mode. Following command will be used for blender rendering:\n"
        f"{full_args}"
        ))
    else:
        proc = run(full_args)
        if proc.returncode != 0:
            raise RuntimeError(
                (
                    "Running following rendering script\n"
                    f"{full_args}\n"
                    f"fails with return code {proc.returncode}."
                )
            )
    return


def render(
    atoms,
    volume=None,
    batoms_input={},
    render_input={},
    settings={},
    post_modifications=[],
    config_file=None,
    display=False,
    queue=None,
    save_input_file=False,
    save_blender_file=False,
    dryrun=False
):
    """
    atoms: an ASE atoms object
    volume: ASE compatible volume object, default is None
    batoms_input: input parameters to create the Batoms object (i.e. those can be passed to Batoms.__init__)
    render_input: input parameters to create the Render object (i.e. those can be passed to Batoms.get_image)
    settings: extra settings that modify the attributes of the batoms object.
    post_modifications: list of commands to be evaluated following the given order
    config_file: default configuration yaml file to load from.
                 parameters `batoms_input` `render_input` `settings` and `post_modifications` overwrite default config
    save_input_file: if True, saves to `.batoms.inp` on cwd; otherwise if given a specifc name, save to that name
    dryrun: do not actually execute the blender_run function. input file is still generated
    """
    if config_file is not None:
        default_config = load_yaml_config(config_file)
    else:
        default_config = {}

    user_config = {
        "batoms_input": batoms_input,
        "render_input": render_input,
        "settings": settings,
        "post_modifications": post_modifications,
    }

    merged_config = merge_dicts(default_config, user_config)

    config = {
        "atoms": atoms,
        "volume": volume,
        "api_version": __version__,
        "save_blender_file": save_blender_file,
        **merged_config,
    }

    input_file = Path(".batoms.inp").resolve()
    if save_input_file and isinstance(save_input_file, (str, Path)):
        input_file = Path(save_input_file)

    with open(input_file, "wb") as f:
        pickle.dump(config, f, protocol=0)
    logger.debug(f"Write input file {input_file.as_posix()}")

    options = {}
    if display:
        options["args_extras"] = []
    if queue:
        options["args_prefix"] = ["srun", "-n", "$SLURM_NTASKS"]

    blender_run(input_file, dryrun=dryrun, **options)

    if not save_input_file:
        os.remove(input_file)
        logger.debug(f"Removed input file {input_file.as_posix()}")

    return


if __name__ == "__main__":
    from ase.build import molecule

    mol = molecule("CH4")
    test_content = {
        "batoms_input": {"label": "ch4", "pbc": False},
        "settings": {
            "model_style": 2,
            "species": {
                "C": {
                    "color": [1, 0.1, 0.1, 1.0],
                    # "material_style": "metallic",
                    "scale": 0.7,
                },
                "H": {
                    "material_style": "plastic",
                    "color": [0, 0.5, 0.5, 1.0],
                    "scale": 0.2,
                },
            },
            "bonds": {"setting": {"('C', 'H')": {"polyhedra": True}}},
            "polyhedras": {"setting": {"C": {"color": [1, 0.1, 0.1, 0.1]}}},
            "render": {"resolution": [200, 200], "engine": "cycles", "samples": 32},
        },
        "post_modifications": ["batoms.location += [0, 0, 10]"],
    }
    render(mol, save_input_file="ch4.inp", save_blender_file=True, **test_content)
