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


def test_cell():
    bpy.ops.batoms.delete()
    from ase.io import read
    from batoms_api import render

    atoms = read(data_path / "tio2.cif")
    config = base_config.copy()

    # Test 1. Normal cell, not drawing cell
    config["settings"].update(
        {
            "model_style": 2,
            "bond": {
                "show_search": True,
            },
            "polyhedra": {"settings": {"Ti": {"color": [0, 0.5, 0.5, 0.5]}}},
        }
    )
    render(atoms, save_blender_file=True, **config)
    with load_blender_file() as do:
        batoms = do["batoms"]
        assert batoms.model_style == 2
        c_polyhedra = get_material_color(batoms.polyhedra.obj)
        assert np.isclose(c_polyhedra, [0, 0.5, 0.5, 0.5]).all()
        with pytest.raises((KeyError, AttributeError)):
            cc = batoms.cell.obj_cylinder
    os.remove(".batoms.blend")

    bpy.ops.batoms.delete()

    # Test 2: add cell
    config["settings"].update({"cell": {"width": 0.1, "color": [1.0, 0, 0, 1.0]}})
    render(atoms, save_blender_file=True, **config)
    with load_blender_file() as do:
        batoms = do["batoms"]
        assert batoms.cell.width == pytest.approx(0.1, 1.0e-4)
        cc = batoms.cell.obj
        c_cell = get_material_color(cc)
        assert np.isclose(c_cell, [1.0, 0, 0, 1.0]).all()

    #  Test 3: do not show cell
    config["settings"].update({"show_unit_cell": False})
    render(atoms, save_blender_file=True, **config)
    with load_blender_file() as do:
        batoms = do["batoms"]
        assert batoms.cell.hide is True
    os.remove(".batoms.blend")

    bpy.ops.batoms.delete()


if __name__ == "__main__":
    test_cell()
    print("\n cell: All pass! \n")
