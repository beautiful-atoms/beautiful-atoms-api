import pickle
import os
from pathlib import Path
from importlib.metadata import version

MODULE_ROOT = Path(__file__).parent.resolve()
SCHEMA_DIR = MODULE_ROOT / "api"
# Python >= 3.8 metadata retrieval for dumping version with the input file
THIS_MODULE_NAME = MODULE_ROOT.name
__version__ = version(THIS_MODULE_NAME)

# import from submodules must be placed after the dir-related lines
from .batoms_api import render
