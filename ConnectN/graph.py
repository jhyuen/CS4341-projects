from collections import defaultdict

class Graph(object):
    
    def __init__(self, connections, directed=False):
        self._graph = defaultdict(set)
        self._directed = directed
        self.add_inital_connections(connections)

    # Add initial connection pairs to graph
    def add_inital_connections(self, connections):

        for node1, node2 in connections:
            self.add_connections(node1, node2)

    # Add connection between node1 and node2 
    def add_connections(self, node1, node2):

        self._graph[node1].add(node2)

        # directed parameter set at construction
        if not self._directed:
            self._graph[node2].add(node1)

    # Removes all references to passed in node
    def remove(self, node):

        for n, cxns in self._graph.iteritems():
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
        except KeyError:
            pass

    # Determines if connection exists between node1 and node2
    def is_connected(self, node1, node2):

        return node1 in self._graph and node2 in self._graph[node1]