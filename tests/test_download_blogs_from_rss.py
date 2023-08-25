from unittest.mock import MagicMock, patch

from newsfeed import download_blogs_from_rss


def test_import_project() -> None:
    # Mock the response from requests.get
    mock_response = MagicMock()
    mock_response.text = "<xml>Some mock XML data here</xml>"
    mock_response.status_code = 200

    # Use the patch to replace the actual requests.get with our mock
    with patch("requests.get", return_value=mock_response):
        # Call the function under test
        download_blogs_from_rss.main(blog_name="mit")

        # Optional: add assertions here to verify the behavior of your code
        # For example, you could check if a file was created or if it has the expected content.
