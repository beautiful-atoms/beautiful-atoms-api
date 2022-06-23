import pytest
from _common_helpers import (
    data_path,
    base_config,
    load_blender_file,
    get_material_color,
    get_gn_attributes,
)
import os
import numpy as np
import bpy


def test_isosurfaces():
    from ase.io.cube import read_cube_data
    from batoms_api import render

    volume, atoms = read_cube_data(data_path / "h2o-homo.cube")
    config = base_config.copy()
    config["settings"].update(
        {
            "model_style": 1,
            "isosurfaces": {
                "setting": {
                    "1": {"level": -0.001, "color": [1, 1, 0, 0.5]},
                    "2": {"level": 0.001, "color": [0, 1, 1, 0.5]},
                }
            },
        }
    )
    config["post_modifications"] = ["batoms.isosurfaces.draw()"]
    render(atoms, volume=volume, save_blender_file=True, **config)
    with load_blender_file() as do:
        batoms = do["batoms"]
        label = batoms.label
        assert len(batoms.isosurfaces.setting) == 2
        iso1 = batoms.coll.objects[f"{label}_isosurface_1"]
        iso2 = batoms.coll.objects[f"{label}_isosurface_2"]
        c1, c2 = get_material_color(iso1), get_material_color(iso2)
        assert np.isclose(c1, [1, 1, 0, 0.5]).all()
        assert np.isclose(c2, [0, 1, 1, 0.5]).all()
    os.remove(".batoms.blend")

    # os.remove(".batoms.blend")


if __name__ == "__main__":
    test_isosurfaces()
    print("\n Isosurfaces: All pass! \n")
