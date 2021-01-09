import json
import node
from node.base import *
from block import Block


class NodeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Block):
            return o.nodes
        if issubclass(o.__class__, BaseNode):
            return {
                "name": o.name,
                "parameters": o.parameters,
                "child_blocks": o.child_blocks}
        # end custom conversion
        return json.JSONEncoder.default(self, o)


class NodeIO():
    def dump(self, node):
        return json.dumps(node, cls=NodeEncoder)

    def load(self, in_json):
        o = json.loads(in_json)
        return self._load(o)

    def _load(self, o):
        ret = node.new(o["name"])
        for name, value in o["parameters"].items():
            ret.setSingleParameter(name, value)
        # end set parameters
        for name, value in o["child_blocks"].items():
            ret.setSingleChildBlock(name, self._loadBlock(value))
        # end set child nodes
        return ret

    def _loadBlock(self, o):
        blk = Block()
        for elem in o:
            blk.insert(self._load(elem))
        # end for
        return blk
