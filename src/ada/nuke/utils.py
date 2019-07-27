"""Utility functions used in Nuke to process python-ada-core tcl,
python-ada-core tabs and to aid with baking down expressions."""

import re
import sys

import nuke

import functools

from .globals import KnobAlias, KnobInput, KnobOutput, ADA_KNOBS, ADA_KNOB_PAIRS, ADA_OPTIONAL_KNOBS


__all__ = ["can_cast", "has_ada_tab", "can_bake_node", "monkey_patch", "parse_tcl_string", "remove_ada_tab",
           "get_class_name", "autolabel", "deconstruct_knobs_to_serialise", "deserialise_knobs_to_serialise"]


def can_cast(value, class_type):
    """
    Check if the value can be cast to the class_type, used in the parse tcl string function for tcl expressions like
    [Ada inputs 0] or [Ada alias robotblur]

    Args:
        value (object): The object we're attempting to cast.
        class_type (class): The class we're attempting to cast to.

    Returns:
        bool: If the value can be successfully cast
    """
    try:
        class_type(value)
        return True
    except (ValueError, TypeError):
        return False


def has_ada_tab(node):
    """
    Checks to see if the node has an ada tab already added

    Args:
        node (nuke.Node): the nuke node to check

    Returns:
        bool: whether or not the node has the ada tab on it
    """
    return isinstance(node.knob("ada"), nuke.Tab_Knob)


def can_bake_node(node):
    """
    Checks to see if the node has an ada tab, is not set to 'do not bake' and has values to bake

    Args:
        node (nuke.Node): The node to check to see if any knobs are set for baking

    Returns:
        bool: Whether or not the node can be baked
    """
    if not has_ada_tab(node) or node["do_not_bake"].value():
        return False
    for enable, value in ADA_KNOB_PAIRS.items():
        if node[enable].value() and node[value].value():
            return True
    return False


# noinspection PyPep8Naming
class monkey_patch(object):
    """
    Patches a function and saves the original function as the variable f
    """
    def __init__(self, f):
        self.f = f

    def __call__(self, f):
        @functools.wraps(f)
        def w(*args, **kwargs):
            return f(*args, **kwargs) or self.f(*args, **kwargs)
        m = nuke if self.f.__module__ == "_nuke" else sys.modules[self.f.__module__]
        setattr(m, self.f.__name__, w)
        return w


def parse_tcl_string(args):
    """
    Iterate over the args of a tcl string, split by space and look up data in the Ada context.

    Args:
        args (str): A string of arguments from tcl, eg. "inputs 0"

    Returns:
        attribute: An attribute from the Ada context or None if it can't be found

    """
    argument_list = args.split(" ")

    if len(argument_list) < 1:
        return

    previous_attr = getattr(nuke.Ada, argument_list[0])

    for argument in argument_list[1:]:
        try:
            # if an argument represents an int, then it is an index into
            # a list in the proto file.
            if can_cast(argument, int):
                try:
                    previous_attr = previous_attr[int(argument)]
                    continue
                except TypeError:
                    pass
            if hasattr(previous_attr, argument):
                previous_attr = getattr(previous_attr, argument)
            else:
                previous_attr = previous_attr[argument]
        except (IndexError, AttributeError, TypeError, ValueError):
            return None

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

    match = re.match(r"(\w+)\((\w+)(?:[ ,]+)?(\w+)(?:[ ,]+)?([^, ]+)\)", alias)
    if not match:
        return

    function_name = match.groups()[0]
    args_index = [argument.strip() for argument in match.groups()[1:]]

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

    if nuke.GUI and ask and not nuke.ask("Delete Ada tab on {0} node(s)?".format(len(nodes))):
        return

    for node in nodes:
        # check and remove optional knobs and ada knobs too
        for knob_name in ADA_OPTIONAL_KNOBS + ADA_KNOBS:
            knob = node.knob(knob_name)
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
