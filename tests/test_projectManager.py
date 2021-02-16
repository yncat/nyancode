# -*- coding: utf-8 -*-

import unittest
import block
import project
import node


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
