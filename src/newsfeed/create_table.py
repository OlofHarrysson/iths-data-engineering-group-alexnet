import json
import logging

from sqlalchemy import *
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
logger = logging.getLogger(__name__)


# Custom classes to define the SQL tables
class BlogInfo(Base):
    __tablename__ = "bloginfo"

    unique_id = Column(String(255), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    link = Column(String(255))
    blog_text = Column(Text)
    blog_name = Column(String(255))
    published = Column(Date)
    timestamp = Column(TIMESTAMP)


class BlogSummaries(Base):
    __tablename__ = "blog_summaries"

    summary_id = Column(Integer, primary_key=True, autoincrement=True)
    unique_id = Column(String(255), ForeignKey("bloginfo.unique_id"))
    translated_title = Column(String(255))
    summary = Column(Text)
    type_of_summary = Column(String(255), server_default=text("'DefaultSummaryType'"))

    __table_args__ = (
        UniqueConstraint("unique_id", "type_of_summary", name="unique_summary_per_type"),
    )


def create_table():
    with open("api-key.json") as file:
        data = json.load(file)

        username = data["DB_username"]
        password = data["DB_password"]
        server_name = data["DB_server_name"]
        database_name = data["DB_database_name"]

    connection_string = f"postgresql://{username}:{password}@{server_name}/{database_name}"
    print(f"Connecting to database using string: {connection_string}")
    logger.info(f"Connecting to database using string: {connection_string}")

    try:
        engine = create_engine(connection_string)
        session = sessionmaker(bind=engine)

        print(f"Successfully connected to {DB_database_name}!")
        logger.info(f"Successfully connected to {database_name} and created tables.")

    except Exception as e:
        print(f"Error while connecting to database:\n {e}")
        logger.error(f"Error while connecting to database or creating tables: {e}")

    # Check if tables exist, else create it.
    inspector = inspect(engine)

    if not inspector.has_table("bloginfo") or not inspector.has_table("blog_summaries"):
        Base.metadata.create_all(engine)
        print("Tables created successfully.")
    else:
        print("Tables already exist.")


def main():
    logging.basicConfig(level=logging.INFO)
    create_table()


if __name__ == "__main__":
    main()
