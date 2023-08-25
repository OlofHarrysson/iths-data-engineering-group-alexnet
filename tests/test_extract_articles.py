import unittest
from unittest.mock import Mock, mock_open, patch

from bs4 import BeautifulSoup

from newsfeed import extract_articles


class TestExtractArticles(unittest.TestCase):
    def test_create_uuid_from_string(self):
        title = "Sample Title"
        uuid_value = extract_articles.create_uuid_from_string(title)
        self.assertIsNotNone(uuid_value)
        self.assertIsInstance(uuid_value, str)

    def test_extract_articles_from_xml(self):
        sample_xml = """
        <rss>
            <channel>
                <item>
                    <title>Sample Title</title>
                    <description>Sample Description</description>
                    <link>https://example.com</link>
                    <pubDate>Thu, 22 Aug 2023 14:00:00 GMT</pubDate>
                    <content:encoded><![CDATA[<p>This is a sample blog content.</p>]]></content:encoded>
                </item>
            </channel>
        </rss>
        """

        parsed_xml = BeautifulSoup(sample_xml, "xml")
        articles = extract_articles.extract_articles_from_xml(parsed_xml)

        self.assertEqual(len(articles), 1)
        article = articles[0]
        self.assertEqual(article.title, "Sample Title")
        self.assertEqual(article.description, "Sample Description")
        self.assertEqual(article.link, "https://example.com")
        self.assertEqual(article.blog_text.strip(), "This is a sample blog content.")

    @patch("builtins.open", new_callable=mock_open)
    def test_load_metadata(self, mock_open_func):
        mock_content = '<?xml version="1.0" encoding="utf-8"?>\n<xml>mocked content</xml>'
        mock_open_func().read.return_value = mock_content
        result = extract_articles.load_metadata("mock_blog")
        self.assertEqual(str(result), mock_content)

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.mkdir")
    def test_save_articles(self, mock_mkdir, mock_open_func):
        mock_article = Mock()
        mock_article.get_filename.return_value = "sample_filename.txt"

        extract_articles.save_articles([mock_article], "mit")
        mock_open_func.assert_called()


if __name__ == "__main__":
    unittest.main()
