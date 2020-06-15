PyPresseportal
==============

A Python interface into the presseportal.de API.

Presseportal is a service provided by 'news aktuell', owned by dpa
 (Deutsche Presse Agentur). It is one of the biggest distributors of
 press releases in Germany. Almost all police and fire departments distribute
 their press releases through Presseportal, for example.

An API key from presseportal.de is required to access data. You can find more
 information and apply for an API key at https://api.presseportal.de/en.

Quickstart
----------
First, you need to create an instance of the ``PresseportalApi`` class, using your API key:

>>> from pypresseportal import PresseportalApi
>>> api_object = PresseportalApi(YOUR_API_KEY)

Next, you can request data from the API. Currently, those three request methods are implemented:

    1. Use the method `get_stories()` to access stories without any further restrictions (https://api.presseportal.de/doc/article/all).
    This method can take the following, optional arguments:

        * media (str, optional): Only request stories containing this specific media type (image, document, audio or video). Defaults to None.
        * start (int, optional): Start/offset of the result article list. Defaults to 0.
        * limit (int, optional): Limit number of articles in response (API maximum is 50). Defaults to 50.
        * teaser (bool, optional): Returns stories with teaser instead of fulltext if set to True. Defaults to False.

        If no arguments are provided, PyPresseportal defaults to retrieving the 50 most recent stories available. For example:

            >>> from pypresseportal import PresseportalApi
            >>> api_object = PresseportalApi(YOUR_API_KEY)
            >>> stories = api_object.get_stories()

        Story data can be accessed through the individual Story object's attributes. For example:

            >>> stories[0].title
            "Kohls Wohnhaus hat keinen Denkmalwert"
            >>> stories[0].id
            "4622388"

    2. The method `get_public_service_news()` to retrieve press releases from
    police and fire departments as well as other public service offices.
    (https://api.presseportal.de/doc/article/publicservice)

    3. The method `get_public_service_specific_region()` to retrieve press releases
    from police and fire departments as well as other public service offices in
    a specific state in Germany. (https://api.presseportal.de/doc/article/publicservice/region)
