import json
from service.models import User, Quiz
from service.bookturks.models.QuizResultModel import QuizResultModel, NotificationModel


class UserProfileModel:
    """
    Contains the User Profile.
    Do not store objects here.
    """

    def __init__(self, user_model=None, display_picture=None, attempted_quiz=None, my_quiz=None, notifications=None):
        # User Model
        self.user_model = user_model
        # Display picture
        self.display_picture = display_picture
        # List of quizzes attempted (quiz result models)
        self.attempted_quiz = attempted_quiz
        # List of my quizzes
        self.my_quiz = my_quiz
        # List of Notifications
        self.notifications = notifications

    def __str__(self):
        return "User : {0} \n" \
               "Display Picture : {1} \n" \
               "Attempted quizzes : {2} \n" \
               "My quizzes : {3} \n" \
               "Notifications : {4}".format(str(self.user_model), self.display_picture, self.attempted_quiz,
                                            self.my_quiz, self.notifications)

    def to_json(self):
        model = dict()
        model['user_model'] = self.user_model.to_json()
        model['display_picture'] = self.display_picture
        model['attempted_quiz'] = [quiz.to_json() for quiz in self.attempted_quiz]
        model['my_quiz'] = [quiz.to_json() for quiz in self.my_quiz]
        model['notifications'] = [notification.to_json() for notification in self.notifications]
        return json.dumps(model, ensure_ascii=False)

    @staticmethod
    def from_json(json_object):
        model = json.loads(json_object)
        return UserProfileModel(user_model=User.from_json(model.get('user_model')),
                                display_picture=model.get('display_picture'),
                                attempted_quiz=[QuizResultModel.from_json(quiz) for quiz in
                                                model.get('attempted_quiz')],
                                my_quiz=[Quiz.from_json(quiz) for quiz in model.get('my_quiz')],
                                notifications=[NotificationModel.from_json(notification) for notification in
                                               model.get('notification')])
