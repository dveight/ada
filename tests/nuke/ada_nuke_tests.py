import os
import tempfile
import unittest2 as unittest

import shutil

import nuke

import ada.core.nuke.executable

from ada.core import ada_pb2, graph_pb2
from ada.core.utils import is_nuke, is_gaffer

from ada.nuke.node import add_ada_tab, ada_knob_changed
from ada.nuke.context import Engine
from ada.nuke.utils import (
    can_cast, has_ada_tab, remove_ada_tab, monkey_patch,
    deconstruct_knobs_to_serialise, parse_tcl_string, can_bake_node
)
from ada.nuke.globals import ADA_KNOBS, ADA_KNOB_PAIRS


@monkey_patch(nuke.thisKnob)
def this_knob():
    return this_knob.k


@monkey_patch(nuke.thisNode)
def this_node():
    return this_knob.n


this_knob.n = None
this_knob.k = None


class AdaCoreNukeTestCase(unittest.TestCase):

    def test_nuke_executable(self):
        self.assertTrue(ada.core.nuke.executable.NUKE_EXECUTABLE)
        self.assertTrue(os.path.exists(ada.core.nuke.executable.NUKE_EXECUTABLE))

    def test_is_nuke(self):
        self.assertTrue(is_nuke())

    def test_is_gaffer(self):
        self.assertFalse(is_gaffer())


class AdaNukeContextTestCase(unittest.TestCase):

    def test_engine__alpha_numeric_sort(self):
        nodes = ["Test10", "Test01"]
        self.assertEqual(Engine.alpha_numeric_sort(nodes), ["Test01", "Test10"])
        nodes = ["Grade1", "Transform2", "Test3", "Abc45"]
        self.assertEqual(Engine.alpha_numeric_sort(nodes), ['Abc45', 'Grade1', 'Test3', 'Transform2'])

    def tearDown(self):
        # reset the context
        nuke.Ada = ada_pb2.Context()
        nuke.Ada.host = nuke.Ada.NUKE


