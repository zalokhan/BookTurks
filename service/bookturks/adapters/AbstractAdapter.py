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

    @staticmethod
    @abstractmethod
    def create_and_save_model():
        """
        Creates a new model instance and saves in database
        :return:
        """
        pass

    @staticmethod
    @abstractmethod
    def create_model():
        """
        Creates model
        :return:
        """

    @staticmethod
    @abstractmethod
    def exists():
        """
        Checks if model already exists in database
        :return:
        """
        pass
