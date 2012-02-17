-----------------
django-urls-sugar
-----------------

django-urls-sugar aims to make defining complex urls in django easier.
It provides a `patterns' method that extends the django.conf.urls.defaults functionalities, allowing to define more complex structured urls.

Its implementation takes inspiration from django-templatetags-sugar_.


Installation
============

Just run ``pip install django-urls-sugar`` in a terminal to do the magic.


Usage
=====

In order to use django-urls-sugar you just need to slightly alter your urls.py files, using the redefined patterns (which just extends the default one, allowing you to define usual urls as well). For example::
    
    from django.conf.urls.defaults import url
    from urls_sugar.utils import patterns, url_sugar
    from urls_sugar.classes import Constant, Variable
    
    urlpatterns = patterns('',
        url('^home$', home_view, name='home'),
        url_sugar([Constant('page'),
                   Variable('pk', '\d+'),
                  ], page_view, name='page'),
        ...


This two urls will handle::

    /home/
    /page/(?P<pk>\d+)/


The first parameter of url_sugar is a list of urls_sugar elements, which can be any of the following:

Constant
--------
A constant is, as the name suggests, a constant part of the url. It accepts a single parameter, that can be eather a string or a list of strings (in which case multiple urls will be generated). For example

* ``Constant('home')`` will generate the simple url ``^home/$``;
* ``Constant(['home', 'homepage'])`` will generate two urls, ``^home/$`` and ``^homepage$``, pointing to the same view.

This allows you to define in a simple way multiple (constant) urls, avoiding redirects or allowing to translate urls.


Variable
--------
A variable is more complex. In general, it allows to define a variable in the url that will be passed to the view, as for usual urls. It accepts two parameters, the variable name, and the regular expression to be matched. A simple example is:

* ``Variable('language', '[a-z]{2}')`` which will, easy to guess, generate the url ``^(?P<language>[a-z]{2}')$``.

Variables allows however more complex interaction. Suppose you want the variable to be an hyphen-separated list of something. Variable allows you to specify this with a simple

* ``Variable('languages', '[a-z]{2}', separator='-')``.

You can also set the ``min`` and ``max`` parameters to specify a lower / upper bound for such list.


Optional
--------
The Optional element allows us to define optional parts in the url. Optional takes (multiple) urls_sugar elements as parameters. For example:

* ``Optional(Constant('home'), Constant('index'))`` will generate ``^/$`` and ``^home/index/$``, while
* ``Optional(Constant('home')), Optional(Constant('index'))`` will generate ``^/$``, ``^home/$``, ``^index/$`` and ``^home/index/$``.


Special cases
=============

Prefix and Suffix
-----------------
Constant and Variable allow to specify a prefix and a suffix, which are by default respectively ``''`` and ``'/'``. In this way, ``Constant('home')`` generates ``^home/$``. Using custom prefixes and suffixes can be useful for example when handling special resource types::

    url_sugar([Constant('resource'),
               Variable('slug', '[a-z0-9-]+', suffix=''),
               Variable('type', '[a-z]+', prefix='.'),
               ], resource_view, name='resource')

This will handle urls like ``/resource/my-awesome-resource.json``


Variable disambiguation
-----------------------
When having too many optional variables, it may become impossible for Django to understand which variable should get the given value. For example::

    url_sugar([Constant('pages'),
               Optional(Variable('language', '[a-z]{2}')),
               Optional(Variable('filter', [a-z]+')),
               ], page_view, name='page')

In this case it is impossible to distinguish between ``/pages/it/`` and ``pages/blogposts/``. Variable allows then to be disambiguated, setting the ``unambiguous`` flag::

    url_sugar([Constant('pages'),
               Optional(Variable('language', '[a-z]{2}', unambiguous=True)),
               Optional(Variable('filter', [a-z]+'), unambiguous=True),
               ], page_view, name='page')

Which will handle urls such as ``/pages/language:it/``, ``/pages/filter:blogposts/`` or ``/pages/language:it/filter:blogposts/``.

.. _django-templatetags-sugar: http://github.com/alex/django-templatetag-sugar