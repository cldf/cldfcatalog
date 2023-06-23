"""
A CLDF Reference catalog is typically available as data in a git repository, often with an
accompanying Python API to access the data.

This module provides functionality for accessing such catalogs, and in particular specified
versions of the catalog (repository).
"""
import sys
import typing
import pathlib
import contextlib
import collections

from pycldf import iter_datasets

from cldfcatalog.repository import Repository
from cldfcatalog.zenodo import Zenodo
from cldfcatalog.config import Config
from cldfcatalog.backend import VERSION_PATTERN

__all__ = ['Catalog']


class Catalog:
    """
    A `Catalog` is a versioned dataset, accessed

    - either via a git repository clone (optionally with a python API),
    - or via a set of locally downloaded CLDF datasets related to a Zenodo concept DOI.
    """
    # If the catalog has a Python API, __api__ should point to the API class, which accepts
    # a repository directory as sole positional argument for initialization:
    __api__ = None

    # Catalogs are often used in command line applications. Thus, they need to be refered to via
    # cli options or arguments. __cli_name__ can be used to specify a name for the catalog in these
    # scenarios, if the default - the lowercased class name - is not useful.
    __cli_name__ = None

    def __init__(self, path, tag=None, doi=None):
        """
        If `doi`:
        - path is a local directory containing zenodo deposits in version_tag subdirectories
        - if `tag` is None, return most recent version
        """
        #
        # FIXME: in case of Zenodo backend we need path **and** concept DOI!
        #
        if doi is None:
            # Repository backend!
            self.backend = Repository(path)
        else:
            self.backend = Zenodo(path, tag=tag, doi=doi)

        if isinstance(self.__api__, str):
            raise ValueError(
                'API for catalog {0} is not available, please install {1}!'.format(
                    self.__class__.__name__, self.__api__))

        self.tag = tag

        # Instantiating the API may be costly, thus, we cache it.
        self._api = None

    #-----------------------
    def update(self, tag=None, log=None):
        return self.backend.update(tag=tag, log=log)

    @property
    def dir(self) -> pathlib.Path:
        return self.backend.dir

    @property
    def url(self) -> typing.Optional[str]:
        return self.backend.url

    @property
    def tags(self) -> typing.List[str]:
        def version_tuple(s):
            m = VERSION_PATTERN.match(s)
            return (int(m.group('major')), int(m.group('minor')), int(m.group('patch') or 0))

        return sorted(
            [t for t in self.backend.tags if VERSION_PATTERN.fullmatch(t)],
            reverse=True,
            key=lambda n: version_tuple(n))

    def describe(self) -> str:
        return self.backend.describe()

    def json_ld(self, **dc) -> dict:
        res = collections.OrderedDict([
            ('rdf:about', self.url),
            ('rdf:type', 'prov:Entity'),
        ])
        res.update(self.backend.json_ld(**dc))
        if self.tag:
            res['dc:created'] = self.tag
        if isinstance(self.backend, Zenodo) and 'dc:title' in self.api.properties:
            res['dc:title'] = self.api.properties['dc:title']
        return res

    #-----------------------

    @classmethod
    def default_location(cls):
        return Config.dir().joinpath(cls.cli_name())

    @classmethod
    def clone(cls, url, target=None):
        #
        # FIXME: Detect backend from URL!
        #
        res = cls(Repository.clone(url, target or cls.default_location()).dir)
        with Config.from_file() as cfg:
            cfg.add_clone(res.cli_name(), res.dir)
        return res

    @classmethod
    def from_config(cls, key=None, fname=None, tag=None):
        cfg = Config.from_file(fname)
        return cls(cfg.get_clone(key or cls.cli_name()), tag=tag)

    def __enter__(self):
        with contextlib.ExitStack() as stack:
            #stack.enter_context(self.backend)
            self._stack = stack.pop_all()
        return self

    def __exit__(self, exc_type, exc, traceback):
        self._stack.__exit__(exc_type, exc, traceback)

    @classmethod
    def cli_name(cls):
        return cls.__cli_name__ or cls.__name__.lower()

    @property
    def api(self):
        if isinstance(self.backend, Zenodo) and not self.__api__:
            return next(iter_datasets(self.backend.dir))

        if self.__api__ and self._api is None:
            self._api = self.__api__(self.dir)
        return self._api

    @classmethod
    def api_version(cls):
        if cls.__api__:
            try:
                return sys.modules[cls.__api__.__module__.split('.')[0]].__version__
            except Exception:  # pragma: no cover
                pass

    def iter_versions(self):
        for tag in self.tags:
            if tag.startswith('v'):
                yield [tag, '']
