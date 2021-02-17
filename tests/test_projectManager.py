# -*- coding: utf-8 -*-

import unittest
import block
import project
import node


def testProjectNode():
    r = node.new("RootNode")
    blk = block.Block()
    n = node.new("MessageNode")
    n.setSingleParameter("title", "title")
    n.setSingleParameter("message", "message")
    blk.insert(n)
    r.setSingleChildBlock("block", blk)
    return r


class TestProjectManager(unittest.TestCase):
    def test_new(self):
        m = project.Manager(logger=None)
        m.new("new project")
        # root nodeができている
        self.assertTrue(isinstance(m.root_node, node.RootNode))
        # root nodeの下に最初のブロックができてるか
        self.assertTrue(isinstance(
            m.root_node.child_blocks["block"], block.Block))
        # ビューで閲覧対象のブロックがルートノードのブロックになっているか
        self.assertEqual(m.root_node.child_blocks["block"], m.browsing_block)
        self.assertEqual("new project", m.project_name)  # プロジェクト名が設定されているか
        self.assertEqual("", m.project_path)  # 保存してないので、パスはまだ設定されてない
        self.assertFalse(m.has_changes)

    def test_getList(self):
        n = testProjectNode()
        m = project.Manager(logger=None)
        m.root_node = n
        m.browsing_block = n.child_blocks["block"]
        want = [
            ("メッセージを表示", 2, 0)
        ]
        self.assertEqual(want, m.getList())

    def test_insertNodeToCurrentBlock(self):
        n = testProjectNode()
        m = project.Manager(logger=None)
        m.has_changes = False
        m.root_node = n
        m.browsing_block = n.child_blocks["block"]
        n2 = node.new("MessageNode")
        n2.setSingleParameter("title", "title2")
        n2.setSingleParameter("message", "message2")
        m.insertNodeToCurrentBlock(n2)
        self.assertEqual(2, len(n.child_blocks["block"].nodes))
        want = [
            ("メッセージを表示", 2, 0),
            ("メッセージを表示", 2, 0)
        ]
        self.assertEqual(want, m.getList())
        self.assertTrue(m.has_changes)

    def test_deleteMultipleNodes(self):
        n = testProjectNode()
        m = project.Manager(logger=None)
        m.has_changes = False
        m.root_node = n
        m.browsing_block = n.child_blocks["block"]
        m.deleteMultipleNodes([0])
        self.assertEqual(0, len(n.child_blocks["block"].nodes))
        want = []
        self.assertEqual(want, m.getList())
        self.assertTrue(m.has_changes)
