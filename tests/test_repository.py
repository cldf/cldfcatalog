import pytest

from cldfcatalog.repository import *


def test_invalid_repo(tmpdir):
    with pytest.raises(ValueError):
        Repository(str(tmpdir))


def test_Repository(tmprepo):
    repository = Repository(tmprepo)
    assert repository.url == 'https://github.com/org/repo'
    ld = repository.json_ld(author='The Author')
    assert 'dc:author' in ld
    assert repository.github_repo == 'org/repo'
