from datetime import date, datetime

import pydantic


# Note: The code below uses Python type hints to clarify the variable types.
# More info: https://realpython.com/lessons/type-hinting/
class BlogInfo(pydantic.BaseModel):
    unique_id: str
    title: str
    description: str
    link: str
    blog_text: str
    published: date
    timestamp: datetime

    def get_filename(self):
        # filename = f'{self.title.replace(" ", "_")}.json'
        filename = f"{self.unique_id}_{self.title.replace(' ', '_')}.json"

        return filename


# Class for summary of articles in different technical levels of language
class BlogSummary(pydantic.BaseModel):
    unique_id: str
    translated_title: str = None
    summary: str = None
    type_of_summary: str = "DefaultSummaryType"

    def get_filename(self):
        filename = f"{self.unique_id}_{self.type_of_summary.replace(' ', '_')}.json"

        return filename
