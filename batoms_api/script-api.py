from batoms.batoms import Batoms
import pickle
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def run():
    with open('.batoms.inp', 'rb') as f:
        atoms, inputs = pickle.load(f)
        if 'label' not in inputs['batoms']:
            inputs['batoms']['label'] = 'batoms'
        logger.debug("Label: {}".format(inputs['batoms']['label']))
        batoms = Batoms(label = inputs['batoms'].pop('label'), from_ase = atoms)
        for key, value in  inputs['batoms'].items():
                setattr(batoms, key, value)
                logger.debug("Set batoms: {}".format(key))
        if "species" in inputs:
            for sp, atts in inputs['species'].items():
                for key, value in atts.items():
                    setattr(batoms.species[sp], key, value)
                logger.debug("Set species: {}".format(sp))
        if "cell" in inputs:
            batoms.cell.draw()
        if "bonds" in inputs:
            if "setting" in inputs['bonds']:
                setting = inputs['bonds'].pop('setting')
                for key, value in setting.items():
                    batoms.bonds.setting[key] = value
                    logger.debug("Set bond pair: {}".format(key))
            for key, value in inputs['bonds'].items():
                logger.debug("Set bonds: {}".format(key))
                setattr(batoms.bonds, key, value)
            batoms.draw()
        if "polyhedras" in inputs:
            if "setting" in inputs['polyhedras']:
                for key, value in inputs['polyhedras']['setting'].items():
                    batoms.polyhedras.setting[key] = value
                    logger.debug("Set polyhedra: {}".format(key))
            batoms.draw()
        if "isosurfaces" in inputs:
            if "setting" in inputs['isosurfaces']:
                for key, value in inputs['isosurfaces']['setting'].items():
                    batoms.isosurfaces.setting[key] = value
                    logger.debug("Set isosurfaces: {}".format(key))
            batoms.isosurfaces.draw()
        if "ms" in inputs:
            if "setting" in inputs['ms']:
                for key, value in inputs['ms']['setting'].items():
                    batoms.ms.setting[key] = value
                    logger.debug("Set ms: {}".format(key))
            batoms.ms.draw()
        
        batoms.get_image(**inputs['render'])

if __name__ == "__main__":
    run()
