from service.bookturks.adapters.QuizTagAdapter import QuizTagAdapter


class QuizTools(object):
    """
    Checks eligibility
    """

    @staticmethod
    def unlink_all_tags_of_quiz(quiz):
        """
        Unlinks all the tags of the quiz
        :param quiz:
        :return:
        """
        for tag in quiz.quiztag_set.all():
            QuizTagAdapter.unlink_quiz(tag_name=tag.tag_name, quiz_id=quiz.quiz_id)

    @staticmethod
    def check_attempt_eligibility(user_profile_model, quiz_complete_model, quiz_id):
        """
        Checks if the user still has number of attempts left for this quiz
        :return:
        """
        # Infinite number of attempts.
        if int(quiz_complete_model.attempts) is -1:
            return

        attempted = 0
        for quiz_result in user_profile_model.attempted_quiz:
            if quiz_result.quiz_model.quiz_id == quiz_id:
                attempted = quiz_result.attempts
                break
        if attempted >= int(quiz_complete_model.attempts):
            raise ValueError("Attempts exceeded.")
