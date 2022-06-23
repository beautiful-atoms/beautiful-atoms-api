import pytest
from _common_helpers import (
    data_path,
    base_config,
    load_blender_file,
    get_material_color,
)
import os
import numpy as np


def test_boundary():
    from ase.io import read
    from batoms_api import render

    atoms = read(data_path / "tio2.cif")
    config = base_config.copy()

    # 1. Set a slightly larger than unity boundary, test bond search settings
    config["settings"].update(
        {
            "model_style": 2,
            # Make boundary slightly over to include all neighbouring atoms
            "boundary": [0.1, 0.1, 0.1],
            "bonds": {
                "show_search": True,
            },
            "polyhedras": {"setting": {"Ti": {"color": [0, 0.5, 0.5, 0.5]}}},
        }
    )
    render(atoms, save_blender_file=True, **config)
    with load_blender_file() as do:
        batoms = do["batoms"]
        # Boundary objects are currently not persistent when saving / loading
        # use bonds etc
        bb = batoms.boundary
        # Conventional cell, 2 x Ti + 4 x O
        assert len(batoms.arrays["species"]) == 6
        assert len(batoms.bonds) == 54
        c_polyhedra = get_material_color(batoms.polyhedras.obj)
        assert np.isclose(c_polyhedra, [0, 0.5, 0.5, 0.5]).all()
    os.remove(".batoms.blend")

    # 2. Shrink the boundary below 1
    config["settings"]["boundary"] = [-0.2, -0.2, -0.2]
    render(atoms, save_blender_file=True, **config)
    with load_blender_file() as do:
        batoms = do["batoms"]
        bb = batoms.boundary
        # Conventional cell, 2 x Ti + 4 x O
        assert len(batoms.arrays["species"]) == 6
        # 2 polyhedrae x 6 bonds each
        assert len(batoms.bonds) == 12
        c_polyhedra = get_material_color(batoms.polyhedras.obj)
        assert np.isclose(c_polyhedra, [0, 0.5, 0.5, 0.5]).all()
    os.remove(".batoms.blend")


if __name__ == "__main__":
    test_boundary()
    print("\n boundary: All pass! \n")
