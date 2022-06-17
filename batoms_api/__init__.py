import pickle
import os
from pathlib import Path

MODULE_ROOT = Path(__file__).parent.resolve()
SCHEMA_DIR = MODULE_ROOT / "api"


def render(
    atoms,
    batoms_input={},
    render_input={},
    settings={},
    post_modifications=[],
    display=False,
    queue=None,
):
    """
    atoms: an ASE atoms object
    batoms_input: input parameters to create the Batoms object
    render_input: input parameters to create the Render object
    post_modifications: list of commands to be evaluated following the given sequences
    """
    preferences = {
        "atoms": atoms,
        "batoms_input": batoms_input,
        "render_input": render_input,
        "settings": settings,
        "post_modifications": post_modifications,
    }
    with open(".batoms.inp", "wb") as f:
        pickle.dump(preferences, f, protocol=0)
        # pickle.dump([atoms, settings, post_modifications], f)
        # pickle.dump([atoms, batoms_input, render_input, settings, post_modifications], f)
    #
    blender_cmd = "blender"
    if "BLENDER_COMMAND" in os.environ.keys():
        blender_cmd = os.environ["BLENDER_COMMAND"]
    root = os.path.normpath(os.path.dirname(__file__))
    script = os.path.join(root, "script-api.py")
    if display:
        cmd = blender_cmd + " -P " + script
    elif queue == "SLURM":
        cmd = "srun -n $SLURM_NTASKS " + blender_cmd + " -b " + " -P " + script
    else:
        cmd = blender_cmd + " -b " + " -P " + script
    errcode = os.system(cmd)
    if errcode != 0:
        raise OSError("Command " + cmd + " failed with error code %d" % errcode)
