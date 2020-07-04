.. image:: https://readthedocs.org/projects/pypresseportal/badge/?version=latest
  :target: https://pypresseportal.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status

.. image:: https://travis-ci.com/tcmetzger/pypresseportal.svg?branch=master
  :target: https://travis-ci.com/tcmetzger/pypresseportal
  :alt: Travis CI Build Status

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
  :target: https://opensource.org/licenses/MIT
  :alt: License: MIT

PyPresseportal
==============

A Python interface into the `presseportal.de <htps://www.presseportal.de>`_ API.

The website presseportal.de is a service provided by 'news aktuell', owned by dpa
(Deutsche Presse Agentur). It is one of the largest distributors of press releases
and investor relations announcements in Germany. For example, almost all police and fire
departments use this service to distribute their press releases.

PyPresseportal is in no way connected to presseportal.de, 'news aktuell' or dpa.
PyPresseportal is independently developed by volunteers as an Open Source
library.

An API key from presseportal.de is required to access data. You can find more
information and apply for an API key at `<https://api.presseportal.de/en>`_.

Documentation
-------------

Documentation is available at `<https://pypresseportal.readthedocs.io>`_.

Quickstart
----------

1. Installing with ``pip``
**************************

Use ``pip`` on a command line to download PyPresseportal from PyPI and install it on your system:

.. code-block:: bash

    $ pip install pypresseportal

2. Getting an API key
*********************

PyPresseportal requires a valid API key from `<https://api.presseportal.de/en>`_. This website is
also where you can find general information on the API as well as the API's Terms.

3. Initializing the API
***********************

First, create an instance of the ``PresseportalApi`` class,
using your API key:

>>> from pypresseportal import PresseportalApi
>>> api_object = PresseportalApi(YOUR_API_KEY)

4. Requesting data
******************

Next, request data from the API through the ``PresseportalApi`` class. It
contains several methods to access API data, all of which work similarly.

The easiest way to access the most recently published stories is the
``get_stories()`` method. If you do not provide any arguments to this method,
PyPresseportal defaults to retrieving the 50 most recent stories available.

For example:

>>> from pypresseportal import PresseportalApi
>>> api_object = PresseportalApi(YOUR_API_KEY)
>>> stories = api_object.get_stories()

``get_stories()`` returns a list of ``Story`` objects. Access Story data
through the individual Story object's attributes.

For example:

>>> stories[0].title
"Kohls Wohnhaus hat keinen Denkmalwert"
>>> stories[0].id
"4622388"

PyPresseportal offers many more methods for accessing and finding data. You can find all details in
the documentation: `<https://pypresseportal.readthedocs.io>`_
