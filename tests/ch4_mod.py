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
render(atoms, 
       batoms_input={
           "label": "ch4_mod"
       },
       render_input={
       },
    #    render_input=render_input, 
       settings={
           "batoms":{
            #    "label": "ch4",
               "model_style": 2,
           },
           "render":{
               "viewport": [2, 1, 1],
               "engine": "cycles",
            #    "output": "figs/ch4_mod.png",
               "resolution": [500, 500],
               "samples": 10,
           },
           "bonds": {
               "setting":
               {("C", "H"): {"order": 2, "width": 0.2, "polyhedra": True},
               ("C", "C"): {"order": 2, "width": 0.2, "polyhedra": True}
               }
           },
           "polyhedras":
           {
               "draw": {}
           }
       },
       display=False, 
)
    #    post_modifications=modifications)
