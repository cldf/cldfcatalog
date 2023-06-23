import pathlib

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


def test_api_version():
    class Cat(Catalog):
        __api__ = Catalog
        __cli_name__ = 'abc'

    assert Cat.api_version()


def test_init_norepos(tmpdir):
    pass


def test_context_manager(catalog):
    with catalog as cat:
        assert cat.describe()
        assert len(cat.tags) == 1
        assert cat.dir


def test_iter_versions(tmprepo):
    cat = Catalog(tmprepo.working_dir)
    assert len(list(cat.iter_versions())) == 1


def test_clone(appdirs, Git):
    class MyCat(Catalog):
        pass
    MyCat.clone('http://example.org')
    # The default name of a Catalog is the lowercase class name:
    assert pathlib.Path(appdirs).joinpath('mycat').exists()
    assert MyCat.from_config().dir == pathlib.Path(appdirs).joinpath('mycat')

#
# test catalog from DOI with python API!
#