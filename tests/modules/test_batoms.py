import pytest
from _common_helpers import data_path, base_config, load_blender_file
import os
import bpy


def test_batoms():
    from ase.build import molecule
    from batoms_api import render
    bpy.ops.batoms.delete()

    atoms = molecule("CH4")
    config = base_config.copy()
    config["batoms_input"].update(
        {
            "model_style": 1,
        }
    )
    config["settings"]["species"] = {
        "C": {"color": [0.0, 0.8, 0.0, 1.0]},
        "H": {"color": [0.1, 0.1, 0.1, 1.0]},
    }
    render(atoms, save_blender_file=True, **config)
    with load_blender_file() as do:
        batoms = do["batoms"]
        assert batoms.label == "test_batoms"
        assert batoms.model_style == 1
        assert batoms.species["C"].color[1] == pytest.approx(0.8, 1.0e-4)
        assert batoms.species["H"].color[1] == pytest.approx(0.1, 1.0e-4)

    # Outside of the context batoms is not linked with any collection
    with pytest.raises(Exception):
        print(batoms.label)
    os.remove(".batoms.blend")
    bpy.ops.batoms.delete()


if __name__ == "__main__":
    test_batoms()
    print("\n Batoms: All pass! \n")
