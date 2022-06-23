def test_isosurfaces():
    from ase.io.cube import read_cube_data
    from batoms_api import render

    volume, atoms = read_cube_data("../tests/datas/h2o-homo.cube")
    batoms_input = {
        "label": "h2o_cube",
        "model_style": "1",
        "volume": volume,
    }
    isosurfaces_input = {
        "setting": {
            "1": {"level": -0.001, "color": [1, 1, 0, 0.5]},
            "2": {"level": 0.001, "color": [0, 0, 0.8, 0.5]},
        }
    }
    render_input = {
        "viewport": [0, 1, 0],
        "engine": "workbench",
        "output": "figs/h2o_cube.png",
    }
    inputs = {
        "batoms": batoms_input,
        "isosurfaces": isosurfaces_input,
        "render": render_input,
    }
    render(atoms, inputs=inputs, display=False)


if __name__ == "__main__":
    test_isosurfaces()
    print("\n Isosurfaces: All pass! \n")
