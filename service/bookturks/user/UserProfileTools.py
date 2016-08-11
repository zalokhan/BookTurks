import os

from django.conf import settings
from django.utils import timezone
from dropbox.exceptions import ApiError

from service.bookturks.dropbox_adapter.DropboxClient import DropboxClient
from service.bookturks.models.NotificationModel import NotificationModel
from service.bookturks.models.UserProfileModel import UserProfileModel

# App Config
from service.apps import ServiceConfig
from service.bookturks.Constants import USER_PROFILE, USER_PROFILE_MODEL
from service.bookturks.serializer import serialize, deserialize


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
        return "".join([USER_PROFILE, "/", str(user_model.username), "_profile"])

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
        Return a serialized object
        :param user_profile:
        :return:
        """
        if not user_profile:
            raise ValueError("UserProfile:create_content:Invalid User profile passed")
        return serialize(user_profile)

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
        with open(path, 'rb') as user_file:
            content = user_file.read()
            user_file.close()
        os.remove(path)
        deserialized_content = deserialize(content)
        return deserialized_content

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
            if error.is_path() and error.get_path().is_not_found():
                user_profile_model = UserProfileTools.create_profile(user_model)
                rc = self.upload_profile(filename=UserProfileTools.create_filename(user_model),
                                         content=UserProfileTools.create_content(user_profile_model))
                if rc:
                    return user_profile_model
            return None
        return user_profile_model

    def save_profile(self, session):
        """
        Called by threads. Saves the profile to storage asynchronously
        :param session:
        :return:
        """
        if not session or not session.get(USER_PROFILE_MODEL):
            raise ValueError("UserProfileTool: Error in saving the profile to dropbox")
        user_profile_model = session.get(USER_PROFILE_MODEL)
        future = ServiceConfig.profile_sync_thread_pool.submit(self.upload_profile,
                                                               self.create_content(user_profile_model),
                                                               UserProfileTools.create_filename(
                                                                   user_profile_model.user_model))
        # Returning for debugging and assertions
        return future

    @staticmethod
    def save_attempted_quiz_profile(session, quiz_result_model):
        """
        Saves the quiz result to the profile if not already present
        :return:
        """
        if not session or not quiz_result_model:
            return False
        user_profile_model = session.get(USER_PROFILE_MODEL)
        attempted_quiz = user_profile_model.attempted_quiz
        for quiz_result in attempted_quiz:
            if quiz_result.quiz_model.quiz_id == quiz_result_model.quiz_model.quiz_id:
                quiz_result_model.attempts = quiz_result.attempts + 1
                attempted_quiz.remove(quiz_result)
                break
        attempted_quiz.append(quiz_result_model)
        session.save()
        return True

    @staticmethod
    def save_my_quiz_profile(session, quiz_model):
        """
        Saves the quiz model to the profile.
        :return:
        """
        # Do not check for duplicates as that is already taken care of.
        if not session or not quiz_model:
            return False
        user_profile_model = session.get(USER_PROFILE_MODEL)
        my_quiz = user_profile_model.my_quiz
        my_quiz.append(quiz_model)
        session.save()
        return True

    @staticmethod
    def remove_my_quiz_profile(session, quiz_model):
        """
        Removes the quiz model from the profile.
        :return:
        """
        # Do not check for duplicates as that is already taken care of.
        if not session or not quiz_model:
            return False
        user_profile_model = session.get(USER_PROFILE_MODEL)
        my_quiz = user_profile_model.my_quiz
        for quiz in my_quiz:
            if quiz.quiz_id == quiz_model.quiz_id:
                my_quiz.remove(quiz)
                session.save()
                return True
        return False
