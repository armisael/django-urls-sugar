""" django-urls-sugar utils
"""

from django.conf.urls.defaults import patterns as django_patterns
from classes import UrlSugar


def patterns(prefix, *args):
    """ A substitute for django.conf.urls.defaults.patterns: cycles over the
    given url list looking for instances of UrlSugar, adding the generated
    urls and calling the original `patterns'.
    """
    pattern_list = []
    for an_url in args:
        if isinstance(an_url, UrlSugar):
            pattern_list += an_url.generate_urls()
        else:
            pattern_list.append(an_url)
    return django_patterns(prefix, *pattern_list)


def url_sugar(params, *args, **kwargs):
    """ Builds an UrlSugar class with the given parameters.
    """
    return UrlSugar(params, *args, **kwargs)
