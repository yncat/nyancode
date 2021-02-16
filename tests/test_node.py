# -*- coding: utf-8 -*-

import unittest
import node
import node.test
from block import *


class TestNode(unittest.TestCase):
    def test_new(self):
        n = node.new("TestNode")
        self.assertTrue(isinstance(n, node.test.TestNode))
        self.assertRaises(ValueError, lambda: node.new("nonexistent"))

    def test_new_with_parent(self):
        blk = Block()
        n = node.new("TestNode", parent_block=blk)
        self.assertEqual(blk, n.parent_block)

    def test_parameterOrBlankString(self):
        n = node.new("TestNode")
        n.setSingleParameter("test", "test_content")
        self.assertEqual("test_content", n.parameterOrBlankString("test"))
        self.assertEqual("", n.parameterOrBlankString("nonexistent"))
