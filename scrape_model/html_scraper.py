import os
import re

import requests

source_path = "scrape_model/data/urls"
source_files = [
    os.path.join(source_path, file) for file in os.listdir(source_path) if file.endswith(".txt")
]
saved_pages = "scrape_model/data/pages/"

urls = []

for file_path in source_files:
    with open(file_path, "r") as file:
        text_data = file.read()
        urls.extend(text_data.split(","))

urls.append("testing:not_an_url")

url_pattern = re.compile(r"https?://\S+")

for url in urls:
    url = url.strip()
    if url_pattern.match(url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                html_content = response.text
                print("Connection successful:", url)

                cleaned_url = re.sub(r"https?://(www\.)?", "", url)
                filename = re.sub(r"[/\:\.]", "_", cleaned_url)[:20] + ".html"

                new_dir = "scrape_model/data/pages/"
                os.makedirs(new_dir, exist_ok=True)

                with open(os.path.join(new_dir, filename), "w", encoding="utf-8") as html_file:
                    html_file.write(html_content)
            else:
                print(f"Failed to fetch content from {url}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching content from {url}: {str(e)}")
