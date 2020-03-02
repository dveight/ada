import os
import tempfile
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import shutil
import sys 

from ada.core import ada_pb2
from ada.core import graph_pb2
from ada.core.io import read_graph_file, read_ada_file, write_proto_file
from ada.core.utils import is_nuke, is_gaffer

from google.protobuf.pyext._message import (
    RepeatedCompositeContainer,
    RepeatedScalarContainer,
)


class AdaCoreTestCase(unittest.TestCase):

    def test_is_nuke(self):
        self.assertFalse(is_nuke())

    def test_is_gaffer(self):
        self.assertFalse(is_gaffer())


class AdaTestCase(unittest.TestCase):

    def setUp(self):
        self.context = ada_pb2.Context()
        self.tempdir = None

    def test_script_output(self):

        script = self.context.output_script

        self.assertIsInstance(script.dir, unicode)
        self.assertIsInstance(script.name, unicode)

    def test_script_range(self):

        script_range = self.context.script_frame_range
        self.assertIsInstance(script_range.start, int)
        self.assertIsInstance(script_range.end, int)

    def test_template_location_is_unicode(self):

        self.assertIsInstance(self.context.template.location, unicode)

    def test_inputs(self):
        self.context.inputs["scan"] = "/SHOW/shot/scan/scan.####.exr"
        self.assertEqual(self.context.inputs["scan"], "/SHOW/shot/scan/scan.####.exr")

    def test_outputs(self):

        self.context.outputs["comp"] = "/SHOW/shot/out/comp.####.exr"
        self.assertEqual(self.context.outputs["comp"], "/SHOW/shot/out/comp.####.exr")

    def test_aliases(self):

        self.context.aliases["this_is_a_test"] = True
        self.assertTrue(self.context.aliases["this_is_a_test"])

    def test_host_types(self):

        self.assertIsInstance(self.context.host, int)

    def test_job(self):

        self.assertIsInstance(self.context.job, unicode)

    def test_shot(self):

        self.assertIsInstance(self.context.shot, unicode)

    def test_format(self):
        self.assertIsInstance(self.context.format, unicode)

    def test_read_write_context(self):
        self.tempdir = tempfile.mkdtemp()
        write_proto_file(self.context, self.tempdir, "foo", ".bar")
        file_path = os.sep.join([self.tempdir, "foo.bar"])
        self.assertTrue(os.path.exists(file_path))
        context = read_ada_file(file_path)
        self.assertIsNotNone(context)

    def tearDown(self):
        del self.context
        if self.tempdir and os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir)


class GraphTestCase(unittest.TestCase):

    def setUp(self):
        self.scene = graph_pb2.Scene()
        self.tempdir = None

    def test_scene_queue_nodes_is_repeated(self):
        queue = self.scene.queue.add()
        self.assertIsInstance(self.scene.queue, RepeatedCompositeContainer)
        queue.nodes.add()
        self.assertIsInstance(queue.nodes, RepeatedCompositeContainer)

    def test_scene_queue_nodes_attributes(self):
        queue = self.scene.queue.add()

        self.assertIsInstance(queue.order, int)

        node = queue.nodes.add()

        self.assertIsInstance(node.name, str)
        self.assertIsInstance(node.Class, unicode)
        self.assertIsInstance(node.full_name, unicode)

        attribute = node.attributes.add()
        self.assertIsInstance(attribute.name, unicode)
        self.assertIsInstance(attribute.label, unicode)
        self.assertIsInstance(attribute.value, unicode)
        self.assertIsInstance(attribute.values, RepeatedScalarContainer)
        self.assertIsInstance(attribute.animated, bool)
        self.assertIsInstance(attribute.Class, unicode)

        self.assertIsInstance(attribute.alias, graph_pb2.Attribute.Alias)
        self.assertIsInstance(attribute.alias.name, unicode)

    def test_scene_root(self):
        self.assertIsInstance(self.scene.root, graph_pb2.Scene.Root)
        self.assertIsInstance(self.scene.root.fps, float)
        self.assertIsInstance(self.scene.root.views, RepeatedScalarContainer)

    def test_read_write_scene(self):
        self.scene.root.fps = 24
        self.scene.root.views.append("main")
        self.tempdir = tempfile.mkdtemp()
        write_proto_file(self.scene, self.tempdir, "foo", ".bar")
        file_path = os.sep.join([self.tempdir, "foo.bar"])
        self.assertTrue(os.path.exists(file_path))
        scene = read_graph_file(file_path)
        self.assertIsNotNone(scene)

    def tearDown(self):
        del self.scene
        if self.tempdir and os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir)


if __name__ == "__main__":
    unittest.main()
