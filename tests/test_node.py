# -*- coding: utf-8 -*-

import unittest
import node
import node.test


class TestNode(unittest.TestCase):
    def test_new(self):
        n = node.new("TestNode")
        self.assertTrue(isinstance(n, node.test.TestNode))
        self.assertRaises(ValueError, lambda: node.new("nonexistent"))

    def test_parameterOrBlankString(self):
        n = node.new("TestNode")
        n.setSingleParameter("test", "test_content")
        self.assertEqual("test_content", n.parameterOrBlankString("test"))
        self.assertEqual("", n.parameterOrBlankString("nonexistent"))


