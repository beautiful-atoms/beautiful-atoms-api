from ase.io import read
from ase.io.cube import read_cube_data
from batoms.batoms import Batoms
from batoms.butils import removeAll
import pickle
import os


def main():
    removeAll()
    with open(".batoms.inp", "rb") as f:
        batoms_input, render_input = pickle.load(f)
        inputfile = batoms_input["inputfile"]
        base = os.path.basename(inputfile)
        base = os.path.splitext(base)
        label = base[0]
        label = label.replace("-", "_")
        label = label.replace(".", "")
        if label[:1].isdigit():
            label = "b_" + label
        ext = base[1]
        if ext == ".cube":
            cube = read(
                inputfile,
                index="::%s" % (batoms_input["skip"] + 1),
                format="cube",
                read_data=True,
                full_output=True,
            )
            volume = cube["data"]
            atoms = cube["atoms"]
            origin = cube["origin"]
            atoms.translate(-origin[0:3])
        else:
            atoms = read(inputfile, index="::%s" % (batoms_input["skip"] + 1))
            volume = None
    if batoms_input["wrap"]:
        if isinstance(atoms, list):
            for i in range(len(atoms)):
                atoms[i].wrap()
        else:
            atoms.wrap()
    batoms = Batoms(label, from_ase=atoms, volume=volume)
    batoms.model_style = batoms_input["model_style"]
    batoms.set_frames()
    batoms.render.init()
    batoms.render.engine = render_input["engine"]
    if render_input["run_render"]:
        batoms.get_image(
            viewport=render_input["viewport"], output=render_input["output"]
        )


if __name__ == "__main__":
    main()
