"""
Configfile support for discovering local clones of Catalogs.
"""
import typing
import pathlib
import collections
import configparser

import platformdirs

__all__ = ['Config']
CLONES = 'clones'


class Config(configparser.ConfigParser):
    """
    A config file for the cli, usable as context manager.
    """
    def __init__(self):
        self._files = None
        super().__init__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.to_file()

    def read(self, filenames, encoding=None):  # pylint: disable=C0116
        if self._files:
            raise ValueError('Config cannot read more than one file!')
        self._files = filenames
        super().read(filenames, encoding=encoding)

    @staticmethod
    def dir() -> pathlib.Path:  # pylint: disable=C0116
        res = pathlib.Path(platformdirs.user_config_dir('cldf'))
        if not res.exists():
            res.mkdir(parents=True, exist_ok=True)
        return res

    # Note: `fname` must not be defined at import, because we need to patch `appdirs` for tests!
    @staticmethod
    def fname() -> pathlib.Path:  # pylint: disable=C0116
        return Config.dir() / 'catalog.ini'

    @property
    def clones(self) -> configparser.SectionProxy:  # pylint: disable=C0116
        if CLONES not in self.sections():
            self[CLONES] = collections.OrderedDict()
        return self[CLONES]

    @classmethod
    def from_file(cls, fname=None) -> 'Config':  # pylint: disable=C0116
        cfg = cls()
        cfg.read(str(fname or cls.fname()))
        return cfg

    def to_file(self, fname=None):  # pylint: disable=C0116
        with (fname or self.fname()).open('w', encoding='utf8') as fp:
            self.write(fp)

    def add_clone(self, key: str, path: typing.Union[str, pathlib.Path]):  # pylint: disable=C0116
        self.clones[key] = str(pathlib.Path(path).resolve())

    def get_clone(self, key: str) -> pathlib.Path:  # pylint: disable=C0116
        try:
            return pathlib.Path(self.clones[key])
        except KeyError as e:
            raise KeyError(f'Config {self._files} has no entry for {key}') from e
