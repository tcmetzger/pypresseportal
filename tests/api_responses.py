import os
import responses


DEEP_SEARCH_URL = "http://www.zillow.com/webservice/GetDeepSearchResults.htm"
PROPERTY_DETAIL_URL = "http://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm"

JSON_RESPONSE = {
    "story_mapping": {
        "url": "https://api.presseportal.de/api/article/all?api_key=NO_KEY_NEEDED_DUE_TO_MOCKING_API&format=json&start=0&limit=50&teaser=0",
        "file": "get_public_service_news.json"
    },
    "entity_search": {
        "url": "https://api.presseportal.de/api/article/all?api_key=NO_KEY_NEEDED_DUE_TO_MOCKING_API&format=json&start=0&limit=50&teaser=0",
        "file": "entity_search.json"
    },
}


class APIReponses(object):
    @staticmethod
    def load_response(key):
        BASE_PATH = "tests/replies/"
        data = JSON_RESPONSE[key]
        with open(os.path.join(BASE_PATH, data["file"]), "r") as content_file:
            content = content_file.read()
        return data["url"], content

    def get(self, key):
        url, content = self.load_response(key)
        responses.add(
            responses.GET,
            url,
            body=content,
            content_type="application/javascript",
            status=200,
        )