### Beautiful Atoms

batoms_api is a API for Beautiful Atoms package. Beautiful Atoms is a Python package for editing and rendering atoms and molecules objects using blender. A Python interface that allows for automating workflows.

Features:

* Model: space-filling, ball-stick, polyhedral, cavity and so on.
* File type: cif, xyz, cube, pdb, json, VASP-out and so on.
* Volumetric data (Isosurface)
* Animation
* ``High quality rendering``:  3D models
* ``Free, Open Source``: Easy to download and install.
* ``Cross-platform``: (Linux, Windows, macOS)



### Author
* Xing Wang  <xingwang1991@gmail.com>

### How to use

On command line:

```bash
batoms h2o.xyz -m '1'
```


Use python script:

```python
from ase.build import molecule
from batoms_api import render

atoms = molecule('H2O')
# Windows
input = {'output': 'D:\\projects\\batoms\\figs\\h2o.png'}
# Linux
input = {'output': 'figs/h2o.png'}
render(atoms, render_input = input)
```

Please vist: https://beautiful-atoms.readthedocs.io/en/latest/
