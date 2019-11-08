import os

import ada_pb2
import graph_pb2
from common import getLog


def write_proto_file(data, directory, name, ext):
    """
    Simple write function to be used in all applications to serialise a rich object to binary strings.

    Args:
        data (protobuf): A protocol buffer to serialise to a binary string.
        directory (str): A valid directory that exists on disk.
        name (str): The name of the protofile we are trying to write.
        ext (str): An extension for our serialised protocol buffer.

    Returns:
        str: Path to the serialised data.

    """
    path = os.path.join(directory, name + ext)
    if not os.path.exists(directory):
        getLog().error("Directory does not exist: {}".format(path))
        return

    with open(path, "wb") as output:
        output.write(data.SerializeToString())

    return path


def read_graph_file(path):
    """
    Create and read a graph protobuf file.

    Args:
        path (str): File path ondisk of the graph protocol buffer object.

    Returns:
        graph_pb2.Scene: A graph protocol buffer with the data for the queues and their attributes stored in it.

    """

    node_graph = graph_pb2.Scene()

    if not os.path.exists(path):
        getLog().error("Missing graph file: {}".format(path))
        return

    with open(path, "rb") as read_file:
        node_graph.ParseFromString(read_file.read())

    return node_graph


def read_ada_file(path):
    """
    Create a context object and load a Ada graph from disk.

    Args:
        path (str): File path ondisk of the ada protocol buffer object.

    Returns:
        ada_pb2.Context: A rich python ada context object.

    """
    context = ada_pb2.Context()
    if not os.path.exists(path):
        getLog().error("Missing ada file: {}".format(path))
        return

    with open(path, "rb") as read_file:
        context.ParseFromString(read_file.read())

    return context
