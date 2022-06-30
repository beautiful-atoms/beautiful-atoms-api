import pytest
from _common_helpers import (
    data_path,
    base_config,
    load_blender_file,
    get_material_color,
)
import os
import numpy as np
import bpy


def test_cs():
    from ase.build import molecule
    from batoms_api import render

    config = base_config.copy()
    atoms = molecule("C6H6", cell=[5, 5, 4]) * (2, 2, 2)
    config["settings"].update(
        {
            "model_style": 0,
            "boundary": -0.1,
            "cavity": {
                "resolution": 0.25,
                "minRadius": 0.5,
                "settings": {
                    "1": {
                        "min": 0.5,
                        "max": 3.0,
                        "color": [1.0, 0, 0, 0.5],
                        "material_style": "ceramic",
                    }
                },
                "draw": True,
            },
        }
    )
    render(atoms, save_blender_file=True, display=False, **config)
    # with load_blender_file() as do:
    #     batoms = do["batoms"]
    #     # 8 symmetries of 111 + 12 symmetries of -110
    #     assert len(batoms.crystal_shape.setting) == 20
    #     # Non-exhaustive, just to check symbol
    #     assert batoms.crystal_shape.setting.find("1-1-1") is not None
    #     assert batoms.crystal_shape.setting.find("-1-1-1") is not None
    #     assert batoms.crystal_shape.setting.find("-1-1-0") is not None
    #     assert batoms.crystal_shape.setting.find("-1--1-0") is not None

    os.remove(".batoms.blend")


if __name__ == "__main__":
    test_cs()
    print("\n ms: All pass! \n")
