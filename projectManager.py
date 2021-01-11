import os
import block
import constants
import node
import nodeIO
import nyancode_runtime
from logging import getLogger


class ProjectManager:
    def __init__(self):
        self.log = getLogger(
            "%s.%s" %
            (constants.LOG_PREFIX, "ProjectManager"))
        self.root_node = None
        self.browsing_block = None
        self.scope_level = 1
        self.project_path = ""
        self.nodeIO = nodeIO.NodeIO()
        self.log.debug("Created.")

    def new(self, project_name):
        """新規作成"""
        self.root_node = node.new("RootNode")
        self.root_node.setSingleChildBlock("block", block.Block())
        self.browseRootNodeContent()
        self.project_name = project_name
        self.project_path = ""
        self.log.debug("Initialized a new project.")

    def getList(self):
        lst = []
        for elem in self.browsing_block:
            lst.append((elem.display_name, str(
                elem.parameters), len(elem.child_blocks)))
        # end for
        self.log.debug(
            "Retrieved %d nodes from the currently browsing block %s." %
            (len(lst), self.browsing_block))
        return lst

    def insertNodeToCurrentBlock(self, node, index=-1):
        index_str = str(index) if index != -1 else "last"
        self.browsing_block.insert(node, index=index)
        self.log.debug(
            "Added node %s to the currently browsing block %s (index: %s" %
            (node, self.browsing_block, index_str))

    def deleteMultipleNodes(self, indexList):
        self.log.debug("Deleting %d nodes from block %s." %
                       (len(indexList), self.browsing_block))
        self.browsing_block.deleteMultipleNodes(indexList)

    def outputProgram(self):
        return "\n".join(self.root_node.generate())

    def outputProgramForDirectRun(self):
        return "\n".join(self.root_node.generate(for_direct_run=True))

    def outputProject(self):
        return self.nodeIO.dump(self.root_node)

    def getProjectName(self):
        if self.project_path == "":
            return ""
        # end no project name
        return os.path.basename(self.project_path).split(".")[0]

    def mustSaveAs(self):
        return self.project_path == ""

    def saveAs(self, project_path):
        self.project_path = project_path
        self.save()

    def save(self):
        with open(self.project_path, "w", encoding="UTF-8") as f:
            f.write(self.outputProject())

    def savePythonProgram(self, path):
        with open(path, "w", encoding="UTF-8") as f:
            f.write(self.outputProgram())

    def load(self, path):
        with open(path, "r", encoding="UTF-8") as f:
            p = f.read()
        # end with
        self.root_node = self.nodeIO.load(p)
        self.project_path = path
        self.browseRootNodeContent()

    def browseRootNodeContent(self):
        self.browsing_block = self.root_node.child_blocks["block"]

    def run(self):
        exec(self.outputProgramForDirectRun(), {"nyancode": nyancode_runtime})
