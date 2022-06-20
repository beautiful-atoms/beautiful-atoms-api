from batoms import Batoms
import numpy as np
import pickle

blender_globals = globals().copy()


def type_convert(inheritance, value):
    """Use the proper value conversion"""
    # In the beginning no value conversion
    return value


def run():
    """post_modifications are like `ase run --modify` parameters that are direct python expressions (use at your own risk!)
    format of post_modifications looks like follows:
        - batoms.<property>.<sub_property><[indices/keys]> = something
    each post-modification line is directly evaluated in sequence.
    """
    with open(".batoms.inp", "rb") as f:
        # atoms, batoms_input, render_input, settings, post_modifications = pickle.load(f)
        # atoms, settings, post_modifications = pickle.load(f)
        preferences = pickle.load(f)
        atoms = preferences["atoms"]
        batoms_input = preferences.get("batoms_input", {})
        batoms = Batoms(from_ase=atoms, **batoms_input)
        # Handle the setting parts, may be a little tricky
        # There are two types of parameters:
        # 1. batoms itself, direct intialization
        # 2. initializable objects: render, boundary. invoke as batoms.<obj> = ObjClass(param=param)
        # 3. requiring special treatment: species. Has "update" section
        # 4. objects need setting: polyhedras, bonds, lattice_plane, crystal_shape, isosurfaces, cavity, ms, magres etc
        #    an ObjectSetting instance needs to be updated. Usage batoms.<obj>.setting[key] = setting_dict
        # YAML parser need to distinguish between the levels that are used
        # TODO: add global lighting / plane setting
        # TODO: add file io settings
        settings = preferences.get("settings", {})
        for prop_name, prop_setting in settings.items():
            # TODO prototype API check
            print(prop_name, prop_setting)
            if prop_name == "batoms":
                prop_obj = batoms
                # do not change label after creation
                prop_setting.pop("label", None)
                for key, value in prop_setting.items():
                    print(key, value, type(value))
                    setattr(prop_obj, key, value)
                print(prop_obj)
                # setattr(prop_obj, key, type_convert({}, value))
            elif prop_name in ["render", "boundary"]:
                prop_obj = getattr(batoms, prop_name)
                for key, value in prop_setting.items():
                    setattr(prop_obj, key, type_convert({}, value))
            else:
                # TODO: check if prop_name is valid
                prop_obj = getattr(batoms, prop_name)
                draw_params = {}
                for sub_prop_name, sub_prop_setting in prop_setting.items():
                    if sub_prop_name == "setting":
                        sub_prop_obj = prop_obj.setting
                        # sub_prop_setting is by default a dict
                        for key, value in sub_prop_setting.items():
                            sub_prop_obj[key] = value
                    elif sub_prop_name == "draw":
                        if sub_prop_setting is not False:
                            draw_params = sub_prop_setting
                        else:
                            draw_params = False
                    else:
                        raise ValueError(f"Unknown sub_prop_setting {sub_prop_setting}")
                if draw_params is not False:
                    if hasattr(prop_obj, "draw"):
                        prop_obj.draw(**draw_params)
                    else:
                        batoms.draw()
                print(prop_obj)

        # for prop_name, setting in settings.items():
        #     # TODO: catch AttributeError
        #     prop_obj = getattr(batoms, prop_name)
        #     for key, value in setting.items():
        #         val_string = f"_obj.{key}"
        #         handle = eval(val_string, {}, {"_obj": prop_obj})
        #         handle = value
        post_modifications = preferences.get("post_modifications", [])
        for mod in post_modifications:
            # TODO: sanity check of expression?
            blender_globals.update({"batoms": batoms, "np": np})
            exec(mod, blender_globals)
        render_input = preferences.get("render_input", {})
        # Force run self
        print(batoms.bonds)
        print(batoms.bonds.setting)
        batoms.draw()

        # batoms.render.run(batoms)
        batoms.get_image(**render_input)
        return


if __name__ == "__main__":
    run()
