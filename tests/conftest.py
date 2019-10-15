import git
import pytest


@pytest.fixture
def tmprepo(tmpdir):
    """
    Turns `tmpdir` into a git repository.
    """
    repo = git.Repo.init(str(tmpdir.join('repo')))
    fname = tmpdir.join('repo', 'README.md')
    fname.write_text('abc', encoding='utf-8')
    repo.index.add([str(fname)])
    repo.index.commit("initial commit")
    repo.git.checkout('master')
    repo.create_tag('v1.0')
    repo.git.branch('other')
    repo.create_remote('origin', url='https://github.com/org/repo.git')
    return repo.working_dir
