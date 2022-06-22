import pytest
from unittest.mock import patch
import bpy


@pytest.mark.filterwarnings("error:Input file api")
def test_version_check():
    from batoms_api import __version__
    from batoms_api.script_api import _check_version

    # Dumped version higher than current, raises Exception
    with pytest.raises(Exception):
        _check_version("10.0.0")
    # Dumped version lower than current, raises Warning
    with pytest.raises(UserWarning):
        _check_version("0.1.0")
    # same version
    _check_version(__version__)


def test_args_handler():
    import sys
    from batoms_api.script_api import _handle_argv_extras

    blender_args_base = [
        "blender",
        "-b",
        "--python-expr",
        "from batoms_api import script_api; script_api.run()",
    ]
    # No additional parameter provided, return None
    with patch.object(sys, "argv", blender_args_base):
        assert _handle_argv_extras() is None
    # Only add "--" without extra args
    with patch.object(sys, "argv", blender_args_base + ["--"]):
        with pytest.raises(ValueError):
            _handle_argv_extras()
    # More args than needed
    with patch.object(sys, "argv", blender_args_base + ["--", ".batoms.inp", "a", "b"]):
        with pytest.raises(ValueError):
            _handle_argv_extras()
    # Exactly one arg
    with patch.object(sys, "argv", blender_args_base + ["--", ".batoms.inp"]):
        filename = _handle_argv_extras()
        assert filename == ".batoms.inp"


def test_apply_batoms_settings():
    """This is not an exhaustive test for setting batoms but rather to test applying settins etc"""
    from batoms_api.script_api import apply_batoms_settings
    from batoms import Batoms
    from ase.build import molecule

    bpy.ops.batoms.delete()

    batoms = Batoms(label="ch4", from_ase=molecule("CH4"))

    # Test 1: test root level configs
    config = {"label": "ch4_mod", "location": [0, 0, 10], "model_style": 2}
    apply_batoms_settings(batoms, settings=config)
    assert batoms.label != "ch4_mod"
    assert batoms.location[-1] == 10
    assert all(batoms.model_style == 2)

    # Test 2: test direct property setting
    config = {"render": {"engine": "cycles", "viewport": [1, 1, 0]}}
    apply_batoms_settings(batoms, settings=config)
    # cycles changed to capital
    assert batoms.render.engine.lower() == "cycles"
    assert all([i == j for i, j in zip(batoms.render.viewport, [1, 1, 0])])
    config = {"render": {"engine": "cycles", "viewport": [1, 1, 0]}}
    apply_batoms_settings(batoms, settings=config)
    # cycles changed to capital
    assert batoms.render.engine.lower() == "cycles"
    assert all([i == j for i, j in zip(batoms.render.viewport, [1, 1, 0])])

    # Test 3: set properties that are indexed by keys
    config = {"species": {"C": {"color": [1.0, 1.0, 1.0, 1.0]}}}
    apply_batoms_settings(batoms, settings=config)
    # cycles changed to capital
    assert all([c == 1.0 for c in batoms.species["C"].color])

    # Test 4: set properties with tuple keys
    config = {"bonds": {"setting": {("C", "H"): {"polyhedra": True}}}}
    apply_batoms_settings(batoms, settings=config)
    # cycles changed to capital
    assert batoms.bonds.setting[("C", "H")].polyhedra is True

    # Test 4-1: raw string of tuple keys --> exception
    config = {"bonds": {"setting": {'("C", "H")': {"polyhedra": False}}}}
    with pytest.raises(Exception):
        apply_batoms_settings(batoms, settings=config)


def test_apply_batoms_modifications():
    """Test easy modifications"""
    from batoms_api.script_api import apply_batoms_modifications
    from batoms import Batoms
    from ase.build import molecule

    bpy.ops.batoms.delete()

    # Line-specific modifications
    batoms = Batoms(label="ch4", from_ase=molecule("CH4"))
    mods = ["batoms.render.resolution = [50, 50]", "batoms.render.engine = 'cycles'"]
    apply_batoms_modifications(batoms, mods)
    assert batoms.render.resolution[0] == 50
    assert batoms.render.resolution[1] == 50
    assert batoms.render.engine.lower() == "cycles"

    # Test numpy
    assert batoms.cell[0][0] == 0
    mods = ["batoms.cell = np.array([[10, 0, 0], [0, 10, 0], [0, 0, 10]])"]
    apply_batoms_modifications(batoms, mods)
    assert batoms.cell[0][0] == 10

    # Full name of numpy won't work
    mods = ["batoms.cell = numpy.array([[15, 0, 0], [0, 15, 0], [0, 0, 15]])"]
    with pytest.raises(Exception):
        apply_batoms_modifications(batoms, mods)

    # Quick test of for loop
    mods = [
        "for elem, sp in batoms.species.species.items():  sp.color = [0.1, 0.1, 0.1, 0.1]"
    ]
    apply_batoms_modifications(batoms, mods)
    assert batoms.species["C"].color[0] == pytest.approx(0.1, 1.0e-6)
    assert batoms.species["H"].color[0] == pytest.approx(0.1, 1.0e-6)