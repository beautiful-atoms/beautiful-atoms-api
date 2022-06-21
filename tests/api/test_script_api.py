import pytest


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
