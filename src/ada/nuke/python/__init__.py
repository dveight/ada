import os
import sys

import nuke
from ada.core import ada_pb2
from ada.core.common import getLog
from ada.core.io import write_proto_file

import context
import registry
import utils

__all__ = ["utils", "registry", "context"]


def ada():
    """Extra attribute so that we can call the current
    Ada context via 'nuke'.

    Returns:
        ada_pb2.Context: a proto buf context.

    """
    return ada.value


ada.value = None
nuke.Ada = ada_pb2.Context()

# create a global Ada module in the nuke __main__ module
sys.modules["__main__"].Ada = nuke.Ada


def load_ada_context_from_file():
    """From a root script find an associated ada file with it."""

    root_script = nuke.Root().name()
    if not root_script.endswith(".nk"):
        return

    script_directory = os.path.dirname(root_script)
    script_name = os.path.basename(root_script)

    ada_context_file = "{0}.{1}".format(os.path.splitext(script_name)[0], "ada")
    ada_file_path = os.path.join(script_directory, ada_context_file)

    getLog().info("Ada: Attempting to find context file: {0}".format(ada_file_path))

    if os.path.exists(ada_file_path):
        getLog().debug("Ada: context found: {0}".format(ada_file_path))

        # read the ada context file from the script dir
        f = open(ada_file_path, "rb")
        nuke.Ada.ParseFromString(f.read())
        f.close()

        getLog().debug(
            "Ada: context successfully loaded from file: {0}".format(nuke.Ada)
        )
    elif nuke.Root().knobs().get("__ada"):
        get_ada_from_root = nuke.Root()["__ada"].value()
        nuke.Ada.ParseFromString(get_ada_from_root)
        getLog().debug(
            "Ada: context successfully loaded from root: {0}".format(nuke.Ada)
        )


def save_ada_context_to_file():
    """Save an Ada file with the script if there is something in the context."""

    root_script = nuke.Root().name()
    if not root_script.endswith(".nk"):
        return

    script_directory = os.path.dirname(root_script)
    script_name = os.path.basename(root_script)

    write_proto_file(
        nuke.Ada, script_directory, os.path.splitext(script_name)[0], ".ada"
    )


def setupGUI():
    # Right-mouse Popcorn menu for knobs derived from nuke.Array_Knob
    nuke.menu("Animation").addCommand(
        "Ada/Bake This Knob",
        "__import__('ada.nuke.node', "
        "fromlist=['add_knob_to_bake']).add_knob_to_bake(nuke.thisNode(), nuke.thisKnob().name())",
    )

    menu = nuke.menu("Nuke")

    menu.addCommand(
        "Tools/Ada/Remove Ada Tab",
        "__import__('ada.nuke.utils', "
        "fromlist=['remove_ada_tab']).remove_ada_tab(nuke.selectedNodes())",
        shortcut="Shift+Alt+t",
    )
    menu.addCommand(
        "Tools/Ada/Bake Selected",
        "__import__('ada.nuke.context', "
        "fromlist=['Engine']).Engine.run(nodes=nuke.selectedNodes())",
        shortcut="Shift+b",
    )

    menu.addCommand(
        "Tools/Ada/Add Knobs To Bake",
        "__import__('ada.nuke.node', "
        "fromlist=['add_knob_to_bake']).add_knob_to_bake(nuke.selectedNode())",
        shortcut="Shift+t",
    )


# add ada file loader
nuke.addOnScriptLoad(load_ada_context_from_file)
# add ada file loader
nuke.addOnScriptSave(save_ada_context_to_file)

# add on destroy callback to remove any context information that nodes are associated with.
