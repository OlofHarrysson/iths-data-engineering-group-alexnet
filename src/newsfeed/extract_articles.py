import argparse
import string
import uuid
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

from newsfeed.datatypes import BlogInfo


def create_uuid_from_string(title):
    if title is None or title == "":
        return None
    assert isinstance(title, str)
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, title))


def sanitize_filename(filename):  # Required for Windows users in teams
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return "".join(c if c in valid_chars else "_" for c in filename)


def load_metadata(blog_name):
    metadata_path = Path("data/data_lake") / blog_name / "metadata.xml"
    with open(metadata_path, encoding="utf-8") as f:
        xml_text = f.read()
    parsed_xml = BeautifulSoup(xml_text, "xml")
    return parsed_xml


def extract_mit_articles_from_xml(parsed_xml, blog_name):
    articles = []
    for item in parsed_xml.find_all("item"):
        raw_blog_text = item.find("encoded").text
        soup = BeautifulSoup(raw_blog_text, "html.parser")
        blog_text = soup.get_text()
        title = item.title.text if item.title else None
        unique_id = create_uuid_from_string(title)
        article_info = BlogInfo(
            unique_id=unique_id,
            title=title,
            description=item.description.text if item.description else None,
            link=item.link.text if item.link else None,
            blog_text=blog_text,
            blog_name=blog_name,
            published=pd.to_datetime(item.pubDate.text).date() if item.pubDate else None,
            timestamp=datetime.now(),
        )
        articles.append(article_info)
    return articles


def extract_tensorflow_articles_from_xml(parsed_xml, blog_name):
    articles = []
    for item in parsed_xml.find_all("item"):
        encoded_element = item.find("encoded")
        raw_blog_text = encoded_element.text if encoded_element else ""

        title = item.title.text if item.title else ""
        unique_id = create_uuid_from_string(title)

        link = item.link.text if item.link else None
        if link:
            blog_text = fetch_blog_content(link)
        else:
            blog_text = None

        article_info = BlogInfo(
            unique_id=unique_id,
            title=title,
            description=item.description.text if item.description else None,
            link=link,
            blog_text=blog_text,
            blog_name=blog_name,
            published=pd.to_datetime(item.pubDate.text).date() if item.pubDate else None,
            timestamp=datetime.now(),
        )

        if blog_text and title:  # only add articles with text and title
            articles.append(article_info)

    return articles


def fetch_blog_content(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        article_div = soup.find("div", class_="tensorsite-detail__body")

        if article_div:
            paragraphs = article_div.find_all("p")
            article_text = " ".join(p.get_text() for p in paragraphs if p.get_text())
            return article_text

    except Exception as e:
        print(f"Failed to fetch {link}: {e}")

    return None


def save_articles(articles, blog_name):
    save_dir = Path("data/data_warehouse", blog_name, "articles")
    save_dir.mkdir(exist_ok=True, parents=True)
    for article in articles:
        sanitized_filename = sanitize_filename(article.get_filename())
        save_path = save_dir / sanitized_filename
        with open(save_path, "w") as f:
            f.write(article.json(indent=2))


def main(blog_name):
    print(f"Processing {blog_name}")
    parsed_xml = load_metadata(blog_name)

    if blog_name == "mit":
        articles = extract_mit_articles_from_xml(parsed_xml, blog_name)
    elif blog_name == "ts":
        articles = extract_tensorflow_articles_from_xml(parsed_xml, blog_name)
    else:
        print("Invalid blog_name. Supported names are 'mit' and 'ts'")
        return

    save_articles(articles, blog_name)
    print(f"Done processing {blog_name}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--blog_name", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(blog_name="ts")
