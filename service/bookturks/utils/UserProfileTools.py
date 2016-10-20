from django.conf import settings
from django.utils import timezone
from dropbox.exceptions import ApiError

from service.bookturks.Constants import USER_PROFILE_MODEL
from service.bookturks.dropbox_adapter.DropboxClient import DropboxClient
from service.bookturks.models import NotificationModel, UserProfileModel
from service.bookturks.storage_handlers import UserProfileStorageHandler


class UserProfileTools:
    """
    User tools
    """

    def __init__(self):
        self.dbx = DropboxClient(settings.DROPBOX_CLIENT)

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
    def get_profile(user_model):
        """
        Gets the user profile if present.
        Else creates a new user profile
        :param user_model:
        :return:
        """
        user_profile_storage_handler = UserProfileStorageHandler()
        try:
            user_profile_model = user_profile_storage_handler.download_profile_content(user_model)
        except ApiError as err:
            metadata, error = err.args
            if error.is_path() and error.get_path().is_not_found():
                user_profile_model = UserProfileTools.create_profile(user_model)
                rc = user_profile_storage_handler.upload_profile(
                    filename=UserProfileStorageHandler.create_filename(user_model.username),
                    content=UserProfileStorageHandler.create_content(user_profile_model))
                if rc:
                    return user_profile_model
            return None
        return user_profile_model

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
