"""Utility functions used in Nuke to process python-ada-core tcl,
python-ada-core tabs and to aid with baking down expressions."""

from .globals import KnobAlias, KnobInput, KnobOutput, ADA_KNOBS

import nuke


def represents_int(string):
    """
    Check if the string is an int or not, used in the parse tcl string function for tcl expressions like
    [Ada inputs 0] or [Ada alias robotblur]

    Args:
        string (int, str): Could be an int or a str.

    Returns:

    """
    try:
        int(string)
        return True
    except ValueError:
        return False


def parse_tcl_string(args):
    """
    Iterate over the args of a tcl string, split by space and look up data in the Ada context.

    Args:
        args (str): A string of arguments from tcl.

    Returns:
        attribute: An attribute from the Ada context.

    """
    previous_attr = None

    argument_list = args.split(" ")

    for index, argument in enumerate(argument_list):
        # if an argument represents an int, then it is an index into
        # a list in the proto file.
        try:
            if represents_int(argument):
                argument = int(argument)
                previous_attr = previous_attr[int(argument)]
                continue

            if index == 0:
                previous_attr = getattr(nuke.Ada, argument)
            else:
                try:
                    previous_attr = getattr(previous_attr, argument)
                except AttributeError:
                    if previous_attr:
                        previous_attr = previous_attr[argument]
        except IndexError:
            return previous_attr
        except AttributeError:
            return previous_attr
        except TypeError:
            return previous_attr

    return previous_attr


def deconstruct_knobs_to_serialise(alias):
    """
    On an Ada tab in Nuke the knobs to serialise section will have multiple aliases defined. This function takes an
    alias and parses it to determine its type and argument values.

    Args:
        alias (str): a string such as alias(size, myblur, 100) or input(file, /path/)

    Returns:
        namedtuple: KnobInput, KnobOutput or KnobAlias named tuple object.

    """

    if alias == "":
        return

    function_name, args_str = alias.split("(")
    raw_args_index = args_str.split(",")
    raw_args_index[-1] = raw_args_index[-1].replace(")", "")

    args_index = [argument.strip() for argument in raw_args_index]

    if function_name.startswith("alias"):
        return KnobAlias(*args_index)

    if function_name.startswith("input"):
        return KnobInput(*args_index)

    if function_name.startswith("output"):
        return KnobOutput(*args_index)


def remove_ada_tab(nodes=None, ask=False):
    """
    Function for removing the Ada context tab and knobs from the
    selected nodes.

    Args:
        nodes (optional) : node or list of nodes
            if nodes is not supplied, use nuke.selectedNodes()
        ask (optional) : bool
            pop up a dialog to confirm

    Returns:
        node (nuke.Node): the node we have just removed the tab from.

    """
    nodes = nodes or nuke.selectedNodes()

    if not isinstance(nodes, list):
        nodes = [nodes]

    result = nuke.message("Delete Ada tab on {0} node(s) OK?".format(len(nodes)))
    if nuke.GUI and ask and not result:
        return

    for node in nodes:
        # remove knobs
        for knobName in reversed(ADA_KNOBS):
            knob = node.knob(knobName)
            if knob:
                node.removeKnob(knob)

        # remove auto label
        if node.knobs().get("autolabel"):
            node.knob("autolabel").setValue("")

        # clear icon
        icon = node.knob("icon").value()
        if icon.startswith("ada_"):
            node.knob("icon").setValue("")


def get_class_name(node):
    """
    Simple wrapper to get a _class knob off a node so that you can use standard nuke nodes like group, NoOp etc, but
    give them their own "class".

    Args:
        node (nuke.Node): A node object we want to get a class from.

    Returns:
        str: The node class.

    """
    _class = node.knobs().get("_class")

    if not _class:
        return node.Class()

    return _class.value()


def autolabel():
    """

    Returns:

    """
    pass


def deserialise_knobs_to_serialise(knob, prune=None):

    knobs_to_serialise = knob.value().split("\n")

    if not knobs_to_serialise != [""]:
        return

    for serialised in knobs_to_serialise:
        data = deconstruct_knobs_to_serialise(serialised)
        if prune == data.knob:
            return data
