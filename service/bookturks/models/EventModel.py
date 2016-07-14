import json
from django.utils import timezone
from dateutil.parser import parse


class EventModel:
    """
    Event Model
    """

    def __init__(self, start_time, end_time):
        # Start time of event
        self.start_time = start_time
        # End time of event
        self.end_time = end_time

    def __str__(self):
        return "start_time : {0}\n" \
               "end_time : {1}".format(str(self.start_time),
                                       str(self.end_time))

    def to_json(self):
        model = dict()
        model['start_time'] = str(self.start_time)
        model['end_time'] = str(self.end_time)
        return json.dumps(model, ensure_ascii=False)

    @staticmethod
    def from_json(json_object):
        model = json.loads(json_object)
        return EventModel(start_time=parse(model.get('start_time')).astimezone(timezone.utc),
                          end_time=parse(model.get('end_time')).astimezone(timezone.utc))
