from service.bookturks.Exceptions import AuthenticationException
from apiclient import errors

"""
Performs basic functions on files in google drive:
"""


class GoogleDriveClient:
    def __init__(self, credentials):
        self.credentials = credentials

    def upload(self, path_to_file):

        if not self.credentials:
            raise AuthenticationException

        source_files = (
            (path_to_file, None),
        )

        for filename, mimeType in source_files:
            metadata = {'name': filename}
            if mimeType:
                metadata['mimeType'] = mimeType

            try:
                result = self.credentials.files().create(body=metadata, media_body=filename).execute()
            except errors.HttpError, error:
                print "Error: GoogleDriveClient.py; upload; %s" % error
                return
            return result

    def list_all(self):

        if not self.credentials:
            raise AuthenticationException

        try:
            results = self.credentials.files().list(pageSize=100, fields="nextPageToken, files(id, name)").execute()
        except errors.HttpError, error:
            print "Error: GoogleDriveClient.py; upload; %s" % error
            return
        items = results.get('files', [])

        while results.get('nextPageToken'):
            try:
                results = self.credentials.files().list(pageSize=100, pageToken=results.get('nextPageToken'),
                                                        fields="nextPageToken, files(id, name)").execute()
            except errors.HttpError, error:
                print "Error: GoogleDriveClient.py; upload; %s" % error
                return
            items.append(results.get('files', []))

        return items

    def get_file_content(self, id):

        if not self.credentials:
            raise AuthenticationException

        try:
            file_data = self.credentials.files().get_media(fileId=id).execute()
        except errors.HttpError, error:
            print "Error: GoogleDriveClient.py; upload; %s" % error
            return
        return file_data
