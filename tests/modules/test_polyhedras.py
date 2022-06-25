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


def test_polyhedras():
    bpy.ops.batoms.delete()
    from ase.io import read
    from batoms_api import render

    atoms = read(data_path / "tio2.cif")
    config = base_config.copy()
    config["settings"].update(
        {
            "model_style": 2,
            "bonds": {"show_search": True},
            "polyhedras": {"setting": {"Ti": {"color": [1, 0, 1, 0.5]}}},
        }
    )
    render(atoms, save_blender_file=True, **config)
    # Check if the real material assigned is the same color
    with load_blender_file() as do:
        batoms = do["batoms"]
        c_polyhedra = get_material_color(batoms.polyhedras.obj)
        assert np.isclose(c_polyhedra, [1, 0, 1, 0.5]).all()
    os.remove(".batoms.blend")

    bpy.ops.batoms.delete()


def test_bond_search():
    bpy.ops.batoms.delete()
    from ase.io import read
    from batoms_api import render

    atoms = read(data_path / "tio2.cif")
    config = base_config.copy()
    config["settings"].update({"model_style": 2, "bonds": {"show_search": False}})
    render(atoms, save_blender_file=True, **config)
    # Check if the real material assigned is the same color
    with load_blender_file() as do:
        batoms = do["batoms"]
        assert batoms.bonds.show_search is False
        bond_search_obj = batoms.bonds.search_bond.obj
        att = get_gn_attributes(bond_search_obj, "show")
        # When search_bond not set, the value is an empty list
        assert len(att) == 0
    os.remove(".batoms.blend")
    bpy.ops.batoms.delete()

    # Enable the search_bond
    config["settings"]["bonds"]["show_search"] = True
    render(atoms, save_blender_file=True, **config)
    # Check if the real material assigned is the same color
    with load_blender_file() as do:
        batoms = do["batoms"]
        assert batoms.bonds.show_search is True
        bond_search_obj = batoms.bonds.search_bond.obj
        att = get_gn_attributes(bond_search_obj, "show")
        # Currently att is not persistent
        # assert len(att) == 7
    os.remove(".batoms.blend")
    bpy.ops.batoms.delete()


if __name__ == "__main__":
    test_polyhedras()
    test_bond_search()
    print("\n polyhedras: All pass! \n")
