import pytest

import saltext.mattermost.modules.mattermost as mattermost_module


@pytest.fixture
def configure_loader_modules():
    module_globals = {}
    return {
        mattermost_module: module_globals,
    }


def test_replace_this_this_with_something_meaningful():
    assert True
