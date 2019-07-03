import os
import tempfile
import unittest2 as unittest

import shutil

import nuke

from ada.core import ada_pb2, graph_pb2
from ada.core.io import read_graph_file, read_ada_file, write_proto_file

from google.protobuf.pyext._message import (
    RepeatedCompositeContainer,
    RepeatedScalarContainer,
)


class AdaNukeTestCase(unittest.TestCase):

    def setUp(self):
        self.context = ada_pb2.Context()
        self.tempdir = None

    def test_bake_noop(self):
        noop = nuke.createNode("NoOp")
        self.assertIsNotNone(noop)
        self.assertEqual(noop.name(), "NoOp1")

    def tearDown(self):
        del self.context
        if self.tempdir and os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir)
        for node in nuke.allNodes():
            nuke.delete(node)


if __name__ == "__main__":
    unittest.main()
