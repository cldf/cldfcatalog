import typing

from cldfzenodo import search, Record
from cldfzenodo.record import ZENODO_DOI_PATTERN
from clldutils.misc import lazyproperty

from cldfcatalog.backend import Backend, VERSION_PATTERN


class Zenodo(Backend):
    def __init__(self, path, tag=None, doi=None, **kw):
        super().__init__(path, tag)
        assert doi
        self.doi = doi
        if tag and tag not in self.tags:
            #
            # FIXME: Maybe interactively offer downloading?
            #
            raise ValueError(tag)

    @property
    def url(self):
        return 'https://doi.org/{}'.format(self.doi)

    @property
    def dir(self):
        return self.path / (self.tag or self.tags[0])

    @lazyproperty
    def tags(self) -> typing.List[str]:
        return [d.name for d in self.path.iterdir() if VERSION_PATTERN.fullmatch(d.name)]

    def _tags(self):
        return [rec.version_tag for rec in search.Results.from_params(
            q='conceptrecid:"{}"'.format(ZENODO_DOI_PATTERN.search(self.doi).group('recid')),
            sort='-version',
            all_versions=True
        ) if rec.version_tag]

    def update(self, tag=None, log=None):
        for t in self._tags():
            if tag is None or (tag == t):
                out = self.path / t
                if not out.exists():
                    Record.from_concept_doi(self.doi, t).download(out, log=log)

    def json_ld(self, **dc) -> dict:
        """
        A description in JSON-LD - suitable for inclusion in CLDF metadata.
        """
        return {'dc:{0}'.format(k.replace('dc:', '')): v for k, v in sorted(dc.items())}
