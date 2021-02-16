import os
import block
import constants
import node
import nodeIO
import nyancode_runtime


class Manager:
    def __init__(self, logger=None):
        self.logger = logger
        self.root_node = None
        self.browsing_block = None
        self.scope_level = 1
        self.project_path = ""
        self.has_changes = False
        self.nodeIO = nodeIO.NodeIO()
        self._logDebug("Created.")

    def new(self, project_name):
        """新規作成"""
        self.root_node = node.new("RootNode")
        self.root_node.setSingleChildBlock("block", block.Block())
        self.browseRootNodeContent()
        self.project_name = project_name
        self.project_path = ""
        self.has_changes = False
        self._logDebug("Initialized a new project.")

    def getList(self):
        lst = []
        for elem in self.browsing_block:
            lst.append((elem.display_name, len(
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
        self.has_changes = True

    def deleteMultipleNodes(self, indexList):
        self.log.debug("Deleting %d nodes from block %s." %
                       (len(indexList), self.browsing_block))
        self.browsing_block.deleteMultipleNodes(indexList)
        self.has_changes = True

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

    def getNodeAt(self, index):
        """現在閲覧中のブロックの、指定したインデックスのノードを取得。"""
        return self.browsing_block.getNodeAt(index)

    def enterSubBlock(self, index, sub_block_name):
        self.scope_level += 1
        node = self.getNodeAt(index)
        self.browsing_block = node.child_blocks[sub_block_name]

    def leaveSubBlock(self):
        """現在閲覧中のブロックから出て、１個上の階層のブロックへ移動する。ブロックから出た後、復帰すべきインデックスを返す。これ以上出られない場合は None を返す。"""
        if self.scope_level == 0:
            return None
        # 出た後、今さっきまで入っていたブロックにフォーカスさせたい
        cb = self.browsing_block
        self.scope_level -= 1
        self.browsing_block = cb.parent
        # さっきまでいたブロックが含まれているノードを探す
        found = 0
        i = 0
        for elem in self.browsing_block.nodes:
            if cb in elem.child_blocks:
                found = i
                break
            # end 見つけた
            i += 1
        # end 探した
        return found

    def getBrowsingBlock(self):
        return self.browsing_block

    def _logDebug(self, msg):
        if self.logger:
            self.logger.debug(msg)
