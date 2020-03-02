from ada.core.io import read_graph_file


class AdaGraph:
    def __init__(self, filepath=None, graph=None):
        self.file = filepath
        self.graph = graph

    def read(self):
        graph = read_graph_file(self.file)
        self.graph = graph
        print graph
        return graph

    def all_nodes(self, _class=None):
        """
        Search all queues for nodes and if _class is supplied limit the results to only those classes.

        Args:
            _class (str): The class name of the node you are looking for.

        Examples:
            AdaGraph.all_nodes("Write")

        Returns:
            list: All the nodes found.

        """
        if not self.graph:
            self.read()

        _nodes = []

        for queue in self.graph.queue:
            for node in queue.nodes:
                if _class:
                    if node.Class.encode("UTF-8") == _class:
                        _nodes.append(node.full_name)
                else:
                    _nodes.append(node.full_name)
        return _nodes

    def outputs(self):
        if not self.graph:
            self.read()

        _nodes = []

        for queue in self.graph.queue:
            for node in queue.nodes:
                for attribute in node.attributes:
                    if attribute.type == 2:
                        _nodes.append(node.full_name)
        return _nodes
