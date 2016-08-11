class EventModel(object):
    """
    Event Model
    """

    def __init__(self, start_time=None, end_time=None):
        # Start time of event
        self.start_time = start_time
        # End time of event
        self.end_time = end_time

    def __str__(self):
        return "start_time : {0}\n" \
               "end_time : {1}".format(str(self.start_time),
                                       str(self.end_time))
