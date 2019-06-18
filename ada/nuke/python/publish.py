import os
import shutil
import tempfile

import nuke
from ada.core import graph_pb2
from ada.core.io import write_proto_file

from .context import Engine
from .globals import KnobAlias, KnobInput, KnobOutput
from .utils import deconstruct_knobs_to_serialise


def publish(save_dir, save_name, nodes=None):
    """
    Very simple "publisher" where the script is saved along side a graph file.

    Args:
        save_dir (str): A valid file path.
        save_name (str): What you want to call the script.
        nodes (list): List of nodes to publish.

    Returns:

    """
    nodes = nodes or nuke.selectedNodes()

    if not os.path.exists(save_dir):
        return

    id, path = tempfile.mkstemp(".nk", "F_")
    nuke.nodeCopy(path)

    nuke_script = "F_{0}.nk".format(save_name)
    script_path = os.path.join(save_dir, nuke_script)
    shutil.move(path, script_path)

    processor = Engine()
    nodes = processor.gather(nodes)
    queue = processor.queue(nodes)

    graph = serialise_node_knobs(queue)
    write_proto_file(graph, save_dir, "F_{0}".format(save_name), ".graph")


def serialise_node_knobs(queues):
    """
    Create a graph object, iterate over all the nodes in each queue setting the attributes from the nodes and root
    format.

    Args:
        queues (itertools.groupby): A groupby object of the queue order and the nodes in that queue.

    Returns:
        graph_pb2: A graph object that we will later write to disk.

    """
    graph = graph_pb2.Scene()

    graph.root.fps = nuke.Root()["fps"].value()
    graph.root.views.extend(nuke.views())

    for order, nodes in queues:
        current_queue = graph.queue.add()
        current_queue.order = order

        for node_name in list(nodes):
            node = nuke.toNode(node_name)

            knobs_to_serialise = node["knobs_to_serialise"].value()

            current_node = current_queue.nodes.add()
            current_node.name = node.name()
            current_node.full_name = node.fullName()
            current_node.Class = node.Class()

            if not knobs_to_serialise:
                continue

            knob_list_to_serialise = knobs_to_serialise.split("\n")
            for knob in knob_list_to_serialise:

                alias_settings = deconstruct_knobs_to_serialise(knob)

                if not alias_settings or not node.knobs().get(alias_settings.knob):
                    continue

                knob_object = node[alias_settings.knob]
                attribute = current_node.attributes.add()
                field_names = attribute.DESCRIPTOR.fields_by_name

                # set the alias name
                if isinstance(alias_settings, KnobAlias):
                    attribute.type = 0
                    attribute.alias.name = alias_settings.alias

                elif isinstance(alias_settings, KnobInput):
                    attribute.type = 1

                elif isinstance(alias_settings, KnobOutput):
                    attribute.type = 2

                for field_name in field_names:
                    if hasattr(knob_object, field_name):
                        # we are setting a default knob value type

                        if field_name == "value":
                            value = knob_object.value()
                            if hasattr(knob_object, "evaluate"):
                                value = knob_object.evaluate()

                            setattr(attribute, field_name, str(value))

                        else:
                            get_knob_object = getattr(knob_object, field_name)
                            if isinstance(get_knob_object(), list):
                                get_repeated = getattr(attribute, field_name)
                                get_repeated.extend(get_knob_object())
                            else:
                                setattr(attribute, field_name, str(get_knob_object()))
    return graph
