import datetime as dt
import json
import os


def get_latest_article() -> str:
    directory_path = "data/data_warehouse/mit/articles"

    # list of json files.
    article_list = os.listdir(directory_path)

    latest_date = None
    latest_id = None

    # Iterates through the list of json files.
    for article in article_list:
        # Gets the path of the json file.
        file_path = os.path.join(directory_path, article)

        with open(file_path, "r") as a:
            data = json.load(a)

            # Converts the date to date format.
            article_date = dt.datetime.strptime(data["published"], "%Y-%m-%d")

            # Checks if articles date is later than previous.
            if latest_date is None or article_date > latest_date:
                latest_date = article_date
                latest_id = data["unique_id"]

    return latest_id