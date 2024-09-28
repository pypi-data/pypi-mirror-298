import pytest

from python_plugins.utils.remove_pycache import remove_pycache

@pytest.mark.skip
def test_remove_pycache():
    remove_pycache("./tests")

