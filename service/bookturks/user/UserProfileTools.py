import os
from django.conf import settings
from django.utils import timezone

from dropbox.exceptions import ApiError

from service.bookturks.dropbox_adapter.DropboxClient import DropboxClient
from service.bookturks.models.UserProfileModel import UserProfileModel
from service.bookturks.models.NotificationModel import NotificationModel
from service.bookturks.models.QuizResultModel import QuizResultModel


class UserProfileTools:
    """
    User tools
    """

    def __init__(self):
        self.dbx = DropboxClient(settings.DROPBOX_CLIENT)

    @staticmethod
    def create_filename(user_model):
        """
        Creates filename to store the profile in storage
        :param user_model:
        :return:
        """
        if not user_model or not user_model.username or not str(user_model.username).strip():
            raise ValueError("UserProfileTools:create_filename:Invalid User model passed")
        return "".join(["/user_profile/", str(user_model.username), "_profile.JSON"])

    @staticmethod
    def create_profile(user_model):
        """
        Creates new profile for a first time user
        :return:
        """
        notifications = list()
        notifications.append(NotificationModel(sender="BookTurks",
                                               level=NotificationModel.Level.SUCCESS,
                                               message="Congratulations on your new Account !",
                                               time=timezone.now()))
        notifications.append(NotificationModel(sender="BookTurks",
                                               level=NotificationModel.Level.INFO,
                                               message="You have unfinished items in your profile",
                                               time=timezone.now()))
        return UserProfileModel(user_model=user_model,
                                display_picture="",
                                attempted_quiz=list(),
                                my_quiz=list(),
                                notifications=notifications)

    @staticmethod
    def create_content(user_profile):
        """
        Return a json object
        :param user_profile:
        :return:
        """
        if not user_profile:
            raise ValueError("UserProfile:create_content:Invalid User profile passed")
        return user_profile.to_json()

    def upload_profile(self, content, filename):
        """
        Uploads the profile to storage
        :param content:
        :param filename:
        :return:
        """
        try:
            return_code = self.dbx.upload_file(content=content, filename=filename)
        except Exception as err:
            # TODO: Handle this properly
            # print (err)
            return None
        return return_code

    def download_profile_content(self, user_model):
        """
        Downloads the user and returns the content as JSON
        :param user_model:
        :return:
        """
        if not user_model or not user_model.username:
            raise ValueError("Invalid model is passed. User not recognized.")
        try:
            path, metadata = self.dbx.get_file(filename=UserProfileTools.create_filename(user_model))
        except ApiError:
            # TODO: Something went wrong here. Handle this properly
            raise
        # Open files with the keyword 'with' only
        with open(path, 'r') as user_file:
            content = ""
            # Read in chunks to avoid memory over utilization
            while True:
                temp_data = user_file.read(1000)
                if not temp_data:
                    break
                content += temp_data
            user_file.close()
        os.remove(path)
        content = UserProfileModel.from_json(content)
        return content

    def get_profile(self, user_model):
        """
        Gets the user profile if present.
        Else creates a new user profile
        :param user_model:
        :return:
        """
        try:
            user_profile_model = self.download_profile_content(user_model)
        except ApiError as err:
            metadata, error = err.args
            if error.is_path():
                if error.get_path().is_not_found():
                    user_profile_model = UserProfileTools.create_profile(user_model)
                    rc = self.upload_profile(filename=UserProfileTools.create_filename(user_model),
                                             content=UserProfileTools.create_content(user_profile_model))
                    if rc:
                        return user_profile_model
            return None
        return user_profile_model
