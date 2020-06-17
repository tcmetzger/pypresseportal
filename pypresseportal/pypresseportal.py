"""PyPresseportal - Python wrapper for the presseportal.de API

PyPresseportal makes data from the presseportal.de API
 accessible as Python objects. You need an API key from
 presseportal.de to use PyPresseportal (https://api.presseportal.de/en).
"""

import json

from datetime import datetime
from typing import Dict, List, Tuple, Union

import requests

from pypresseportal.constants import (
    MEDIA_TYPES,
    PUBLIC_SERVICE_MEDIA_TYPES,
    INVESTOR_RELATIONS_NEWS_TYPES,
    PUBLIC_SERVICE_REGIONS,
    TOPICS,
    KEYWORDS,
)
from pypresseportal.pypresseportal_errors import (
    ApiError,
    ApiConnectionFail,
    ApiKeyError,
    ApiDataError,
    MediaError,
    RegionError,
    TopicError,
    KeywordError,
    NewsTypeError,
    SearchTermError,
    SearchEntityError,
)


class Entity:
    """Represents a company or a public service office search result
    """

    def __init__(self, data: dict):
        self.data = data
        data_keys = self.data.keys()
        required_keys = ("id", "url", "name", "type")
        for required_key in required_keys:
            if required_key not in data_keys:
                raise ApiDataError(f"Required key {required_key} missing.")

        self.id = data["id"]
        self.url = data["url"]
        self.name = data["name"]
        self.type = data["type"]


class Story:
    """Represents a story retrieved from the API.

    A Story object can contain different attributes, depending on the API query method.
    """

    def __init__(self, data: dict):
        """Constructor method.

        Args:
            data (dict): Raw data from API request
        """
        self.data = data
        data_keys = self.data.keys()
        required_keys = ("id", "url", "title", "published", "highlight", "short")
        for required_key in required_keys:
            if required_key not in data_keys:
                raise ApiDataError(f"Required key {required_key} missing.")

        self.id = data["id"]
        self.url = data["url"]
        self.title = data["title"]
        self.published = datetime.strptime(data["published"], "%Y-%m-%dT%H:%M:%S%z")
        self.highlight = data["highlight"]
        self.short = data["short"]

        # Check whether data contains body or teaser
        if "body" in data_keys:
            self.body = data["body"]
        elif "teaser" in data_keys:
            self.teaser = data["teaser"]
        else:
            raise ApiDataError("'body' or 'teaser' not included in response.")

        if "language" in data_keys:
            self.language = data["language"]
        if "ressort" in data_keys:
            self.ressort = data["ressort"]

        # TBD: "Extended" info: https://api.presseportal.de/doc/format/company?
        # Check whether data contains company or office
        if "company" in data_keys:
            self.company_id = data["company"]["id"]
            self.company_url = data["company"]["url"]
            self.company_name = data["company"]["name"]
        elif "office" in data_keys:
            self.office_id = data["office"]["id"]
            self.office_url = data["office"]["url"]
            self.office_name = data["office"]["name"]
        else:
            raise ApiDataError("'company' or 'office' data not included in response.")

        # Check if keywords are present, map keywords
        if type(data["keywords"]) is dict and "keyword" in data["keywords"]:
            self.keywords = data["keywords"]["keyword"]

        # Check if media information is present
        media_keys = []
        if "media" in data_keys:
            media_keys = data["media"].keys()
        # PresseportalAPI.media_types
        # Map media information as dicts
        # MEDIA_TYPES are "image", "document", "audio", "video"
        for media_type in MEDIA_TYPES:
            if media_keys and media_type in media_keys:
                # Dynamically create attributes for media_type
                setattr(self, media_type, data["media"][media_type])


