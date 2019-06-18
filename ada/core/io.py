import os

import ada_pb2
import graph_pb2
from common import getLog


def write_proto_file(data, dir, name, ext):
    """
    Simple write function to be used in all applications to serialise a rich object to binary strings.

    Args:
        data (protobuf): A protocol buffer to serialise to a binary string.
        dir (str): A valid directory that exists on disk.
        name (str): The name of the protofile we are trying to write.
        ext (str): An extension for our serialised protocol buffer.

    Returns:
        str: Path to the serialised data.

    """
    path = os.path.join(dir, name + ext)
    if not os.path.exists(dir):
        getLog().error("Directory does not exist: {}".format(path))
        return

    output = open(path, "wb")
    output.write(data.SerializeToString())
    output.close()

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

    read_file = open(path, "rb")
    node_graph.ParseFromString(read_file.read())
    read_file.close()

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

    read_file = open(path, "rb")
    context.ParseFromString(read_file.read())
    read_file.close()

    return context
