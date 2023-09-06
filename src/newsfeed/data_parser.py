import json
import os
from urllib.parse import unquote

from sqlalchemy import create_engine, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.automap import automap_base

from newsfeed.datatypes import BlogSummary
from newsfeed.summarize import summarize_text, summary_types, translate_title

with open("api-key.json") as file:
    data = json.load(file)

    username = data["DB_username"]
    password = data["DB_password"]

server_name = "localhost"
database_name = "postgres"

# postgreSQL database connection URL
DB_URL = f"postgresql://{username}:{password}@{server_name}/{database_name}"

print("Connecting to database using URL string:")

try:
    engine = create_engine(DB_URL)
    with engine.connect() as connection:
        print(f"Successfully connected to {database_name}!")
except Exception as e:
    print("Error while connecting to database:\n")
    print(e)

Base = automap_base()
Base.prepare(engine, reflect=True)


def get_data(path: str) -> list:
    if os.path.isfile(path):
        with open(path) as data:
            return [json.load(data)]

    if os.path.isdir(path):
        data_list = []

        files = os.listdir(path)

        for file in files:
            with open(os.path.join(path, file)) as data:
                data_list.append(json.load(data))

        return data_list

    raise ValueError(f"Error: '{path}' is not a path to a folder or file.")


def store_in_database(path: str = None, data: [] = None):
    data_list = []
    article_table = "bloginfo"
    summary_table = "blog_summaries"

    if path is None and data is None:
        raise ValueError(
            "Error no data was provided, need to provide either 'path' or 'data' object or both."
        )

    if path != None:
        data_list += get_data(path)
        print(data_list)

    if data != None:
        data_list.append[data]

    db_table = Base.classes.get(article_table)

    for item in data_list:
        query = insert(db_table).values(**item)

        with engine.connect() as conn:
            try:
                result = conn.execute(query)
                parse_summary(item, summary_table)
                conn.commit()
            except IntegrityError as e:
                print(f"Error: {e}. Skipping duplicate row with ID {item['unique_id']}.")
                conn.rollback()  # Rollback the transaction to keep the database in a consistent state


def parse_summary(article: object, summary_table: str):
    summary_list = []

    summary_tabel = Base.classes.get(summary_tabel)

    for key in summary_types:
        if article.blog_name != "mit" and key == "swedish":
            pass

        blog_summary = BlogSummary(**article)

        blog_summary.summary = summarize_text(article["blog_text"], suffix=summary_types[key])

        # checks if it should translate the title.
        if key not in ["normal", "non_technical"]:
            blog_summary.translated_title = translate_title(article["title"], key)

        # Only static text (e.g. "English Simplified", "Swedish Technical")
        blog_summary.type_of_summary = key

        summary_list.append(blog_summary)

    with engine.connect() as conn:
        for summary in summary_list:
            query = insert(summary_table).values(**summary)

            try:
                result = conn.execute(query)
                conn.commit()
            except IntegrityError as e:
                print(f"Error: {e}. Skipping duplicate row with ID {summary['unique_id']}.")
                conn.rollback()  # Rollback the transaction to keep the database in a consistent state


store_in_database(
    path="data/data_warehouse/ts/articles/1ec205c0-dbb8-522b-8838-0f6302734c32_A_new_Kaggle_competition_to_help_parents_of_deaf_children_learn_sign_language.json"
)
