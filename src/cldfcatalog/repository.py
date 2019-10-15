"""
This module provides a thin wrapper around `git.Repo`, exposing only a small portion of its
functionality, following the [Facade pattern](https://en.wikipedia.org/wiki/Facade_pattern).
"""
import re
import pathlib
import collections

import git
import git.exc

__all__ = ['Repository']


class Repository:
    """
    A (clone of a) git repository.
    """
    def __init__(self, path):
        try:
            self.repo = git.Repo(str(path))
        except (git.exc.NoSuchPathError, git.exc.InvalidGitRepositoryError):
            raise ValueError('invalid git repository: {0}'.format(path))
        self._url = None

    @property
    def dir(self):
        """
        :return: The path of the repository clone as `pathlib.Path`.
        """
        return pathlib.Path(self.repo.working_dir)

    @property
    def active_branch(self):
        """
        :return: Name of the active branch or `None`, if in "detached HEAD" state.
        """
        try:
            return self.repo.active_branch.name
        except TypeError:
            return None

    @property
    def url(self):
        """
        :return: The URL of the remote called `origin` - if it is set, else `None`.

        Note: Since computing the remote may require a `git` call, and we assume the origin will
        not change, we cache the result.
        """
        if self._url is None:
            try:
                url = self.repo.remotes.origin.url
                if url.endswith('.git'):
                    url = url[:-4]
                self._url = url
            except AttributeError:  # pragma: no cover
                pass
        return self._url

    @property
    def github_repo(self):
        """
        :return: GitHub repository name in the form "ORG/REPO", or `None`, if no matching \
        `self.url` is found.
        """
        match = re.search('github\.com/(?P<org>[^/]+)/(?P<repo>[^.]+)', self.url or '')
        if match:
            return match.group('org') + '/' + match.group('repo')

    @property
    def tags(self):
        """
        :return: `list` of tags available for the repository. A tag can be used as `spec` argument \
        for `Repository.checkout`
        """
        return self.repo.git.tag().split()

    def describe(self):
        return self.repo.git.describe('--always', '--tags')

    def checkout(self, spec):
        return self.repo.git.checkout(spec)

    def json_ld(self, **dc):
        """
        A repository description in JSON-LD - suitable for inclusion in CLDF metadata.
        """
        res = collections.OrderedDict([
            ('rdf:type', 'prov:Entity'),
            ('dc:title', self.__class__.__name__),
        ])
        if self.url:
            res['rdf:about'] = self.url
        res['dc:created'] = self.describe()
        res.update({'dc:{0}'.format(k): dc[k] for k in sorted(dc)})
        return res
