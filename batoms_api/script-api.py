from batoms.batoms import Batoms
import numpy as np
import pickle
blender_globals = globals().copy()


def run():
    """post_modifications are like `ase run --modify` parameters that are direct python expressions (use at your own risk!)
    format of post_modifications looks like follows:
        - batoms.<property>.<sub_property><[indices/keys]> = something
    each post-modification line is directly evaluated in sequence.
    """
    with open(".batoms.inp", "rb") as f:
        atoms, batoms_input, render_input, post_modifications = pickle.load(f)
        if "label" not in batoms_input:
            batoms_input["label"] = "batoms"
        batoms = Batoms(from_ase=atoms, **batoms_input)
        for mod in post_modifications:
            # TODO: sanity check of expression?
            blender_globals.update({"batoms": batoms, "np": np})
            exec(mod, blender_globals)
        batoms.get_image(**render_input)
        return
            


if __name__ == "__main__":
    run()
