# -*- coding: utf-8 -*-

import unittest
import node
from block import Block


class TestCodegen(unittest.TestCase):
    def test_root(self):
        r = node.new("RootNode")
        p = node.new("PrintNode")
        p.setSingleParameter("title", "hello")
        p.setSingleParameter("message", "hello")
        blk = Block()
        blk.insert(p)
        r.setSingleChildBlock("block", blk)
        generated = r.generate()
        self.assertEqual(generated[0], "# generated by nyancode.")
        self.assertEqual(generated[1], "import nyancode_runtime as nyancode")
        self.assertEqual(generated[2], "")
        self.assertEqual(generated[3], "nyancode.message(\"hello\", \"hello\")")

    def test_root_for_direct_run(self):
        r = node.new("RootNode")
        p = node.new("PrintNode")
        p.setSingleParameter("title", "hello")
        p.setSingleParameter("message", "hello")
        blk = Block()
        blk.insert(p)
        r.setSingleChildBlock("block", blk)
        generated = r.generate(for_direct_run=True)
        self.assertEqual(generated[0], "# generated by nyancode.")
        self.assertEqual(generated[1], "")
        self.assertEqual(generated[2], "nyancode.message(\"hello\", \"hello\")")


    def test_print(self):
        n = node.new("PrintNode")
        n.setSingleParameter("title", "meow")
        n.setSingleParameter("message", "meow")
        generated = n.generate()
        self.assertEqual("nyancode.message(\"meow\", \"meow\")", generated[0])
