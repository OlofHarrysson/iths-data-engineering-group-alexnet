# import json

# import pytest
# from bs4 import BeautifulSoup

# from newsfeed import extract_articles


# @pytest.fixture
# def mock_open(monkeypatch):
#     json_data = json.dumps({"DB_username": "username", "DB_password": "password"})

# @pytest.mark.parametrize(
#     "input_str, expected_result", [("Sample Title", str), ("", None), (None, None)]
# )
# def test_create_uuid_from_string(input_str, expected_result):
#     result = extract_articles.create_uuid_from_string(input_str)
#     if expected_result:
#         assert result is not None
#         assert isinstance(result, expected_result)
#     else:
#         assert result is None

#     def mock_open_func(*args, **kwargs):
#         return [json_data]
#     monkeypatch.setattr("builtins.open", mock_open_func)


# @pytest.mark.parametrize(
#     "input_str, expected_result", [("Sample Title", str), ("", None), (None, None)]
# )
# def test_create_uuid_from_string(input_str, expected_result, mock_open):
#     result = extract_articles.create_uuid_from_string(input_str)
#     if expected_result:
#         assert result is not None
#         assert isinstance(result, expected_result)
#     else:
#         assert result is None


# def test_extract_mit_articles_from_xml(mock_open):
#     sample_xml = "<rss><channel></channel></rss>"
#     parsed_xml = BeautifulSoup(sample_xml, "xml")
#     articles = extract_articles.extract_mit_articles_from_xml(parsed_xml, "sample blog_name")
#     assert articles == []


# def test_extract_tensorflow_articles_from_xml(mock_open):

# def test_extract_mit_articles_from_xml():
#     sample_xml = "<rss><channel></channel></rss>"
#     parsed_xml = BeautifulSoup(sample_xml, "xml")
#     articles = extract_articles.extract_mit_articles_from_xml(parsed_xml, "sample blog_name")
#     assert articles == []


# def test_extract_tensorflow_articles_from_xml():

#     sample_xml = "<rss><channel></channel></rss>"
#     parsed_xml = BeautifulSoup(sample_xml, "xml")
#     articles = extract_articles.extract_tensorflow_articles_from_xml(parsed_xml, "sample blog_name")
#     assert articles == []
