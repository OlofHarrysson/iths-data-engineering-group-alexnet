import json

from sqlalchemy import *
from sqlalchemy.ext.automap import automap_base


def connect_to_db():
    with open("api-key.json") as file:
        data = json.load(file)

        username = data["DB_username"]
        password = data["DB_password"]
        server_name = data["DB_server_name"]
        database_name = data["DB_database_name"]

    connection_string = f"postgresql://{username}:{password}@localhost/{database_name}"
    print(f"Connecting to database using string: {connection_string}")

    try:
        engine = create_engine(connection_string)

        print(f"Successfully connected to {database_name}!")

        metadata = MetaData()
        metadata.reflect(engine)

        Base = automap_base(metadata=metadata)

        Base.prepare()

        return engine, Base

    except Exception as e:
        print(f"Error while connecting to database:\n {e}")
