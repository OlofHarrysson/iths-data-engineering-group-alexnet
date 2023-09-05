import json
import os
from urllib.parse import unquote

from sqlalchemy import create_engine, insert, text
from sqlalchemy.engine import URL
from sqlalchemy.ext.automap import automap_base

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

folder_path = "data/data_warehouse/mit/articles"

file_list = os.listdir(folder_path)
print(os.path.join(folder_path, file_list[0]))

Base = automap_base()
Base.prepare(engine, reflect=True)

db_table = Base.classes.bloginfo

with open(os.path.join(folder_path, file_list[0])) as file:
    data = json.load(file)

    unique_id = data["unique_id"]
    title = data["title"]
    description = data["description"]
    link = data["link"]
    blog_text = data["blog_text"]
    published = data["published"]
    timestamp = data["timestamp"]

query = insert(db_table).values(
    unique_id=unique_id,
    title=title,
    description=description,
    link=link,
    blog_text=blog_text,
    published=published,
    timestamp=timestamp,
)

# compiled = query.compile()

with engine.connect() as conn:
    result = conn.execute(query)
    conn.commit()
