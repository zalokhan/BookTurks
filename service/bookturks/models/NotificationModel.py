class NotificationModel(object):
    """
    Notifications Model
    """

    class Level(object):
        """
        Level of notification alertness
        """
        DEFAULT = 'default'
        INFO = 'info'
        WARN = 'warn'
        DANGER = 'danger'
        SUCCESS = 'success'

    def __init__(self, sender, level, message, time):
        # String full name
        self.sender = sender
        # Level of alertnemss
        self.level = level
        # Message of the notification
        self.message = message
        # Time of sending the notification
        self.time = time

    def __str__(self):
        return "SENDER : {0}\n" \
               "LEVEL : {1}\n" \
               "MESSAGE : {2}\n" \
               "TIME : {3}".format(str(self.sender),
                                   str(self.level),
                                   str(self.message),
                                   str(self.time))
