# import json
# import os
# import tempfile

# import pytest

# from newsfeed.summarize import find_file, get_save_path, open_json


# # setting up test case.
# @pytest.fixture
# def temp_test_directory():
#     temp_dir = tempfile.mkdtemp()
#     yield temp_dir
#     # Cleanup: Remove the temporary directory and its contents
#     for root, dirs, files in os.walk(temp_dir, topdown=False):
#         for file in files:
#             os.remove(os.path.join(root, file))
#         for dir in dirs:
#             os.rmdir(os.path.join(root, dir))
#     os.rmdir(temp_dir)


# # test the function.
# def test_find_file(temp_test_directory):
#     file_name_to_find = "test_file.txt"
#     file_content = "This is a test file content."
#     file_path = os.path.join(temp_test_directory, file_name_to_find)

#     # Create a test file inside the temporary directory
#     with open(file_path, "w") as f:
#         f.write(file_content)

#     found_path = find_file(file_name_to_find, temp_test_directory)
#     assert found_path == file_path


# # test for if function fails.
# def test_find_file_not_found(temp_test_directory):
#     file_name_to_find = "non_existent_file.txt"

#     found_path = find_file(file_name_to_find, temp_test_directory)
#     assert found_path is None


# """
#     Test for open_json() function. OBSOLETE
# """


# # setting up test.
# @pytest.fixture
# def temp_test_json_file():
#     temp_dir = tempfile.mkdtemp()
#     json_data = {"key": "value"}

#     json_file_path = os.path.join(temp_dir, "test_file.json")
#     with open(json_file_path, "w") as json_file:
#         json.dump(json_data, json_file)

#     yield json_file_path
#     os.remove(json_file_path)
#     os.rmdir(temp_dir)


# # test the function using the test
# def test_open_json(temp_test_json_file):
#     json_data = {"key": "value"}
#     file_path = temp_test_json_file

#     loaded_data = open_json(file_path)
#     assert loaded_data == json_data


# """
#     Test for get_save_path() function.
# """


# # test cases for get save path.
# @pytest.mark.parametrize(
#     "input_dir, expected_path",
#     [
#         ("some_directory/mit/some_subdirectory", "data/data_warehouse/mit/summaries"),
#         ("another_directory/ts/some_subdirectory", "data/data_warehouse/ts/summaries"),
#         ("random_directory/some_subdirectory", "No root path found"),
#     ],
# )

# # testing test cases.
# def test_get_save_path(input_dir, expected_path):
#     try:
#         save_path = get_save_path(input_dir)
#         assert save_path == expected_path
#     except ValueError as e:
#         assert str(e) == expected_path
