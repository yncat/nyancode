import node
from .base import *
from .root import *


def new(name):
    try:
        cls = globals()[name]
    except KeyError:
        return None
    # end except
    ret = cls()
    return ret


def generateFromBlock(blk, indent_level=0):
    code = []
    for elem in blk.nodes:
        g = new(elem.name)
        code.extend(g.generate(elem), indent_level)
