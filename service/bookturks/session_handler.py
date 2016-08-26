def session_insert_keys(session, **kwargs):
    """
    Insert keys to the session
    :param session:
    :param kwargs:
    :return:
    """
    for key in kwargs:
        session[key] = kwargs[key]
    session.save()


def session_remove_keys(session, *args):
    """
    REmove the keys from session
    :param session:
    :param args:
    :return:
    """
    for key in args:
        if session.get(key):
            session.pop(key)
    session.save()


def session_clear(session):
    """
    Clears all the keys
    :param session:
    :return:
    """
    session.clear()
    session.save()
