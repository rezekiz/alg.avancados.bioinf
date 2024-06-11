"""
Base code sourced from class powerpoints (authored by Rui Mendes) with minor edits
changes to the workflow, namely:

    - implementation of tagging
    - implementation of de-tagging for reconstruction
    - handling multiple hamiltonian paths for future proofing
"""


from grafos import Graph
from typing import List, Dict


"""
=============================
#                           #
#       Static Methods      #
#                           #
=============================
"""
def k_merify(seq: str, k: int = 3) -> List[str]:
    """
    Generates a list of k-mers from a given sequence.

    Args:
        k: size of k-mers
        seq: target sequence

    Returns:
        list: list of k-mers
    """
    assert k > 0 and k < len(seq)
    return sorted([seq[i:i+k] for i in range(len(seq)-k+1)])


def suffix(seq):
    """
    Returns the suffix of the given sequence, excluding the first character.

    Args:
        seq: target sequence

    Returns:
        str: suffix of the sequence
    """
    return seq[1:]


def prefix(seq):
    """
    Returns the prefix of the given sequence, excluding the last character.

    Args:
        seq: target sequence

    Returns:
        str: prefix of the sequence
    """
    return seq[:-1]


class AssemblyGraph(Graph):
    def __init__(self, frags: List[str]) -> Dict[str, str]:
        """
        Initializes the AssemblyGraph with the given fragments.

        Args:
            frags: list of string fragments
        """
        super().__init__()
        self.assemble(frags)

    def assemble(self, frags: List[str]):
        """
        Assembles the graph by adding edges between fragments where the suffix of one fragment matches the prefix of another.

        Args:
            frags: list of string fragments
        """
        idA = 1  # Adds a tag in the order of fragment appearance
        for A in frags:
            suf = suffix(A)
            idB = 1
            for B in frags:
                if prefix(B) == suf:
                    self.add_edges(f'{A}-{idA} -> {B}-{idB}')
                idB += 1
            idA += 1

    def valid_path(self, path: List[str]) -> bool:
        """
        Checks if the given path is a valid path in the graph.

        Args:
            path: list of nodes representing the path

        Returns:
            bool: True if the path is valid, False otherwise
        """
        if path[0] not in self.g.keys():
            return False
        for i in range(1, len(path)):
            if path[i] not in self.g.keys():
                return False
        return True

    def is_hamiltonian(self, path: List[str]) -> bool:
        """
        Checks if the given path is a Hamiltonian path in the graph.

        Args:
            path: list of nodes representing the path

        Returns:
            bool: True if the path is Hamiltonian, False otherwise
        """
        if self.valid_path(path):
            dests = list(self.g.keys())
            if len(path) != len(dests):
                return False
            for i in range(len(path)):
                if path[i] in dests:
                    dests.remove(path[i])
                else:
                    return False
            return not dests
        return False

    def hamiltonian_reconstruction(self, path: List[str]) -> List[str]:
        """
        Reconstructs the sequence from the Hamiltonian path.

        Args:
            path: list of nodes representing the Hamiltonian path

        Returns:
            list: the reconstructed sequence, or None if the path is not Hamiltonian
        """
        import re

        if self.is_hamiltonian(path):
            seq = self._get_seq(path[0])
            for i in range(1, len(path)):
                next = self._get_seq(path[i])
                seq += next[-1]
            return seq
        else:
            return None

    def _get_seq(self, node: str) -> str:
        """
        Extracts the sequence part of the node string.

        Args:
            node: node string

        Returns:
            str: sequence part of the node string
        """
        import re

        if node not in self.g.keys():
            return None
        else:
            return re.match(r"([A-Z]+)-\d+", node).group(1)

    def get_hamiltonian_paths(self) -> List[List[str]]:
        """
        Gets all Hamiltonian paths in the graph.

        Returns:
            list: list of Hamiltonian paths
        """
        res = []
        for node in self.g.keys():
            path = self.scan_hamiltonian_from_node(node)
            if path is not None:
                res.append(path)
        if len(res) > 1:
            return res
        else:
            return res[0]

    def scan_hamiltonian_from_node(self, start: str) -> List[str]:
        """
        Scans for a Hamiltonian path starting from the given node.

        Args:
            start: starting node

        Returns:
            list: Hamiltonian path if found, None otherwise
        """
        current = start
        visited = {start: 0}
        path = [start]
        while len(path) < len(self.g.keys()):
            next_index = visited[current]
            if len(self.g[current]) > next_index:
                next_node = self.g[current][next_index]
                visited[current] += 1
                if next_node not in path:
                    path.append(next_node)
                    visited[next_node] = 0
                    current = next_node
            else:
                if len(path) > 1:
                    remove_node = path.pop()
                    del visited[remove_node]
                    current = path[-1]
                else:
                    return None
        return path
