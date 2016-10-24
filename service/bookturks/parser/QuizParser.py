from dateutil.parser import parse
from django.utils import timezone

from service.bookturks.models import EventModel


class QuizParser(object):
    """
    Parser for Quiz components
    """

    @staticmethod
    def parse_quiz_form(quiz_form):
        """
        Removes redundant data from form
        :param quiz_form: String form data
        :return: Modified form
        """
        form_tags = quiz_form.split('<')

        # Checking if less html tags then something is wrong or empty form has been submitted
        if len(form_tags) < 10:
            raise ValueError(
                "Empty quizzes cannot be submitted. Form cannot be empty.")

        # One more check to make sure that the form submitted has relevant tags.
        # Need to avoid script attacks
        if "rendered-form" in form_tags[1] and "form action=" in form_tags[2]:
            pass
        else:
            raise ValueError(
                "Quiz form is not properly generated. Something wrong with data")

        # Removing redundant lines
        # <div rendered-form></div>
        # <form></form>
        form_tags = form_tags[3:-4]
        final_form = "<" + "<".join(form_tags)
        return final_form

    # Parser
    @staticmethod
    def get_timezone_aware_datetime(datetime):
        """
        Converts string datetime to timezone aware datetime.
        :param datetime:
        :return:
        """
        if not datetime:
            return None
        local = timezone.get_current_timezone()
        return (local.localize(parse(datetime), is_dst=None)).astimezone(timezone.utc)

    # Parser
    @staticmethod
    def get_event_model(start_event, end_event):
        """
        Creates an event model after converting the 2 date times to timezone aware.
        :param start_event: String event start date time
        :param end_event: String event end date time
        :return:
        """
        if not start_event or not end_event:
            return None
        return EventModel(start_time=QuizParser.get_timezone_aware_datetime(start_event),
                          end_time=QuizParser.get_timezone_aware_datetime(end_event))
