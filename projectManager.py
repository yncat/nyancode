import block
import constants
import node
from logging import getLogger


class ProjectManager:
    def __init__(self):
        self.log = getLogger("%s.%s" % (constants.LOG_PREFIX, "ProjectManager"))
        self.root_node = None
        self.browsing_block = None
        self.scope_level = 1
        self.log.debug("Created.")

    def new(self):
        """新規作成"""
        self.root_node = node.new("RootNode")
        self.root_node.setSingleChildBlock("block", block.Block())
        self.browsing_block = self.root_node.child_blocks["block"]
        self.log.debug("Initialized a new project.")

    def getList(self):
        lst = []
        for elem in self.browsing_block:
            lst.append((elem.display_name, str(
                elem.parameters), str(elem.child_blocks)))
        # end for
        self.log.debug("Retrieved %d nodes from the currently browsing block %s." % (len(lst), self.browsing_block))
        return lst

    def addNodeToCurrentBlock(self, node):
        self.browsing_block.append(node)
        self.log.debug("Added node %s to the currently browsing block %s" % (node, self.browsing_block))

