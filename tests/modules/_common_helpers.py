"""This module is only to be used together with tests
"""
import os
from pathlib import Path
from contextlib import contextmanager


data_path = Path(__file__).parents[1].resolve() / "datas"
base_config = {
    "batoms_input": {"label": "test_batoms"},
    "settings": {
        "render": {"engine": "cycles", "samples": 1, "resolution": [20, 20]},
    },
}


@contextmanager
def load_blender_file(filepath=".batoms.blend", label="test_batoms"):
    """Load the scene objects from the .blend file
    return dict contains:
    batoms: a Batoms instance
    """
    import bpy
    from batoms import Batoms
    from batoms.utils.butils import removeAll

    bpy.ops.wm.open_mainfile(filepath=filepath)
    #
    ba = Batoms(label=label)
    data_obj = {"batoms": ba}
    try:
        yield data_obj
    finally:
        removeAll()
