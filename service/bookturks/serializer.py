import cPickle


def serialize(value):
    """
    Serializes the object. Using cPickle.
    :param value:
    :return:
    """
    return cPickle.dumps(value)


def deserialize(value):
    """
    Deserialize the value. Unpickle.
    :param value:
    :return:
    """
    return cPickle.loads(value)
