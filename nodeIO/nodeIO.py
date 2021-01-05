import json
import node
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

    def load(self, in_json):
        o = json.loads(in_json)
        return self._load(o)

    def _load(self, o):
        ret = node.new(o["name"])
        for name, value in o["parameters"].items():
            ret.setSingleParameter(name, value)
        # end set parameters
        for name, value in o["child_nodes"].items():
            ret.setSingleChildNode(name, self._load(value))
        # end set child nodes
        return ret
