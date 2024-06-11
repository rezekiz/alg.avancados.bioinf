"""
Autor: Rui Sousa

This is a basic implementation of graphs, with the ability to
add/remove nodes/edges, basic traversing and distance calculation.

"""

from typing import Union, List, Dict
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
            #It would be interesting to revise the way this is processed.
            #Initializing with {'1': ['2','3'] , '2' : ['4','5'] would just give 2 nodes.
            #Perhaps adapt _build from weighted graphs?!
            self.g = g

    # Section with methods and basic operations of graphs:
    #    - Addition and removal of nodes
    #    - Addition and removal of edges

    def add_node(self, node: Union[str, int]) -> None:
        """
        Adds a node to the graph.

        Args:
            node (str): The node to be added.
        """
        if not isinstance(node, str):
            if isinstance(node, list):
                raise TypeError('Node must be a string or a number.')

            node = str(node)

        if node not in self.g:
            self.g[node] = []

    def add_edges(self, edges: Union[str, List[str]]) -> None:
        """
        Adds edges to the graph.

        Args:
            edges (list of str): List of edges to be added in the format "Origin -> Destination".
        """
        assert isinstance(edges, (str, list)), 'Edges must be in list or string format'

        if isinstance(edges, str):
            edges = [edges]

        assert all(isinstance(edge, str) for edge in edges), \
            'All elements in the list must be strings'

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

    def show(self, txt: bool = False, gviz: bool = True):
        """
        Displays the graph.

        Args:
            txt (bool, optional): If True, prints graph structure in text format. Defaults to False.
            gviz (bool, optional): If True, displays the graph using Graphviz. Defaults to True.

        Returns:
            graphviz.Digraph: The Graphviz object representing the graph.

        To export to PDF use render():
            graph.show().render()
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

    def rm_node(self, node: Union[str, int]) -> None:
        """
        Removes a node from the graph.

        Args:
            node (str): The node to be removed.
        """
        assert isinstance(node, str), "Node must be in string format"

        if node not in self.g.keys():
            print('Node does not exist.')

        for edge in self.g.values():
            if node in edge:
                edge.remove(node)
        del self.g[node]

    def rm_edges(self, edges: Union[str, List[str]]) -> None:
        """
        Removes edges from the graph.

        Args:
            edges (list of str): List of edges to be removed in the format "Origin -> Destination".
        """
        assert isinstance(edges, (str, list)), 'Edges must be in list or string format'

        if isinstance(edges, str):
            edges = [edges]

        assert all(isinstance(edge, str) for edge in edges), \
            'All elements in the list must be strings'

        for edge in edges:
            edge = edge.replace(' ', '')
            origin, destinations = edge.split('->')
            for destination in destinations.split(','):
                self.g[origin].remove(destination)


    # Section with methods for basic graph information:
    #  - Finding successors, predecessors, and adjacent nodes
    #  - Degree (in/out) of each node
    #  - Adjacency matrix


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
        if node in self.g.keys():
            predecessors = []
            for key, value in self.g.items():
                if node in value:
                    predecessors.append(key)
            return predecessors

        raise KeyError('Node does not exist.')

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
        return sorted(adjacents)

    def adj_matrix(self) -> pd.DataFrame:
        """
        Generates the adjacency matrix of the graph.

        Returns:
            pd.DataFrame: The adjacency matrix.
        """
        matrix = [[] for _ in self.g.keys()]
        nodes = list(self.g.keys())
        cycle = 0

        for node in self.g.keys():
            for _ in nodes:
                if node in self.get_adjacents(_):
                    matrix[cycle].append(1)
                else:
                    matrix[cycle].append(0)
            cycle += 1

        matrix = pd.DataFrame(
            matrix,
            index=list(self.g.keys()),
            columns=list(self.g.keys())
        )
        return matrix

    # Section with methods for traversing the graphs

    def traverse_bfs(self, node):
        """
        Performs a Breadth-First Search (BFS) traversal on the graph starting from a given node.

        This function explores all neighbor nodes at the current level before moving on to the
        nodes at the next level. Use a queue data structure to maintain order of exploration.

        Args:
            node: The starting node for the traversal.

        Returns:
            A list containing all reachable nodes from the starting node by visit order
        """

        destinations = [(node, None)]  # Queue for BFS traversal - (current node, parent)
        visited = set()  # Set to keep track of visited nodes
        reachables = []  # List to store reachable nodes

        while destinations:
            current, parent = destinations.pop(0)
            visited.add(current)

            # If the current node has no successors and hasn't been added to reachables yet, add it.
            if not self.get_successors(current) and current not in reachables:
                reachables.append(current)
                continue

            for successor in self.get_successors(current):
                # Explore unvisited neighbors
                if successor not in visited:
                    destinations.append((successor, current))  # Add neighbor and parent to queue

                # If the neighbor has already been visited but isn't the parent,
                # add it to reachables if not already there.

                # This ensures all connected components are explored.
                elif successor != parent:
                    if successor not in reachables:
                        reachables.append(successor)

        return reachables

    def traverse_dfs(self, node, visited=None):
        """
        Performs a Depth-First Search (DFS) traversal on the graph starting from a given node.

        This function recursively explores each branch as deeply as possible before backtracking.

        Args:
            node: The starting node for the traversal.
            visited (optional): set to keep track of visited nodes (used internally for recursion).

        Returns:
            A list containing all reachable nodes from starting node by order of visit.

        Credits:
            Base code authored by Neelam Yadav for understanding recursive implementation:
            https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/

            Modified to include caching of reachable nodes for efficiency.
        """

        reachables = []

        if visited is None:
            visited = set()

        visited.add(node)
        if self.get_successors(node):
            for successor in self.get_successors(node):
                if successor not in visited:
                    reachables += self.traverse_dfs(successor, visited)  # Recursive call
        else:
            reachables.append(node)  # Add leaf node
        return reachables

    def dist(self, start, end, visited=None):
        """
        Compute the shortest distance between two nodes in a graph using depth-first search.

        Args:
            start: The starting node.
            end: The target node.
            visited: A set to keep track of visited nodes. Defaults to None.

        Returns:
            The shortest distance between the start and end nodes if they are connected,
            None otherwise.
        """
        assert start in self.g.keys(), f'{start} node does not exist.'
        assert end in self.g.keys(), f'{end} node does not exist.'

        # Initialize visited set if not provided
        if visited is None:
            visited = set()

        # Mark the current node as visited
        visited.add(start)

        # Check if the start node has successors
        if self.get_successors(start):
            # Iterate over each successor of the current node
            for successor in self.get_successors(start):
                # If the successor is the target node, return 1 (distance from start to end)
                if successor == end:
                    return 1

                # If the successor has not been visited, recursively calculate the distance
                if successor not in visited:
                    distance = self.dist(successor, end, visited)
                    # If a valid distance is found, return the distance + 1
                    if distance is not None:
                        return distance + 1

        # If the end node is not reachable from the start node, return None
        return None

    def reach_dist_dfs(self, node, visited=None, distance=0):
        """
        Find reachable nodes from a given node and their distances using breadth-first search.

        Args:
            node: The current node.
            visited: A set to keep track of visited nodes. Defaults to None.
            distance: The distance from the starting node. Defaults to 0.

        Returns:
            A list of tuples, each containing a reachable node and its distance from the given node.
        """

        # Initialize list to store reachable nodes and distances
        reachables = []

        # Initialize visited set if not provided
        if visited is None:
            visited = set()

        # Mark the current node as visited
        visited.add(node)

        # If the node has no successors, append the node itself with its distance
        if not self.get_successors(node):
            reachables.append((node, distance))
            return reachables

        # If the node has successors
        for successor in self.get_successors(node):
            # If the successor has not been visited
            if successor not in visited:
                # Recursively call reach_dist_dfs on the successor with updated distance
                reachables_from_successor = self.reach_dist_dfs(successor, visited, distance + 1)
                # Extend the list of reachable nodes and distances with those from the successor
                reachables.extend(reachables_from_successor)

        return reachables

    def has_cycle(self, node):
        """
        Checks if a node traverses back to itself

        Approach: Check if node is reachable from itself.
        """

        if node in self.traverse_bfs(node):
            return True

        return False
