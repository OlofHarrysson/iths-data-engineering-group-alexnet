import json
import os
from datetime import datetime
from urllib.parse import unquote

from sqlalchemy import MetaData, create_engine, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from newsfeed.datatypes import BlogSummary
from newsfeed.summarize import summarize_text, summary_types, translate_title

with open("api-key.json") as file:
    data = json.load(file)

    username = data["DB_username"]
    password = data["DB_password"]

server_name = "postgres"
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

    if path is None and data is None:
        raise ValueError(
            "Error no data was provided, need to provide either 'path' or 'data' object or both."
        )

    if path != None:
        data_list += get_data(path)
        print(data_list)

    if data != None:
        data_list += data

    metadata = MetaData()
    metadata.reflect(engine)

    Base = automap_base(metadata=metadata)

    Base.prepare()

    Blog_articles = Base.classes.bloginfo

    Session = sessionmaker(bind=engine)
    session = Session()

    for item in data_list:
        new_record = Blog_articles(
            unique_id=item.unique_id,
            title=item.title,
            description=item.description,
            link=item.link,
            blog_text=item.blog_text,
            blog_name=item.blog_name,
            published=item.published,
            timestamp=item.timestamp,
        )

        print(f"processing article: '{item.unique_id}'")

        try:
            session.add(new_record)
            session.commit()
            # parse_summary(item)
        except IntegrityError as e:
            print(f"Error: {e}. Skipping duplicate row with ID {item.unique_id}.")
            session.rollback()  # Rollback the transaction to keep the database in a consistent state

        print(f"successfully stored article: '{item.unique_id}' into database")


def parse_summary(article):
    print("Starting to summarize article.")

    metadata = MetaData()
    metadata.reflect(engine)

    Base = automap_base(metadata=metadata)

    Base.prepare()

    Blog_summaries = Base.classes.blog_summaries

    Session = sessionmaker(bind=engine)
    session = Session()

    for key in summary_types:
        if key == "swedish" and article["blog_name"] != "mit":
            continue

        if datetime.strptime(article["published"], "%Y-%m-%d") < datetime(2023, 9, 5):
            break

        print(f"Sums up '{article['unique_id']} with type: {key}'")

        new_record = Blog_summaries(
            unique_id=article["unique_id"],
            translated_title=translate_title(article["title"], key)
            if key not in ["normal", "non_technical"]
            else None,
            summary=summarize_text(article["blog_text"], suffix=key),
            type_of_summary=key,
        )

        print("Summation success!")

        session.add(new_record)
        session.commit()

    session.close()
