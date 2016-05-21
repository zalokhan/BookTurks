from abc import ABCMeta, abstractmethod


class AbstractAdapter():
    """
    Abstract adapter class
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        """
        Abstract init
        """
        pass

    @abstractmethod
    def create_and_save_model(self):
        """
        Creates a new model instance and saves in database
        :return:
        """
        pass

    @abstractmethod
    def create_model(self):
        """
        Creates model
        :return:
        """

    @abstractmethod
    def exists(self):
        """
        Checks if model already exists in database
        :return:
        """
        pass
