import json

from service.models import Quiz


class QuizResultModel:
    """
    Contains the result of the quiz
    """

    def __init__(self, quiz_model=None, answer_key=None, user_answer_key=None,
                 correct_answers=None, wrong_answers=None, correct_score=None, wrong_score=None, max_score=None,
                 attempts=1):
        # Quiz being attempted
        self.quiz_model = quiz_model
        # Correct answer key set by the quiz owner
        self.answer_key = answer_key
        # Answer attempted by the user
        self.user_answer_key = user_answer_key
        # Right answers
        self.correct_answers = correct_answers
        # Wrong answers
        self.wrong_answers = wrong_answers
        # Answers correct score
        self.correct_score = correct_score
        # Wrong  answers score
        self.wrong_score = wrong_score
        # Maximum possible score
        self.max_score = max_score
        # Number of attempts user has made on this quiz
        self.attempts = attempts

    def __str__(self):
        return "".join(["QUIZ : ", str(self.quiz_model), "\n",
                        "ANSWER KEY : ", str(self.answer_key), "\n",
                        "USER KEY : ", str(self.user_answer_key), "\n",
                        "CORRECT ANSWERS : ", str(self.correct_answers), "\n",
                        "WRONG ANSWERS : ", str(self.wrong_answers), "\n",
                        "CORRECT SCORE : ", str(self.correct_score), "\n",
                        "WRONG SCORE : ", str(self.wrong_score), "\n",
                        "MAX SCORE : ", str(self.max_score), "\n",
                        "ATTEMPTS : ", str(self.max_score)])

    def to_json(self):
        model = dict()
        model['quiz_model'] = self.quiz_model.to_json()
        model['answer_key'] = self.answer_key
        model['user_answer_key'] = self.user_answer_key
        model['correct_answers'] = self.correct_answers
        model['wrong_answers'] = self.wrong_answers
        model['correct_score'] = self.correct_score
        model['wrong_score'] = self.wrong_score
        model['max_score'] = self.max_score
        model['attempts'] = self.max_score
        return json.dumps(model, ensure_ascii=False)

    @staticmethod
    def from_json(json_object):
        model = json.loads(json_object)
        return QuizResultModel(quiz_model=Quiz.from_json(model.get('quiz_model')),
                               answer_key=model.get('answer_key'),
                               user_answer_key=model.get('user_answer_key'),
                               correct_answers=model.get('correct_answers'),
                               wrong_answers=model.get('wrong_answers'),
                               correct_score=model.get('correct_score'),
                               wrong_score=model.get('wrong_score'),
                               max_score=model.get('max_score'),
                               attempts=model.get('attempts'))
