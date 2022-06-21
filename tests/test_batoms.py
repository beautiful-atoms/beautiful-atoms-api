
def test_batoms():
    from ase.build import molecule
    from batoms_api import render
    atoms = molecule('CH4')
    batoms_input = {
        'label': 'ch4', 
        'model_style': '1',
    }
    species_input = {
        'C':{'color': [0.0, 0.8, 0.0, 1.0]},
        'H':{'color': [0.1, 0.1, 0.1, 1.0]}
    }
    render_input = {
        'viewport': [1, 1, 0],
        'engine': 'eevee',
        'output': 'figs/ch4.png',
        }
    inputs = {
        "batoms": batoms_input,
        "species": species_input,
        "render": render_input,
    }
    render(atoms,inputs = inputs, display = False)

if __name__ == "__main__":
    test_batoms()
    print("\n Batoms: All pass! \n")

