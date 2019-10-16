import pytest

from cldfcatalog.catalog import *


@pytest.fixture
def catalog(tmprepo):
    return Catalog(tmprepo.working_dir, 'other')


def test_init_noapi():
    class Cat(Catalog):
        __api__ = 'nope'

    with pytest.raises(ValueError):
        _ = Cat('')


def test_init_api(mocker):
    api = mocker.Mock

    class Cat(Catalog):
        __api__ = api
        __cli_name__ = 'abc'

    _ = Cat('').api
    assert api.called
    assert Cat('').cli_name() == 'abc'


def test_init_norepos(tmpdir):
    with pytest.raises(ValueError):
        _ = Catalog(str(tmpdir))


def test_context_manager(catalog):
    with catalog as cat:
        assert cat.describe()
        assert len(cat.tags) == 1
        assert cat.dir
        assert cat.active_branch == 'other'
    assert cat.active_branch == 'master'


def test_context_manager_no_branch(tmprepo):
    from cldfcatalog.repository import Repository

    r = Repository(tmprepo.working_dir)
    r.checkout('v1.0')
    with Catalog(tmprepo.working_dir, 'master') as cat:
        assert cat.active_branch == 'master'
    assert cat.active_branch is None
    assert cat.describe() == 'v1.0'
