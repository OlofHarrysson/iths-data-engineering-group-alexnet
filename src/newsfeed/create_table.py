import json

from sqlalchemy import (
    TIMESTAMP,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    create_engine,
    inspect,
    text,
)
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


# table class
class BlogInfo(Base):
    __tablename__ = "bloginfo"

    unique_id = Column(String(255), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    link = Column(String(255))
    blog_text = Column(Text)
    blog = Column(String(255))
    published = Column(Date)
    timestamp = Column(TIMESTAMP)


# table class
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
    # gets password and username.
    with open("api-key.json") as file:
        data = json.load(file)

        username = data["DB_username"]
        password = data["DB_password"]

    # server name and db name.
    server_name = "localhost"
    database_name = "postgres"

    # postgreSQL database connection URL
    DB_URL = f"postgresql://{username}:{password}@{server_name}/{database_name}"

    print("Connecting to database using URL string:")

    # try to connect to db.
    try:
        engine = create_engine(DB_URL)
        session = sessionmaker(bind=engine)

        print(f"Successfully connected to {database_name}!")

    except Exception as e:
        print("Error while connecting to database:\n")
        print(e)

    # inspector object to check if tables exist.
    inspector = inspect(engine)

    # creates tables if they dont exist.
    if not inspector.has_table("bloginfo") or not inspector.has_table("blog_summaries"):
        Base.metadata.create_all(engine)
        print("Tables created successfully.")
    else:
        print("Tables already exist.")
