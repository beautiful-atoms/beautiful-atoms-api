from ase.build import molecule
from batoms_api import render
from batoms import Batoms
import batoms_api

atoms = molecule("CH4")
atoms.cell = [3, 3, 3]
atoms.pbc = True
atoms = atoms * [2, 2, 2]

ba = Batoms(from_ase=atoms, label="ch4")
ba.model_style = 2
ba.render.viewport = [2, 1, 1]
ba.render.engine = "cycles"
ba.render.resolution = [500, 500]
ba.render.samples = 10

ba.bonds.setting[("C", "H")] = {"order": 2, "width": 0.2, "polyhedra": True}
ba.bonds.setting[("C", "C")] = {"order": 2, "width": 0.2, "polyhedra": True}
# ba.bonds.setting[("C", "H")] = {"polyhedra": True}
# ba.bonds.setting[("C", "C")] = {"polyhedra": True}
# ba.bonds.setting[("C", "H")].polyhedra = True
# ba.model_style = 2
ba.draw()
ba.get_image()
