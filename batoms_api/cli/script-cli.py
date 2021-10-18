from ase.io import read
from ase.io.cube import read_cube_data
from batoms.batoms import Batoms
from batoms.butils import removeAll
import pickle
import os

def main():
    removeAll()
    with open('.batoms.inp', 'rb') as f:
        batoms_input, render_input = pickle.load(f)
        inputfile = batoms_input['inputfile']
        base = os.path.basename(inputfile)
        base = os.path.splitext(base)
        label = base[0]
        label = label.replace('-', '_')
        ext = base[1]
        if ext == '.cube':
            volume, atoms = read_cube_data(inputfile)
            batoms = Batoms(label, atoms = atoms, volume=volume)
        else:
            atoms = read(inputfile, ':')
            batoms = Batoms(label = label, atoms = atoms)
    batoms.model_type = batoms_input['model_type']
    batoms.set_frames()
    batoms.render.run(direction = [0, 0, 1], output_image = render_input['output'], 
            run_render = render_input['run_render'])

if __name__ == "__main__":
    main()
