import json
from node.base import *


class NodeEncoder(json.JSONEncoder):
    def default(self, o):
        if issubclass(o.__class__, BaseNode):
            return {"name": o.name, "parameters": o.parameters, "child_nodes": o.child_nodes}
        # end custom conversion
        return json.JSONEncoder.default(self, o)


class NodeIO():
    def dump(self, node):
        return json.dumps(node, cls=NodeEncoder)
