import json

import pytest
from bs4 import BeautifulSoup

from newsfeed import extract_articles


@pytest.mark.parametrize(
    "input_str, expected_result", [("Sample Title", str), ("", None), (None, None)]
)
def test_create_uuid_from_string(input_str, expected_result):
    result = extract_articles.create_uuid_from_string(input_str)
    if expected_result:
        assert result is not None
        assert isinstance(result, expected_result)
    else:
        assert result is None


def test_extract_articles_from_xml_no_articles():
    sample_xml = "<rss><channel></channel></rss>"
    parsed_xml = BeautifulSoup(sample_xml, "xml")
    articles = extract_articles.extract_articles_from_xml(parsed_xml)
    assert articles == []
