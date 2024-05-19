"""
Testes escritos por Rui Sousa

Check list:

- testar criação de nós;
- testar adição de pesos;
- testar adição de edges;
- testar traversing bfs e dfs;
- testar dijkstra;
- testar matriz de adjacência;
- testar reachables com e sem distância;

"""

import unittest
from grafos import Graph, WeightedGraph

class TestGrafos(unittest.TestCase):

    # Testar criação de grafos com e sem pré-definição

    def testCreate(self):
        grafo_none = Graph()
        grafo_pred = Graph({'1':['2','3']})

        self.assertEqual(grafo_none.g, {})
        self.assertEqual(grafo_pred.g, {'1':['2','3']})

    def testAddNode(self):
        g = Graph()

        # Adicionar nó válido
        g.add_node('1A@')
        self.assertEqual(g.g, {'1A@':[]})

        # Adicionar nó inválido
        with self.assertRaises(AssertionError):
            g.add_node(1)


    def testAddEdge(self):
        g = Graph()

        # Adicionar uma edge válida
        g.add_edges('1 -> 2')
        self.assertEqual(
            g.g,
            {
                '1':['2'],
                '2':[]
            }
        )

        # Adicionar várias válidas
        g.add_edges('2 ->  3, @')
        self.assertEqual(
            g.g,
            {
                '1':['2'],
                '2':['3','@'],
                '3':[],
                '@':[]
            }
        )

        # Adicionar inválidas
        with self.assertRaises(ValueError):
            g.add_edges('1 -> 2 -> 3')

        with self.assertRaises(AssertionError):
            g.add_edges([1,2])

        with self.assertRaises(ValueError):
            g.add_edges(['1','2'])

    def testDisplay(self):
        #Faz sentido testar esta função?
        import graphviz # Apenas para efeitos do teste

        g = Graph({'1':['2','3'], '2' : ['4','5']})
        export = g.show()

        self.assertIsInstance(export, graphviz.graphs.Digraph, 'Output not correct.')

    def testNodeRemoval(self):
        g = Graph({'1':['2','3'], '2' : ['4','5'], '3' : ['6','7']})

        # Valid node
        g.rm_node('2')
        self.assertEqual(
            g.g,
            {
                '1':['3'],
                '3':['6','7']
            }
        )

        # Invalid node
        with self.assertRaises(KeyError):
            g.rm_node('@@')

        with self.assertRaises(AssertionError):
            g.rm_node(2)

    def testEdgeRemoval(self):
        g = Graph({'1':['2','3'], '2' : ['4','5'], '3' : ['6','7']})

        # Valid edges
        # Single
        g.rm_edges('1 -> 2')
        self.assertEqual(
            g.g,
            {
                '1':['3'],
                '2':['4','5'],
                '3':['6','7']

            }
        )

        # Multiple
        g.rm_edges(['3 -> 6,7','2->4'])
        self.assertEqual(
            g.g,
            {
                '1':['3'],
                '2':['5'],
                '3':[]
            }
        )

        # Invalid edges
        with self.assertRaises(ValueError):
            g.rm_edges(['1','2'])

        with self.assertRaises(AssertionError):
            g.rm_edges([1,2])
    def testGetSuccessors(self):
        g = Graph({'1': ['2', '3'], '2': ['4', '5'], '3': ['6', '7'], '4':[]})

        # Valid node
        self.assertEqual(g.get_successors('1'), ['2','3'])
        self.assertEqual(g.get_successors('4'), [])
        # Invalid node

        with self.assertRaises(KeyError):
            g.get_successors('@@')

        with self.assertRaises(KeyError):
            g.get_successors(2)

    def testGetPredecessors(self):
        g = Graph({'1': ['2', '3'], '2': ['3','4', '5'], '3': ['6', '7']})

        # Valid node
        self.assertEqual(g.get_predecessors('3'), ['1', '2'])

        self.assertEqual(g.get_predecessors('1'), [])

        # Invalid node

        with self.assertRaises(KeyError):
            g.get_successors('@@')

        with self.assertRaises(KeyError):
            g.get_successors(2)

    def testGetAdjacents(self):
        g = Graph({'1': ['2', '3'], '2': ['4', '5'], '3': ['6', '7']})

        # Valid node
        self.assertEqual(g.get_adjacents('2'), ['1','4','5'])

        # Invalid node

        with self.assertRaises(KeyError):
            g.get_successors('@@')

        with self.assertRaises(KeyError):
            g.get_successors(2)

    def testAdjMatrix(self):
        # Considering how finicky the initialization is right now
        g = Graph({'1': ['2', '3'], '2': ['1', '5'], '3': ['6', '7']})

        matrix = g.adj_matrix().to_dict() # Para ficar em formato comparável

        self.assertEqual(
            matrix,
            {
                '1':{'1' : 0, '2' : 1, '3' : 1},
                '2':{'1' : 1, '2' : 0, '3' : 0},
                '3':{'1' : 1, '2' : 0, '3' : 0},
            }
        )

        g = Graph()

        g.add_edges(['1 -> 2,3','3->4', '2 ->4'])

        matrix = g.adj_matrix().to_dict()
        self.assertEqual(
            matrix,
            {
                '1':{'1' : 0, '2' : 1, '3' : 1, '4' : 0},
                '2':{'1' : 1, '2' : 0, '3' : 0, '4' : 1},
                '3':{'1' : 1, '2' : 0, '3' : 0, '4' : 1},
                '4':{'1' : 0, '2' : 1, '3' : 1, '4' : 0},

            }
        )

    def testBFSTraversal(self):

        g = Graph()
        g.add_edges(['1 -> 2, 3, 4', '2 -> 5, 6', '5 -> 7', '3 -> 6, 8', '4 -> 8'])

        # Valid node
        self.assertEqual(g.traverse_bfs('1'), ['6','8','7'])

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
        self.assertEqual(g.dist('1','8'),2)

        # Invalid start/destination/both
        with self.assertRaises(AssertionError):
            g.dist('0','8')

        with self.assertRaises(AssertionError):
            g.dist('@@','8')

        with self.assertRaises(AssertionError):
            g.dist('1','50')

    def testDistTable(self):
        g = Graph()
        g.add_edges(['1 -> 2, 3, 4', '2 -> 5, 6', '5 -> 7', '3 -> 6, 8', '4 -> 8'])

        # Valid nodes
        self.assertEqual(
            g.reach_dist_dfs('1'),
            [('7' , 3) , ('6', 2), ('8', 2)]
        )

        test_nodes = ['@@',2]

        for test_node in test_nodes:

            with self.assertRaises(KeyError):
                g.reach_dist_dfs(test_node)

    def testCycleCheckR(self):
        '''

        IGNORE THIS ONE

        '''
        pass


class TestGrafosPesados(unittest.TestCase):

    def testCreateWeightedGraph(self):
        '''

        IGNORE THIS ONE

        '''
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)




