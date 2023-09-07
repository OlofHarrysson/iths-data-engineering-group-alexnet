import json
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from newsfeed.datatypes import BlogInfo
from newsfeed.extract_articles import create_uuid_from_string

### Actual blog text is stored under: ui-richtext


def get_openai_blog_articles(link="https://openai.com/blog"):
    response = requests.get(link)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to get data from {link}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")  # Parse the HTML as a string

    # Find article elements
    articles = soup.find_all("a", class_="ui-link")
    print(f"Found {len(articles)} article elements.")

    # This will store our article data
    article_data = []

    for article in articles:
        title_element = article.find("h3", {"class": "f-subhead-2"})  # Find the title element
        date_element = article.find("span", {"aria-hidden": "true"})

        if date_element:
            print(
                f"Found an article with date: {date_element.get_text().strip()}"
            )  # Also strip to clean the text

        # Filter for articles from 2023
        if date_element and "2023" in date_element.get_text().strip():
            if title_element:
                title = title_element.get_text()
                article_link = "https://openai.com" + article["href"]

                print(f"Fetching article: {title}, link: {article_link}")

                # Fetch the article
                article_response = requests.get(article_link)
                article_soup = BeautifulSoup(article_response.text, "html.parser")

                # Now look for the description element
                description_element = article_soup.find("div", {"class": "ui-richtext"})
                if description_element:
                    print(f"Found description: {description_element.get_text().strip()}")
                else:
                    print("No description found.")
                # Find the article text
                article_text_elements = article_soup.find_all("div", {"class": "ui-richtext"})
                description = description_element.get_text().strip()
                article_texts = []
                for article_text_element in article_text_elements:
                    paragraphs = article_text_element.find_all("p")
                    for paragraph in paragraphs:
                        article_texts.append(
                            paragraph.get_text()
                        )  # Get the text from the paragraph

                article_content = " ".join(article_texts)  # Join the paragraphs together

                # Create an object of BlogInfo
                blog_info = BlogInfo(
                    unique_id=create_uuid_from_string(title),
                    title=title,
                    description=description,
                    blog_name="OpenAI",
                    link=article_link,
                    blog_text=article_content,
                    published=datetime.strptime(
                        date_element.get_text().strip(), "%b %d, %Y"
                    ).date(),
                    timestamp=datetime.now(),
                )

                article_data.append(blog_info)

    return article_data


def save_articles_as_json(articles, save_path):
    os.makedirs(save_path, exist_ok=True)

    for i, article in enumerate(articles):
        # Serialize the BlogInfo object to JSON
        article_data = json.loads(article.json())

        file_name = article.get_filename()
        file_path = os.path.join(save_path, file_name)

        with open(file_path, "w") as json_file:
            json.dump(article_data, json_file, indent=4)
        print(f"Saved {file_path}")


if __name__ == "__main__":
    articles = get_openai_blog_articles()
    print("OpenAI Blog Articles from 2023:")

    if not articles:
        print("No articles from 2023 found.")
    else:
        for i, article in enumerate(articles):
            print(
                f"{i+1}. {article.title}\n   link: {article.link}\n   Date: {article.published}\n   Content: {article.blog_text[:10]}..."
            )

        save_path = "data/data_warehouse/openai/articles"
        save_articles_as_json(articles, save_path)


## Todo,
# 1. Fix so that everything works through main
# 2. Fix so that BlogInfo class is used within blog_scraper.py
