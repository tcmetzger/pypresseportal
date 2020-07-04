"""Tests for methods and errors of PyPresseportal."""

import json
import os

import pytest
import unittest

import responses
from api_responses import APIReponses
from pypresseportal import Company, Office, PresseportalApi, Story
from pypresseportal.pypresseportal import Company
from pypresseportal.pypresseportal_errors import (
    ApiConnectionFail,
    ApiDataError,
    ApiError,
    ApiKeyError,
    KeywordError,
    MediaError,
    NewsTypeError,
    RegionError,
    SearchTermError,
    TopicError,
)


API_KEY = "NO_KEY_NEEDED_DUE_TO_MOCKING_API"


class TestPyPressePortalMethods(unittest.TestCase):
    """Test for PyPresseportal methods."""

    @classmethod
    def setup_class(cls):
        """Setup API warpper object."""
        cls.test_response_obj = APIReponses()
        cls.api_obj = PresseportalApi(API_KEY)

    @responses.activate
    def test_get_stories(self):
        """Test get_stories()."""
        self.test_response_obj.set_mock_response("get_stories")
        stories = self.api_obj.get_stories()

        test_object = stories[0]
        self.assertEqual(len(stories), 1)
        self.assertEqual(test_object.id, "1234567")
        self.assertEqual(test_object.body, "Test body, full text.")
        self.assertEqual(test_object.keywords, ["Umwelt", "Klimaschutz"])
        self.assertEqual(test_object.image[0]["name"], "test_image_url.jpg")

    def test_get_stories_wrong_media_type(self):
        """Test get_stories() with invalid mediatype."""
        stories = self.api_obj.get_stories(media="radio")
        self.assertEqual(stories, [])

    @responses.activate
    def test_get_stories_parse_error(self):
        """Test get_stories() with empty json."""
        self.test_response_obj.set_mock_response("empty_json")

        with pytest.raises(ApiDataError):
            _ = self.api_obj.get_stories()

    @responses.activate
    def test_get_stories_auth_failed(self):
        """Test get_stories() with invalid API key."""
        self.test_response_obj.set_mock_response("authentification_failed_error")

        with pytest.raises(ApiError) as excinfo:
            _ = self.api_obj.get_stories()

        self.assertIn(
            "The API returned error code 101 (authentification failed)",
            str(excinfo.value),
        )

    # @responses.activate
    # def test_search_results_mapping(self):

    #     self.test_response_obj.get("entity_search")
    #     stories = self.api_object.get_stories()
    #     test_object = stories[0]

    #     assert test_object.id == "1234"
    #     assert test_object.url == "https://www.presseportal.de/nr/1234"
    #     assert test_object.name == "Berlin Test AG"
    #     assert test_object.type == "company"

    def test_company_info_mapping(self):
        """Test mapping for Company class."""
        # read file
        with open("tests/replies/company_info.json", "r") as in_file:
            data = in_file.read()
        # parse json
        json_data = json.loads(data)
        # test
        test_object = Company(json_data["company"])
        assert test_object.id == "100255"
        assert test_object.url == "https://www.presseportal.de/nr/100255"
        assert test_object.name == "Test GmbH"
        assert test_object.homepage == "http://www.test.test"

    def test_office_info_mapping(self):
        """Test mapping for Office class."""
        # read file
        with open("tests/replies/office_info.json", "r") as in_file:
            data = in_file.read()
        # parse json
        json_data = json.loads(data)
        # test
        test_object = Company(json_data["office"])
        assert test_object.id == "115876"
        assert test_object.url == "https://www.presseportal.de/blaulicht/nr/115876"
        assert test_object.name == "Feuerwehr Test"
        assert test_object.homepage == "http://www.test.test"


class TestErrors:
    """Test for PyPresseportal errors."""

    @classmethod
    def setup_class(cls):
        """Setup API warpper object."""
        # cls.test_response_obj = APIReponses()
        cls.api_obj = PresseportalApi(API_KEY)

    def test_key_error(self):
        """Test ApiKeyError."""
        api_key = "12"
        with pytest.raises(ApiKeyError) as excinfo:
            _ = PresseportalApi(api_key)
        error_msg = f"Valid API key required. Key '{api_key}' is not valid."
        assert error_msg == str(excinfo.value)

    def test_region_error(self):
        """Test RegionError."""
        invalid_region = "invalid"
        error_msg = f"Region '{invalid_region}' not permitted. API only accepts"
        with pytest.raises(RegionError) as excinfo:
            PresseportalApi.get_public_service_specific_region(
                self.api_obj, region_code=invalid_region
            )
        assert error_msg in str(excinfo.value)

    def test_topic_error(self):
        """Test TopicError."""
        invalid_topic = "invalid"
        error_msg = f"Topic '{invalid_topic}' not permitted. API only accepts"
        with pytest.raises(TopicError) as excinfo:
            PresseportalApi.get_stories_topic(self.api_obj, topic=invalid_topic)
        assert error_msg in str(excinfo.value)

    def test_keyword_error(self):
        """Test KeywordError."""
        invalid_keyword = "invalid"
        error_msg = f"Keyword '{invalid_keyword}' not permitted. API only accepts"
        with pytest.raises(KeywordError) as excinfo:
            PresseportalApi.get_stories_keywords(
                self.api_obj, keywords=[invalid_keyword]
            )
        assert error_msg in str(excinfo.value)

    def test_news_type_error(self):
        """Test NewsTypeError."""
        invalid_news_type = "invalid"
        error_msg = f"'{invalid_news_type}' not permitted. API only accepts"
        with pytest.raises(NewsTypeError) as excinfo:
            PresseportalApi.get_investor_relations_news(
                self.api_obj, news_type=invalid_news_type
            )
        assert error_msg in str(excinfo.value)

    def test_search_term_error(self):
        """Test SearchTermError."""
        invalid_search_term = "no"
        error_msg = "not permitted. Search term must be"
        with pytest.raises(SearchTermError) as excinfo:
            PresseportalApi.get_entity_search_results(
                self.api_obj, search_term=invalid_search_term
            )
        assert error_msg in str(excinfo.value)