class AdaNukeUtilsTestCase(unittest.TestCase):

    def test_parse_tcl_string__valid(self):
        nuke.Ada.show = "TEST"
        nuke.Ada.shot = "test_shot"
        nuke.Ada.format.width = 1828
        nuke.Ada.format.height = 1556
        nuke.Ada.format.pixel_aspect = 2.0
        nuke.Ada.frame_range.start = 1001
        nuke.Ada.frame_range.end = 1010
        nuke.Ada.output_script.dir = "/SHOW/shot/outputs/"
        nuke.Ada.output_script.name = ".ada_script.nk"

        nuke.Ada.inputs["scan"] = "/SHOW/shot/scan/scan.####.exr"
        nuke.Ada.inputs["denoise"] = "/SHOW/shot/denoise/denoised.####.exr"
        nuke.Ada.outputs["output1"] = "/SHOW/shot/outputs/output1.####.exr"
        nuke.Ada.outputs["2"] = "/SHOW/shot/outputs/output2.####.exr"

        nuke.Ada.aliases["foo"] = ["blah", "zay"]
        nuke.Ada.aliases["bar"] = {"holy": 6.9}

        self.assertEqual(parse_tcl_string("show"), nuke.Ada.show)
        self.assertEqual(parse_tcl_string("shot"), nuke.Ada.shot)
        self.assertEqual(parse_tcl_string("format width"), nuke.Ada.format.width)
        self.assertEqual(parse_tcl_string("format height"), nuke.Ada.format.height)
        self.assertEqual(parse_tcl_string("format pixel_aspect"), nuke.Ada.format.pixel_aspect)
        self.assertEqual(parse_tcl_string("frame_range start"), nuke.Ada.frame_range.start)
        self.assertEqual(parse_tcl_string("frame_range end"), nuke.Ada.frame_range.end)
        self.assertEqual(parse_tcl_string("output_script dir"), nuke.Ada.output_script.dir)
        self.assertEqual(parse_tcl_string("output_script name"), nuke.Ada.output_script.name)

        self.assertEqual(parse_tcl_string("inputs scan"), nuke.Ada.inputs["scan"])
        self.assertEqual(parse_tcl_string("inputs denoise"), nuke.Ada.inputs["denoise"])

        self.assertEqual(parse_tcl_string("outputs output1"), nuke.Ada.outputs["output1"])
        self.assertEqual(parse_tcl_string("outputs 2"), nuke.Ada.outputs["2"])

        self.assertEqual(parse_tcl_string("aliases foo 0"), "blah")
        self.assertEqual(parse_tcl_string("aliases foo 1"), "zay")
        self.assertEqual(parse_tcl_string("aliases bar holy"), 6.9)

    def test_parse_tcl_string__invalid(self):
        self.assertIsNone(parse_tcl_string("inputs scan"))
        self.assertIsNone(parse_tcl_string("outputs output3"))
        self.assertIsNone(parse_tcl_string("aliases foo 0"))
        self.assertIsNone(parse_tcl_string("frame_range endz"))

        self.assertEqual(parse_tcl_string("show"), "")
        self.assertEqual(parse_tcl_string("shot"), "")

        self.assertEqual(parse_tcl_string("format width"), 0)
        self.assertEqual(parse_tcl_string("format height"), 0)
        self.assertEqual(parse_tcl_string("format pixel_aspect"), 0.0)

        self.assertEqual(parse_tcl_string("frame_range start"), 0)
        self.assertEqual(parse_tcl_string("frame_range end"), 0)

    def test_can_cast(self):
        self.assertTrue(can_cast(1, int))
        self.assertTrue(can_cast("1", int))
        self.assertTrue(can_cast("1.3345", float))
        self.assertFalse(can_cast("1.3345", int))
        self.assertFalse(can_cast(None, int))
        self.assertFalse(can_cast("blah", int))

    def test_deconstruct_knobs_to_serialise_aliases(self):
        alias_knob = deconstruct_knobs_to_serialise("aliases(knob_name alias_name 100)")
        self.assertEqual(alias_knob.knob, "knob_name")
        self.assertEqual(alias_knob.alias, "alias_name")
        self.assertEqual(alias_knob.default_value, "100")

        alias_knob = deconstruct_knobs_to_serialise("aliases(knob_name, alias_name, 100)")
        self.assertEqual(alias_knob.knob, "knob_name")
        self.assertEqual(alias_knob.alias, "alias_name")
        self.assertEqual(alias_knob.default_value, "100")

    def test_deconstruct_knobs_to_serialise_inputs(self):
        inputs_knob = deconstruct_knobs_to_serialise("inputs(input_name alias_name /file/path.####.exr)")
        self.assertEqual(inputs_knob.knob, "input_name")
        self.assertEqual(inputs_knob.alias, "alias_name")
        self.assertEqual(inputs_knob.default_value, "/file/path.####.exr")

        inputs_knob = deconstruct_knobs_to_serialise("inputs(input_name, alias_name, /file/path.####.exr)")
        self.assertEqual(inputs_knob.knob, "input_name")
        self.assertEqual(inputs_knob.alias, "alias_name")
        self.assertEqual(inputs_knob.default_value, "/file/path.####.exr")

    def test_deconstruct_knobs_to_serialise_outputs(self):
        outputs_knob = deconstruct_knobs_to_serialise("outputs(output_name alias_name /file/path.####.exr)")
        self.assertEqual(outputs_knob.knob, "output_name")
        self.assertEqual(outputs_knob.alias, "alias_name")
        self.assertEqual(outputs_knob.default_value, "/file/path.####.exr")

        outputs_knob = deconstruct_knobs_to_serialise("outputs(output_name, alias_name, /file/path.####.exr)")
        self.assertEqual(outputs_knob.knob, "output_name")
        self.assertEqual(outputs_knob.alias, "alias_name")
        self.assertEqual(outputs_knob.default_value, "/file/path.####.exr")

    def test_has_ada_tab(self):
        noop = nuke.createNode("NoOp", inpanel=False)
        self.assertFalse(has_ada_tab(noop))
        add_ada_tab(noop)
        self.assertTrue(has_ada_tab(noop))

    def test_remove_ada_tab(self):
        noop = nuke.createNode("NoOp", inpanel=False)
        knob_names = noop.knobs().keys()
        add_ada_tab(noop)
        self.assertTrue(has_ada_tab(noop))
        self.assertEqual(noop["icon"].value(), "ada_raw.png")
        remove_ada_tab(noop)
        self.assertEqual(knob_names, noop.knobs().keys())
        self.assertEqual(noop["icon"].value(), "")

    def test_can_bake_node(self):
        noop = nuke.createNode("NoOp", inpanel=False)
        self.assertFalse(can_bake_node(noop))
        add_ada_tab(noop)
        self.assertFalse(can_bake_node(noop))
        for knob_check, knob_value in ADA_KNOB_PAIRS.items():
            noop[knob_check].setValue(True)
            noop[knob_value].setValue("something")
            self.assertTrue(can_bake_node(noop))
            noop[knob_check].setValue(False)
            self.assertFalse(can_bake_node(noop))
        for knob_check in ADA_KNOB_PAIRS.keys():
            noop[knob_check].setValue(True)
        self.assertTrue(can_bake_node(noop))
        noop["do_not_bake"].setValue(True)
        self.assertFalse(can_bake_node(noop))

    def tearDown(self):
        # reset the context
        nuke.Ada = ada_pb2.Context()
        nuke.Ada.host = nuke.Ada.NUKE
        for node in nuke.allNodes():
            nuke.delete(node)


