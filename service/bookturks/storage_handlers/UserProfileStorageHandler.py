import os

from django.conf import settings
from dropbox.exceptions import ApiError

from service.apps import ServiceConfig
from service.bookturks.Constants import USER_PROFILE, USER_PROFILE_MODEL
from service.bookturks.dropbox_adapter.DropboxClient import DropboxClient
from service.bookturks.serializer import serialize, deserialize


class UserProfileStorageHandler(object):
    """
    Storage handler for User Profiles
    """

    def __init__(self):
        self.dbx = DropboxClient(settings.DROPBOX_CLIENT)

    @staticmethod
    def create_filename(username):
        """
        Creates filename to store the profile in storage
        :param username:
        :return:
        """
        if not username or not username.strip():
            raise ValueError("UserProfileTools:create_filename:Invalid username passed")
        return "".join([USER_PROFILE, "/", username, "_profile"])

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
            path, metadata = self.dbx.get_file(filename=UserProfileStorageHandler.create_filename(user_model.username))
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
                                                               UserProfileStorageHandler.create_filename(
                                                                   user_profile_model.user_model.username))
        # Returning for debugging and assertions
        return future

    def delete_profile_from_storage(self, username):
        """
        Deletes the users profile from the storage.
        Should not be used !
        :param username:
        :return:
        """
        if not username:
            raise ValueError("DeleteProfile : username invalid")

        filename = self.create_filename(username)
        try:
            self.dbx.delete_file(filename)
        except ApiError:
            raise ValueError("UserProfile file not found in storage.")
