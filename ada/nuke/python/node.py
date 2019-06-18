import re

import nuke
import nukescripts

from ada.core.common import getLog

from .globals import (
    ALIAS_STRING,
    INPUT_STRING,
    OUTPUT_STRING,
    KnobAlias,
    KnobOutput,
    KnobInput,
    ADA_KNOB_CHANGED,
    IGNORE_KNOBS,
    INPUT_NODES,
    OUTPUT_NODES,
    KNOB_TO_EXECUTION_TYPE,
)
from .utils import (
    deconstruct_knobs_to_serialise,
    deserialise_knobs_to_serialise,
    represents_int,
    get_class_name,
)

from .globals import ALIAS_STRING


def add_ada_tab(nodes=None):
    """
    Add an ada tab to a given list of nodes. The tab is the instructions for what Ada should do to this node.

    Args:
        nodes (list): List of nuke node objects (including root).

    """
    if nodes is None:
        nodes = nuke.selectedNodes()

    elif not isinstance(nodes, list):
        nodes = [nodes]

    for node in nodes:
        if node.Class() == "Viewer":
            continue
        if not node.knob("Ada"):
            ada_tab = nuke.Tab_Knob("ada", "Ada")
            bake_knobs_boolean = nuke.Boolean_Knob("bake_knobs", " ")
            bake_knobs_boolean.setValue(False)
            bake_knobs_boolean.setTooltip("bake knobs to bake")
            bake_knobs_boolean.setFlag(nuke.STARTLINE)

            knobs_to_bake_string = nuke.EvalString_Knob(
                "knobs_to_bake", "knobs to bake     "
            )
            knobs_to_bake_string.clearFlag(nuke.STARTLINE)
            knobs_to_bake_string.setTooltip(
                "comma-separated list of knobs to bake, or values "
                "to assign. eg: 'value=10, file=[pcrn input 1]'"
            )

            set_knobs_boolean = nuke.Boolean_Knob("set_knobs", " ")
            set_knobs_boolean.setValue(False)
            set_knobs_boolean.setTooltip("set knobs to bake")
            set_knobs_boolean.setFlag(nuke.STARTLINE)

            knobs_to_set_string = nuke.EvalString_Knob(
                "knobs_to_set", "knobs to set        "
            )
            knobs_to_set_string.clearFlag(nuke.STARTLINE)
            knobs_to_set_string.setTooltip(
                "assign value. eg: 'value=10, file=[pcrn input 1]'"
            )

            execute_buttons_boolean = nuke.Boolean_Knob("execute_knobs", " ")
            execute_buttons_boolean.setValue(False)
            execute_buttons_boolean.setTooltip("execute knobs/buttons")
            execute_buttons_boolean.setFlag(nuke.STARTLINE)

            execute_buttons_string = nuke.EvalString_Knob(
                "knobs_to_execute", "knobs to execute "
            )
            execute_buttons_string.clearFlag(nuke.STARTLINE)
            execute_buttons_string.setTooltip(
                "comma-separated list of knobs (buttons) to execute()"
            )

            exeucte_code_boolean = nuke.Boolean_Knob("execute_code", " ")
            exeucte_code_boolean.setValue(False)
            exeucte_code_boolean.setTooltip("run the code to exec")
            exeucte_code_boolean.setFlag(nuke.STARTLINE)

            execute_code_string = nuke.Multiline_Eval_String_Knob(
                "code_to_execute", "code to execute   "
            )
            execute_code_string.setTooltip(
                "python code to exec()\nnuke.thisNode() " "is available to the code"
            )
            execute_code_string.clearFlag(nuke.STARTLINE)

            queue_order_int = nuke.Int_Knob("queue_order", "queue order")
            queue_order_int.clearFlag(nuke.STARTLINE)
            queue_order_int.setTooltip(
                "Nodes are baked from the lowest order to the "
                "highest. Default value is 0"
            )

            do_not_bake_boolean = nuke.Boolean_Knob(
                "do_not_bake", "  do not bake this node      "
            )
            do_not_bake_boolean.setValue(False)
            do_not_bake_boolean.setTooltip("do not bake this node")
            do_not_bake_boolean.setFlag(nuke.STARTLINE)

            knobs_to_serialise = nuke.Multiline_Eval_String_Knob(
                "knobs_to_serialise", "knobs to serialise"
            )
            knobs_to_serialise.setTooltip(
                "these knobs will be saved with the template and "
                "then can be set externally"
            )

            node.addKnob(ada_tab)

            node.addKnob(bake_knobs_boolean)
            node.addKnob(knobs_to_bake_string)
            node.addKnob(set_knobs_boolean)
            node.addKnob(knobs_to_set_string)
            node.addKnob(execute_buttons_boolean)
            node.addKnob(execute_buttons_string)
            node.addKnob(exeucte_code_boolean)
            node.addKnob(execute_code_string)
            node.addKnob(do_not_bake_boolean)
            node.addKnob(queue_order_int)
            node.addKnob(knobs_to_serialise)

        try:
            node.knob("autolabel").setValue(
                "__import__('ada.nuke.utils', fromlist=['autolabel']).autolabel()"
            )
        except ImportError:
            pass

        # set knob changed on the newly created ada node
        kc = node.knob("knobChanged")
        cur_kc = kc.value()
        new_kc = "{}\n{}".format(cur_kc, ADA_KNOB_CHANGED)
        kc.setValue(new_kc)

        icon_knob = node.knob("icon").value().startswith("ada_")
        note_font_knob = node.knob("note_font").value().startswith("ada_")
        if not icon_knob and not note_font_knob:
            node.knob("icon").setValue("ada_raw.png")


