import pathlib
import shutil

import pytest


@pytest.fixture
def tmprepo(tmpdir):
    """
    Turns `tmpdir` into a git repository.
    """
    from cldfcatalog.repository import get_test_repo

    repo = get_test_repo(
        str(tmpdir), remote_url='https://github.com/org/repo.git', tags=['v1.0'], branches=['other'])
    return repo


@pytest.fixture
def Git(tmpdir, mocker):
    from cldfcatalog.repository import get_test_repo

    class Git(object):
        def __init__(self, d):
            self.d = d

        def clone(self, url, target):
            get_test_repo(str(tmpdir), remote_url=url)
            shutil.copytree(str(tmpdir.join('repo')), str(pathlib.Path(self.d) / target))

    mocker.patch('cldfcatalog.repository.git.Git', Git)
    return


@pytest.fixture
def appdirs(tmpdir, mocker):
    mocker.patch(
        'cldfcatalog.config.platformdirs',
        mocker.Mock(user_config_dir=mocker.Mock(return_value=str(tmpdir.join('u')))))
    return str(tmpdir.join('u'))
