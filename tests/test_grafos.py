"""
Test Suite for Graph and WeightedGraph Classes

This module contains a collection of unit tests for the Graph and WeightedGraph
classes from the 'grafos' module. These tests ensure that the graph classes
function correctly in terms of creating graphs, adding/removing nodes and edges,
displaying the graph, and performing various graph operations such as traversals,
distance calculations, and cycle detection.

Classes:
    TestGrafos (unittest.TestCase):
        Contains unit tests for the Graph class.
    TestGrafosPesados (unittest.TestCase):
        Contains unit tests for the WeightedGraph class.

Tests in TestGrafos:
    - testCreate: Tests creation of graphs with and without predefined structure.
    - testAddNode: Tests addition of valid and invalid nodes to the graph.
    - testAddEdge: Tests addition of valid and invalid edges to the graph.
    - testDisplay: Tests the graphical display function of the graph.
    - testNodeRemoval: Tests removal of valid and invalid nodes from the graph.
    - testEdgeRemoval: Tests removal of valid and invalid edges from the graph.
    - testGetSuccessors: Tests retrieval of successors for valid and invalid nodes.
    - testGetPredecessors: Tests retrieval of predecessors for valid and invalid nodes.
    - testGetAdjacents: Tests retrieval of adjacent nodes for valid and invalid nodes.
    - testAdjMatrix: Tests generation of adjacency matrix for the graph.
    - testBFSTraversal: Tests Breadth-First Search (BFS) traversal from a valid node and handling of invalid nodes.
    - testDFSTraversal: Tests Depth-First Search (DFS) traversal from a valid node and handling of invalid nodes.
    - testDistCalc: Tests calculation of shortest path distance between nodes.
    - testDistTable: Tests generation of distance table using DFS.
    - testCycleCheckR: Tests cycle detection in the graph.

Tests in TestGrafosPesados:
    - testAddWeight: Tests addition of weights to edges and handling of invalid inputs.
    - testBuildR: Tests the build process of the weighted graph.
    - testDijkstra: Tests Dijkstra's algorithm for shortest path calculation and handling of invalid nodes.

This test suite covers some of the essential aspects of graph functions. It could be further improving by experimenting
extreme and edge cases.

"""
import unittest

# Add parent dir to path to ensure module is found
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modules
from grafos import Graph
from grafos.grafos_pesados import WeightedGraph


