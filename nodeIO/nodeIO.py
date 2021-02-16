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
    def dump(self, node, pretty=True):
        """pretty=False にすると、改行されなくなって、全部つながったJSONができる。テスト用。"""
        indent = 2 if pretty else None
        return json.dumps(node, cls=NodeEncoder, indent=indent)

    def load(self, in_json):
        o = json.loads(in_json)
        return self._loadNode(o)

    def _loadNode(self, o, parent_block=None):
        n = node.new(o["name"], parent_block=parent_block)
        for name, value in o["parameters"].items():
            n.setSingleParameter(name, value)
        # end set parameters
        for name, value in o["child_blocks"].items():
            n.setSingleChildBlock(name, self._loadBlock(value, parent_node=n))
        # end set child nodes
        return n

    def _loadBlock(self, o, parent_node):
        blk = Block(parent_node=parent_node)
        for elem in o:
            blk.insert(self._loadNode(elem, parent_block=blk))
        # end for
        return blk
