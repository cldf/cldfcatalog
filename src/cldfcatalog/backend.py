"""
Catalogs may be accessed via tags of a git repository or via versions related to a Zenodo
concept DOI. The `Backend` class defines the interface expected from these two implementations.
"""
import re
import typing

VERSION_PATTERN = re.compile(r'v(?P<major>[0-9]+)\.(?P<minor>[0-9]+)(\.(?P<patch>[0-9]+))?')


class Backend:
    def __init__(self, path, tag=None, **kw):
        self.tag = tag
        self.path = path

    def __enter__(self):
        """
        Switch to the appropriate version/tag of the catalog.
        """
        pass  # pragma: no cover

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # pragma: no cover

    @property
    def url(self):
        raise NotImplementedError()  # pragma: no cover

    @property
    def dir(self):
        return self.path  # pragma: no cover

    def describe(self):
        raise NotImplementedError()  # pragma: no cover

    @property
    def tags(self) -> typing.List[str]:
        raise NotImplementedError()  # pragma: no cover

    def update(self, tag=None, log=None):
        """
        Fetch new versions from remote.
        """
        raise NotImplementedError()  # pragma: no cover