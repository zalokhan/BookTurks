class QuizResultModel:
    """
    Contains the result of the quiz
    """

    def __init__(self, user_model=None, quiz_model=None, answer_key=None, user_answer_key=None,
                 correct_answers=None, wrong_answers=None, correct_score=None, wrong_score=None, max_score=None):
        # User attempting the quiz
        self.user_model = user_model
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
