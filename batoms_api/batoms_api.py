from ruamel_yaml import YAML
from . import MODULE_ROOT, SCHEMA_DIR
from warnings import warn
from collections import OrderedDict
from mergedeep import merge, Strategy


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
    # warn("Not implemented")
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
        # print(key, value)
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


def render():
    pass


if __name__ == "__main__":
    test_content = {
        "batoms_input": {"label": "ch4", "pbc": [1, 2, 3]},
        "settings": {
            "bonds": {"setting": {"('C', 'H')": {"order": 2}}},
            "polyhedras": {"setting": {"C": {"color": [0.1, 0.1, 0.1, 1.0]}}},
        },
        "post_modifications": ["batoms.render.resolution = [200, 200]"],
    }
    output = {}
    set_dict(test_content, output, default_schema)
    print(output)
