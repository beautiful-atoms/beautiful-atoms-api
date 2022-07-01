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


def test_boundary():
    bpy.ops.batoms.delete()
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
            "bond": {
                "show_search": True,
            },
            "polyhedra": {"settings": {"Ti": {"color": [0, 0.5, 0.5, 0.5]}}},
        }
    )
    render(atoms, save_blender_file=True, **config)
    with load_blender_file() as do:
        batoms = do["batoms"]
        bb = batoms.boundary
        assert bb[0, 0] == pytest.approx(-0.1, 1.e-4)
        assert bb[0, 1] == pytest.approx(1.1, 1.e-4)

        # Conventional cell, 2 x Ti + 4 x O
        assert len(batoms.arrays["species"]) == 6
        assert len(batoms.bond) == 54
        assert len(batoms.polyhedra) == 54
        c_polyhedra = get_material_color(batoms.polyhedra.obj)
        assert np.isclose(c_polyhedra, [0, 0.5, 0.5, 0.5]).all()
    os.remove(".batoms.blend")

    bpy.ops.batoms.delete()

    # 2. Shrink the boundary below 1
    config["settings"]["boundary"] = [-0.2, -0.2, -0.2]
    render(atoms, save_blender_file=True, **config)
    with load_blender_file() as do:
        batoms = do["batoms"]
        bb = batoms.boundary
        assert bb[0, 0] == pytest.approx(0.2, 1.e-4)
        assert bb[0, 1] == pytest.approx(0.8, 1.e-4)
        # Conventional cell, 2 x Ti + 4 x O
        assert len(batoms.arrays["species"]) == 6
        # 2 polyhedrae x 6 bonds each
        assert len(batoms.bond) == 12
        assert len(batoms.polyhedra) == 12
        c_polyhedra = get_material_color(batoms.polyhedra.obj)
        assert np.isclose(c_polyhedra, [0, 0.5, 0.5, 0.5]).all()
    
    # os.system("cp .batoms.blend test.blend")
    os.remove(".batoms.blend")

    bpy.ops.batoms.delete()


if __name__ == "__main__":
    test_boundary()
    print("\n boundary: All pass! \n")
