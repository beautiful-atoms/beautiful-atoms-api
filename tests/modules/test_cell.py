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

    # 1. Normal cell, not drawing cell
    # TODO: test draw_unit_cell later
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
        c_polyhedra = get_material_color(batoms.polyhedras.obj)
        assert np.isclose(c_polyhedra, [0, 0.5, 0.5, 0.5]).all()
        with pytest.raises((KeyError, AttributeError)):
            cc = batoms.cell.obj_cylinder
    os.remove(".batoms.blend")

    bpy.ops.batoms.delete()

    # Test 2: add cell drawing (currently manual)
    # TODO: test show_unit_cell
    config["post_modifications"] = ["batoms.cell.draw()"]
    render(atoms, save_blender_file=True, **config)
    with load_blender_file() as do:
        batoms = do["batoms"]
        assert batoms.model_style == 2
        c_polyhedra = get_material_color(batoms.polyhedras.obj)
        assert np.isclose(c_polyhedra, [0, 0.5, 0.5, 0.5]).all()
        # The new Bcells from v2.2.0 up has cancelled usage of obj_cylinder
        # cc = batoms.cell.obj_cylinder
        # c_cell = get_material_color(cc)
        # assert np.isclose(c_cell, [0, 0, 0, 1.0]).all()
    os.remove(".batoms.blend")

    bpy.ops.batoms.delete()


if __name__ == "__main__":
    test_cell()
    print("\n cell: All pass! \n")
