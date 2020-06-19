"""Error handling for PyPresseportal
"""

from typing import Union

import requests


class ApiKeyError(Exception):
    """Raised if no API key is provided.

    Args:
        api:key (str): Invalid API key.
    """

    def __init__(self, api_key: str):
        self.message = f"Valid API key required. Key '{api_key}' is not valid."
        super().__init__(self.message)


class ApiDataError(Exception):
    """Raised if the API returned invalid data.

    Args:
        msg (str, optional): Custom error message. Defaults to None.
    """

    def __init__(self, msg: str = None):
        self.message = (
            f"The API returned invalid data or data could not be processed. {msg}"
        )
        super().__init__(self.message)


class ApiError(Exception):
    """Raised if API returns an error.

    Args:
        error_code (str): Error code returned by API.
        error_msg (str): Error message returned by API.
    """

    def __init__(self, error_code: str, error_msg: str):

        self.message = f"The API returned error code {error_code} ({error_msg})."
        super().__init__(self.message)


class ApiConnectionFail(Exception):
    """Raised if ``requests`` raises an error.

    Args:
        error_msg (Union[ requests.exceptions.ConnectionError, requests.exceptions.TooManyRedirects, requests.exceptions.Timeout, ]): Error raised by requests package.
    """

    def __init__(
        self,
        error_msg: Union[
            requests.exceptions.ConnectionError,
            requests.exceptions.TooManyRedirects,
            requests.exceptions.Timeout,
        ],
    ):
        self.message = f"The API could not be reached ({str(error_msg)})."
        super().__init__(self.message)


class MediaError(Exception):
    """Raised if media type is not supported. List of media types: `<https://api.presseportal.de/en/doc/value/media>`_

    Args:
        media (str): Unsupported media type.
        allowed (list): List of media types allowed by API.
    """

    def __init__(self, media: Union[str, None], allowed: tuple):
        self.message = f"Media type '{media}' not permitted. API only accepts {', '.join(allowed)}."
        super().__init__(self.message)


class RegionError(Exception):
    """Raised if region is not supported. List of regions: `<https://api.presseportal.de/en/doc/value/region>`_

    Args:
        region (str): Unsupported region.
        allowed (list): List of regions allowed by API.
    """

    def __init__(self, region: str, allowed: tuple):
        self.message = (
            f"Region '{region}' not permitted. API only accepts {', '.join(allowed)}."
        )
        super().__init__(self.message)


class TopicError(Exception):
    """Raised if topic is not supported. List of topics: `<https://api.presseportal.de/en/doc/value/topic>`_

    Args:
        topic (str): Unsupported topic.
        allowed (list): List of topics allowed by API.
    """

    def __init__(self, topic: str, allowed: tuple):
        self.message = (
            f"Topic '{topic}' not permitted. API only accepts {', '.join(allowed)}."
        )
        super().__init__(self.message)


class KeywordError(Exception):
    """Raised if keyword is not supported. List of keywords: `<https://api.presseportal.de/en/doc/value/keyword>`_

    Args:
        keyword (str): Unsupported keyword.
        allowed (list): List of keyword allowed by API.
    """

    def __init__(self, keyword: str, allowed: tuple):
        self.message = (
            f"Keyword '{keyword}' not permitted. API only accepts {', '.join(allowed)}."
        )
        super().__init__(self.message)


class NewsTypeError(Exception):
    """Raised if investor relations news type is not supported. List of news types: `<https://api.presseportal.de/en/doc/value/ir_type>`_

    Args:
        news_type (str): Unsupported investor relations news type.
        allowed (list): List of investor relations news type allowed by API.
    """

    def __init__(self, news_type: str, allowed: tuple):
        self.message = f"Investor relations news type '{news_type}' not permitted. API only accepts {', '.join(allowed)}."
        super().__init__(self.message)


class SearchTermError(Exception):
    """Raised if search term is not supported.

    Args:
        search_term (str): Unsupported search term.
    """

    def __init__(self, search_term: str):
        self.message = f"Search term '{search_term}' not permitted. Search term must be at least 3 characters long."
        super().__init__(self.message)


class SearchEntityError(Exception):
    """Raised if entity for search is not supported.

    Args:
        entity (str): Unsupported entity.
    """

    def __init__(self, search_term: str):
        self.message = f"Can not search for entity '{search_term}', entity must be either 'company' or 'office'."
        super().__init__(self.message)
