

def test_bonds():
    from ase.build import molecule
    from batoms_api import render
    atoms = molecule('CH4')
    batoms_input = {
        'label': 'ch4', 
        'model_style': '1',
    }
    bonds_input = {
    "setting":{
        ('C', 'H'): {'style': '3'}
        }
    }
    render_input = {
        'viewport': [1, 1, 0],
        'engine': 'eevee',
        'output': 'figs/ch4.png',
        }
    inputs = {
        "batoms": batoms_input,
        'bonds': bonds_input,
        "render": render_input,
    }
    render(atoms,inputs = inputs, display = False)

def test_hydrogen_bond():
    from ase.build import molecule
    from batoms_api import render
    atoms = molecule('CH3OH')
    batoms_input = {
        'label': 'ch3oh', 
        'model_style': '1',
    }
    bonds_input = {
    "show_hydrogen_bond":True
    }
    render_input = {
        'viewport': [1, 1, 0],
        'engine': 'eevee',
        'output': 'figs/ch3oh.png',
        }
    inputs = {
        "batoms": batoms_input,
        'bonds': bonds_input,
        "render": render_input,
    }
    render(atoms,inputs = inputs, display = False)

if __name__ == "__main__":
    test_bonds()
    test_hydrogen_bond()
    print("\n Bonds: All pass! \n")

