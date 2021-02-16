# -*- coding: utf-8 -*-

import unittest
import nodeIO
from node.test import *
from block import Block


class TestNodeIO(unittest.TestCase):
    def test_dump_without_child_block(self):
        n = TestNode()
        n.setSingleParameter("test_int", 1)
        n.setSingleParameter("test_str", "abc")
        io = nodeIO.NodeIO()
        dumped = io.dump(n, pretty=False)
        expected = '{"name": "TestNode", "parameters": {"test_int": 1, "test_str": "abc"}, "child_blocks": {}}'
        self.assertEqual(dumped, expected)

    def test_dump_with_child_block(self):
        n = TestNode()
        n.setSingleParameter("test_int", 1)
        n.setSingleParameter("test_str", "abc")
        blk = Block()
        ni = TestNode()
        ni.setSingleParameter("is_inner", True)
        blk.insert(ni)
        n.setSingleChildBlock("block", blk)
        io = nodeIO.NodeIO()
        dumped = io.dump(n, pretty=False)
        expected = '{"name": "TestNode", "parameters": {"test_int": 1, "test_str": "abc"}, "child_blocks": {"block": [{"name": "TestNode", "parameters": {"is_inner": true}, "child_blocks": {}}]}}'
        self.assertEqual(dumped, expected)

    def test_load_without_child_block(self):
        in_json = '{"name": "TestNode", "parameters": {"test_int": 1, "test_str": "abc"}, "child_blocks": {}}'
        expected = TestNode()
        expected.setSingleParameter("test_int", 1)
        expected.setSingleParameter("test_str", "abc")
        io = nodeIO.NodeIO()
        loaded = io.load(in_json)
        self.assertTrue(isinstance(loaded, TestNode))
        self.assertEqual(expected.parameters, loaded.parameters)
        self.assertEqual({}, loaded.child_blocks)

    def test_load_with_child_block(self):
        expected = TestNode()
        expected.setSingleParameter("test_int", 1)
        expected.setSingleParameter("test_str", "abc")
        blk = Block()
        ni = TestNode()
        ni.setSingleParameter("is_inner", True)
        blk.insert(ni)
        expected.setSingleChildBlock("block", blk)
        in_json = '{"name": "TestNode", "parameters": {"test_int": 1, "test_str": "abc"}, "child_blocks": {"block": [{"name": "TestNode", "parameters": {"is_inner": true}, "child_blocks": {}}]}}'
        io = nodeIO.NodeIO()
        loaded = io.load(in_json)
        self.assertTrue(isinstance(loaded.child_blocks["block"], Block))
        self.assertTrue(expected, loaded.child_blocks["block"].parent_node)
        self.assertTrue(
            blk, loaded.child_blocks["block"].getNodeAt(0).parent_block)
