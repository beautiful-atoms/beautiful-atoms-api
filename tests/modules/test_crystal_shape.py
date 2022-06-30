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
    from ase.build import bulk
    from batoms_api import render

    config = base_config.copy()
    atoms = bulk("Au", cubic=True)
    config["settings"].update(
        {
            "model_style": 0,
            "crystal_shape": {
                "settings": {
                    "(1, 1, 1)": {
                        "distance": 6,
                        "color": [0, 0.8, 0, 1],
                        "material_style": "plastic",
                        "width": 0.2,
                        "symmetry": True,
                        "crystal": True,
                    },
                    "(-1, 1, 0)": {
                        "distance": 6,
                        "color": [0.8, 0.1, 0, 1],
                        "symmetry": True,
                        "crystal": True,
                        "material_style": "mirror",
                        "show_edge": False,
                    },
                },
                "draw": True,
            },
        }
    )
    render(atoms, save_blender_file=True, display=False, **config)
    with load_blender_file() as do:
        batoms = do["batoms"]
        # 8 symmetries of 111 + 12 symmetries of -110
        assert len(batoms.crystal_shape.settings) == 20
        # Non-exhaustive, just to check symbol
        assert batoms.crystal_shape.settings.find("1-1-1") is not None
        assert batoms.crystal_shape.settings.find("-1-1-1") is not None
        assert batoms.crystal_shape.settings.find("-1-1-0") is not None
        assert batoms.crystal_shape.settings.find("-1--1-0") is not None

    os.remove(".batoms.blend")


if __name__ == "__main__":
    test_cs()
    print("\n ms: All pass! \n")
