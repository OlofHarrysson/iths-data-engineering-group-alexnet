import datetime as dt
import json
import os
from pathlib import Path

import openai

from newsfeed.datatypes import BlogSummary

summary_types = {
    "normal": "Ignore previous prompts and summarize the text in as if it was for scientists studying AI, do this using30 words max. ",
    "non_technical": "summarize the article in non-technical text using max of 30 words. ",
    "french": "in french and in 30 words.",
    "swedish": "translate it into swedish, and use max 30 words",
}


def summarize_text(article_text, prefix="normal") -> str:
    # Get key
    with open("api-key.json") as f:
        OPENAI_API_KEY = json.load(f)

    openai.api_key = OPENAI_API_KEY["OPENAI_API_KEY"]

    base_prompt = f"Summarize the following text:\n{article_text}\n"

    if prefix == "normal":
        prompt = base_prompt + "Summary:"
    else:
        prompt = f"{prefix}, " + base_prompt + "Summary:"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"""Summarize this MIT article in a clear and simple manner suitable for a broad audience. Avoid technical jargon and keep sentences concise. Make sure a 4 year old could read and understand it. The text must simple enough that a 4 year old could read and understand it. People with no previous knowledge in technology needs to be able to read it. The english must be simple and plain, so that people with english as second language can understand it. Include descriptions for any acronyms such as AI (Artifical Intellegence). {prefix}""",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=200,
    )
    summary = response.choices[0].message["content"].strip()
    return summary


def translate_title(title, type):
    # prompt / context to chat gpt.
    conversation = [
        {"role": "system", "content": "You are a helpful assistant that translates titles."},
        {
            "role": "user",
            "content": f"Translate the following title from English to {type}: {title}",
        },
    ]

    # the response from chat gpt.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=conversation, max_tokens=50
    )

    # gets the title from the response.
    translated_title = response["choices"][0]["message"]["content"].strip()
    return translated_title


def get_save_path(input_dir):
    root_paths = {
        "mit": "data/data_warehouse/mit/summaries",
        "ts": "data/data_warehouse/ts/summaries",
        "openai": "data/data_warehouse/openai/summaries",
    }

    # check if blog is from "mit" or "ts"
    for key in root_paths:
        if key in input_dir:
            return root_paths[key]

    raise ValueError("No root path found")


# Generate new json files with BlogSummary class
def create_summary_json(input_dir, summary_type):
    # checks if type is a summary type.
    if summary_type in summary_types:
        # makes it so it can only translate "mit" blogs to swedish.
        if summary_type == "swedish" and "mit" not in input_dir:
            raise ValueError("Error: Can only translate 'Mit' blogs to Swedish.")

        # Create subdir for each summary type
        output_dir = os.path.join(get_save_path(input_dir), summary_type)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    else:
        # if no summary type was found.
        raise f"Error: '{summary_type}' is not a summary type!"

    # Set to keep track of existing output files
    existing_outputs = set(os.listdir(get_save_path(input_dir)))

    # checks if file is json.
    if input_dir.endswith(".json"):
        json_path = input_dir

        with open(json_path, "r") as file:
            json_content = json.load(file)

            blog_summary = BlogSummary(**json_content)

            blog_summary.summary = summarize_text(
                json_content["blog_text"], prefix=summary_types[summary_type]
            )

            # checks if it should translate the title.
            if summary_type not in ["normal", "non_technical"]:
                blog_summary.translated_title = translate_title(json_content["title"], summary_type)

            # Only static text (e.g. "English Simplified", "Swedish Technical")
            blog_summary.type_of_summary = summary_type

            sum_file = blog_summary.get_filename()
            new_json_path = os.path.join(get_save_path(input_dir), summary_type, sum_file)

            # Check if output already exist (Or should we overwrite?)
            if sum_file not in existing_outputs:
                with open(new_json_path, "w") as new_file:
                    json.dump(blog_summary.dict(), new_file, indent=4)
                existing_outputs.add(sum_file)

                # returns summary text.
                return blog_summary.summary, blog_summary.translated_title

            else:
                print(f"{sum_file} already exist.")


def open_json(filepath: str):
    # opens a json file and returns
    with open(filepath, "r") as file:
        data = json.load(file)

        return data


def find_file(file_name, folder_path):
    if os.path.exists(folder_path):
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


def get_latest_article(blog_identifier: str = "mit", summary_type: str = "normal") -> tuple:
    # path to articles.
    directory_path = f"data/data_warehouse/{blog_identifier}/articles"

    # list of json files.
    article_list = os.listdir(directory_path)

    latest_date = None
    latest_id = None
    latest_file_path = None
    latest_title = None
    latest_link = None

    # Iterates through the list of json files.
    for article in article_list:
        # Gets the path of the json file.
        file_path = os.path.join(directory_path, article)

        data = open_json(file_path)

        # Converts the date to date format.
        article_date = dt.datetime.strptime(data["published"], "%Y-%m-%d")

        # Checks if articles date is later than previous.
        if latest_date is None or article_date > latest_date:
            latest_date = article_date
            latest_id = data["unique_id"]
            latest_file_path = file_path
            latest_title = data["title"]
            latest_link = data["link"]

    # path to summary file.
    summary_file = find_file(
        latest_id, f"data/data_warehouse/{blog_identifier}/summaries/{summary_type}"
    )

    # if summary is not None get summary.
    if summary_file != None:
        data = open_json(summary_file)
        summary = data["summary"]

        # checks if a translated title exist.
        if data["translated_title"] != None:
            latest_title = data["translated_title"]

    # if None create summary.
    else:
        print("found no file, creating one!")
        summary, translated_title = create_summary_json(latest_file_path, summary_type)

        # checks if a translated title exist.
        if translated_title != None:
            latest_title = translated_title

    return latest_title, summary, latest_link, latest_date
