from django.conf import settings

MOCK_QUIZ_FILE_CONTENT = {"quiz_name": "Mock Test Quiz 1", "quiz_description": "Mock Test 101",
                     "quiz_data": "<form-template>\r\n\t<fields>\r\n\t\t<field class=\"header\" label=\"Header\" "
                                  "type=\"header\" subtype=\"h1\"></field>\r\n\t\t<field class=\"form-control select\" "
                                  "label=\"Select\" multiple=\"true\" name=\"select-1464031178941\" type=\"select\">"
                                  "\r\n\t\t\t<option value=\"option-1\">Physics</option>\r\n\t\t\t<option value=\""
                                  "option-2\">Biology</option>\r\n\t\t\t<option>Chemistry</option>\r\n\t\t\t<option>"
                                  "History</option>\r\n\t\t\t<option>English</option>\r\n\t\t</field>\r\n\t</fields>"
                                  "\r\n</form-template>",
                          "answer_key": {"select-1464031178941": ["option-1", "option-2", "Chemistry"]},
                          "quiz_form": "<div class=\"\"><h1>Header</h1></div><div class=\""
                                  "form-group field-select-1464031178941\"><label for=\"select-1464031178941\">Select  "
                                  "</label><select class=\"form-control select\" multiple=\"true\" name=\""
                                  "select-1464031178941\" type=\"select\" id=\"select-1464031178941\"><option "
                                  "value=\"option-1\">Physics</option><option value=\"option-2\">Biology</option>"
                                  "<option>Chemistry</option><option>History</option><option>English</option></select>"
                                  "</div>",
                          "quiz_owner": "test@email.com", "quiz_id": "testemailcomMockTestQuiz1"}


class MockFileList:
    """
    Mock class to mock file lists returned from dropbox
    """
    entries = ["mock_file_1", "mock_file_2", "mock_file_3"]
    has_more = False

    def __init__(self):
        return

    def __call__(self, *args, **kwargs):
        return self


def mock_dropbox(test_obj, mock_dbx):
    """
    Mock dropbox
    :param test_obj:
    :param mock_dbx:
    :return:
    """
    dbx = mock_dbx.return_value
    dbx.files_upload.return_value = "mock_id"
    test_obj.mock_file_list = MockFileList()
    dbx.files_list_folder.return_value = test_obj.mock_file_list
    dbx.files_delete.return_value = None
    # It should return an object not contents
    dbx.files_download_to_file.return_value = MOCK_QUIZ_FILE_CONTENT
    test_obj.dbx = dbx
    settings.DROPBOX_CLIENT = test_obj.dbx
