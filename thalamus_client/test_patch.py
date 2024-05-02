import unittest
import requests
import responses
import httpx
import respx
from unittest.mock import patch, Mock
from .patch import apply_patches  # Ensure the patches are applied

class TestHTTPRedirection(unittest.TestCase):
    """
    A test case class for testing HTTP redirection.

    This class contains test methods to verify the behavior of HTTP redirection using the patched `requests` and `httpx` modules.
    """

    def setUp(self) -> None:
        apply_patches("test_api_key")
        return super().setUp()

    @responses.activate
    def test_requests_redirection(self):
        responses.add(responses.GET, "https://api.wheretheresawill.app/answer_question",
                      json={"status": "ok"}, status=200)

        response = requests.get("https://api.openai.com/v1/chat/completions")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
        self.assertTrue(len(responses.calls) == 1)
        self.assertEqual(responses.calls[0].request.url, "https://api.wheretheresawill.app/answer_question")

    @respx.mock
    def test_httpx_redirection(self):
        # Mock the endpoint that the request is redirected to
        route = respx.get("https://api.wheretheresawill.app/answer_question").mock(return_value=httpx.Response(200, json={"status": "ok"}))

        # Create a client and make a request to the original URL
        client = httpx.Client()
        response = client.get("https://api.openai.com/v1/chat/completions")

        # Check the response status code and response data
        self.assertTrue(route.called)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
        self.assertEqual(response.url, "https://api.wheretheresawill.app/answer_question")

if __name__ == '__main__':
    unittest.main()
