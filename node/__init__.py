from .test import *
from .root import *
from .message import *


def new(name):
    try:
        cls = globals()[name]
    except KeyError:
        return None
    # end except
    ret = cls()
    return ret
