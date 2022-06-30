"""Unit tests for setter functions in batoms_api.batoms_api
"""
import pytest
from pathlib import Path
from typing import Dict

curdir = Path(__file__).parent.resolve()


def test_value_conversion():
    from batoms_api.batoms_api import type_check

    assert isinstance(type_check(1, "_float"), float)
    assert isinstance(type_check(1.0, "_int"), int)
    assert isinstance(type_check(1.0, "_str"), str)
    assert type_check(1, ("_float", "_int"))
    with pytest.raises(Exception):
        type_check("1", ("_float", "_int"))
    assert type_check(True, "_bool")
    assert type_check([1, 2], "_list")
    assert type_check((1, 2), "_list")
    with pytest.raises(Exception):
        type_check("s", "_int")


def test_dict_set():
    from batoms_api.batoms_api import set_dict, default_schema

    # Test type conversion
    output = {}
    set_dict({"batoms_input": {"scale": 1}}, output, default_schema)
    assert isinstance(output["batoms_input"]["scale"], float)
    # Type key converson (string to tuple)
    output = {}
    set_dict(
        {
            "settings": {
                "bond": {"settings": {"('C', 'H')": {"order": 2}}},
            }
        },
        output,
        default_schema,
    )
    assert ("C", "H") in output["settings"]["bond"]["settings"].keys()
    # Test if explicity python types can be added
    output = {}
    set_dict(
        {
            "settings": {
                "bond": {"settings": {("C", "H"): {"order": 2}}},
            }
        },
        output,
        default_schema,
    )
    assert ("C", "H") in output["settings"]["bond"]["settings"].keys()
    # property 'bonds' is deprecated and not in settings
    output = {}
    set_dict(
        {
            "settings": {
                "bonds": {"settings": {'("C", "H")': {"order": 2}}},
            }
        },
        output,
        default_schema,
    )
    assert "bonds" not in output["settings"].keys()


def test_disabled_vals():
    from batoms_api.batoms_api import set_dict, default_schema

    # Test if disabled fields are prevented from loading
    output = {}
    set_dict(
        {
            "batoms_input": {
                "polyhedra_style": 1,
                "model_style": 1,
                "radius_style": "1",
            }
        },
        output,
        default_schema,
    )
    assert "polyhedra_style" not in output["batoms_input"].keys()
    assert "model_style" in output["batoms_input"].keys()
    assert "radius_style" in output["batoms_input"].keys()

    # Special case: batoms label should be an initializer instead of modifier
    # therefore providing label to `settings.batoms` will be ignored
    output = {}
    set_dict(
        {
            "batoms_input": {"label": "mol-1"},
            "settings": {"label": "mol-2"},
        },
        output,
        default_schema,
    )
    assert output["batoms_input"]["label"] == "mol-1"
    assert "label" not in output["settings"]


def test_yaml_load():
    from batoms_api.batoms_api import load_yaml_config

    yaml_file = open((curdir / "example.yaml"), "r")
    config = load_yaml_config(yaml_file)
    assert "polyhedra_style" not in config["batoms_input"].keys()
    assert "model_style" in config["batoms_input"].keys()
    assert config["batoms_input"]["radius_style"] == 1
    assert ("C", "H") in config["settings"]["bond"]["settings"].keys()


def test_merge_dict():
    from batoms_api.batoms_api import load_yaml_config, merge_dicts

    yaml_file = open((curdir / "example.yaml"), "r")
    config = load_yaml_config(yaml_file)
    new_config = {
        "batoms_input": {"label": "ch4_mod"},
        "settings": {
            "bond": {
                "settings": {
                    ("C", "H"): {
                        "order": 1,
                    },
                    ("C", "C"): {
                        "order": 2,
                        "polyhedra": False,
                    },
                }
            }
        },
    }
    merged = merge_dicts(config, new_config)
    assert merged["batoms_input"]["label"] == "ch4_mod"
    assert ("C", "C") in merged["settings"]["bond"]["settings"].keys()
    assert merged["settings"]["bond"]["settings"][("C", "H")]["order"] == 1
    assert merged["settings"]["bond"]["settings"][("C", "C")]["order"] == 2
    assert merged["settings"]["bond"]["settings"][("C", "H")]["polyhedra"] is True
    assert merged["settings"]["bond"]["settings"][("C", "C")]["polyhedra"] is False
