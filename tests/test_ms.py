def test_ms():
    from ase.build import molecule
    from batoms_api import render

    atoms = molecule("C2H6SO")
    batoms_input = {
        "label": "c2h6so",
        "model_style": "1",
    }
    ms_input = {
        "setting": {
            "1": {"type": "SAS", "color": [1, 1, 0, 0.5]},
            "2": {"type": "SES", "color": [0, 0, 0.8, 0.5]},
        }
    }
    render_input = {
        "viewport": [0, 1, 0],
        "engine": "workbench",
        "output": "figs/c26so.png",
    }
    inputs = {
        "batoms": batoms_input,
        "ms": ms_input,
        "render": render_input,
    }
    render(atoms, inputs=inputs, display=False)


if __name__ == "__main__":
    test_ms()
    print("\n ms: All pass! \n")
