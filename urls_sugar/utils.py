""" django-urls-sugar utils
"""

from classes import UrlSugar


def sugar_patterns(original_patterns, prefix, *args):
    """ A substitute for django patterns: cycles over the
    given url list looking for instances of UrlSugar, adding the generated
    urls and calling the original `patterns'.
    """
    pattern_list = []
    for an_url in args:
        if isinstance(an_url, UrlSugar):
            pattern_list += an_url.generate_urls()
        else:
            pattern_list.append(an_url)
    return original_patterns(prefix, *pattern_list)


def patterns(prefix, *args):
    """ calls sugar_patterns with default django patterns 
    """
    from django.conf.urls.defaults import patterns as django_patterns
    return sugar_patterns(django_patterns, prefix, *args)


def i18n_patterns(prefix, *args):
    """ calls sugar_patterns with django 1.4 localized patterns
    """
    from django.conf.urls.i18n import i18n_patterns as django_i18n_patterns
    return sugar_patterns(django_i18n_patterns, prefix, *args)


def url_sugar(params, *args, **kwargs):
    """ Builds an UrlSugar class with the given parameters.
    """
    return UrlSugar(params, *args, **kwargs)
