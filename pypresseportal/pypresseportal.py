"""PyPresseportal - Python wrapper for the presseportal.de API

PyPresseportal makes data from the presseportal.de API
 accessible as Python objects. You need an API key from
 presseportal.de to use PyPresseportal.
"""

import json

from datetime import datetime
from typing import Dict, List, Tuple, Union

import requests

from .pypresseportal_errors import (
    ApiError,
    ApiConnectionFail,
    ApiKeyError,
    ApiDataError,
    MediaError,
    RegionError,
    TopicError,
    KeywordError,
    NewsTypeError,
)


class Story:
    """Represents a story retrieved from the API.

    A Story object can contain different attributes, depending on the API query method.
    """

    def __init__(self, data: dict):
        """Constructor method.

        Args:
            data (dict): Raw data from API request
        """
        #### TBD: decide behavior (keywords, media, etc.):
        # - always have all attributes and some of them are None
        # - only have attributes that have valid data

        try:
            self.data = data
            self.keys = data.keys()
        except (TypeError, KeyError) as error:
            raise ApiDataError(str(error))

        try:
            self.id = data["id"]
            self.url = data["url"]
            self.title = data["title"]

            # Check whether data contains body or teaser
            if "body" in self.keys:
                self.body = data["body"]
            elif "teaser" in self.keys:
                self.teaser = data["teaser"]
            else:
                raise ApiDataError("'body' or 'teaser' not included in response.")

            self.published = datetime.strptime(data["published"], "%Y-%m-%dT%H:%M:%S%z")
            if "language" in self.keys:
                self.language = data["language"]
            if "ressort" in self.keys:
                self.ressort = data["ressort"]

            # TBD: "Extended" info: https://api.presseportal.de/doc/format/company?
            # Check whether data contains company or office
            if "company" in self.keys:
                self.company_id = data["company"]["id"]
                self.company_url = data["company"]["url"]
                self.company_name = data["company"]["name"]
            elif "office" in self.keys:
                self.office_id = data["office"]["id"]
                self.office_url = data["office"]["url"]
                self.office_name = data["office"]["name"]
            else:
                raise ApiDataError(
                    "'company' or 'office' data not included in response."
                )

            # Check if keywords are present, map keywords
            if isinstance(data["keywords"], dict) and "keyword" in data["keywords"]:
                self.keywords = []
                for keyword in data["keywords"]["keyword"]:
                    self.keywords.append(keyword)

            # Check if media information is present
            if "media" in self.keys:
                media_keys = data["media"].keys()
            else:
                media_keys = None
            # Map media information as dicts
            if media_keys and "image" in media_keys:
                self.image = data["media"]["image"]
            elif media_keys and "audio" in media_keys:
                self.audio = data["media"]["audio"]
            elif media_keys and "video" in media_keys:
                self.video = data["media"]["video"]
            elif media_keys and "document" in media_keys:
                self.document = data["media"]["document"]

            self.highlight = data["highlight"]
            self.short = data["short"]
        except (TypeError, KeyError) as error:
            raise ApiDataError(str(error))

    # def __init__(self, ressort):
    #     self.ressort = ressort

    # @property
    # def department(self):
    #     return self.ressort


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
        if not type(api_key) is str or len(api_key) < 5:
            raise ApiKeyError(api_key)
        else:
            self.api_key = api_key

        with open("../assets/assets.json", "r") as in_file:
            data = in_file.read()
        assets = json.loads(data)

        self.media_types = assets["media_types"]
        self.public_service_media_types = assets["public_service_media_types"]
        self.public_service_regions = assets["public_service_regions"]
        self.topics = assets["topics"]
        self.keywords = assets["keywords"]
        self.investor_relations_news_types = assets["investor_relations_news_types"]
        self.data_format = "json"

    def build_request(
        self,
        base_url: str,
        media: Union[str, None],
        start: Union[int, None],
        limit: int,
        teaser: Union[bool, None],
    ) -> Tuple[str, Dict[str, str], Dict[str, str]]:

        # Set up url and append media type, if required
        if media != None:
            url = f"{base_url}/{media}"
        else:
            url = base_url

        # Set up params (all arguments that are not None)
        params = {
            "api_key": self.api_key,
            "format": self.data_format,
        }
        if start != None:
            params["start"] = str(start)
        if limit != None:
            params["limit"] = str(limit)
        if teaser != None:
            params["teaser"] = str(int(teaser))

        # Set up headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"
        }

        return url, params, headers

    def get_data(self, url: str, params: dict, headers: dict) -> List[Story]:
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

        # Raise error if API does not report success (ApiError or NotImplementedError)
        if "success" in json_data.keys() and json_data["success"] == "1":
            pass
        elif "error" in json_data.keys():
            if (
                "code" in json_data["error"].keys()
                and "msg" in json_data["error"].keys()
            ):
                error_code = json_data["error"]["code"]
                error_msg = json_data["error"]["msg"]
                raise ApiError(error_code, error_msg)
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError

        # Parse stories from API into list of Story objects
        stories_list = []
        for item in json_data["content"]["story"]:
            stories_list.append(Story(item))

        return stories_list

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
        if media and not media in self.public_service_media_types:
            raise MediaError(media, self.public_service_media_types)

        # Set up query components
        base_url = "https://api.presseportal.de/api/article/publicservice"
        url, params, headers = self.build_request(base_url, media, start, limit, teaser)

        # Query API and map results
        stories_list = self.get_data(url=url, params=params, headers=headers)

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
        if media and not media in self.public_service_media_types:
            raise MediaError(media, self.public_service_media_types)

        # Check if region is supported by API
        if region_code not in self.public_service_regions:
            raise RegionError(region_code, self.public_service_regions)

        # Set up query components
        base_url = f"https://api.presseportal.de/api/article/publicservice/region/{region_code}"
        url, params, headers = self.build_request(base_url, media, start, limit, teaser)

        # Query API and map results
        stories_list = self.get_data(url=url, params=params, headers=headers)

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
        if media and not media in self.media_types:
            raise MediaError(media, self.media_types)

        # Set up query components
        base_url = "https://api.presseportal.de/api/article/all"
        url, params, headers = self.build_request(base_url, media, start, limit, teaser)

        # Query API and map results
        stories_list = self.get_data(url=url, params=params, headers=headers)

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
        if media and not media in self.media_types:
            raise MediaError(media, self.media_types)

        # Check if topic is supported by API
        if topic not in self.topics:
            raise TopicError(topic, self.topics)

        # Set up query components
        base_url = f"https://api.presseportal.de/api/article/topic/{topic}"
        url, params, headers = self.build_request(base_url, media, start, limit, teaser)

        # Query API and map results
        stories_list = self.get_data(url=url, params=params, headers=headers)

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
        if media and not media in self.media_types:
            raise MediaError(media, self.media_types)

        # Check if keywords are supported by API
        for keyword in keywords:
            if keyword not in self.keywords:
                raise KeywordError(keyword, self.keywords)

        # Construct keyword string
        keywords_str = ",".join(keywords)

        # Set up query components
        base_url = f"https://api.presseportal.de/api/article/keyword/{keywords_str}"
        url, params, headers = self.build_request(base_url, media, start, limit, teaser)

        # Query API and map results
        stories_list = self.get_data(url=url, params=params, headers=headers)

        return stories_list

    def get_investor_relations_news(
        self, news_type: str, start: int = 0, limit: int = 50, teaser: bool = False,
    ) -> List[Story]:
        """https://api.presseportal.de/doc/ir/list
        """

        # Check if investor relations news type is supported by API
        if news_type not in self.investor_relations_news_types:
            raise NewsTypeError(news_type, self.investor_relations_news_types)

        # Set up query components
        base_url = f"https://api.presseportal.de/api/ir/{news_type}"
        url, params, headers = self.build_request(
            base_url=base_url, media=None, start=start, limit=limit, teaser=teaser
        )

        # Query API and map results
        stories_list = self.get_data(url=url, params=params, headers=headers)

        return stories_list
