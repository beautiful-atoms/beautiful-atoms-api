def test_cell():
    from ase.io import read
    from batoms_api import render

    atoms = read("../tests/datas/tio2.cif")
    batoms_input = {
        "label": "tio2",
        "model_style": "2",
    }
    cell_input = {}
    bonds_input = {
        "show_search": True,
    }
    polyhedras_input = {"setting": {"Ti": {"color": [0, 0.5, 0.5, 0.5]}}}
    render_input = {
        "viewport": [1, 0, 0],
        "engine": "eevee",
        "output": "figs/cell_tio2.png",
    }
    inputs = {
        "batoms": batoms_input,
        "cell": cell_input,
        "bonds": bonds_input,
        "polyhedras": polyhedras_input,
        "render": render_input,
    }
    render(atoms, inputs=inputs, display=False)


if __name__ == "__main__":
    test_cell()
    print("\n cell: All pass! \n")
