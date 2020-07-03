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
    @classmethod
    def setup_class(cls):
        cls.test_response_obj = APIReponses()
        cls.api_obj = PresseportalApi(API_KEY)

    def test_build_request(self):
        media = "image"
        start = 0
        limit = 10
        teaser = False
        base_url = "https://api.presseportal.de/api/article/publicservice"
        url, params, headers = PresseportalApi.build_request(
            self.api_obj,
            base_url=base_url,
            media=media,
            start=start,
            limit=limit,
            teaser=teaser,
        )
        expected_header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"
        }
        assert headers == expected_header
        assert url == f"{base_url}/{media}"
        assert params == {
            "api_key": API_KEY,
            "format": "json",
            "start": str(start),
            "limit": str(limit),
            "teaser": str(int(teaser)),
        }

    @responses.activate
    def test_get_stories(self):

        self.test_response_obj.set_mock_response("get_stories")
        stories = self.api_obj.get_stories()

        test_object = stories[0]
        self.assertEqual(len(stories), 1)
        self.assertEqual(test_object.id, "1234567")
        self.assertEqual(test_object.body, "Test body, full text.")
        self.assertEqual(test_object.keywords, ["Umwelt", "Klimaschutz"])
        self.assertEqual(test_object.image[0]["name"], "test_image_url.jpg")

    def test_get_stories_wrong_media_type(self):
        stories = self.api_obj.get_stories(media="radio")
        self.assertEqual(stories, [])

    @responses.activate
    def test_get_stories_parse_error(self):

        self.test_response_obj.set_mock_response("empty_json")

        with pytest.raises(ApiDataError):
            _ = self.api_obj.get_stories()

    @responses.activate
    def test_get_stories_auth_failed(self):

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

    # def test_company_info_mapping(self):
    #     # read file
    #     with open("replies/company_info.json", "r") as in_file:
    #         data = in_file.read()
    #     # parse json
    #     json_data = json.loads(data)
    #     # test
    #     test_object = Company(json_data["company"])
    #     assert test_object.id == "100255"
    #     assert test_object.url == "https://www.presseportal.de/nr/100255"
    #     assert test_object.name == "Test GmbH"
    #     assert test_object.homepage == "http://www.test.test"

    # def test_office_info_mapping(self):
    #     # read file
    #     with open("replies/office_info.json", "r") as in_file:
    #         data = in_file.read()
    #     # parse json
    #     json_data = json.loads(data)
    #     # test
    #     test_object = Company(json_data["office"])
    #     assert test_object.id == "115876"
    #     assert test_object.url == "https://www.presseportal.de/blaulicht/nr/115876"
    #     assert test_object.name == "Feuerwehr Test"
    #     assert test_object.homepage == "http://www.test.test"


class TestErrors:
    @classmethod
    def setup_class(cls):
        # cls.test_response_obj = APIReponses()
        cls.api_obj = PresseportalApi(API_KEY)

    def test_api_data_error(self):
        # read file
        with open("tests/replies/authentification_failed_error.json", "r") as in_file:
            data = in_file.read()
        # parse json
        json_data = json.loads(data)
        # map file
        with pytest.raises(ApiDataError) as excinfo:
            _ = Story(json_data)
        error_msg = "The API returned invalid data or data could not be processed"
        assert error_msg in str(excinfo.value)

    def test_key_error(self):
        api_key = "12"
        with pytest.raises(ApiKeyError) as excinfo:
            _ = PresseportalApi(api_key)
        error_msg = f"Valid API key required. Key '{api_key}' is not valid."
        assert error_msg == str(excinfo.value)

    # # This will slow down tests because requests waits for a timeout before raising the error
    # def test_connection_fail(self):
    #     invalid_url = "https://invalid.incorrect"
    #     with pytest.raises(ApiConnectionFail) as excinfo:
    #         PresseportalApi.get_data(
    #             self.api_obj, url=invalid_url, params={}, headers={}
    #         )
    #     error_msg = "The API could not be reached"
    #     assert error_msg in str(excinfo.value)

    def test_region_error(self):
        invalid_region = "invalid"
        error_msg = f"Region '{invalid_region}' not permitted. API only accepts"
        with pytest.raises(RegionError) as excinfo:
            PresseportalApi.get_public_service_specific_region(
                self.api_obj, region_code=invalid_region
            )
        assert error_msg in str(excinfo.value)

    def test_topic_error(self):
        invalid_topic = "invalid"
        error_msg = f"Topic '{invalid_topic}' not permitted. API only accepts"
        with pytest.raises(TopicError) as excinfo:
            PresseportalApi.get_stories_topic(self.api_obj, topic=invalid_topic)
        assert error_msg in str(excinfo.value)

    def test_keyword_error(self):
        invalid_keyword = "invalid"
        error_msg = f"Keyword '{invalid_keyword}' not permitted. API only accepts"
        with pytest.raises(KeywordError) as excinfo:
            PresseportalApi.get_stories_keywords(
                self.api_obj, keywords=[invalid_keyword]
            )
        assert error_msg in str(excinfo.value)

    def test_news_type_error(self):
        invalid_news_type = "invalid"
        error_msg = f"'{invalid_news_type}' not permitted. API only accepts"
        with pytest.raises(NewsTypeError) as excinfo:
            PresseportalApi.get_investor_relations_news(
                self.api_obj, news_type=invalid_news_type
            )
        assert error_msg in str(excinfo.value)

    def test_search_term_error(self):
        invalid_search_term = "no"
        error_msg = "not permitted. Search term must be"
        with pytest.raises(SearchTermError) as excinfo:
            PresseportalApi.get_entity_search_results(
                self.api_obj, search_term=invalid_search_term
            )
        assert error_msg in str(excinfo.value)