def add_knob_to_bake(node):
    """

    Args:
        node:
        knob_name:

    Returns:

    """
    # launch gui for setting alias
    if nuke.GUI:
        node_class = get_class_name(node)

        if not node.knobs().get("ada"):
            add_ada_tab([node])

        alias_creator = AddKnobsToAda(node)
        knobs = alias_creator.create_knobs()
        if knobs:
            alias_creator.showModalDialog()

        knobs = []
        for alias in alias_creator.alias_knobs:
            if alias.value() != "":
                value, knob = alias_creator.knobs[alias.name()]

                if node_class in INPUT_NODES:
                    if knob not in INPUT_NODES[node_class]:
                        continue
                    next_input = len(nuke.Ada.inputs)
                    new_input = nuke.Ada.inputs.add()
                    new_input.location = value.value()

                    input_string = INPUT_STRING.format(
                        knob=knob,
                        index=next_input,
                        location=value.value(),
                        start="",
                        end="",
                    )
                    knobs.append(input_string)

                elif node_class in OUTPUT_NODES:
                    if knob not in OUTPUT_NODES[node_class]:
                        continue

                    next_output = len(nuke.Ada.outputs)
                    new_output = nuke.Ada.outputs.add()
                    new_output.location = value.value()

                    output_string = OUTPUT_STRING.format(
                        knob=knob,
                        index=next_output,
                        location=value.value(),
                        start="",
                        end="",
                    )
                    knobs.append(output_string)

                else:
                    knob_to_serialise = ALIAS_STRING.format(
                        knob=knob, alias=alias.value(), default=value.value()
                    )
                    knobs.append(knob_to_serialise)

        node["knobs_to_serialise"].setValue("\n".join(knobs))


if nuke.GUI:

    def extract_knobs(node):
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

    class AddKnobsToAda(nukescripts.PythonPanel):
        """

        """

        def __init__(self, node):

            nukescripts.PythonPanel.__init__(self, "com.ada.AliasCreator")
            # CREATE KNOBS
            self.node = node
            self.class_name = get_class_name(node)
            self.knobs = dict()
            self.alias_knobs = list()

            self.node_name = nuke.Text_Knob("node", "Node:", node.name())
            self.addKnob(self.node_name)

        def create_knobs(self):
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
                    data_knob = nuke.Int_Knob(
                        new_knob_name, "Input: ", len(nuke.Ada.inputs)
                    )
                    if ada_knob:
                        data_knob.setValue(int(ada_knob.index))
                    self.alias_knobs.append(data_knob)

                elif knob_is_output:
                    new_knob_name = "output_{}".format(this_knob_name)
                    data_knob = nuke.Int_Knob(
                        new_knob_name, "Output: ", len(nuke.Ada.outputs)
                    )
                    if ada_knob:
                        data_knob.setValue(int(ada_knob.index))
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


def ada_knob_changed():
    """
    When a user interacts with the knobs to serialise knob they will be modifying context information, this knob
    changed keeps that context information up to date.
    """

    this_node = nuke.thisNode()
    this_knob = nuke.thisKnob()

    if this_knob.name() == "knobs_to_serialise" and this_node.knobs().get("ada"):

        # split all the values in knobs_to_serialise by their line
        for alias in this_knob.value().split("\n"):
            current_alias = alias.strip()

            if current_alias == "":
                continue

            # for this alias get the correct object with the data inside the function
            ada_data = deconstruct_knobs_to_serialise(current_alias)

            # look up the knob on this node
            knob = this_node[ada_data.knob.strip()]

            # get the current expression
            expression = knob.toScript()

            getLog().info("Current expression {0}:{1}".format(knob.name(), expression))

            ada_type = KNOB_TO_EXECUTION_TYPE.get(knob.Class())

            if isinstance(ada_data, KnobAlias):
                set_alias_knob(knob, expression, ada_data)
                add_knob_to_ada_tab(this_node, ada_type, knob, ada_data.alias)
            if isinstance(ada_data, KnobInput):
                set_io_item(knob, current_alias, ada_data, "inputs")
                add_knob_to_ada_tab(this_node, ada_type, knob, ada_data.index)
            if isinstance(ada_data, KnobOutput):
                set_io_item(knob, current_alias, ada_data, "outputs")
                add_knob_to_ada_tab(this_node, ada_type, knob, ada_data.index)


