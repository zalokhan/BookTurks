import json
from service.models import Quiz
from service.bookturks.models.EventModel import EventModel


class QuizCompleteModel:
    """
    Quiz Complete Model
    """

    def __init__(self, quiz_model, quiz_data=None, quiz_form=None, attempts=None, pass_percentage=None,
                 event_model=None):
        # Quiz Model from the database
        self.quiz_model = quiz_model
        # Raw quiz data (editable)
        self.quiz_data = quiz_data
        # HTML quiz form attempted by user
        self.quiz_form = quiz_form
        # Number of retries (-1 = infinite)
        self.attempts = attempts
        # pass % for the quiz
        self.pass_percentage = pass_percentage
        # Event of quiz
        self.event_model = event_model

    def __str__(self):
        return "quiz_model : {0}\n" \
               "quiz_data : {1}\n" \
               "quiz_form : {2}\n" \
               "retries : {3}\n" \
               "pass_percentage: {4}\n" \
               "event_model : {5}".format(str(self.quiz_model),
                                          str(self.quiz_data),
                                          str(self.quiz_form),
                                          str(self.attempts),
                                          str(self.pass_percentage),
                                          str(self.event_model))

    def to_json(self):
        model = dict()
        model['quiz_model'] = self.quiz_model.to_json()
        model['quiz_data'] = self.quiz_data
        model['quiz_form'] = self.quiz_form
        model['attempts'] = self.attempts
        model['pass_percentage'] = self.pass_percentage
        model['event_model'] = self.event_model.to_json()
        return json.dumps(model, ensure_ascii=False)

    @staticmethod
    def from_json(json_object):
        model = json.loads(json_object)
        event_model = model.get('event_model')
        if event_model is not 'None':
            event_model = EventModel.from_json(event_model)
        else:
            event_model = None
        return QuizCompleteModel(quiz_model=Quiz.from_json(model.get('quiz_model')),
                                 quiz_data=model.get('quiz_data'),
                                 quiz_form=model.get('quiz_form'),
                                 attempts=model.get('attempts'),
                                 pass_percentage=model.get('pass_percentage'),
                                 event_model=event_model)
