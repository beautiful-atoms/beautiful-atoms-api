import pytest
from _common_helpers import data_path, base_config, load_blender_file, get_material_color
import os
import numpy as np

def test_cell():
    from ase.io import read
    from batoms_api import render

    atoms = read(data_path / "tio2.cif")
    config = base_config.copy()

    config["settings"].update({
        "model_style": 2,
        "bonds": {"show_search": True,},
        "polyhedras": {
            "setting": {
                "Ti": {"color": [0, 0.5, 0.5, 0.5]}
            }
        }

    })
    render(atoms, save_blender_file=True, **config)
    with load_blender_file() as do:
        batoms = do["batoms"]
        assert batoms.model_style == 2
        c_polyhedra = get_material_color(batoms.polyhedras.obj)
        assert np.isclose(c_polyhedra, [0, 0.5, 0.5, 0.5]).all()
    os.remove(".batoms.blend")


if __name__ == "__main__":
    test_cell()
    print("\n cell: All pass! \n")
