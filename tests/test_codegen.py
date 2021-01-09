# -*- coding: utf-8 -*-

import unittest
import node
from block import Block


class TestCodegen(unittest.TestCase):
    def test_root(self):
        r = node.new("RootNode")
        p = node.new("PrintNode")
        p.setSingleParameter("message", "hello")
        blk = Block()
        blk.insert(p)
        r.setSingleChildBlock("block", blk)
        generated = r.generate()
        self.assertEqual(generated[0], "# generated by nyancode.")
        self.assertEqual(generated[1], "print(\"hello\")")

    def test_print(self):
        n = node.new("PrintNode")
        n.setSingleParameter("message", "meow")
        generated = n.generate()
        self.assertEqual("print(\"meow\")", generated[0])
