django-urls-sugar
=================

django-urls-sugar aims to make defining complex urls in django easier.
It provides a `patterns' method that extends the django.conf.urls.defaults functionalities, allowing to define more complex structured urls.

Its implementation takes inspiration from [django-templatetags-sugar](http://github.com/alex/django-templatetag-sugar).

Usage
-----

In order to use django-urls-sugar you just need to slightly alter your urls.py files, using the redefined patterns (which just extends the default one, allowing you to define usual urls as well). For example:

```python
from django.conf.urls.defaults import url
from urls_sugar import patterns, url_sugar, Constant, Variable

urlpatterns = patterns('',
    url('^home$', home_view, name='home'),
    url_sugar([Constant('page'),
               Variable('pk', '\d+'),
	       ], page_view, name='page'),
    ...
```

This two urls will handle

```
/home/
/page/(?P<pk>\d+)/
```

The first parameter of url_sugar is a list of urls_sugar elements, which can be any of the following:

### Constant
A constant is, as the name suggests, a constant chunk of the url. It accepts a single parameter, that can be eather a string or a list of strings (in which case multiple urls will be generated). For example

* Constant('home') will generate the simple url ^home/$
* Constant(['home', 'homepage']) will generate two urls, ^home/$ and ^homepage$, pointing to the same view.

This allows you to define in a simple way multiple (constant) urls, avoiding redirects or allowing to translate urls.
