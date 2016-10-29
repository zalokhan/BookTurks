from django.utils import timezone

from service.bookturks.adapters import QuizTagAdapter


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
    def check_quiz_eligibility(user_profile_model, quiz_complete_model, quiz_id):
        """
        Checks the following :
        If the user still has number of attempts left for this quiz
        If the quiz falls in the valid event window
        :return:
        """

        # We can shift this check before downloading the file.
        quiz_model = quiz_complete_model.quiz_model

        # These can be null since null=true in the models.Quiz
        if quiz_model.event_start and quiz_model.event_end:
            current_time = timezone.now()
            if quiz_model.event_start > current_time:
                time_left = str(quiz_model.event_start - current_time)
                raise ValueError("Quiz Event not yet started. {0} left".format(time_left))
            if quiz_model.event_end < current_time:
                raise ValueError("Quiz Expired")

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
