import pytest

from cldfcatalog.config import *


def test_Config(tmpdir, appdirs):
    with Config.from_file() as cfg:
        with pytest.raises(ValueError):
            cfg.read(__file__)
        assert not cfg.clones
        with pytest.raises(KeyError):
            cfg.get_clone('k')
        cfg.add_clone('k', str(tmpdir))

    assert 'k' in Config.from_file().clones
