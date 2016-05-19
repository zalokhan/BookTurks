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
