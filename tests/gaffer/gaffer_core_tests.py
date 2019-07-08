import os
import tempfile
import unittest2 as unittest

import shutil

import Gaffer

from ada.core import ada_pb2, graph_pb2
from ada.core.io import read_graph_file, read_ada_file, write_proto_file

from google.protobuf.pyext._message import (
    RepeatedCompositeContainer,
    RepeatedScalarContainer,
)


class AdaGafferTestCase(unittest.TestCase):

    def setUp(self):
        self.root = Gaffer.ScriptNode()
        self.context = ada_pb2.Context()
        self.tempdir = None

    def test_bake_noop(self):
        with self.root.context():
            dot = Gaffer.Dot()
            self.root["dot"] = dot

    def tearDown(self):
        del self.context
        del self.root
        if self.tempdir and os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir)


if __name__ == "__main__":
    unittest.main()
