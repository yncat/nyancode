from .test import *
from .root import *
from .message import *


def new(name):
    try:
        cls = globals()[name]
    except KeyError:
        raise ValueError("node not found. identifier: %s" % name)
    # end except
    ret = cls()
    return ret
