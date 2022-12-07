import uuid


def choose(*args):
    for arg in args:
        if arg is not None:
            return arg


def get_uuid4():
    return str(uuid.uuid4())
