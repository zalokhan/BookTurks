class QuizCompleteModel(object):
    """
    Quiz Complete Model
    """

    def __init__(self, quiz_model, quiz_data=None, quiz_form=None, answer_key=None, attempts=-1,
                 pass_percentage=None, event_model=None, tags=None):
        # Quiz Model from the database
        self.quiz_model = quiz_model
        # Raw quiz data (editable)
        self.quiz_data = quiz_data
        # HTML quiz form attempted by user
        self.quiz_form = quiz_form
        # Answer key
        self.answer_key = answer_key
        # Number of retries (-1 = infinite)
        self.attempts = attempts
        # pass % for the quiz
        self.pass_percentage = pass_percentage
        # Event of quiz
        self.event_model = event_model
        # Quiz Tags
        self.tags = tags

    def __str__(self):
        return "quiz_model : {0}\n" \
               "quiz_data : {1}\n" \
               "quiz_form : {2}\n" \
               "retries : {3}\n" \
               "pass_percentage: {4}\n" \
               "event_model : {5}\n" \
               "tags: {6}".format(str(self.quiz_model),
                                  str(self.quiz_data),
                                  str(self.quiz_form),
                                  str(self.attempts),
                                  str(self.pass_percentage),
                                  str(self.event_model),
                                  str(self.tags))
