import pytest

from cldfcatalog.repository import *


def test_invalid_repo(tmpdir):
    with pytest.raises(ValueError):
        Repository(str(tmpdir))


def test_Repository(tmprepo):
    repository = Repository(tmprepo.working_dir)
    assert repository.url == 'https://github.com/org/repo'
    ld = repository.json_ld(author='The Author')
    assert 'dc:author' in ld
    assert repository.github_repo == 'org/repo'
    assert not repository.is_dirty()

    repository.dir.joinpath('README.md').write_text('other', encoding='utf-8')
    assert repository.is_dirty()
    tmprepo.index.commit("commit")
    assert len(repository.hash()) == 7

