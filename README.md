# cldfcatalog

Utilities to use `git` repository clones and reference catalogs.

[![Build Status](https://travis-ci.org/cldf/cldfcatalog.svg?branch=master)](https://travis-ci.org/cldf/cldfcatalog)
[![codecov](https://codecov.io/gh/cldf/cldfcatalog/branch/master/graph/badge.svg)](https://codecov.io/gh/cldf/cldfcatalog)
[![PyPI](https://img.shields.io/pypi/v/cldfcatalog.svg)](https://pypi.org/project/cldfcatalog)

Research data - and in particular CLDF data - is often curated using `git` repositories
for version control. [`cldfcatalog.Repository`](src/cldfcatalog/repository.py) 
provides a wrapper around GitPython's `git.Repo` class, exposing relevant functionality 
in this context.

A particularly important piece of data for CLDF are reference catalogs, which are
consulted during CLDF data creation. Again, such catalogs are often available as
`git` repositories hosted on GitHub, such as 
[Glottolog](https://github.com/glottolog/glottolog) or
[Concepticon](https://github.com/concepticon/concepticon-data).

The typical usage scenario for these catalogs is as follows: 
- To follow upstream development of the catalogs, a user has a local clone of the
  repository, which is periodically synched running `git pull origin`.
- When creating a CLDF dataset, a particular released version of a catalog is consulted.

Thus, we want to 
- checkout a particular version of the catalog,
- run the CLDF creation,
- restore the previous state of the repository clone.

This is exactly the functionality of [`cldfcatalog.Catalog`](src/cldfcatalog/catalog.py):
```python
>>> from cldfcatalog import Catalog
>>> glottolog = Catalog('../../glottolog/glottolog', 'v4.0')
>>> glottolog.active_branch
'master'
>>> with glottolog:
...     print(glottolog.describe())
...     
v4.0
>>> glottolog.describe()
'v4.0-52-ga4cfc90'
```
