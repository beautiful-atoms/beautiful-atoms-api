import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="batoms_api",
    version="0.2.2",
    description="Drawing and rendering beautiful atoms, molecules using Blender.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/beautiful-atoms/beautiful-atoms-api",
    author="Xing Wang",
    author_email="xingwang1991@gmail.com",
    license="GPL",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages(),
    entry_points={"console_scripts": ["batoms=batoms_api.cli.main:main"]},
    install_requires=["ase", "ruamel.yaml", "mergedeep==1.3.4"],
    package_data={"": ["api/*.yaml", "api/*.yml"]},
    # include_package_data=True,
    # package_data={"batoms_api.api": ["*.yaml", "*.yml"]},
    python_requires=">=3.7",
)
