import pickle


def serialize(value):
    """
    Serializes the object. Using cPickle.
    :param value:
    :return:
    """
    return pickle.dumps(value)


def deserialize(value):
    """
    Deserialize the value. Unpickle.
    :param value:
    :return:
    """
    return pickle.loads(value)
