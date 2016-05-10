"""
Creates quizzes
Parses and checks for errors
Uploads the file to DropBox with relevant naming conventions for faster searches.
Add functions in future
"""
import json


def create_quiz(content):
    """
    Create quiz with dict contents
    :param content: Dictionary containing entire quiz
    :return: Dropbox file metadata
    """

    json_data = json.dumps(content)
    return json_data
