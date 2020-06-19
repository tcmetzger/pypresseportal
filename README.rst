PyPresseportal
==============

A Python interface into the `presseportal.de <htps://www.presseportal.de>`_ API.

The website presseportal.de is a service provided by 'news aktuell', owned by dpa
(Deutsche Presse Agentur). It is one of the biggest distributors of press releases 
and investor relations announcements in Germany. For example, almost all police and fire 
departments use this service to distribute their press releases.

PyPresseportal is in no way connected to presseportal.de, 
'news aktuell' or dpa. PyPresseportal is independently developed by volunteers as an Open Source 
library.

An API key from presseportal.de is required to access data. You can find more
information and apply for an API key at https://api.presseportal.de/en.

Quickstart
----------
Installing with ``pip``
***********************

Use ``pip`` on a command line to download PyPresseportal from PyPI and install it on your system:

.. code-block:: bash

    $ pip install pypresseportal

Getting an API key
******************

PyPresseportal requires a valid API key from `<https://api.presseportal.de/en>`_. This website is
also where you can find general information on the API as well as the API's Terms.

Initializing the API
********************

First, create an instance of the ``PresseportalApi`` class, 
using your API key:

>>> from pypresseportal import PresseportalApi
>>> api_object = PresseportalApi(YOUR_API_KEY)

Requesting data
***************

Next, request data from the API through the ``PresseportalApi`` class. It
contains several methods to access API data, all of which work very similarly.

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
