"""
A CLDF Reference catalog is typically available as data in a git repository, often with an
accompanying Python API to access the data.

This module provides functionality for accessing such catalogs, and in particular specified
versions of the catalog (repository).
"""
from cldfcatalog.repository import Repository

__all__ = ['Catalog']


class Catalog(Repository):
    """
    A `Catalog` is a git repository clone (optionally with a python API to access it).
    """
    # If the catalog has a Python API, __api__ should point to the API class, which accepts
    # a repository directory as sole positional argument for initialization:
    __api__ = None

    # Catalogs are often used in command line applications. Thus, they need to refered to via
    # cli options or arguments. __cli_name__ can be used to specify a name for the catalog in these
    # scenarios, if the default - the lowercased class name - is not useful.
    __cli_name__ = None

    def __init__(self, path, tag=None):
        if isinstance(self.__api__, str):
            raise ValueError(
                'API for catalog {0} is not available, please install {1}!'.format(
                    self.__class__.__name__, self.__api__))
        super().__init__(path)
        self._prev_head = None  # We want to restore the previous state upon exiting.
        self.tag = tag

        # Instantiating the API may be costly, thus, we cache it.
        self._api = None

    def __enter__(self):
        if self.tag:
            # Try to store the current state of the repository ...
            try:
                self._prev_head = self.repo.active_branch.name
            except TypeError:
                try:
                    self._prev_head = self.repo.git.describe('--tags')
                except Exception:  # pragma: no cover
                    pass
            # ... then checkout the requested state:
            self.checkout(self.tag)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._prev_head:
            self.checkout(self._prev_head)
            self._prev_head = None

    @classmethod
    def cli_name(cls):
        return cls.__cli_name__ or cls.__name__.lower()

    @property
    def api(self):
        if self.__api__ and self._api is None:
            self._api = self.__api__(self.dir)
        return self._api
