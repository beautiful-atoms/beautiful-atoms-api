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


def test_lp():
    from ase.build import bulk
    from batoms_api import render

    config = base_config.copy()
    atoms = bulk("Au", cubic=True) * [2, 2, 2]
    config["settings"].update(
        {
            "model_style": 0,
            "lattice_plane": {
                "settings": {
                    "(1, 1, 1)": {"distance": 3, "scale": 2.0},
                    "(1, 1, 0)": {
                        "distance": 2,
                        "color": [0.8, 0.1, 0, 0.8],
                        "scale": 1.5,
                    },
                },
                "draw": True,
            },
        }
    )
    render(atoms, save_blender_file=True, display=False, **config)
    with load_blender_file() as do:
        batoms = do["batoms"]
        assert len(batoms.lattice_plane.settings) == 2
        assert batoms.lattice_plane.settings[(1, 1, 1)].distance == pytest.approx(
            3.0, 1.0e-4
        )
        assert batoms.lattice_plane.settings[(1, 1, 0)].distance == pytest.approx(
            2.0, 1.0e-4
        )
        assert batoms.lattice_plane.settings[(1, 1, 1)].scale == pytest.approx(
            2.0, 1.0e-4
        )
        assert batoms.lattice_plane.settings[(1, 1, 0)].scale == pytest.approx(
            1.5, 1.0e-4
        )
        assert batoms.lattice_plane.settings[(1, 1, 1)].slicing is False
        assert batoms.lattice_plane.settings[(1, 1, 0)].slicing is False

    os.remove(".batoms.blend")


def test_lp_material():
    from ase.build import bulk
    from batoms_api import render

    config = base_config.copy()
    atoms = bulk("Au", cubic=True) * [2, 2, 2]
    # Test if all setters work (leaving actual unit tests for boundary and slicing)
    config["settings"].update(
        {
            "model_style": 0,
            "lattice_plane": {
                "settings": {
                    "(1, 0, 0)": {
                        "distance": 1,
                        "color": [0.8, 0, 0.6, 0.95],
                        "material_style": "metallic",
                        "width": 0.2,
                        "show_edge": False,
                        "scale": 1.2,
                        "boundary": False,
                        "slicing": False,
                    },
                },
                "draw": True,
            },
        }
    )
    render(atoms, save_blender_file=True, display=False, **config)
    with load_blender_file() as do:
        batoms = do["batoms"]
        label = batoms.label
        lp_obj = batoms.coll.objects[f"{label}_plane_1-0-0"]
        # Is a metallic plane
        assert np.isclose(get_material_color(lp_obj), [0.8, 0, 0.6, 0.95]).all()
        assert (
            lp_obj.active_material.node_tree.nodes["Principled BSDF"]
            .inputs["Metallic"]
            .default_value
            == 1.0
        )
    os.remove(".batoms.blend")


if __name__ == "__main__":
    test_lp()
    print("\n ms: All pass! \n")
