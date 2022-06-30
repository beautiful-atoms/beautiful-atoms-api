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


def test_ms():
    from ase.build import molecule
    from batoms_api import render

    config = base_config.copy()
    atoms = molecule("C2H6SO")
    config["settings"].update(
        {
            "model_style": 1,
            "molecular_surface": {
                "settings": {
                    "1": {"type": "SAS", "probe": 1.0, "color": [1, 1, 0, 0.5]},
                    "2": {"type": "SES", "resolution": 0.25, "color": [0, 0, 0.8, 0.5]},
                },
                "draw": True,
            },
        }
    )
    render(atoms, save_blender_file=True, display=False, **config)
    with load_blender_file() as do:
        batoms = do["batoms"]
        assert len(batoms.molecular_surface.settings) == 2
        assert batoms.molecular_surface.settings["1"].type == "SAS"
        assert batoms.molecular_surface.settings["2"].type == "SES"
        assert batoms.molecular_surface.settings["1"].resolution == pytest.approx(
            0.5, 1.0e-4
        )
        assert batoms.molecular_surface.settings["2"].resolution == pytest.approx(
            0.25, 1.0e-4
        )
        assert batoms.molecular_surface.settings["1"].probe == pytest.approx(
            1.0, 1.0e-4
        )
        assert batoms.molecular_surface.settings["2"].probe == pytest.approx(
            1.4, 1.0e-4
        )

    os.remove(".batoms.blend")


if __name__ == "__main__":
    test_ms()
    print("\n ms: All pass! \n")
