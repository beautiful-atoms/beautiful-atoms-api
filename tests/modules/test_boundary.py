from batoms_api.script_api import save_blender_file
import pytest
from _common_helpers import data_path, base_config, load_blender_file
import os


def test_boundary():
    from ase.io import read
    from batoms_api import render

    atoms = read(data_path / "tio2.cif")
    config = base_config.copy()
    # config["batoms_input"].update(
    #     {
    #         "model_style": 2,
    #     }
    # )
    config["settings"].update(
        {
            "model_style": 2,
            "boundary": [0.01, 0.01, 0.01],
            "bonds": {
                "show_search": True,
            },
            "polyhedras": {"setting": {"Ti": {"color": [0, 0.5, 0.5, 0.5]}}},
        }
    )
    render(atoms, save_blender_file=True, **config)
    # os.remove(".batoms.blend")


if __name__ == "__main__":
    test_boundary()
    print("\n boundary: All pass! \n")