class AdaNukeNodeTestCase(unittest.TestCase):

    def test_add_ada_tab(self):
        noop = nuke.createNode("NoOp", inpanel=False)
        for knob_name in ADA_KNOBS:
            self.assertFalse(knob_name in noop.knobs(), "{} is in NoOp.knobs".format(knob_name))
        add_ada_tab(noop)
        self.assertTrue(has_ada_tab(noop))
        for knob_name in ADA_KNOBS:
            self.assertTrue(knob_name in noop.knobs(), "{} is not in NoOp.knobs".format(knob_name))
        self.assertEqual(noop["icon"].value(), "ada_raw.png")

    def test_knob_changed_empty(self):
        grade = nuke.createNode("Grade", inpanel=False)
        add_ada_tab(grade)
        knob_to_serialise = grade["knobs_to_serialise"]
        knob_names = grade.knobs().keys()
        this_node.n = grade
        this_knob.k = knob_to_serialise
        ada_knob_changed()
        self.assertEqual(grade.knobs().keys(), knob_names)

    def test_knob_changed_invalid(self):
        grade = nuke.createNode("Grade", inpanel=False)
        add_ada_tab(grade)
        knob_to_serialise = grade["knobs_to_serialise"]
        knob_names = grade.knobs().keys()
        knob_to_serialise.setValue("blah\nfoo\nbar")
        self.assertEqual(grade.knobs().keys(), knob_names)

    def test_knob_changed_aliases(self):
        grade = nuke.createNode("Grade", inpanel=False)
        add_ada_tab(grade)
        knob_to_serialise = grade["knobs_to_serialise"]
        knob_names = grade.knobs().keys()
        knob_to_serialise.setValue("aliases()")
        self.assertEqual(grade.knobs().keys(), knob_names)

    def test_knob_changed_inputs(self):
        read = nuke.createNode("Read", inpanel=False)
        add_ada_tab(read)
        knob_to_serialise = read["knobs_to_serialise"]
        knob_names = read.knobs().keys()
        knob_to_serialise.setValue("inputs(file plate /tmp/path/image.####.exr)")
        self.assertEqual(read.knobs().keys(), knob_names)

    def test_knob_changed_outputs(self):
        write = nuke.createNode("Write", inpanel=False)
        add_ada_tab(write)
        knob_to_serialise = write["knobs_to_serialise"]
        knob_names = write.knobs().keys()
        knob_to_serialise.setValue("outputs(file denoised /tmp/path/image.####.exr)")
        self.assertEqual(write.knobs().keys(), knob_names)

    def setUp(self):
        self.tempdir = None

    def tearDown(self):
        if self.tempdir and os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir)
        for node in nuke.allNodes():
            nuke.delete(node)
        this_knob.k = None
        this_node.n = None


if __name__ == "__main__":
    unittest.main()
