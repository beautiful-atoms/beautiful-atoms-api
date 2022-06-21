from ase.build import molecule
from batoms_api import render

atoms = molecule("CH4")
atoms.cell = [3, 3, 3]
atoms.pbc = True
atoms = atoms * [2, 2, 2]
# batoms_input = {
#     "label": "nh3",
#     "model_style": "1",
#     # 'species_props': {'H':{'color': [0.0, 0.8, 0.0, 1.0]},
#     #   'C':{'color': [0.1, 0.1, 0.1, 1.0]}},
#     # 'bondsetting': {'C-H': [0, 2.0, 1, True]},
#     # 'polyhedrasetting': {'C':[[0.6, 0.0, 0.4, 0.3], 0.01]},
# }
# render_input = {
#     "viewport": [1, 1, 0],
#     "engine": "cycles",
#     "output": "figs/ch4.png",
# }
# modifications = [
# "batoms.render.resolution = [200, 200]",
# ]
render(
    atoms,
    batoms_input={"label": "ch4_mod"},
    render_input={},
    #    render_input=render_input,
    settings={
        "batoms": {
            #    "label": "ch4",
            "model_style": 2,
            "polyhedra_style": 1,
            "color_style": 1,
        },
        "render": {
            "viewport": [2, 1, 1],
            "engine": "cycles",
            #    "output": "figs/ch4_mod.png",
            "resolution": [500, 500],
            "samples": 10,
        },
        "species": {
            "C": {
                "color": [0.1, 0.1, 0.5, 0.1],
                "scale": 1.2,
                "material_style": "metallic",
            }
        },
        "bonds": {
            "setting": {
                ("C", "H"): {
                    "polyhedra": True,
                },
                ("C", "C"): {"polyhedra": True},
            }
        },
        "polyhedras": {
            "setting": {"C": {"color": [0.4, 0.2, 0.3, 0.4], "width": 0.03}}
        },
    },
    display=False,
)
#    post_modifications=modifications)
