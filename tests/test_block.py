# -*- coding: utf-8 -*-

import unittest
import node
from block import Block


class TestBlock(unittest.TestCase):
    def test_insert_last(self):
        r = node.new("RootNode")
        p = node.new("PrintNode")
        blk = Block()
        blk.insert(r)
        blk.insert(p)
        self.assertEqual(list(blk), [r, p])

    def test_insert_middle(self):
        p1 = node.new("PrintNode")
        p2 = node.new("PrintNode")
        r = node.new("RootNode")
        blk = Block()
        blk.insert(p1)
        blk.insert(p2)
        blk.insert(r, index=1)
        self.assertEqual(list(blk), [p1, r, p2])

    def test_insert_outOfIndex(self):
        p1 = node.new("PrintNode")
        p2 = node.new("PrintNode")
        r = node.new("RootNode")
        blk = Block()
        blk.insert(p1)
        blk.insert(p2)
        blk.insert(r, index=2)
        self.assertEqual(list(blk), [p1, p2, r])
        blk = Block()
        blk.insert(p1)
        blk.insert(p2)
        blk.insert(r, index=3)
        self.assertEqual(list(blk), [p1, p2, r])
