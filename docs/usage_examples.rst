.. meta::
   :description: Usage Examples for PyPresseportal - Python wrapper for the Presseportal API
   :keywords: Presseportal, News Aktuell, DPA, press release, investor relations

Usage examples
==============

The following examples give you an idea of what can be done with PyPresseportal,
featuring some of the functionalities of the library. However, PyPresseportal has 
several additional functions that are not part of these examples. You can find more
information about all available classes, methods, and attributes in the :doc:`pypresseportal`.

Police and fire department press releases from a specific state
---------------------------------------------------------------

Use the ``get_public_service_specific_region()`` method to request press releases from public 
service offices in a specific region. 

First, this method requires a ``region_code`` argument, as defined
in this list: `<https://api.presseportal.de/en/doc/value/region>`_. For example, 'by' is the 
region code for Bavaria:

>>> from pypresseportal import PresseportalApi
>>> api_object = PresseportalApi(YOUR_API_KEY)
>>> bavaria_stories = api_object.get_public_service_specific_region(region_code="by", limit=20)

Note that this example also includes the optional argument ``limit=20``, which limits the 
response to the 20 most recently published stories:

>>> len(bavaria_stories)
20

Iterate over the list to extract some of the attributes of each Story object:

>>> for story in bavaria_stories:
>>>     print(story.title)
>>>     print(story.body)
POL-MFR: (797) Warnung vor "falschen Polizeibeamten"
Nürnberg (ots)
In den letzten Tagen registrierte die mittelfränkische Polizei zahlreiche Hinweise
(...)

The :doc:`pypresseportal` contains more information about all possible attributes 
a Story object can have: :class:`pypresseportal.Story`

Press releases with images
--------------------------
Use the ``media`` attribute available to most methods in PyPresseportal to limit the API's response
to stories containing a specific media type (available media types are listed at `<https://api.presseportal.de/en/doc/value/media>`_).

This code requests the 10 most recent news stories featuring an image, by passing ``media="image"``:

>>> from pypresseportal import PresseportalApi
>>> api_object = PresseportalApi(YOUR_API_KEY)
>>> stories_with_image = api_object.get_stories(media="image", limit=10)

Read the relevant attributes for each story, including json data about the attached media file:

>>> for story in stories_with_image:
>>>     print(story.title)
>>>     print(story.image)
Das Erste: Richtiges Rezept für den Sieg? Tim Mälzer und Steffen Henssler treten an gegen Jörg Pilawas "Quizduell-Olymp" am Freitag, 19. Juni 2020, 18:50 Uhr im Ersten (FOTO)
[{'id': '679851', 'url': 'https://cache.pressmailing.net/thumbnail/story_big/ce365907-da06-4542-a8ca-3fc42db21e2b/1_F313_Quizduell_Olymp_2020.jpg', 'name': '1-f313-quizduell-olymp-2020.jpg', 'size': '2371804', 'mime': 'image/jpeg', 'type': 'image', 'caption': 'ARD QUIZDUELL-OLYMP, FOLGE 313, "Steffen Henssler und Tim Mälzer", am Freitag (19.06.20) um 18:50 Uhr im ERSTEN.\nDie Kandidaten des Teams "Köche": Steffen Henssler (l.) und Tim Mälzer (r.), beide TV-Köche.\n© ARD/Uwe Ernst, honorarfrei - Verwendung gemäß der AGB im engen inhaltlichen, redaktionellen Zusammenhang mit genannter ARD-Sendung bei Nennung "Bild: ARD/Uwe Ernst" (S2). ARD-Programmdirektion/Bildredaktion, Tel: 089/5900-23534, bildredaktion@DasErste.de Weiterer Text über ots und www.presseportal.de/nr/6694 / Die Verwendung dieses Bildes ist für redaktionelle Zwecke honorarfrei. Veröffentlichung bitte unter Quellenangabe: "obs/ARD Das Erste"'}]

Press releases from police and fire departments in a specific city
------------------------------------------------------------------

Combine the methods ``get_entity_search_results()`` and ``get_public_service_specific_office()``
to access all available public service office press releases for a specific city.

First, initialize the API and search for all available offices in a city. Use the argument
``entity='office'`` to search for public service offices. Use the argument ``search_term`` to
pass the city you are searching for, for example "Dortmund":

>>> from pypresseportal import PresseportalApi
>>> api_object = PresseportalApi(YOUR_API_KEY)
>>> search_results = api_object.get_entity_search_results(search_term=["Dortmund"], entity="office")

Three public service offices are available in Dortmund:

>>> for office in search_results:
>>>     print(office.id, office.name)
4971 Polizei Dortmund
115869 Feuerwehr Dortmund
121242 Hauptzollamt Dortmund

