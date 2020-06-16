"""Error classes for PyPresseportal"""

from typing import List, Union

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
    """Raised if the returned data is invalid.

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
    """Raised if requests raises an error.

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
    """Raised if media type is not supported.

    Args:
        media (str): Unsupported media type.
        allowed (list): List of media types allowed by API.
    """

    def __init__(self, media: Union[str, None], allowed: List[str]):
        self.message = f"Media type '{media}' not permitted. API only accepts {', '.join(allowed)}."
        super().__init__(self.message)


class RegionError(Exception):
    """Raised if region is not supported.

    Args:
        region (str): Unsupported region.
        allowed (list): List of regions allowed by API.
    """

    def __init__(self, region: str, allowed: list):
        self.message = (
            f"Region '{region}' not permitted. API only accepts {', '.join(allowed)}."
        )
        super().__init__(self.message)


class TopicError(Exception):
    """Raised if topic is not supported.

    Args:
        topic (str): Unsupported topic.
        allowed (list): List of topics allowed by API.
    """

    def __init__(self, topic: str, allowed: list):
        self.message = (
            f"Topic '{topic}' not permitted. API only accepts {', '.join(allowed)}."
        )
        super().__init__(self.message)


class KeywordError(Exception):
    """Raised if keyword is not supported.

    Args:
        keyword (str): Unsupported keyword.
        allowed (list): List of keyword allowed by API.
    """

    def __init__(self, keyword: str, allowed: list):
        self.message = (
            f"Keyword '{keyword}' not permitted. API only accepts {', '.join(allowed)}."
        )
        super().__init__(self.message)


class NewsTypeError(Exception):
    """Raised if investor relations news type is not supported.

    Args:
        news_type (str): Unsupported investor relations news type.
        allowed (list): List of investor relations news type allowed by API.
    """

    def __init__(self, news_type: str, allowed: list):
        self.message = f"Investor relations news type '{news_type}' not permitted. API only accepts {', '.join(allowed)}."
        super().__init__(self.message)
