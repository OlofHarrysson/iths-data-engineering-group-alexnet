import json
import logging

from sqlalchemy import *
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import declarative_base, sessionmaker

from newsfeed.db_engine import connect_to_db

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


class BotHistory(Base):
    __tablename__ = "bot_history"

    publish_id = Column(Integer, primary_key=True, autoincrement=True)
    unique_id = Column(String(255), ForeignKey("bloginfo.unique_id"))
    type_of_summary = Column(String(255), server_default=text("'DefaultSummaryType'"))
    publish_stamp = Column(TIMESTAMP)

    __table_args__ = (
        UniqueConstraint("unique_id", "type_of_summary", name="unique_summary_per_published_type"),
    )


def create_table():
    try:
        engine, _ = connect_to_db()
        session = sessionmaker(bind=engine)

    except Exception as e:
        print(f"Error while connecting to database:\n {e}")
        logger.error(f"Error while connecting to database or creating tables: {e}")

    # Check if tables exist, else create it.
    inspector = inspect(engine)

    if (
        not inspector.has_table("bloginfo")
        or not inspector.has_table("blog_summaries")
        or not inspector.has_table("bot_history")
    ):
        Base.metadata.create_all(engine)
        print("Tables created successfully.")
    else:
        print("Tables already exist.")


def main():
    logging.basicConfig(level=logging.INFO)
    create_table()


if __name__ == "__main__":
    main()
