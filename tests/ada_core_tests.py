import unittest

from ada_core import ada_pb2
from ada_core import graph_pb2
from ada_core.io import read_graph_file, read_ada_file, write_proto_file

from google.protobuf.pyext._message import (
    RepeatedCompositeContainer,
    RepeatedScalarContainer,
)


class AdaTestCase(unittest.TestCase):
    def setUp(self):
        self.context = ada_pb2.Context()

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

    def test_inputs_is_repeated(self):

        self.context.inputs.add()
        self.assertIsInstance(self.context.inputs, RepeatedCompositeContainer)

    def test_inputs_attributes(self):

        self.context.inputs.add()
        self.assertIsInstance(self.context.inputs[0].location, unicode)
        self.assertIsInstance(self.context.inputs[0].range.start, int)
        self.assertIsInstance(self.context.inputs[0].range.end, int)

    def test_outputs_is_repeated(self):

        self.context.outputs.add()

        self.assertIsInstance(self.context.outputs, RepeatedCompositeContainer)

    def test_outputs_attributes(self):

        self.context.outputs.add()
        self.assertIsInstance(self.context.outputs[0].location, unicode)
        self.assertIsInstance(self.context.outputs[0].range.start, int)
        self.assertIsInstance(self.context.outputs[0].range.end, int)

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

    def tearDown(self):
        del self.context


class GraphTestCase(unittest.TestCase):
    def setUp(self):
        self.graph = graph_pb2.Scene()

    def test_nodes_is_repeated(self):
        self.graph.nodes.add()
        self.assertIsInstance(self.graph.nodes, RepeatedCompositeContainer)

    def test_nodes_attributes(self):
        node = self.graph.nodes.add()

        self.assertIsInstance(node.name, unicode)
        self.assertIsInstance(node.Class, unicode)
        self.assertIsInstance(node.full_name, unicode)

        attribute = node.attributes.add()
        self.assertIsInstance(attribute.name, unicode)
        self.assertIsInstance(attribute.label, unicode)
        self.assertIsInstance(attribute.value, unicode)
        self.assertIsInstance(attribute.values, RepeatedScalarContainer)
        self.assertIsInstance(attribute.animated, bool)
        self.assertIsInstance(attribute.Class, unicode)
        self.assertIsInstance(attribute.alias, unicode)

    def test_root_attributes(self):
        node = self.graph.nodes.add()

        self.assertIsInstance(node.name, unicode)
        self.assertIsInstance(node.Class, unicode)
        self.assertIsInstance(node.full_name, unicode)

        attribute = node.attributes.add()
        self.assertIsInstance(attribute.name, unicode)
        self.assertIsInstance(attribute.label, unicode)
        self.assertIsInstance(attribute.value, unicode)
        self.assertIsInstance(attribute.values, RepeatedScalarContainer)
        self.assertIsInstance(attribute.animated, bool)
        self.assertIsInstance(attribute.Class, unicode)
        self.assertIsInstance(attribute.alias, unicode)

    def tearDown(self):
        del self.graph


if __name__ == "__main__":
    unittest.main()
