from .parameter_types import *

from .test import *
from .root import *
from .message import *
from .question_branch import *
from .fifty_fifty_branch import *

from .loop import *

from .wait import *


def new(name, parent_block=None):
    try:
        cls = globals()[name]
    except KeyError:
        raise ValueError("node not found. identifier: %s" % name)
    # end except
    ret = cls(parent_block=parent_block)
    return ret