class PresseportalApi:
    """A Python interface into the presseportal.de API.

    Presseportal is a service provided by 'news aktuell', owned by dpa
     (Deutsche Presse Agentur). An API key from presseportal.de is required.
     You can find more information and apply for an API key at
     https://api.presseportal.de/en.

    First, you need to create an instance of the ``PresseportalApi`` class, using your API key:

    >>> from pypresseportal import PresseportalApi
    >>> api_object = PresseportalApi(YOUR_API_KEY)

    Next, you can request data from the API. Currently, those two request methods are implemented:

        1. Use the method `get_stories()` to access stories without any further restrictions (https://api.presseportal.de/doc/article/all).
        This method can take the following, optional arguments:

            * media (str, optional): Only request stories containing one specific media type (image, document, audio or video). Defaults to None.
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
    """

    def __init__(self, api_key: str):
        """Constructor method.
        """
        self.data_format = "json"
        if type(api_key) is str and len(api_key) > 5:
            self.api_key = api_key
        else:
            raise ApiKeyError(api_key)

    def build_request(
        self,
        base_url: str,
        media: Union[str, None],
        start: Union[int, None],
        limit: int,
        teaser: Union[bool, None],
        search_term: Union[str, None] = None,
    ) -> Tuple[str, Dict[str, str], Dict[str, str]]:

        # Set up url and append media type, if required
        url = base_url
        if media:
            url += f"/{media.lower()}"

        # Set up params (all arguments that are not None)
        params = {
            "api_key": self.api_key,
            "format": self.data_format,
        }
        if start is not None:
            params["start"] = str(start)
        if limit is not None:
            params["limit"] = str(limit)
        if teaser is not None:
            params["teaser"] = str(int(teaser))
        if search_term is not None:
            params["q"] = search_term

        # Set up headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"
        }

        return url, params, headers

    def get_data(self, url: str, params: dict, headers: dict) -> dict:
        """Connects to API and maps raw data into objects.

        Args:
            url (str): URL for query.
            params (dict): Parameters for query.
            headers (dict): Headers for query.

        Raises:
            ApiConnectionFail: Could not connect to API.
            NotImplementedError: Unknown error.
            ApiError: API returned an error.

        Returns:
            List[Story]: List of Story objects
        """
        #######################Disable for testing ##############
        try:
            request = requests.get(url=url, params=params, headers=headers)
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.TooManyRedirects,
            requests.exceptions.Timeout,
        ) as error:
            raise ApiConnectionFail(error)
        json_data = json.loads(request.text)
        # with open("out.json", "w") as outfile:
        #     json.dump(json_data, outfile)
        #######################Enable for testing ###############
        # # read file
        # with open("out.json", "r") as in_file:
        #     data = in_file.read()
        # # parse file
        # json_data = json.loads(data)
        #########################################################

        # Raise error if API does not report success
        if "error" in json_data:
            error_code = json_data["error"]["code"]
            error_msg = json_data["error"]["msg"]
            raise ApiError(error_code, error_msg)

        return json_data

    def parse_story_data(self, json_data: dict) -> List[Story]:
        stories_list = []
        for item in json_data["content"]["story"]:
            stories_list.append(Story(item))

        return stories_list

    def parse_search_results(self, json_data: dict) -> List[Entity]:
        search_results_list = []
        for item in json_data["content"]["result"]:
            search_results_list.append(Entity(item))

        return search_results_list

    def get_public_service_news(
        self, media: str = None, start: int = 0, limit: int = 50, teaser: bool = False,
    ) -> List[Story]:
        """Queries API for public service news.

        Returns a list of Story objects. More information: https://api.presseportal.de/doc/article/publicservice

        Args:
            media (str, optional): Only request stories containing this specific media type (``image`` or ``document``). Defaults to None.
            start (int, optional): Start/offset of the result article list. Defaults to 0.
            limit (int, optional): Limit number of articles in response (API maximum is 20). Defaults to 20.
            teaser (bool, optional): Returns stories with ``teaser`` instead of ``body`` (fulltext) if set to True. Defaults to False.

        Raises:
            ApiConnectionFail: Could not connect to API.
            ApiError: API returned an error.
            MediaError: API does not support the requested media type.
            NotImplementedError: Unknown error.

        Returns:
            List[Story]: List of Story objects
        """

        # Check if media type is supported by API
        # Public service news allows only image or document
        if media and media.lower() not in PUBLIC_SERVICE_MEDIA_TYPES:
            raise MediaError(media, PUBLIC_SERVICE_MEDIA_TYPES)

        # Set up query components
        base_url = "https://api.presseportal.de/api/article/publicservice"
        url, params, headers = self.build_request(base_url, media, start, limit, teaser)

        # Query API and map results
        json_data = self.get_data(url=url, params=params, headers=headers)
        stories_list = self.parse_story_data(json_data)

        return stories_list

    def get_public_service_specific_region(
        self,
        region_code: str,
        media: str = None,
        start: int = 0,
        limit: int = 50,
        teaser: bool = False,
    ) -> List[Story]:
        """Queries API for public service news from specific state.

        Returns a list of Story objects. List of region codes and more information: https://api.presseportal.de/doc/article/publicservice/region

        Args:
            region_code (str): Only request stories located in this specific region. 
            media (str, optional): Only request stories containing this specific media type (``image``, ``document``, ``audio`` or ``video``). Defaults to None.
            start (int, optional): Start/offset of the result article list. Defaults to 0.
            limit (int, optional): Limit number of articles in response (API maximum is 20). Defaults to 20.
            teaser (bool, optional): Returns stories with ``teaser`` instead of ``body`` (fulltext) if set to True. Defaults to False.

        Raises:
            ApiConnectionFail: Could not connect to API.
            ApiError: API returned an error.
            MediaError: API does not support the requested media type.
            NotImplementedError: Unknown error.

        Returns:
            List[Story]: List of Story objects
        """

        # Check if media type is supported by API
        # Public service news allows only image or document
        if media and media.lower() not in PUBLIC_SERVICE_MEDIA_TYPES:
            raise MediaError(media, PUBLIC_SERVICE_MEDIA_TYPES)

        # Check if region is supported by API
        if region_code not in PUBLIC_SERVICE_REGIONS:
            raise RegionError(region_code, PUBLIC_SERVICE_REGIONS)

        # Set up query components
        base_url = f"https://api.presseportal.de/api/article/publicservice/region/{region_code}"
        url, params, headers = self.build_request(base_url, media, start, limit, teaser)

        # Query API and map results
        json_data = self.get_data(url=url, params=params, headers=headers)
        stories_list = self.parse_story_data(json_data)

        return stories_list

    def get_stories(
        self, media: str = None, start: int = 0, limit: int = 50, teaser: bool = False,
    ) -> List[Story]:
        """Queries API for public service news.

        Returns a list of Story objects. More information: https://api.presseportal.de/doc/article/all
        print(api_object.available_media_types) for list of available media types.

        Args:
            media (str, optional): Only request stories containing this specific media type (``image``, ``document``, ``audio`` or ``video``). Defaults to None.
            start (int, optional): Start/offset of the result article list. Defaults to 0.
            limit (int, optional): Limit number of articles in response (API maximum is 20). Defaults to 20.
            teaser (bool, optional): Returns stories with ``teaser`` instead of ``body`` (fulltext) if set to True. Defaults to False.

        Raises:
            ApiConnectionFail: Could not connect to API.
            ApiError: API returned an error.
            MediaError: API does not support the requested media type.
            NotImplementedError: Unknown error.

        Returns:
            List[Story]: List of Story objects
        """

        # Check if media type is supported by API
        if media and media.lower() not in MEDIA_TYPES:
            raise MediaError(media, MEDIA_TYPES)

        # Set up query components
        base_url = "https://api.presseportal.de/api/article/all"
        url, params, headers = self.build_request(base_url, media, start, limit, teaser)

        # Query API and map results
        json_data = self.get_data(url=url, params=params, headers=headers)
        stories_list = self.parse_story_data(json_data)

        return stories_list

    def get_stories_topic(
        self,
        topic: str,
        media: str = None,
        start: int = 0,
        limit: int = 50,
        teaser: bool = False,
    ) -> List[Story]:
        """https://api.presseportal.de/doc/article/topic/ident
        """

        # Check if media type is supported by API
        if media and media.lower() not in MEDIA_TYPES:
            raise MediaError(media, MEDIA_TYPES)

        # Check if topic is supported by API
        if topic not in TOPICS:
            raise TopicError(topic, TOPICS)

        # Set up query components
        base_url = f"https://api.presseportal.de/api/article/topic/{topic}"
        url, params, headers = self.build_request(base_url, media, start, limit, teaser)

        # Query API and map results
        json_data = self.get_data(url=url, params=params, headers=headers)
        stories_list = self.parse_story_data(json_data)

        return stories_list

    def get_stories_keywords(
        self,
        keywords: List[str],
        media: str = None,
        start: int = 0,
        limit: int = 50,
        teaser: bool = False,
    ) -> List[Story]:
        """https://api.presseportal.de/doc/article/keyword/ident
        """

        # Check if media type is supported by API
        if media and media.lower() not in MEDIA_TYPES:
            raise MediaError(media, MEDIA_TYPES)

        # Check if keywords are supported by API
        for keyword in keywords:
            if keyword not in KEYWORDS:
                raise KeywordError(keyword, KEYWORDS)

        # Construct keyword string
        keywords_str = ",".join(keywords)

        # Set up query components
        base_url = f"https://api.presseportal.de/api/article/keyword/{keywords_str}"
        url, params, headers = self.build_request(base_url, media, start, limit, teaser)

        # Query API and map results
        json_data = self.get_data(url=url, params=params, headers=headers)
        stories_list = self.parse_story_data(json_data)

        return stories_list

    def get_investor_relations_news(
        self, news_type: str, start: int = 0, limit: int = 50, teaser: bool = False,
    ) -> List[Story]:
        """https://api.presseportal.de/doc/ir/list
        """

        # Check if investor relations news type is supported by API
        if news_type.lower() not in INVESTOR_RELATIONS_NEWS_TYPES:
            raise NewsTypeError(news_type, INVESTOR_RELATIONS_NEWS_TYPES)

        # Set up query components
        base_url = f"https://api.presseportal.de/api/ir/{news_type.lower()}"
        url, params, headers = self.build_request(
            base_url=base_url, media=None, start=start, limit=limit, teaser=teaser
        )

        # Query API and map results
        json_data = self.get_data(url=url, params=params, headers=headers)
        stories_list = self.parse_story_data(json_data)

        return stories_list

    def get_entity_search_results(
        self,
        search_term: Union[str, List[str]],
        entity: str = "company",
        limit: int = 20,
    ) -> List[Entity]:
        """https://api.presseportal.de/doc/search/company
        can be one str or a list of strings [OR search]
        can be city, company name, part of a city or part of a company name
        """

        # Check search term
        if isinstance(search_term, list):
            search_term = ",".join(search_term).lower()
        elif isinstance(search_term, str) and len(search_term) > 3:
            search_term = search_term.lower()
        else:
            raise SearchTermError(search_term)

        # Check entity and define base_url
        if entity.lower() == "office":
            base_url = "https://api.presseportal.de/api/search/office"
        elif entity.lower() == "company":
            base_url = "https://api.presseportal.de/api/search/company"
        else:
            raise SearchEntityError(entity)

        # Set up query components
        url, params, headers = self.build_request(
            base_url=base_url,
            media=None,
            start=None,
            limit=limit,
            teaser=None,
            search_term=search_term,
        )

        # Query API and map results
        json_data = self.get_data(url=url, params=params, headers=headers)
        search_results_list = self.parse_search_results(json_data)

        return search_results_list
