import json
from django.utils import timezone
from dateutil.parser import parse


class NotificationModel:
    """
    Notifications Model
    """

    class Level:
        """
        Level of notification alertness
        """
        DEFAULT = 'DEFAULT'
        INFO = 'INFO'
        WARN = 'WARN'
        DANGER = 'DANGER'
        REMINDER = 'REMINDER'
        SUCCESS = 'SUCCESS'

    def __init__(self, sender, level, message, time):
        # String full name
        self.sender = sender
        # Level of alertnemss
        self.level = level
        # Message of the notification
        self.message = message
        # Time of sending the notification
        self.time = time

    def to_json(self):
        model = dict()
        model['sender'] = self.sender
        model['level'] = self.level
        model['message'] = self.message
        model['time'] = str(self.time)
        return json.dumps(model, ensure_ascii=False)

    @staticmethod
    def from_json(json_object):
        model = json.loads(json_object)
        NotificationModel(sender=model.get('sender'),
                          level=model.get('level'),
                          message=model.get('message'),
                          time=parse(model.get('time')).astimezone(timezone.utc))
