# -*- coding: utf-8 -*-

import unittest
import nodeIO
from node.base import *


class TestNodeIO(unittest.TestCase):
    def test_dump_without_child_node(self):
        n = BaseNode()
        n.setSingleParameter("test_int", 1)
        n.setSingleParameter("test_str", "abc")
        io = nodeIO.NodeIO()
        dumped = io.dump(n)
        expected = '{"name": "BaseNode", "parameters": {"test_int": 1, "test_str": "abc"}, "child_nodes": {}}'
        self.assertEqual(dumped, expected)

    def test_dump_with_child_node(self):
        n = BaseNode()
        n.setSingleParameter("test_int", 1)
        n.setSingleParameter("test_str", "abc")
        ni = BaseNode()
        ni.setSingleParameter("is_inner", True)
        n.setSingleChildNode("block", ni)
        io = nodeIO.NodeIO()
        dumped = io.dump(n)
        expected = '{"name": "BaseNode", "parameters": {"test_int": 1, "test_str": "abc"}, "child_nodes": {"block": {"name": "BaseNode", "parameters": {"is_inner": true}, "child_nodes": {}}}}'
        self.assertEqual(dumped, expected)

    def test_load_without_child_node(self):
        in_json = '{"name": "BaseNode", "parameters": {"test_int": 1, "test_str": "abc"}, "child_nodes": {}}'
        expected = BaseNode()
        expected.setSingleParameter("test_int", 1)
        expected.setSingleParameter("test_str", "abc")
        io = nodeIO.NodeIO()
        loaded = io.load(in_json)
        self.assertTrue(isinstance(loaded, BaseNode))
        self.assertEqual(expected.parameters, loaded.parameters)
        self.assertEqual({}, loaded.child_nodes)

    def test_load_with_child_node(self):
        expected = BaseNode()
        expected.setSingleParameter("test_int", 1)
        expected.setSingleParameter("test_str", "abc")
        ni = BaseNode()
        ni.setSingleParameter("is_inner", True)
        expected.setSingleChildNode("block", ni)
        in_json = '{"name": "BaseNode", "parameters": {"test_int": 1, "test_str": "abc"}, "child_nodes": {"block": {"name": "BaseNode", "parameters": {"is_inner": true}, "child_nodes": {}}}}'
        io = nodeIO.NodeIO()
        loaded = io.load(in_json)
        self.assertTrue(isinstance(loaded.child_nodes["block"], BaseNode))
