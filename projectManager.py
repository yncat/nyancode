import block
import node


class ProjectManager:
    def __init__(self):
        self.root_node = None
        self.browsing_block = None
        self.scope_level = 1

    def new(self):
        """新規作成"""
        self.root_node = node.new("RootNode")
        self.root_node.setSingleChildBlock("block", block.Block())
        self.browsing_block = self.root_node.child_blocks["block"]

    def getList(self):
        lst = []
        for elem in self.browsing_block:
            lst.append((elem.display_name, str(
                elem.parameters), str(elem.child_blocks)))
        # end for
        return lst