def add_knob_to_ada_tab(node, ada_type, knob, alias=None):

    curent_knobs = node[ada_type]
    curent_knobs_list = curent_knobs.value().split(",")

    if knob.name() in curent_knobs_list:
        return

    if curent_knobs_list == [""]:
        curent_knobs_list = list()

    if ada_type == "knobs_to_bake" or ada_type == "knobs_to_execute":
        curent_knobs_list.append(knob.name())
        sorted_knobs = sorted(curent_knobs_list)

    elif ada_type == "knobs_to_set":
        expression = "{}=[Ada aliases {}]".format(knob.name(), alias)
        curent_knobs_list.append(expression)
        sorted_knobs = sorted(curent_knobs_list)

    joined_knobs = ",".join(sorted_knobs)
    curent_knobs.setValue(joined_knobs)


def set_alias_knob(knob, expression, alias_data):
    """
    Add an expression to the correct knob and add an alias to the ada context or if the user changes it then
    remove the old context item and add a new one.

    Args:
        knob (nuke.Knob): The knob we want to add the expression to.
        expression (str): The current expression on the node's knob.
        alias_data (namedtuple): The data from the knobs_to_serialise knob.

    """
    this_alias = alias_data.alias.strip()

    value = alias_data.default_value.strip()

    expression_to_set = "[Ada {key} {alias}]".format(key="aliases", alias=this_alias)

    if this_alias in nuke.Ada.aliases:
        getLog().info("Updating context data: {0} = {1}".format(this_alias, value))
        nuke.Ada.aliases[unicode(this_alias)] = value

    elif this_alias not in nuke.Ada.aliases:
        getLog().info("Setting context data: {0} = {1}".format(this_alias, value))
        nuke.Ada.aliases[this_alias] = value
        knob.setExpression(expression_to_set)

    if this_alias not in expression and "[Ada" in expression:
        old_alias = expression.split("]")[0].split(" ")[-1]
        del nuke.Ada.aliases[old_alias]
        knob.setExpression(expression_to_set)
    else:
        getLog().info("Updating context data: {0} = {1}".format(this_alias, value))


def set_io_item(knob, current_alias, alias_data, iotype):
    """
    Add a knob to set to the correct knob and add an input to the ada context.

    Args:
        knob (nuke.Knob): The knob we want to add the expression to.
        current_alias (str): The knobs current alias value.
        alias_data (namedtuple): The data from the knobs_to_serialise knob.
        iotype (str): input or output.

    """
    expression_to_set = "[Ada {} {} location]".format(iotype, alias_data.index)
    knob.setValue(expression_to_set)

    io_attr = getattr(nuke.Ada, iotype)
    next_item = len(io_attr)

    if next_item == 0:
        new_item = io_attr.add()
        new_item.location = alias_data.default_value
        if iotype == "inputs":
            new_io_entry = INPUT_STRING.format(
                knob=alias_data.knob,
                index=next_item,
                location=alias_data.default_value,
                start=alias_data.start,
                end=alias_data.end,
            )
        elif iotype == "outputs":
            new_io_entry = OUTPUT_STRING.format(
                knob=alias_data.knob,
                index=next_item,
                location=alias_data.default_value,
                start=alias_data.start,
                end=alias_data.end,
            )
        knob.value().replace(current_alias, new_io_entry)

    else:
        if iotype == "inputs":
            io_attr[int(alias_data.index)].location = alias_data.default_value
        elif iotype == "outputs":
            io_attr[int(alias_data.index)].location = alias_data.default_value


def set_output_item(knob, current_alias, alias_data):
    """
    Add a knob to set to the correct knob and add an output to the ada context.

    Args:
        knob (nuke.Knob): The knob we want to add the expression to.
        current_alias (str): The knobs current alias value.
        alias_data (namedtuple): The data from the knobs_to_serialise knob.

    """
    expression_to_set = "[Ada outputs {index} location]".format(index=alias_data.index)
    knob.setValue(expression_to_set)
    try:
        if represents_int(alias_data.index):
            nuke.Ada.outputs[int(alias_data.index)].location = alias_data.default_value

    except IndexError:
        next_output = len(nuke.Ada.outputs)
        new_output = nuke.Ada.outputs.add()
        new_output.location = alias_data.default_value

        new_alias = OUTPUT_STRING.format(
            knob=alias_data.knob,
            index=next_output,
            location=alias_data.default_value,
            start=alias_data.start,
            end=alias_data.end,
        )
        knob.value().replace(current_alias, new_alias)
