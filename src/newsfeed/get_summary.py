import json
import os

from newsfeed.latest_article import get_latest_article


def get_summary(summary_type) -> str:
    # id of newest article.
    article_id, title, link = get_latest_article()

    # path to summarys.
    directory_path = f"data/data_warehouse/{summary_type}"

    # list of files.
    summary_list = os.listdir(directory_path)

    # Iterates through the list of json files.
    for summary in summary_list:
        # checks if id in file name.
        if article_id in summary:
            # gets path to file.
            file_path = os.path.join(directory_path, summary)

            # reads file.
            with open(file_path, "r") as file:
                data = json.load(file)

                # returns summary.
                return data["summary"], title, link

        else:
            # if no summary was found.
            return "found no summary."
