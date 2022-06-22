"""Testing the logics of batoms_api.render 
"""
import pytest
import os
import pickle
from unittest.mock import patch
from pathlib import Path

def test_save_pickle():
    from batoms_api import render
    from ase.build import molecule

    # No intermediate file saved
    mol = molecule("CH4")
    render(mol, dryrun=True, save_input_file=False)
    assert not Path(".batoms.inp").is_file()

    # Intermediate file saved
    render(mol, dryrun=True, save_input_file=True)
    assert Path(".batoms.inp").is_file()

