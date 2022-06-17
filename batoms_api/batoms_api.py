from cgi import test
from typing import OrderedDict
from matplotlib.pyplot import subplots_adjust
from ruamel_yaml import YAML
from sympy import Order
from . import MODULE_ROOT, SCHEMA_DIR
from warnings import warn
from collections import OrderedDict

DEFAULT_SCHEMA = SCHEMA_DIR / "schema.yaml"

schema = YAML(pure=True).load(DEFAULT_SCHEMA)

def load_yaml_config(custom_yaml, schema=schema):
    """Load yaml from a custom yaml file and validate using schema
    """
    content = YAML(pure=True).load(custom_yaml)
    output_dict = {}
    set_dict(content, output_dict, schema)
    return output_dict
    
def type_check(value, allowed_type):
    """Check if value is in allowed_type
    0. map between string --> python type
    1. if allowed_type is a list, match any
    2. if allowed_type is single instance, try convert 
    if all pass, return the value, or raise Exception
    """
    warn("Not implemented")
    return value


def set_dict(raw_dict, output_dict, schema):
    """Recursively set dict according to schema"""
    # Avoid change of root level schema
    schema = schema.copy()
    raw_dict = raw_dict.copy()
    for key, value in raw_dict.items():
        print(key, value)
        # "_any" in schema key can accept any entry
        # 1. evaluate the key is necessary
        # 2. test if new key is valid in schema
        # 3. create new entries and walk the dict tree
        if key not in schema.keys():
            if ("_any" not in schema.keys()):
                warn(f"Key {key} not in schema, skip")
                continue
            else:
                # Evaluate the key like "('C', 'H')" --> ('C', 'H')
                if schema["_any"].get("_eval_key", False):
                    key = eval(str(key))
                    sub_schema = schema["_any"]
        else:
            sub_schema = schema[key]
        # breakpoint()
        # Determine if we have eached the leaf node
        if "_type" in sub_schema.keys():
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


if __name__ == "__main__":
    test_content = {
        "batoms_input": {"label": "ch4", "pbc": [1, 2, 3]},
        "settings": {
            "bonds":
            {
                "setting":
                {"('C', 'H')": {"order": 2}}
            }
        }
        }
    output = {}
    set_dict(test_content, output, schema)
    print(output)