import pytest
from unittest.mock import patch


@pytest.mark.filterwarnings("error:Input file api")
def test_version_check():
    from batoms_api import __version__
    from batoms_api.script_api import _check_version

    # Dumped version higher than current, raises Exception
    with pytest.raises(Exception):
        _check_version("10.0.0")
    # Dumped version lower than current, raises Warning
    with pytest.raises(UserWarning):
        _check_version("0.1.0")
    # same version
    _check_version(__version__)

def test_args_handler():
    import sys
    from batoms_api.script_api import _handle_argv_extras
    blender_args_base = ["blender", "-b", "--python-expr", "from batoms_api import script_api; script_api.run()",]
    # No additional parameter provided, return None
    with patch.object(sys, "argv", blender_args_base):
        assert _handle_argv_extras() is None
    # Only add "--" without extra args
    with patch.object(sys, "argv", blender_args_base + ["--"]):
        with pytest.raises(ValueError):
            _handle_argv_extras()
    # More args than needed
    with patch.object(sys, "argv", blender_args_base + ["--", ".batoms.inp", "a", "b"]):
        with pytest.raises(ValueError):
            _handle_argv_extras()
    # Exactly one arg
    with patch.object(sys, "argv", blender_args_base + ["--", ".batoms.inp"]):
        filename = _handle_argv_extras()
        assert filename == ".batoms.inp"
    
        
    
