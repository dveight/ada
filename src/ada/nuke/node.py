
import nuke

from ada.core.common import getLog

from .globals import (
    INPUT_STRING,
    OUTPUT_STRING,
    KnobAlias,
    KnobOutput,
    KnobInput,
    ADA_KNOB_CHANGED,
    INPUT_NODES,
    OUTPUT_NODES,
    KNOB_TO_EXECUTION_TYPE,
)
from .gui import AddKnobsToAda
from .utils import (
    deconstruct_knobs_to_serialise,
    get_class_name,
    has_ada_tab
)

from .globals import ALIAS_STRING

__all__ = ["add_ada_tab", "add_knob_to_bake", "ada_knob_changed", "add_knob_to_ada_tab", "set_alias_knob"]


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
        if node.Class() == "Viewer" or has_ada_tab(node):
            continue

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
            "to assign. eg: 'value=10, file=[ada input 1]'"
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
            "assign value. eg: 'value=10, file=[ada input 1]'"
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

        node.knob("icon").setValue("ada_raw.png")


def add_knob_to_bake(node):
    """Launches the AddKnobsToAda gui allowing the user to select which knobs to bake

    Args:
        node (nuke.Node): The node to add the knobs to bake
    """
    # launch gui for setting alias
    if not nuke.GUI:
        return

    node_class = get_class_name(node)

    if not has_ada_tab(node):
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
                knob_to_serialise = INPUT_STRING.format(knob=knob, alias=alias.value(), location=value.value())
                knobs.append(knob_to_serialise)

            elif node_class in OUTPUT_NODES:
                if knob not in OUTPUT_NODES[node_class]:
                    continue

                knob_to_serialise = OUTPUT_STRING.format(knob=knob, alias=alias.value(), location=value.value())
                knobs.append(knob_to_serialise)

            else:
                knob_to_serialise = ALIAS_STRING.format(knob=knob, alias=alias.value(), default=value.value())
                knobs.append(knob_to_serialise)

    node["knobs_to_serialise"].setValue("\n".join(knobs))


def ada_knob_changed():
    """
    When a user interacts with the knobs to serialise knob they will be modifying context information, this knob
    changed keeps that context information up to date.
    """

    this_node = nuke.thisNode()
    this_knob = nuke.thisKnob()

    if this_knob.name() == "knobs_to_serialise" and has_ada_tab(this_node):

        # split all the values in knobs_to_serialise by their line
        for alias in this_knob.value().split("\n"):
            current_alias = alias.strip()

            if current_alias == "":
                continue

            # for this alias get the correct object with the data inside the function
            ada_data = deconstruct_knobs_to_serialise(current_alias)

            # check to make sure that the serialised data can be parsed
            if not ada_data:
                continue

            # look up the knob on this node
            knob = this_node[ada_data.knob.strip()]

            # get the current expression
            expression = knob.toScript()

            getLog().info("Current expression {0}:{1}".format(knob.name(), expression))

            execution_type = KNOB_TO_EXECUTION_TYPE.get(knob.Class())
            if isinstance(ada_data, KnobAlias):
                set_alias_knob(knob, expression, ada_data, "aliases")
                add_knob_to_ada_tab(this_node, execution_type, "aliases", knob, ada_data.alias)
            if isinstance(ada_data, KnobInput):
                set_alias_knob(knob, expression, ada_data, "inputs")
                add_knob_to_ada_tab(this_node, execution_type, "inputs", knob, ada_data.alias)
            if isinstance(ada_data, KnobOutput):
                set_alias_knob(knob, expression, ada_data, "outputs")
                add_knob_to_ada_tab(this_node, execution_type, "outputs", knob, ada_data.alias)


def add_knob_to_ada_tab(node, execution_type, data_type, knob, alias):
    """

    Args:
        node (nuke.Node):
        execution_type (str):
        data_type (str):
        knob:
        alias:

    Returns:

    """

    ada_tab_knob = node[execution_type]
    if execution_type == "knobs_to_bake" or execution_type == "knobs_to_execute":
        if not node["bake_knobs"].value():
            node["bake_knobs"].setValue(True)

        knob_list = ada_tab_knob.value().split(",")
        if knob_list == [""]:
            knob_list = list()

        if knob.name() in knob_list:
            return

        knob_list.append(knob.name())
        sorted_knobs = sorted(knob_list)

    elif execution_type == "knobs_to_set":
        if not node["set_knobs"].value():
            node["set_knobs"].setValue(True)

        knob_list = ada_tab_knob.toScript().split(",")
        if knob_list == [""]:
            knob_list = list()

        expression = "{}=[Ada {} {}]".format(knob.name(), data_type, alias)
        if expression in knob_list:
            return

        knob_list.append(expression)
        sorted_knobs = sorted(knob_list)

    joined_knobs = ",".join(sorted_knobs)

    ada_tab_knob.setValue(joined_knobs)


def set_alias_knob(knob, expression, alias_data, kind):
    """
    Add an expression to the correct knob and add an alias to the ada context or if the user changes it then
    remove the old context item and add a new one.

    Args:
        knob (nuke.Knob): The knob we want to add the expression to.
        expression (str): The current expression on the node's knob.
        alias_data (namedtuple): The data from the knobs_to_serialise knob.
        kind (str):

    """
    this_alias = alias_data.alias.strip()

    value = alias_data.default_value.strip()

    expression_to_set = "[Ada {kind} {value}]".format(kind=kind, value=this_alias)

    get_ada_kind = getattr(nuke.Ada, kind)

    if this_alias in get_ada_kind:
        getLog().info("Updating context data: {0} = {1}".format(this_alias, value))
        get_ada_kind[this_alias] = value

    elif this_alias not in get_ada_kind:
        getLog().info("Setting context data: {0} = {1}".format(this_alias, value))
        get_ada_kind[this_alias] = value
        knob.setExpression(expression_to_set)

    if this_alias not in expression and "[Ada" in expression:
        old_alias = expression.split("]")[0].split(" ")[-1]
        del get_ada_kind[old_alias]
        knob.setExpression(expression_to_set)
    else:
        getLog().info("Updating context data: {0} = {1}".format(this_alias, value))
