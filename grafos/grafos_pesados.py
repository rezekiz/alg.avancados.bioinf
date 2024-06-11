"""
Autor: Rui Sousa

Graph subclass that implements weight features to graphs.
"""

from typing import Dict, List
import graphviz
from . import Graph



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
        # Convert to string
        node = str(node)
        neighbour = str(neighbour)

        # Handle weight
        if not self._is_number(weight):
            raise TypeError('Weight must be a number')

        weight = int(weight)

        if weight < 0:
            raise ValueError('Weight must be positive.')

        # Add node if not exists
        if node not in self.g.keys():
            super().add_node(node)

        # Add the edge if it doesn't exist already
        if neighbour not in self.g[node]:
            super().add_edges([f'{node} -> {neighbour}'])
        # Store the weight for the edge
        self.weights[(node, neighbour)] = weight

    def _is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

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
            txt (bool, optional): If True, prints the graph structure. Defaults to False.
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
            dot.edge(node, neighbour, label=str(weight))

        # Add non weighted edges
        for (node, neighbours) in self.g.items():
            for neighbour in neighbours:
                if (node, neighbour) not in self.weights:
                    dot.edge(node, neighbour)

        return dot

    def dijkstra(self, start):
        """
        Find the shortest paths from a starting node to the other nodes.
    
        Args:
            start: The starting node for the shortest path calculation.
    
        Returns:
            distances: A dictionary where keys are nodes and values are the shortest distances
            from the start node to each node.
        """

        # Ensure weights is not empty and weights are properly build
        if not self.weights:
            self._build()

        # Initialize distances for all nodes to infinity except the starting node (set to 0).
        distances = {node: float('inf') for node in self.g}
        distances[start] = 0

        # Initialize a queue with the starting node and its parent.
        queue = [(start, None)]
        visited = set()  # Set to keep track of visited nodes and avoid cycles.

        # While there are nodes left in the queue:
        while queue:
            # Pop the first node and its parent from the queue.
            current, parent = queue.pop(0)

            # Keep track of visited nodes to avoid cycles.
            if current in visited:
                continue

            visited.add(current)

            # For each successor of the current node:
            for successor in self.get_successors(current):
                # If the successor is not visited:
                if successor not in visited:
                    # Add the successor and current node pair to the queue.
                    queue.append((successor, current))

                    # Update the distance to the successor if a shorter path is found.
                    edge_weight = self.weights[current, successor]
                    if distances[successor] == float('inf'):
                        distances[successor] = distances[current] + edge_weight
                    elif distances[successor] > distances[current] + edge_weight:
                        distances[successor] = distances[current] + edge_weight

        return distances
