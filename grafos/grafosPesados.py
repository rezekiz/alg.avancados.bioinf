from typing import Dict, List
from . import Graph
import graphviz

class WeightedGraph(Graph):
    """
    A subclass of Graph representing a weighted graph.

    Attributes:
        weights: A dictionary to store weights of edges.
    """

    def __init__(self, g: Dict[str, List[str]] = None):
        """
        Initialize a weighted graph.

        Args:
            g: An optional dictionary representing the graph structure.
        """
        super().__init__(g)
        self.weights = {}  # Initialize a dictionary to store edge weights
        self._build()

    def add_weight(self, node, neighbour, weight):
        """
        Add a weight to an edge between two nodes.

        Args:
            node: The source node.
            neighbour: The target node.
            weight: The weight of the edge.
        """
        # Add the edge if it doesn't exist already
        if neighbour not in self.g[node]:
            super().add_edges([f'{node} -> {neighbour}'])
        # Store the weight for the edge
        self.weights[(node, neighbour)] = weight

    def _build(self):
        """
        Build the weighted graph by assigning default weight 0 to all edges.
        """
        # Iterate over all nodes and their neighbors
        for node in self.g.keys():
            for neighbour in self.g[node]:
                if (node, neighbour) not in self.weights.keys():
                    # Add the edge with default weight 0
                    self.add_weight(node, neighbour, 0)

    def show(self, txt: bool = False, gviz: bool = True) -> graphviz.Digraph:
        """
        Displays the graph.

        Args:
            txt (bool, optional): If True, prints the graph structure in text format. Defaults to False.
            gviz (bool, optional): If True, displays the graph using Graphviz. Defaults to True.

        Returns:
            graphviz.Digraph: The Graphviz object representing the graph.
        """
        if txt:
            for key in self.g.keys():
                print(f'{key} ==> {self.g.get(key)}')

        if gviz:
            return self._display()
        
    def _display(self) -> graphviz.Digraph:
        """
        Helper method to display the graph using Graphviz.

        Returns:
            graphviz.Digraph: The Graphviz object representing the graph.
        """
        dot = graphviz.Digraph()

        # Add weighted edges
        for (node, neighbour), weight in self.weights.items():
            dot.edge(node,neighbour, label = str(weight))

        # Add non weighted edges
        for (node, neighbours) in self.g.items():
            for neighbour in neighbours:
                if (node, neighbour) not in self.weights:
                    dot.edge(node,neighbour)
        
        return dot
    
    def shortest_dijkstra_nonweighted(self, start):
        """
        
        """
        pass

"""
# TODO

- Add Dijkstra
"""