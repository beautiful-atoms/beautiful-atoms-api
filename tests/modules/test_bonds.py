import pytest
from _common_helpers import data_path, base_config, load_blender_file
import os


def test_bonds():
    from ase.build import molecule
    from batoms_api import render

    config = base_config.copy()

    atoms = molecule("CH4")
    config["batoms_input"].update({"model_style": 1})
    config["settings"].update({"bonds": {"setting": {("C", "H"): {"style": "3"}}}})
    render(atoms, save_blender_file=True, **config)
    with load_blender_file() as do:
        batoms = do["batoms"]
        assert batoms.model_style == 1
        assert batoms.bonds.setting[("C", "H")].style == "3"
    os.remove(".batoms.blend")


def test_hydrogen_bond():
    from ase.build import molecule
    from batoms_api import render

    config = base_config.copy()

    # 1. Enable hydrogen bond. # of hydrogen bonds become 3 with style 2
    atoms = molecule("CH3OH")
    config["batoms_input"].update({"model_style": 1})
    config["settings"].update({"bonds": {"show_hydrogen_bond": True}})

    render(atoms, save_blender_file=True, **config)
    with load_blender_file() as do:
        batoms = do["batoms"]
        assert batoms.model_style == 1
        assert batoms.bonds.show_hydrogen_bond is True
        # 5 cov bonds + 3 H-bonds
        assert len(batoms.bonds.arrays["style"]) == 8
        assert all(batoms.bonds.arrays["style"][:5] == 1)
        assert all(batoms.bonds.arrays["style"][5:] == 2)
    os.remove(".batoms.blend")

    # 2. Disable hydrogen bond, # of total bonds --> 5
    config["settings"]["bonds"].update({"show_hydrogen_bond": False})
    render(atoms, save_blender_file=True, **config)
    with load_blender_file() as do:
        batoms = do["batoms"]
        assert batoms.model_style == 1
        assert batoms.bonds.show_hydrogen_bond is False
        # 5 cov bonds
        assert len(batoms.bonds.arrays["style"]) == 5
        assert all(batoms.bonds.arrays["style"] == 1)
    os.remove(".batoms.blend")


if __name__ == "__main__":
    test_bonds()
    test_hydrogen_bond()
    print("\n Bonds: All pass! \n")
