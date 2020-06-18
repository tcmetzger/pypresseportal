import json
import os
from pypresseportal.pypresseportal import Company

import pytest

from pypresseportal import PresseportalApi, Story, Company, Office
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
)

API_KEY = os.environ["API_KEY"]
api_object = PresseportalApi(API_KEY)


class TestFunctions:
    def test_build_request(self):
        media = "image"
        start = 0
        limit = 10
        teaser = False
        base_url = "https://api.presseportal.de/api/article/publicservice"
        url, params, headers = PresseportalApi.build_request(
            api_object,
            base_url=base_url,
            media=media,
            start=start,
            limit=limit,
            teaser=teaser,
        )
        assert url == f"{base_url}/{media}"
        assert params == {
            "api_key": API_KEY,
            "format": "json",
            "start": str(start),
            "limit": str(limit),
            "teaser": str(int(teaser)),
        }

    def test_story_mapping(self):
        # read file
        with open("replies/get_public_service_news.json", "r") as in_file:
            data = in_file.read()
        # parse json
        json_data = json.loads(data)
        # test
        test_object = PresseportalApi.parse_story_data(api_object, json_data)[0]
        assert test_object.id == "1234567"
        assert test_object.body == "Test message body."
        assert test_object.keywords == ["Polizei", "Kriminalität"]
        assert test_object.office_id == "12345"
        assert test_object.image[0]["name"] == "test.jpg"

    def test_search_results_mapping(self):
        # read file
        with open("replies/entity_search.json", "r") as in_file:
            data = in_file.read()
        # parse json
        json_data = json.loads(data)
        # test
        test_object = PresseportalApi.parse_search_results(api_object, json_data)[0]
        assert test_object.id == "1234"
        assert test_object.url == "https://www.presseportal.de/nr/1234"
        assert test_object.name == "Berlin Test AG"
        assert test_object.type == "company"

    def test_company_info_mapping(self):
        # read file
        with open("replies/company_info.json", "r") as in_file:
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
        # read file
        with open("replies/office_info.json", "r") as in_file:
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
    def test_api_data_error(self):
        # read file
        with open("replies/authentification_failed_error.json", "r") as in_file:
            data = in_file.read()
        # parse json
        json_data = json.loads(data)
        # map file
        with pytest.raises(ApiDataError) as excinfo:
            test_object = Story(json_data)
        error_msg = "The API returned invalid data or data could not be processed"
        assert error_msg in str(excinfo.value)

    def test_key_error(self):
        api_key = "12"
        with pytest.raises(ApiKeyError) as excinfo:
            test_object = PresseportalApi(api_key)
        error_msg = f"Valid API key required. Key '{api_key}' is not valid."
        assert error_msg == str(excinfo.value)

    # This will slow down tests because requests waits for a timeout before raising the error
    def test_connection_fail(self):
        invalid_url = "https://invalid.incorrect"
        with pytest.raises(ApiConnectionFail) as excinfo:
            PresseportalApi.get_data(api_object, url=invalid_url, params={}, headers={})
        error_msg = "The API could not be reached"
        assert error_msg in str(excinfo.value)

    def test_media_error(self):
        invalid_media = "invalid"
        error_msg = "not permitted. API only accepts"
        with pytest.raises(MediaError) as excinfo:
            PresseportalApi.get_public_service_news(api_object, media=invalid_media)
        assert error_msg in str(excinfo.value)
        with pytest.raises(MediaError) as excinfo:
            PresseportalApi.get_public_service_specific_region(
                api_object, region_code="sh", media=invalid_media
            )
        assert error_msg in str(excinfo.value)
        with pytest.raises(MediaError) as excinfo:
            PresseportalApi.get_stories(api_object, media=invalid_media)
        assert error_msg in str(excinfo.value)

    def test_region_error(self):
        invalid_region = "invalid"
        error_msg = f"Region '{invalid_region}' not permitted. API only accepts"
        with pytest.raises(RegionError) as excinfo:
            PresseportalApi.get_public_service_specific_region(
                api_object, region_code=invalid_region
            )
        assert error_msg in str(excinfo.value)

    def test_topic_error(self):
        invalid_topic = "invalid"
        error_msg = f"Topic '{invalid_topic}' not permitted. API only accepts"
        with pytest.raises(TopicError) as excinfo:
            PresseportalApi.get_stories_topic(api_object, topic=invalid_topic)
        assert error_msg in str(excinfo.value)

    def test_keyword_error(self):
        invalid_keyword = "invalid"
        error_msg = f"Keyword '{invalid_keyword}' not permitted. API only accepts"
        with pytest.raises(KeywordError) as excinfo:
            PresseportalApi.get_stories_keywords(api_object, keywords=[invalid_keyword])
        assert error_msg in str(excinfo.value)

    def test_news_type_error(self):
        invalid_news_type = "invalid"
        error_msg = f"'{invalid_news_type}' not permitted. API only accepts"
        with pytest.raises(NewsTypeError) as excinfo:
            PresseportalApi.get_investor_relations_news(
                api_object, news_type=invalid_news_type
            )
        assert error_msg in str(excinfo.value)

    def test_search_term_error(self):
        invalid_search_term = "no"
        error_msg = "not permitted. Search term must be"
        with pytest.raises(SearchTermError) as excinfo:
            PresseportalApi.get_entity_search_results(
                api_object, search_term=invalid_search_term
            )
        assert error_msg in str(excinfo.value)
