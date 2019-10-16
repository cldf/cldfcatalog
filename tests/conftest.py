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