class TestGrafos(unittest.TestCase):

    # Testar criação de grafos com e sem pré-definição

    def testCreate(self):
        grafo_none = Graph()
        grafo_pred = Graph({'1': ['2', '3']})

        self.assertEqual(grafo_none.g, {})
        self.assertEqual(grafo_pred.g, {'1': ['2', '3']})

    def testAddNode(self):
        g = Graph()

        # Adicionar nó válido
        g.add_node('1A@')
        self.assertEqual(g.g, {'1A@': []})

        # If user inputs a number
        g.add_node(1)
        self.assertEqual(g.g, {'1A@': [], '1': []})

        # If user inputs a diferent type
        with self.assertRaises(TypeError):
            g.add_node(['1', 1])

    def testAddEdge(self):
        g = Graph()

        # Adicionar uma edge válida
        g.add_edges('1 -> 2')
        self.assertEqual(
            g.g,
            {
                '1': ['2'],
                '2': []
            }
        )

        # Adicionar várias válidas
        g.add_edges('2 ->  3, @')
        self.assertEqual(
            g.g,
            {
                '1': ['2'],
                '2': ['3', '@'],
                '3': [],
                '@': []
            }
        )

        # Adicionar inválidas
        with self.assertRaises(ValueError):
            g.add_edges('1 -> 2 -> 3')

        with self.assertRaises(AssertionError):
            g.add_edges([1, 2])

        with self.assertRaises(ValueError):
            g.add_edges(['1', '2'])

    def testDisplay(self):
        # Faz sentido testar esta função?
        import graphviz  # Apenas para efeitos do teste

        g = Graph({'1': ['2', '3'], '2': ['4', '5']})
        export = g.show()

        self.assertIsInstance(export, graphviz.graphs.Digraph, 'Output not correct.')

    def testNodeRemoval(self):
        g = Graph({'1': ['2', '3'], '2': ['4', '5'], '3': ['6', '7']})

        # Valid node
        g.rm_node('2')
        self.assertEqual(
            g.g,
            {
                '1': ['3'],
                '3': ['6', '7']
            }
        )

        # Invalid node
        with self.assertRaises(KeyError):
            g.rm_node('@@')

        with self.assertRaises(AssertionError):
            g.rm_node(2)

    def testEdgeRemoval(self):
        g = Graph({'1': ['2', '3'], '2': ['4', '5'], '3': ['6', '7']})

        # Valid edges
        # Single
        g.rm_edges('1 -> 2')
        self.assertEqual(
            g.g,
            {
                '1': ['3'],
                '2': ['4', '5'],
                '3': ['6', '7']

            }
        )

        # Multiple
        g.rm_edges(['3 -> 6,7', '2->4'])
        self.assertEqual(
            g.g,
            {
                '1': ['3'],
                '2': ['5'],
                '3': []
            }
        )

        # Invalid edges
        with self.assertRaises(ValueError):
            g.rm_edges(['1', '2'])

        with self.assertRaises(AssertionError):
            g.rm_edges([1, 2])

    def testGetSuccessors(self):
        g = Graph({'1': ['2', '3'], '2': ['4', '5'], '3': ['6', '7'], '4': []})

        # Valid node
        self.assertEqual(g.get_successors('1'), ['2', '3'])
        self.assertEqual(g.get_successors('4'), [])
        # Invalid node

        with self.assertRaises(KeyError):
            g.get_successors('@@')

        with self.assertRaises(KeyError):
            g.get_successors(2)

    def testGetPredecessors(self):
        g = Graph({'1': ['2', '3'], '2': ['3', '4', '5'], '3': ['6', '7']})

        # Valid node
        self.assertEqual(g.get_predecessors('3'), ['1', '2'])

        self.assertEqual(g.get_predecessors('1'), [])

        # Invalid node

        with self.assertRaises(KeyError):
            g.get_predecessors('@@')

        with self.assertRaises(KeyError):
            g.get_predecessors(2)

    def testGetAdjacents(self):
        g = Graph({'1': ['2', '3'], '2': ['4', '5'], '3': ['6', '7']})

        # Valid node
        self.assertEqual(g.get_adjacents('2'), ['1', '4', '5'])

        # Invalid node

        with self.assertRaises(KeyError):
            g.get_adjacents('@@')

        with self.assertRaises(KeyError):
            g.get_adjacents(2)

    def testAdjMatrix(self):
        # Considering how finicky the initialization is right now
        g = Graph({'1': ['2', '3'], '2': ['1', '5'], '3': ['6', '7']})

        matrix = g.adj_matrix().to_dict()  # Para ficar em formato comparável

        self.assertEqual(
            matrix,
            {
                '1': {'1': 0, '2': 1, '3': 1},
                '2': {'1': 1, '2': 0, '3': 0},
                '3': {'1': 1, '2': 0, '3': 0},
            }
        )

        g = Graph()

        g.add_edges(['1 -> 2,3', '3->4', '2 ->4'])

        matrix = g.adj_matrix().to_dict()
        self.assertEqual(
            matrix,
            {
                '1': {'1': 0, '2': 1, '3': 1, '4': 0},
                '2': {'1': 1, '2': 0, '3': 0, '4': 1},
                '3': {'1': 1, '2': 0, '3': 0, '4': 1},
                '4': {'1': 0, '2': 1, '3': 1, '4': 0},

            }
        )

    def testBFSTraversal(self):

        g = Graph()
        g.add_edges(['1 -> 2, 3, 4', '2 -> 5, 6', '5 -> 7', '3 -> 6, 8', '4 -> 8'])

        # Valid node
        self.assertEqual(g.traverse_bfs('1'), ['6', '8', '7'])

        # Invalid node
        with self.assertRaises(KeyError):
            g.traverse_bfs('@@')

        with self.assertRaises(KeyError):
            g.traverse_bfs(2)

    def testDFSTraversal(self):
        g = Graph()
        g.add_edges(['1 -> 2, 3, 4', '2 -> 5, 6', '5 -> 7', '3 -> 6, 8', '4 -> 8'])

        # Valid node
        self.assertEqual(g.traverse_dfs('1'), ['7', '6', '8'])

        # Invalid node
        with self.assertRaises(KeyError):
            g.traverse_bfs('@@')

        with self.assertRaises(KeyError):
            g.traverse_bfs(2)

    def testDistCalc(self):
        g = Graph()
        g.add_edges(['1 -> 2, 3, 4', '2 -> 5, 6', '5 -> 7', '3 -> 6, 8', '4 -> 8'])

        # Valid nodes
        self.assertEqual(g.dist('1', '8'), 2)

        # Invalid start/destination/both
        with self.assertRaises(AssertionError):
            g.dist('0', '8')

        with self.assertRaises(AssertionError):
            g.dist('@@', '8')

        with self.assertRaises(AssertionError):
            g.dist('1', '50')

    def testDistTable(self):
        g = Graph()
        g.add_edges(['1 -> 2, 3, 4', '2 -> 5, 6', '5 -> 7', '3 -> 6, 8', '4 -> 8'])

        # Valid nodes
        self.assertEqual(
            g.reach_dist_dfs('1'),
            [('7', 3), ('6', 2), ('8', 2)]
        )

        test_nodes = ['@@', 2]

        for test_node in test_nodes:

            with self.assertRaises(KeyError):
                g.reach_dist_dfs(test_node)

    def testCycleCheckR(self):

        g = Graph({
            '1': ['2', '3', '4'],
            '2': ['5', '6'],
            '3': ['6', '8'],
            '4': ['8'],
            '5': ['7'],
            '6': [],
            '7': [],
            '8': ['1']
        })

        # A node that returns to itself
        self.assertEqual(g.has_cycle('1'), True)
        # A node that does not have a cycle
        self.assertEqual(g.has_cycle('2'), False)
        # An invalid node
        with self.assertRaises(KeyError):
            g.has_cycle('@@')


