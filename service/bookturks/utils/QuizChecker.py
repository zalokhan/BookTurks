from service.bookturks.models import QuizResultModel


class QuizChecker(object):
    """
    Checks quiz and generates result
    """

    @staticmethod
    def compare_quiz_dict(answer_key, user_answer_key):
        """
        Compares the 2 dictionaries. Only works with quiz dicts
        :param answer_key:
        :param user_answer_key:
        :return: right answers, wrong answers
        """
        correct_answers = list()
        wrong_answers = list()
        for key in answer_key.keys():
            l_ak = answer_key.get(key)
            l_uak = user_answer_key.get(key)
            if not l_uak:
                wrong_answers.append(key)
            elif l_ak != l_uak:
                wrong_answers.append(key)
            else:
                correct_answers.append(key)
        return correct_answers, wrong_answers

    @staticmethod
    def get_quiz_result(quiz_model, answer_key, user_answer_key):
        """
        Checks and returns the result of the quiz
        :param quiz_model:
        :param answer_key:
        :param user_answer_key:
        :return:
        """
        if 'csrfmiddlewaretoken' in user_answer_key:
            del user_answer_key['csrfmiddlewaretoken']
        if 'csrfmiddlewaretoken' in answer_key:
            del answer_key['csrfmiddlewaretoken']
        max_score = len(answer_key.keys())

        # Compares the answer key and the solution.
        correct_answers, wrong_answers = QuizChecker.compare_quiz_dict(answer_key, user_answer_key)
        result = QuizResultModel(quiz_model=quiz_model,
                                 answer_key=answer_key,
                                 user_answer_key=user_answer_key,
                                 correct_answers=correct_answers,
                                 wrong_answers=wrong_answers,
                                 correct_score=len(correct_answers),
                                 wrong_score=max_score - len(correct_answers),
                                 max_score=max_score)
        return result
