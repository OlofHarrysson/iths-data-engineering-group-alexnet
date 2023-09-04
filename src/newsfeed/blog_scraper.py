import json
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from newsfeed.extract_articles import create_uuid_from_string

### Actual blog text is stored under: ui-richtext


def get_openai_blog_articles(url="https://openai.com/blog"):
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to get data from {url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")  # Parse the HTML as a string

    # Find article elements
    articles = soup.find_all("a", class_="ui-link")
    print(f"Found {len(articles)} article elements.")

    # This will store our article data
    article_data = []

    for article in articles:
        title_element = article.find("h3", {"class": "f-subhead-2"})  # Find the title element
        date_element = soup.find("span", {"aria-hidden": "true"})

        if date_element:
            print(
                f"Found an article with date: {date_element.get_text().strip()}"
            )  # Also strip to clean the text

        # Filter for articles from 2023
        if date_element and "2023" in date_element.get_text().strip():
            if title_element:
                title = title_element.get_text()
                article_url = "https://openai.com" + article["href"]

                print(f"Fetching article: {title}, URL: {article_url}")

                # Fetch the article
                article_response = requests.get(article_url)
                article_soup = BeautifulSoup(article_response.text, "html.parser")

                # Find the article text
                article_text_elements = article_soup.find_all("div", {"class": "ui-richtext"})

                article_texts = []
                for article_text_element in article_text_elements:
                    paragraphs = article_text_element.find_all("p")
                    for paragraph in paragraphs:
                        article_texts.append(
                            paragraph.get_text()
                        )  # Get the text from the paragraph

                article_content = " ".join(article_texts)  # Join the paragraphs together

                article_data.append(
                    {
                        "title": title,
                        "date": date_element.get_text().strip(),
                        "url": article_url,
                        "blog_text": article_content,
                    }
                )

    return article_data


def convertify_date(date_string):
    date_object = datetime.strptime(date_string, "%b %d, %Y")
    formatted_date = date_object.strftime("%Y-%m-%d")

    return formatted_date


# TODO: parse through BlogInfo class
def save_articles_as_json(articles, save_path):
    os.makedirs(save_path, exist_ok=True)

    for i, article in enumerate(articles):
        article_data = {
            "unique_id": create_uuid_from_string(article["title"]),
            "title": article["title"],
            "url": article["url"],
            "published": convertify_date(article["date"]),
            "blog_text": article["blog_text"],
        }
        file_name = f"article_{i+1}.json"

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
                f"{i+1}. {article['title']}\n   URL: {article['url']}\n   Date: {article['date']}\n   Content: {article['blog_text'][:100]}..."
            )
        save_path = "data/data_warehouse/openai/articles"
        save_articles_as_json(articles, save_path)
