# -*- coding: utf-8 -*-
"""All page copy for Ensō Foot Clinic, in one dictionary.

Keys are page slugs; each value carries `h1`, `title`, `description`, `date`
and `html`. Internal links inside `html` use the `@/` sentinel, which build.py
rewrites to the right relative path for each page's depth.

Named `pagecopy` rather than `copy` so it never shadows the standard library.

Split across modules purely so each file stays readable:
  copy_services.py   · the four services
  copy_pages.py      · «Ποιοι είμαστε», practitioner, legal
  copy_articles.py   · the nine articles
  copy_seminars.py   · the seminars hub and each seminar
  copy_en.py         · the English pages
"""
from copy_services import SERVICES_COPY
from copy_pages import PAGES_COPY
from copy_articles import ARTICLES_COPY
from copy_seminars import SEMINARS_COPY
from copy_en import EN_COPY

COPY = {}
for _part in (SERVICES_COPY, PAGES_COPY, ARTICLES_COPY,
              SEMINARS_COPY, EN_COPY):
    for _k, _v in _part.items():
        if _k in COPY:
            raise KeyError("duplicate copy key: " + _k)
        COPY[_k] = _v
