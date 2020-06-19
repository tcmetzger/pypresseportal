.. meta::
   :description: Usage Examples for PyPresseportal - Python wrapper for the Presseportal API
   :keywords: Presseportal, News Aktuell, DPA, press release, investor relations

Usage examples
==============

Request police and fire department press releases for a specific state
----------------------------------------------------------------------

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

Request press releases with images
----------------------------------
Use the ``media`` attribute available to most methods in PyPresseportal to limit the API's response
to stories containing a specific media type (available media types are listed at `<https://api.presseportal.de/en/doc/value/media>`_).

This code requests the 10 most recent news stories featuring an image:

>>> from pypresseportal import PresseportalApi
>>> api_object = PresseportalApi(YOUR_API_KEY)
>>> bavaria_stories = api_object.get_public_service_specific_region(region_code="by", limit=10)

Extract attributes for each story, including json data about the attached media file:

>>> for story in stories_with_image:
>>>     print(story.title)
>>>     print(story.image)
Das Erste: Richtiges Rezept für den Sieg? Tim Mälzer und Steffen Henssler treten an gegen Jörg Pilawas "Quizduell-Olymp" am Freitag, 19. Juni 2020, 18:50 Uhr im Ersten (FOTO)
[{'id': '679851', 'url': 'https://cache.pressmailing.net/thumbnail/story_big/ce365907-da06-4542-a8ca-3fc42db21e2b/1_F313_Quizduell_Olymp_2020.jpg', 'name': '1-f313-quizduell-olymp-2020.jpg', 'size': '2371804', 'mime': 'image/jpeg', 'type': 'image', 'caption': 'ARD QUIZDUELL-OLYMP, FOLGE 313, "Steffen Henssler und Tim Mälzer", am Freitag (19.06.20) um 18:50 Uhr im ERSTEN.\nDie Kandidaten des Teams "Köche": Steffen Henssler (l.) und Tim Mälzer (r.), beide TV-Köche.\n© ARD/Uwe Ernst, honorarfrei - Verwendung gemäß der AGB im engen inhaltlichen, redaktionellen Zusammenhang mit genannter ARD-Sendung bei Nennung "Bild: ARD/Uwe Ernst" (S2). ARD-Programmdirektion/Bildredaktion, Tel: 089/5900-23534, bildredaktion@DasErste.de Weiterer Text über ots und www.presseportal.de/nr/6694 / Die Verwendung dieses Bildes ist für redaktionelle Zwecke honorarfrei. Veröffentlichung bitte unter Quellenangabe: "obs/ARD Das Erste"'}]
