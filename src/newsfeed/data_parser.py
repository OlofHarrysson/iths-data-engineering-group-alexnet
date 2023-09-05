import json
import os
from urllib.parse import unquote

from sqlalchemy import create_engine, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.automap import automap_base


def get_data(path: str) -> list:
    if os.path.isfile(path):
        with open(path) as data:
            return [json.load(data)]

    if os.path.isdir(path):
        data_list = []

        files = os.listdir(path)

        for file in files:
            with open(os.path.join(path, file)) as data:
                data_list.append(data)

        return data_list

    raise ValueError(f"Error: '{path}' is not a path to a folder or file.")


def store_in_database(table_name: str, path: str = None, data: object = None):
    data_list = []

    if path is None and data is None:
        raise ValueError(
            "Error no data was provided, need to provide either 'path' or 'data' object or both."
        )

    if path != None:
        data_list += get_data(path)

    if data != None:
        data_list.append[data]

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

    db_table = Base.classes.get(table_name)

    for item in data_list:
        query = insert(db_table).values(**item)

        with engine.connect() as conn:
            try:
                result = conn.execute(query)
                conn.commit()
            except IntegrityError as e:
                print(f"Error: {e}. Skipping duplicate row with ID {item['unique_id']}.")
                conn.rollback()  # Rollback the transaction to keep the database in a consistent state


store_in_database(
    "bloginfo",
    path="data/data_warehouse/mit/articles/26609bc3-35e4-53aa-aa63-e6f9e2456422_Bringing_the_social_and_ethical_responsibilities_of_computing_to_the_forefront.json",
)
