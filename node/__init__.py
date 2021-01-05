from .test import *
from .root import *
from .print import *


def new(name):
    try:
        cls = globals()[name]
    except KeyError:
        return None
    # end except
    ret = cls()
    return ret
