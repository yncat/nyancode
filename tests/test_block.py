# -*- coding: utf-8 -*-

import unittest
import node
from block import Block


class TestBlock(unittest.TestCase):
    def test_insert_last(self):
        r = node.new("RootNode")
        p = node.new("MessageNode")
        blk = Block()
        blk.insert(r)
        blk.insert(p)
        self.assertEqual(list(blk), [r, p])

    def test_insert_middle(self):
        p1 = node.new("MessageNode")
        p2 = node.new("MessageNode")
        r = node.new("RootNode")
        blk = Block()
        blk.insert(p1)
        blk.insert(p2)
        blk.insert(r, index=1)
        self.assertEqual(list(blk), [p1, r, p2])

    def test_insert_outOfIndex(self):
        p1 = node.new("MessageNode")
        p2 = node.new("MessageNode")
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

    def test_deleteMultipleNodes_single(self):
        p1 = node.new("MessageNode")
        p2 = node.new("MessageNode")
        r = node.new("RootNode")
        blk = Block()
        blk.insert(p1)
        blk.insert(p2)
        blk.insert(r)
        blk.deleteMultipleNodes([1])
        self.assertEqual(list(blk), [p1, r])

    def test_deleteMultipleNodes_multiple(self):
        p1 = node.new("MessageNode")
        p2 = node.new("MessageNode")
        r = node.new("RootNode")
        blk = Block()
        blk.insert(p1)
        blk.insert(p2)
        blk.insert(r)
        blk.deleteMultipleNodes([1, 2])
        self.assertEqual(list(blk), [p1])

    def test_generate_empty(self):
        blk = Block()
        self.assertEqual(["pass"], blk.generate())

    def test_generate(self):
        p1 = node.new("MessageNode")
        p1.setSingleParameter("title", "title")
        p1.setSingleParameter("message", "message")
        blk = Block()
        blk.insert(p1)
        self.assertEqual(
            ["nyancode.message(\"title\", \"message\")"],
            blk.generate())

    def test_generate_indented(self):
        p1 = node.new("MessageNode")
        p1.setSingleParameter("title", "title")
        p1.setSingleParameter("message", "message")
        blk = Block()
        blk.insert(p1)
        self.assertEqual(
            ["    nyancode.message(\"title\", \"message\")"],
            blk.generate(1))
