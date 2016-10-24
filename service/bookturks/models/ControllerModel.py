class ControllerModel(object):
    """
    Model for View.
    """

    def __init__(self, view, redirect, context=None):
        self.view = view
        self.redirect = redirect
        self.context = context if context else dict()
