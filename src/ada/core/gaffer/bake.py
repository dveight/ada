from .executable import GAFFER_EXECUTABLE

GAFFER_COMMAND = [GAFFER_EXECUTABLE, "-t"]


def bake_graph(args):
    """
    bakes a gaffer script out removing / substituting any ada variables

    :param list args: the arguments for baking the graph

    :return: error code
    :rtype: int
    """
    pass
