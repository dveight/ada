import os
import tempfile
import unittest2 as unittest

import shutil

import nuke

from ada.core.utils import is_nuke, is_gaffer
import ada.core.nuke.executable

from ada.nuke.node import add_ada_tab, ada_knob_changed
from ada.nuke.utils import remove_ada_tab, monkey_patch, deconstruct_knobs_to_serialise
from ada.nuke.globals import ADA_KNOBS


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


class AdaNukeUtilsTestCase(unittest.TestCase):

    def test_deconstruct_knobs_to_serialise_aliases(self):
        alias_knob = deconstruct_knobs_to_serialise("aliases(knob_name alias_name 100)")
        self.assertEqual(alias_knob.knob, "knob_name")
        self.assertEqual(alias_knob.alias, "alias_name")
        self.assertEqual(alias_knob.default_value, "100")

    def test_deconstruct_knobs_to_serialise_inputs(self):
        inputs_knob = deconstruct_knobs_to_serialise("inputs(input_name alias_name filepath)")
        self.assertEqual(inputs_knob.knob, "input_name")
        self.assertEqual(inputs_knob.alias, "alias_name")
        self.assertEqual(inputs_knob.default_value, "filepath")

    def test_deconstruct_knobs_to_serialise_outputs(self):
        outputs_knob = deconstruct_knobs_to_serialise("outputs(output_name alias_name filepath)")
        self.assertEqual(outputs_knob.knob, "output_name")
        self.assertEqual(outputs_knob.alias, "alias_name")
        self.assertEqual(outputs_knob.default_value, "filepath")


class AdaNukeNodeTestCase(unittest.TestCase):

    def setUp(self):
        self.tempdir = None

    def test_add_and_remove_ada_tab(self):
        noop = nuke.createNode("NoOp", inpanel=False)
        self.assertIsNotNone(noop)
        knob_names = noop.knobs().keys()
        for knob_name in ADA_KNOBS:
            self.assertFalse(knob_name in noop.knobs(), "{} is in NoOp.knobs".format(knob_name))
        add_ada_tab(noop)
        for knob_name in ADA_KNOBS:
            self.assertTrue(knob_name in noop.knobs(), "{} is not in NoOp.knobs".format(knob_name))
        self.assertEqual(noop["icon"].value(), "ada_raw.png")
        remove_ada_tab(noop)
        self.assertEqual(knob_names, noop.knobs().keys())
        self.assertEqual(noop["icon"].value(), "")

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

    def tearDown(self):
        if self.tempdir and os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir)
        for node in nuke.allNodes():
            nuke.delete(node)
        this_knob.k = None
        this_node.n = None


if __name__ == "__main__":
    unittest.main()
