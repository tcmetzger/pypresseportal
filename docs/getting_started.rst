.. meta::
   :description: Getting started with PyPresseportal - Python wrapper for the Presseportal API
   :keywords: Presseportal, News Aktuell, DPA, press release, investor relations

Getting started with PyPresseportal
===================================

.. Explain setting up api and one module - mention other modules and link to modules documentation.

Follow these steps to set up PyPresseportal and retrieve data from `presseportal.de <https://api.presseportal.de/en>`_:

1. Getting an API key
---------------------

PyPresseportal requires a valid API key from `presseportal.de <https://api.presseportal.de/en>`_.
You can request an API key on this website: `<https://api.presseportal.de/en>`_. This website is
also where you can find general information on the API, as well as the API's Terms.

2. Initializing the API
-----------------------

First, create an instance of the :class:`pypresseportal.PresseportalApi` class,
using your API key::

    >>> from pypresseportal import PresseportalApi
    >>> api_object = PresseportalApi(YOUR_API_KEY)

3. Requesting data from the API
-------------------------------

Next, request data from the API through the ``PresseportalApi`` class. This class
offers several methods to access API data. The :doc:`pypresseportal` explains all
available methods in detail.

The easiest way to access the most recently published stories is the
``get_stories()`` method. If you do not provide any arguments to this method,
PyPresseportal defaults to retrieving the 50 most recent stories available.

For example:

    >>> from pypresseportal import PresseportalApi
    >>> api_object = PresseportalApi(YOUR_API_KEY)
    >>> stories = api_object.get_stories()

4. Accessing the data
---------------------
``get_stories()`` returns a list of ``Story`` objects. Access Story data
through the individual Story object's attributes.

For example:

    >>> stories[0].title
    "Kohls Wohnhaus hat keinen Denkmalwert"
    >>> stories[0].id
    "4622388"

For each story the API returns, the method ``get_stories()`` will generate a ``Story`` object
with the following attributes:

    * ``data`` - The raw json data returned by the API.
    * ``id`` - The story's unique id as generated by the API.
    * ``url`` - URL of the story on the presseportal.de website.
    * ``title`` - Headline of the story.
    * ``body`` - Full text body.
    * optional: ``teaser`` - Teaser text. Only included if ``teaser=True`` is passed to
      ``get_stories()``. If a teaser is requested, it will replace the ``body`` attribute.
    * ``published`` - Publication date (as datetime object).
    * ``language`` - Language of the story (usually 'de' or 'en').
    * ``ressort`` - Editorial department.
    * ``company_id`` - Unique id of the company publishing the story.
    * ``company_url`` - URL of the company publishing the story.
    * ``company_name`` - Name of the company publishing the story.
    * ``keywords`` - List of keywords assigned to the story.
    * optional: ``media`` - Information on media attachments, if present.
    * ``highlight`` - Promoted story flag (on/off).
    * ``short`` - Shortened URL.

5. Learning more about PyPresseportal
-------------------------------------

The presseportal.de API offers several ways to request data. See the
:doc:`usage_examples` to see PyPresseportal in action. Detailed information
about PyPresseportal is available in the :doc:`pypresseportal`.

These are the methods supported by PyPresseportal:

* :meth:`pypresseportal.PresseportalApi.get_company_information()`: Return detailed
  info about a specific company (requires company id).
* :meth:`pypresseportal.PresseportalApi.get_entity_search_results()`: Search for
  company or public service office by location or name (provides company/office id).
* :meth:`pypresseportal.PresseportalApi.get_investor_relations_news()`: Return investor
  relations news (Ad Hoc news, Directors’ Dealings, reports, etc).
* :meth:`pypresseportal.PresseportalApi.get_investor_relations_news_company()`: Return
  investor relations news about a specific company (requires company id).
* :meth:`pypresseportal.PresseportalApi.get_public_service_news()`: Return stories
  released by public service offices (police and fire departments, etc).
* :meth:`pypresseportal.PresseportalApi.get_public_service_office_information()`:
  Return detailed info about a specific public service office (requires office id).
* :meth:`pypresseportal.PresseportalApi.get_public_service_specific_office()`: Return
  stories released by a specific public service office (requires office id).
* :meth:`pypresseportal.PresseportalApi.get_public_service_specific_region()`: Return
  Stories released by public service offices in a specific geographic region
  (`list of available regions <https://api.presseportal.de/en/doc/value/region>`_).
* :meth:`pypresseportal.PresseportalApi.get_stories_specific_company()`: Return stories
  released by a specific company (requires company id).
* :meth:`pypresseportal.PresseportalApi.get_stories_keywords()`: Return stories
  assigned to specific keywords
  (`list of available keywords <https://api.presseportal.de/en/doc/value/keyword>`_).
* :meth:`pypresseportal.PresseportalApi.get_stories_topic()`: Return stories assigned
  to a specific topic
  (`list of available topics <https://api.presseportal.de/en/doc/value/topic>`_).
* :meth:`pypresseportal.PresseportalApi.get_stories()`: Return recently published stories.
