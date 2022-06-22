"""Testing the logics of batoms_api.render 
"""
from tempfile import tempdir
import pytest
import os
import pickle
from unittest.mock import patch
from pathlib import Path


def test_save_pickle():
    from batoms_api import render
    from ase.build import molecule
    import tempfile

    # No intermediate file saved
    mol = molecule("CH4")
    render(mol, dryrun=True, save_input_file=False)
    assert not Path(".batoms.inp").is_file()

    # Intermediate file saved
    render(mol, dryrun=True, save_input_file=True)
    assert Path(".batoms.inp").is_file()
    os.system("rm -rf .batoms.inp")

    # Save different file name
    fn = ".ch4.inp"
    render(mol, dryrun=True, save_input_file=fn)
    assert Path(fn).is_file()
    os.system(f"rm -rf {fn}")

    # Use tempdir
    with tempfile.TemporaryDirectory() as tmpdir:
        fn = Path(tempdir) / ".ch4.inp"
        render(mol, dryrun=True, save_input_file=fn)
        assert fn.is_file()


def test_pickle_content():
    from batoms_api import render
    from ase.build import molecule
    import tempfile

    mol = molecule("CH4")

    with tempfile.TemporaryDirectory() as tmpdir:
        fn = Path(tempdir) / ".ch4.inp"
        render(mol, dryrun=True, save_input_file=fn)
        assert fn.is_file()
        config = pickle.load(open(fn, "rb"))
        for key in [
            "atoms",
            "volume",
            "batoms_input",
            "render_input",
            "settings",
            "post_modifications",
            "api_version",
            "save_blender_file",
        ]:
            assert key in config.keys()
