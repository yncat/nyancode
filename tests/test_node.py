# -*- coding: utf-8 -*-

import unittest
import node
from node.base import *


class TestNode(unittest.TestCase):
    def test_new(self):
        n = node.new("BaseNode")
        self.assertTrue(isinstance(n, BaseNode))
        n2 = node.new("nonexistent")
        self.assertIsNone(n2)