Next, store the offices' ids in a list:

>>> local_office_ids = []
>>> for data in search_results:
>>>     local_office_ids.append(data.id)

Finally, use ``get_public_service_specific_office()`` to access the 
most recent press releases of those three offices:

>>> for office in local_office_ids:
>>>     office_data = api_object.get_public_service_specific_office(id=office, limit=4)
>>>     for story in office_data:
>>>         print(story.title)
>>>         print(story.body)
POL-DO: Mehrere Fahrzeuge in Dortmund-Dorstfeld beschädigt - Polizei sucht Zeugen
Dortmund (ots) - Lfd. Nr.: 0628
(...)

Instead of ``get_public_service_specific_office()``, you can use ``get_stories_specific_company()`` to
access press releases of a specific company, or ``get_investor_relations_news_company()`` to access
a specific company's investor relations announcements.

Press releases from a specific company
--------------------------------------

Combine the methods ``get_entity_search_results()`` and ``get_stories_specific_company()``
to access press releases published by a specific company.

First, initialize the API and use ``get_entity_search_results()`` to search the API's
database for any results matching the company you are looking for. For example the company "ARD":

>>> from pypresseportal import PresseportalApi
>>> api_object = PresseportalApi(YOUR_API_KEY)
>>> search_results = api_object.get_entity_search_results(search_term=["ARD"], entity="company")

Next, inspect the search results. ``get_entity_search_results()`` returns a list of all
companies matching your search string. Note that ``get_entity_search_results()`` will return 
None if the API did not find any matching entries, so make sure to check first:

>>> if search_results:  # Check if search yielded any results
>>>     for company in search_results:
>>>         print(company.id, company.name)
6694 ARD Das Erste
22512 ARD ZDF
29876 ARD Presse
64887 ARDEX GmbH
73846 ARD Das Erste / ZDF
(...)

Finally, pick the id of the company you were looking for and pass it to 
``get_stories_specific_company()``, using the attribute ``id`` :

>>> company_stories = api_object.get_stories_specific_company(id=search_results[0].id)
>>> for story in company_stories:
>>>     print(story.title)
>>>     print(story.body)
Das Erste / "Wenn Frauen Austern essen" - der erste Gewinner des "Tatort"-Votings zum 50-jährigen Jubiläum der Krimireihe (FOTO)
München (ots) - 143.997 Zuschauerinnen und Zuschauer aus Deutschland und Österreich beteiligten sich an der ersten Abstimmungsrunde des Sommer-Events.
(...)

Investor relations announcements from a specific company
--------------------------------------------------------

presseportal.de keeps investor relations announcements by public companies separated from regular
press releases. Combine the methods ``get_entity_search_results()`` and ``get_investor_relations_news_company()``
to access investor relations announcements from a specific company.

First, initialize the API and use ``get_entity_search_results()`` to search the API's
database for any results matching the company you are looking for. For example the company "Fraport":

>>> from pypresseportal import PresseportalApi
>>> api_object = PresseportalApi(YOUR_API_KEY)
>>> search_results = api_object.get_entity_search_results(search_term=["Fraport"], entity="company")

Next, inspect the search results. ``get_entity_search_results()`` returns a list of all
companies matching your search string. Note that ``get_entity_search_results()`` will return 
None if the API did not find any matching entries, so make sure to check first:

>>> if search_results:  # Check if search yielded any results
>>>     for company in search_results:
>>>         print(company.id, company.name)
31522 Fraport AG

Optionally, you can now use the method ``get_company_information()`` to query the API
for more information about the company, such as `WKN <https://en.wikipedia.org/wiki/Wertpapierkennnummer>`_,
`ISIN <https://en.wikipedia.org/wiki/International_Securities_Identification_Number>`_ or the 
company's RSS feed:

>>> company_info = api_object.get_company_information(id=search_results[0].id)
>>> print(company_info.wkn)
>>> print(company_info.isin)
>>> print(company_info.rss)
577330
DE0005773303
https://www.presseportal.de/rss/pm_31522.rss2

Finally, use the ``get_investor_relations_news_company()`` method with the id you
acquired above to access the company's most recent investor relations press releases:

>>> investor_relations_stories = api_object.get_investor_relations_news_company(search_results[0].id)
>>> for story in investor_relations_stories:
>>>     print(story.title)
>>>     print(story.body)
EANS-Hinweisbekanntmachung: Fraport AG Frankfurt Airport Services Worldwide /
Bekanntmachung gemäß § 37v, 37w, 37x ff. WpHG mit dem Ziel der europaweiten
Verbreitung
Hiermit gibt die Fraport AG Frankfurt Airport Services Worldwide bekannt, 
(...)
