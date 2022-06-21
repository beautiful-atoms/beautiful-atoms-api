import pickle
import os
import sys
from tempfile import gettempdir
from pathlib import Path
import logging

from .metadata import __version__
from .batoms_api import render

logger = logging.getLogger(__name__)

formatter = "%(levelname)s " "[%(name)s %(funcName)s]: %(message)s"
logging.basicConfig(stream=sys.stdout, format=formatter, level=logging.DEBUG)
# add logger file
filepath = Path(gettempdir()) / ("beautiful_atoms_api.log")
logger.info("Log file: " + str(filepath))
file_handler = logging.FileHandler(filepath, mode="w")
file_handler.setFormatter(logging.Formatter(formatter))
logger.addHandler(file_handler)
logger.info("Python version: {} ".format(sys.version))

# def render(atoms, inputs = {}, display = False, queue = None, ):
#     with open('.batoms.inp', 'wb') as f:
#         pickle.dump([atoms, inputs], f)
#     #
#     blender_cmd = 'blender'
#     if 'BLENDER_COMMAND' in os.environ.keys():
#         blender_cmd = os.environ['BLENDER_COMMAND']
#     root = os.path.normpath(os.path.dirname(__file__))
#     script = os.path.join(root, 'script-api.py')
#     if display:
#         cmd = blender_cmd + ' -P ' + script
#     elif queue == 'SLURM':
#         cmd = 'srun -n $SLURM_NTASKS ' +  blender_cmd + ' -b ' + ' -P ' + script
#     else:
#         cmd = blender_cmd + ' -b ' + ' -P ' + script
#     errcode = os.system(cmd)
#     if errcode != 0:
#         raise OSError('Command ' + cmd +
#                       ' failed with error code %d' % errcode)
