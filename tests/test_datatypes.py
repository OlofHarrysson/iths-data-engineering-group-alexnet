import datetime

import pytest
from pydantic import BaseModel

from newsfeed.datatypes import BlogInfo, BlogSummary


# test cases for blogInfo.
@pytest.mark.parametrize(
    "unique_id, title, expected_filename",
    [
        ("123", "Sample Title", "123_Sample_Title.json"),
        ("456", "Another Title", "456_Another_Title.json"),
    ],
)
def test_blogInfo_get_filename(unique_id, title, expected_filename):
    # creates a test object of class with test data.
    blog_info = BlogInfo(
        unique_id=unique_id,
        title=title,
        description="Sample Description",
        link="https://example.com",
        blog_text="This is a sample blog text.",
        blog_name="This is a sample blog name",
        published=datetime.date(2023, 8, 31),
        timestamp=datetime.datetime(2023, 8, 31, 12, 0, 0),
    )

    # checks if name is the same as expected_filename.
    assert blog_info.get_filename() == expected_filename


# test cases for blogSummary
@pytest.mark.parametrize(
    "unique_id, type_of_summary, expected_filename",
    [
        ("123", "Sample Summary", "123_Sample_Summary.json"),
        ("456", "Another Summary", "456_Another_Summary.json"),
        ("789", "Default Summary Type", "789_Default_Summary_Type.json"),
    ],
)
def test_blogSummary_get_filename(unique_id, type_of_summary, expected_filename):
    # makes a object with the test data.
    blog_summary = BlogSummary(
        unique_id=unique_id, summary="This is a sample summary.", type_of_summary=type_of_summary
    )

    # checks if filename is correct.
    assert blog_summary.get_filename() == expected_filename
