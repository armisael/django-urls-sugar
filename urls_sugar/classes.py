""" django-urls-sugar classes
"""

from django.conf.urls.defaults import url


class UrlSugarElement(object):
    """ Base urls_sugar element, with name, prefix and suffix.
    """
    def __init__(self, name, prefix, suffix):
        self.name = name
        self.prefix = prefix.replace('.', '\.')
        self.suffix = suffix.replace('.', '\.')

    def get_regexp(self):
        """ Returns the regular expression for matching this particular
        urls_sugar element.
        """
        return self.name


class Constant(UrlSugarElement):
    """ urls_sugar constant. Represents a piece of url such as `/home/' or
    `my-new-awesome-page'. It also accepts a list as `name', in order to
    map different urls in the same way.
    """
    def __init__(self, name, prefix='', suffix='/'):
        super(Constant, self).__init__(name, prefix, suffix)

    def __unicode__(self):
        return "Constant(%s)" % self.get_regexp()


class Optional(UrlSugarElement):
    """ urls_sugar optional. Represents an optional part of url, given as
    a list of urls_sugar elements.
    """
    def __init__(self, *args):
        super(Optional, self).__init__('Optional', '', '')
        self.args = args

    def __unicode__(self):
        return "Optional[%s]" % ", ".join([unicode(x) for x in self.args])


class Variable(UrlSugarElement):
    """ urls_sugar variable. Represents a variable that will be given to
    the view. It requires a name and a regular expression, but can also
    be treated as a list setting the parameters `separator', `min' and `max'.
    """
    def __init__(self, name, regexp, **kwargs):
        prefix = kwargs.get('prefix', '')
        suffix = kwargs.get('suffix', '/')
        min_v = kwargs.get('min', 1)
        max_v = kwargs.get('max', 0)
        super(Variable, self).__init__(name, prefix, suffix)

        self.regexp = regexp
        self.separator = kwargs.get('separator', None)
        self.min = min_v if min_v >= 1 else 1
        self.max = max_v if max_v >= 0 else 0
        self.unambiguous = kwargs.get('unambiguous', False)
        if self.max != 0 and self.min > self.max:
            self.max = self.min

    def get_regexp(self):
        """ Returns the regular expression for matching this particular
        urls_sugar element.
        """
        regexp_prefix = self.name + ":" if self.unambiguous else ''
        repeat = "%d,%s" % \
                 (self.min - 1, str(self.max) if self.max > 0 else '')
        regexp_suffix = "(%s%s){%s}" % (self.separator, self.regexp, repeat) \
                         if self.separator else ''
        return "%s(?P<%s>%s%s)" % \
               (regexp_prefix, self.name, self.regexp, regexp_suffix,)

    def __unicode__(self):
        return "Variable(%s, %s, %s, %d, %d)" % (
            self.name, self.get_regexp(), self.separator, self.min, self.max)


class UrlSugar(object):
    """ An UrlSugar url. It represents a generic set of urls, that can be
    generated and added to the django-patterns.
    """
    def __init__(self, params, *args, **kwargs):
        self.params = params
        self.args = args
        self.kwargs = kwargs

    def generate_urls(self):
        """ Generates the urls for this UrlSugar instance.
        """
        regexps = UrlSugar._generate_urls_for_elements(self.params)
        return [url(r, *self.args, **self.kwargs) for r in regexps[::-1]]

    @staticmethod
    def _generate_urls_for_elements(elements):
        """ Static method for generating urls from a list of urls_sugar
        elements.
        """

        def __generate(elements):
            """ Recursive support function.
            """
            new_urls = [[]]
            for elem in elements:
                if isinstance(elem, (Constant, Variable)):
                    sub_urls = elem.get_regexp()
                    if not isinstance(sub_urls, list):
                        sub_urls = [sub_urls]
                    new_urls = [x + [elem.prefix + y + elem.suffix]
                                for x in new_urls for y in sub_urls]
                elif isinstance(elem, Optional):
                    sub_urls = __generate(elem.args)
                    new_urls.extend([x + y
                                     for x in new_urls
                                     for y in sub_urls])
            return new_urls

        return ["^%s$" % "".join(x) for x in __generate(elements)]
