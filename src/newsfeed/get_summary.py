import json
import os

from newsfeed.latest_article import get_latest_article
from newsfeed.summarize import create_summary_json


def find_file(file_name, folder_path):
    # list of files in folder.
    file_list = os.listdir(folder_path)

    # loops through the files.
    for file in file_list:
        # check if filename is in file.
        if file_name in file:
            # returns file path.
            return os.path.join(folder_path, file)

    # if no file was found returns none.
    return None


def get_summary(summary_type) -> str:
    # id of newest article.
    article_id = get_latest_article()

    # path to summarys.
    directory_path = f"data/data_warehouse/{summary_type}"

    # gets file path
    file = find_file(article_id, directory_path)

    # checks so file is not None.
    if file != None:
        # reads file.
        with open(file, "r") as file:
            data = json.load(file)

            # returns summary.
            return data["summary"]

    else:
        # if file is none generate a summary.
        print("found no file, creating one")
        # path to article folder and file.
        directory_path = "data/data_warehouse/mit/articles"
        file = find_file(article_id, directory_path)
        # creates a summary of article in type.
        create_summary_json(file, "data/data_warehouse", "French")

        # success message.
        return f"Successfuly cretated a summary of type {summary_type}"


print(get_summary("French"))
