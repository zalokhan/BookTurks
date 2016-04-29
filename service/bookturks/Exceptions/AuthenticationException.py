class AuthenticationException(Exception):
    def __init__(self, dErrArguments):
        Exception.__init__(self, "{0}".format(dErrArguments))
        self.dErrorArguments = dErrArguments
