import re

from bs4 import BeautifulSoup


def find_possible_titles(soup):
    # Starting point for finding article titles
    possible_titles = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    titles = [title.get_text(strip=True) for title in possible_titles if title.get_text(strip=True)]
    return titles


def find_possible_dates(html_content):
    date_patterns = [
        r"\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b",  # yyyy-mm-dd or yyyy/mm/dd
        r"\b\d{1,2}[-/]\d{1,2}[-/]\d{4}\b",  # dd-mm-yyyy or dd/mm/yyyy
        r"\b\w{3,9} \d{1,2},? \d{4}\b",  # month dd, yyyy
        r"\b\d{1,2} \w{3,9},? \d{4}\b",  # dd month, yyyy
    ]

    for pattern in date_patterns:
        date_matches = re.findall(pattern, html_content)
        if date_matches:
            return date_matches

    return []


def find_candidates(html_file_path):
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # Find possible article titles
    article_titles = find_possible_titles(soup)
    if article_titles:
        print("Possible Article Titles:")
        for title in article_titles:
            print("-> ", title)
    else:
        print("No Article Titles found.")

    # Find possible published dates
    possible_dates = find_possible_dates(html_content)
    if possible_dates:
        print("\nPossible Published Dates:")
        for date in possible_dates:
            print("-> ", date)
    else:
        print("No Published Dates found.")


if __name__ == "__main__":
    find_candidates("scrape_model/data/pages/aftonbladet_se.html")
