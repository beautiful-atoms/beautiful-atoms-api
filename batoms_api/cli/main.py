#!/usr/bin/env python
from ase.io import read
from ase.build import molecule
from ase.io.cube import read_cube_data
import pickle
import sys
import argparse
import os


def save(batoms_input, render_input):
    with open(".batoms.inp", "wb") as f:
        pickle.dump([batoms_input, render_input], f)


commands = [
    ("info", "batoms.cli.info"),
    ("gui", "batoms.gui.ag"),
    ("render", "batoms.cli.run"),
]


def main(prog="batoms", description="Batoms command line tool.", commands=commands):
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument(
        "inputfile",
        type=str,
        default="",
        help="the input json file, includes coordinates of a \
                        set of points, threshold and a list of pairs of points ",
    )
    parser.add_argument("--display", action="store_true", default=True, help="render")
    parser.add_argument(
        "--run_render", "-r", action="store_true", default=False, help="render"
    )
    parser.add_argument(
        "--viewport", "-v", type=str, default="0,0,1", help="Camera viewport"
    )
    parser.add_argument(
        "--model_style", "-m", type=str, default="0", help="structure model"
    )
    parser.add_argument("--engine", "-e", type=str, default="eevee", help="Engine")
    parser.add_argument("--skip", "-sk", type=int, default=0, help="skip frame")
    parser.add_argument(
        "--level", "-iso", type=str, default="0.002", help="structure model"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="output",
        help="write output to specified file ",
    )
    parser.add_argument("--wrap", action="store_false", default=False, help="wrap")
    parser.add_argument(
        "--animation", "-a", action="store_false", default=True, help="wrap"
    )
    parser.add_argument("--light", action="store_false", default=False, help="light")
    args = parser.parse_args()
    #
    render_input = {}
    batoms_input = {}
    viewport = [float(x) for x in args.viewport.split(",")]
    render_input["output"] = args.output
    render_input["run_render"] = args.run_render
    render_input["engine"] = args.engine
    render_input["viewport"] = viewport
    batoms_input["inputfile"] = args.inputfile
    batoms_input["model_style"] = args.model_style
    batoms_input["wrap"] = args.wrap
    batoms_input["skip"] = args.skip
    if args.run_render:
        args.display = False
    save(batoms_input, render_input)
    print(render_input)
    # -----------
    root = os.path.normpath(os.path.dirname(__file__))
    script = os.path.join(root, "script-cli.py")
    #
    blender_cmd = "blender"
    if "BLENDER_COMMAND" in os.environ.keys():
        blender_cmd = os.environ["BLENDER_COMMAND"]
    if args.display:
        cmd = blender_cmd + " -P " + script
    else:
        cmd = blender_cmd + " -b " + " -P " + script
    errcode = os.system(cmd)


if __name__ == "__main__":
    main()