class TestGrafosPesados(unittest.TestCase):

    def testAddWeight(self):

        g = WeightedGraph()
        g.add_edges('1->2')

        # Valid input
        g.add_weight('1', '2', 3)
        self.assertEqual(g.weights, {('1', '2'): 3})

        # Updates the weight
        g.add_weight('1', '2', 4)
        self.assertEqual(g.weights, {('1', '2'): 4})

        # Creates a node
        g.add_weight('1', '3', 3)
        self.assertEqual(g.weights, {('1', '2'): 4, ('1', '3'): 3})

        # Type correction
        g.add_weight('1', 5, '3')
        self.assertEqual(g.weights, {('1', '2'): 4, ('1', '3'): 3, ('1', '5'): 3})

        # Invalid input        
        with self.assertRaises(TypeError):
            g.add_weight('1', '2', 'one')

        # Adding negative weights
        with self.assertRaises(ValueError):
            g.add_weight('1', '2', -3)



    def testBuildR(self):

        g = WeightedGraph()

        g.add_edges(['1 -> 2,3', '2 -> 4,5'])

        g.add_weight('4', '5', 3)

        g._build()
        
        self.assertEqual(
                g.weights,
                {
                    ('1', '2'): 0,
                    ('1', '3'): 0,
                    ('2', '4'): 0,
                    ('2', '5'): 0,
                    ('4', '5'): 3
                }
                ) 
        
    def testDijkstra(self):

        g = WeightedGraph()

        g.add_edges(['1 -> 2,3,4', '2 -> 5,6', '3 ->6,8', '4->8', '5->7'])

        # Check if auto-build is working proper
        self.assertEqual(
            g.dijkstra('1'),
            {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0}
        )

        g.add_weight('1', '2', '1')
        g.add_weight('1', '3', '1')
        g.add_weight('1', '4', '2')
        g.add_weight('2', '5', '34')
        g.add_weight('2', '6', '3')
        g.add_weight('3', '6', '21')
        g.add_weight('3', '8', '9')
        g.add_weight('5', '7', '5')
        g.add_weight('4', '8', '054')
        self.assertEqual(
            g.dijkstra('1'),
            {'1': 0, '2': 1, '3': 1, '4': 2, '5': 35, '6': 4, '8': 10, '7': 40}
        )

        # Invalid node
        test_nodes = ['@@', 2]

        for _ in test_nodes:
            with self.assertRaises(KeyError):
                g.dijkstra(_)


if __name__ == '__main__':
    unittest.main(verbosity=2)
