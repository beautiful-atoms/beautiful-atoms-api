"""This module is only to be used together with tests
"""
import os
import numpy as np
from pathlib import Path
from contextlib import contextmanager
from bpy.types import Object, Mesh


data_path = Path(__file__).parents[1].resolve() / "datas"
base_config = {
    "batoms_input": {"label": "test_batoms"},
    "settings": {
        "render": {"engine": "cycles", "samples": 1, "resolution": [20, 20]},
    },
}


def get_material_color(obj):
    """Get the active material color of current batoms_property"""
    if not isinstance(obj, Object):
        raise TypeError("Must provide a blender Object as input!")
    active_mater = getattr(obj, "active_material")
    c = (
        active_mater.node_tree.nodes["Principled BSDF"]
        .inputs["Base Color"]
        .default_value
    )
    return np.array(c)


def get_gn_attributes(obj, attribute):
    if not isinstance(obj, Object):
        raise TypeError("Must provide a blender Object as input!")
    mesh = obj.data
    att = mesh.attributes.get(str(attribute))
    if att:
        return list(att.data)
    else:
        raise AttributeError(f"{obj.name} does not have attribute {attribute}")


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
