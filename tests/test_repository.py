import pytest

from cldfcatalog.repository import *


def test_invalid_repo(tmpdir):
    with pytest.raises(ValueError):
        Repository(str(tmpdir / 'no'))

    with pytest.raises(ValueError):
        Repository(str(tmpdir))

    repo = Repository(str(tmpdir), not_git_repo_ok=True)
    assert repo.url is None
    with pytest.raises(ValueError):
        repo.update()


def test_Repository(tmprepo):
    repository = Repository(tmprepo.working_dir)
    assert repository.url == 'https://github.com/org/repo'
    ld = repository.json_ld(author='The Author', **{'dc:format': 'CLDF'})
    assert 'dc:author' in ld
    assert 'dc:format' in ld
    assert 'dc:title' in ld
    assert repository.github_repo == 'org/repo'
    assert not repository.is_dirty()

    repository.dir.joinpath('README.md').write_text('other', encoding='utf-8')
    assert repository.is_dirty()
    tmprepo.index.commit("commit")
    assert len(repository.hash()) == 7


def test_Repository_url(tmp_path):
    repository = Repository(
        get_test_repo(tmp_path / 'repo', remote_url='http://user:pwd@example.com').working_dir)
    assert repository.url == 'http://example.com'


def test_clone(tmpdir, Git):
    assert Repository.clone('http://example.org', str(tmpdir.join('xy'))).dir.name == 'xy'
