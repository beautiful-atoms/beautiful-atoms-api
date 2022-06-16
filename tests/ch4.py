from ase.build import molecule
from batoms_api import render

atoms = molecule("CH4")
atoms.cell = [3, 3, 3]
atoms.pbc = True
atoms = atoms * [2, 2, 2]
batoms_input = {
    "label": "nh3",
    "model_style": "1",
    # 'species_props': {'H':{'color': [0.0, 0.8, 0.0, 1.0]},
    #   'C':{'color': [0.1, 0.1, 0.1, 1.0]}},
    # 'bondsetting': {'C-H': [0, 2.0, 1, True]},
    # 'polyhedrasetting': {'C':[[0.6, 0.0, 0.4, 0.3], 0.01]},
}
render_input = {
    "viewport": [1, 1, 0],
    "engine": "cycles",
    "output": "figs/ch4.png",
}
render(atoms, batoms_input=batoms_input, render_input=render_input, display=False)
