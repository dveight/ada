import nuke
import nukescripts.panels

from .utils import deserialise_knobs_to_serialise, get_class_name
from .globals import (
    INPUT_NODES,
    OUTPUT_NODES,
    IGNORE_KNOBS,
)
from ..core.common import getLog


__all__ = ["AddKnobsToAda"]


class AddKnobsToAda(nukescripts.panels.PythonPanel):

    def __init__(self, node):
        """

        Args:
            node:
        """
        super(AddKnobsToAda, self).__init__("com.ada.AliasCreator")
        # CREATE KNOBS
        self.node = node
        self.class_name = get_class_name(node)
        self.knobs = dict()
        self.alias_knobs = list()

        self.node_name = nuke.Text_Knob("node", "Node:", node.name())
        self.addKnob(self.node_name)

    def create_knobs(self):
        """

        Returns:
            True if the knobs are successfully created

        """
        knobs = extract_knobs(self.node)
        if not knobs:
            nuke.message("No knobs can be set on this node")
            return False

        self.node_name = nuke.Text_Knob("node ", "Node: ", self.node.name())

        for knob in knobs:

            ada_knob = deserialise_knobs_to_serialise(
                self.node["knobs_to_serialise"], prune=knob.name()
            )

            this_knob_name = knob.name()

            knob_name = nuke.Text_Knob(
                "{} ".format(this_knob_name), "Knob: ", this_knob_name
            )

            knob_is_input = this_knob_name in INPUT_NODES.get(self.class_name, [])
            knob_is_output = this_knob_name in OUTPUT_NODES.get(self.class_name, [])

            self.addKnob(knob_name)
            if knob_is_input:
                new_knob_name = "input_{}".format(this_knob_name)
                data_knob = nuke.String_Knob(new_knob_name, "Input: ")
                if ada_knob:
                    data_knob.setValue(ada_knob.alias)
                self.alias_knobs.append(data_knob)

            elif knob_is_output:
                new_knob_name = "output_{}".format(this_knob_name)
                data_knob = nuke.String_Knob(new_knob_name, "Output: ")
                if ada_knob:
                    data_knob.setValue(ada_knob.alias)
                self.alias_knobs.append(data_knob)
            else:
                new_knob_name = "alias_{} ".format(this_knob_name)
                data_knob = nuke.String_Knob(new_knob_name, "Alias: ")
                if ada_knob:
                    data_knob.setValue(ada_knob.alias)
                self.alias_knobs.append(data_knob)

            try:
                self.addKnob(data_knob)

            except RuntimeError:
                getLog().warning("Ada: Unable to add knob alias, input or output!")

            default_knob = "default_{} ".format(knob.name())

            try:
                value = knob.evaluate()
            except AttributeError:
                value = knob.value()

            default_value = nuke.String_Knob(
                default_knob, "Default Value: ", str(value)
            )
            default_value.clearFlag(nuke.STARTLINE)

            self.knobs[new_knob_name] = (default_value, knob.name())

            self.addKnob(default_value)

        return True


def extract_knobs(node):
    """

    Args:
        node (nuke.Node):

    Returns:
        list of knobs (nuke.Knob)

    """
    knobs = []
    knob_names = []
    for knob in range(node.numKnobs()):
        knob = node.knob(knob)
        knob_name = knob.name()
        if (
            knob.visible()
            and knob_name != ""
            and knob.enabled()
            and knob_name not in knob_names
            and knob_name not in IGNORE_KNOBS
        ):
            knobs.append(knob)
            knob_names.append(knob_name)

    return knobs
