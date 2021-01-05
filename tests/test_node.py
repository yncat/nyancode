# -*- coding: utf-8 -*-

import unittest
import node
import node.test


class TestNode(unittest.TestCase):
    def test_new(self):
        n = node.new("TestNode")
        self.assertTrue(isinstance(n, node.test.TestNode))
        n2 = node.new("nonexistent")
        self.assertIsNone(n2)
