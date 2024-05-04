"""
Criação de módulo de grafos
Utilização de graphviz para visualizar
A testagem tem de considerar a adição de nós, vértices e ligações


Autor: Rui Sousa
"""

from typing import List, Dict
import graphviz
import pandas as pd

class Graph:
    """
    Class representing a graph and providing basic graph operations.
    """

    def __init__(self, g: Dict[str, List[str]] = None):
        """
        Initializes the graph.

        Args:
            g (dict, optional): A dictionary representing the graph structure. Defaults to None.
        """
        if g is None:
            self.g = {}
        else:
            self.g = g

    """
    Section with methods and basic operations of graphs:
      - Addition and removal of nodes
      - Addition and removal of edges
    """
    def add_node(self, node: str) -> None:
        """
        Adds a node to the graph.

        Args:
            node (str): The node to be added.
        """
        assert isinstance(node, str),"Node must be in string format"

        if node not in self.g:
            self.g[node] = []

    def add_edges(self, edges: List[str]) -> None:
        # TODO implementar possibilidade de descrever edges como "1 -> 2 -> 2 -> .. n"
        """
        Adds edges to the graph.

        Args:
            edges (list of str): List of edges to be added in the format "Origin -> Destination".
        """
        assert isinstance(edges, (str, list)), 'Edges must be in list or string format'

        if type(edges) is str:
            edges = [edges]

        assert all(isinstance(edge, str) for edge in edges), 'All elements in the list must be strings'

        for edge in edges:
            edge = edge.replace(' ', '')
            origin, destinations = edge.split('->')

            if origin not in self.g.keys():
                self.add_node(origin)

            for destination in destinations.split(','):
                
                if not destination.strip():
                    continue

                if destination not in self.g.keys():
                    self.add_node(destination)

                if destination not in self.g[origin]:
                    self.g[origin].append(destination)

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
        for key in self.g.keys():
            dot.node(str(key))
            for dest in self.g[key]:
                dot.edge(str(key), str(dest))
        return dot

    def rm_node(self, node: str) -> None:
        """
        Removes a node from the graph.

        Args:
            node (str): The node to be removed.
        """
        assert isinstance(node, str),"Node must be in string format"

        if node not in self.g.keys():
            print('Node does not exist.')

        for edge in self.g.values():
            if node in edge:
                edge.remove(node)
        del self.g[node]

    def rm_edges(self, edges: List[str]) -> None:
        """
        Removes edges from the graph.

        Args:
            edges (list of str): List of edges to be removed in the format "Origin -> Destination".
        """
        assert isinstance(edges, (str, list)), 'Edges must be in list or string format'

        if type(edges) is str:
            edges = [edges]

        assert all(isinstance(edge, str) for edge in edges), 'All elements in the list must be strings'

        for edge in edges:
            edge = edge.replace(' ', '')
            origin, destinations = edge.split('->')
            for destination in destinations.split(','):
                self.g[origin].remove(destination)

    """
    Section with methods for basic graph information:
      - Finding successors, predecessors, and adjacent nodes
      - Degree (in/out) of each node
      - Adjacency matrix
    """

    def get_successors(self, node: str) -> List[str]:
        """
        Retrieves the successors of a node.

        Args:
            node (str): The node to retrieve successors for.

        Returns:
            list of str: List of successor nodes.
        """
        return list(self.g[node])

    def get_predecessors(self, node: str) -> List[str]:
        """
        Retrieves the predecessors of a node.

        Args:
            node (str): The node to retrieve predecessors for.

        Returns:
            list of str: List of predecessor nodes.
        """
        predecessors = []
        for key, value in self.g.items():
            if node in value:
                predecessors.append(key)
        return predecessors

    def get_adjacents(self, node: str) -> List[str]:
        """
        Retrieves the adjacent nodes of a given node.

        Args:
            node (str): The node to retrieve adjacent nodes for.

        Returns:
            list of str: List of adjacent nodes.
        """
        predecessors = self.get_predecessors(node)
        successors = self.get_successors(node)
        adjacents = list(set(predecessors + successors))
        return adjacents

    def adj_matrix(self) -> pd.DataFrame:
        """
        Generates the adjacency matrix of the graph.

        Returns:
            pd.DataFrame: The adjacency matrix.
        """
        matrix = [[] for node in self.g.keys()]
        nodes = list(self.g.keys())
        iter = 0

        for node in self.g.keys():
            for _ in nodes:
                if node in self.get_adjacents(_):
                    matrix[iter].append(1)
                else:
                    matrix[iter].append(0)
            iter += 1

        matrix = pd.DataFrame(
            matrix,
            index=[node for node in self.g.keys()],
            columns=[node for node in self.g.keys()]
        )

        return matrix
    
    """
    Section with methods for traversing the graphs
    """

    def traverse_bfs(self,node):

        # TODO corrigir para grafos circulares, está neste momento a ignorar possíveis reachables se o nó original estiver nos visited

        destinations = self.get_successors(node)
        visited = set(node)
        reachables = []

        while destinations:

            current = destinations.pop(0)

            if current in visited:
                continue

            visited.add(current)
            
            if not self.get_successors(current):
                reachables.append(current)
                continue

            for successor in self.get_successors(current):
                if successor not in visited:
                    destinations.append(successor)
            
        return reachables


    def traverse_dfs(self,node):
        pass
