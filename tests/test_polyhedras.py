

def test_polyhedras():
    from ase.io import read
    from batoms_api import render
    atoms = read('../tests/datas/tio2.cif')
    batoms_input = {
        'label': 'tio2', 
        'model_style': '2',
    }
    bonds_input = {
    "show_search": True,
    }
    polyhedras_input = {
    "setting":{
        'Ti': {'color': [1, 0, 1, 0.5]}
        }
    }
    render_input = {
        'viewport': [1, 0, 0],
        'engine': 'eevee',
        'output': 'figs/tio2.png',
        }
    inputs = {
        "batoms": batoms_input,
        'bonds': bonds_input,
        'polyhedras': polyhedras_input,
        "render": render_input,
    }
    render(atoms,inputs = inputs, display = False)


if __name__ == "__main__":
    test_polyhedras()
    print("\n polyhedras: All pass! \n")

