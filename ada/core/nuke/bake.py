import os
import argparse
from ada.core.common import getLog
from ada.core.graph import AdaGraph
from ada.core.utils import run_command

NUKE_COMMAND = ["/Applications/Nuke11.3v1/Nuke11.3v1.app/Contents/MacOS/Nuke11.3v1", "-i", "-t"]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Ada is a template baking system that can be run "
        "in any application that supports python."
    )

    parser.add_argument(
        "template",
        action="store",
        help="Template script to bake, ada file should be stored "
        "with the same name on disk.",
    )

    parser.add_argument(
        "--queues",
        default=list(),
        action="store",
        help="Template script to bake, ada file should be stored "
        "with the same name on disk.",
    )

    arguments = parser.parse_args()

    return arguments


def bake_graph(args):
    """
    Create an instance of the engine and fuel it with our template.

    Args:
        args (namespace): Argparse namespace object.

    Returns:
        str: The baked script.

    """
    import nuke
    from ada.nuke.context import Engine
    from ada.nuke.utils import remove_ada_tab
    from ada.nuke.publish import serialise_node_knobs

    engine = Engine()
    engine.fuel(args.template)
    baked = engine.run()

    graph = serialise_node_knobs(engine.queue(baked))

    getLog().info("Ada: removing tabs")
    for node_name in baked:
        node = nuke.toNode(node_name)
        node["knobChanged"].setValue("")
        remove_ada_tab()

    script_path = os.path.join(
        nuke.Ada.output_script.dir, nuke.Ada.output_script.name + ".nk"
    )

    nuke.scriptSaveAs(script_path, overwrite=True)
    getLog().info("Ada: saving: {}".format(script_path))

    return script_path, graph


if __name__ == "__main__":
    args = parse_args()
    script, graph = bake_graph(args)