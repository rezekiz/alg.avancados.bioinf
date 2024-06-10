import unittest


class TestArvoreDeSufixos(unittest.TestCase):

    def test_add_sufixo(self):
        arvore = ArvoreDeSufixos()
        arvore.add_sufixo("ACT", 0)
        self.assertIn(1, arvore.nodes[0][1].values())  # Primeiro sufixo
        self.assertIn(2, arvore.nodes[1][1].values())  # Segundo sufixo
        self.assertIn(3, arvore.nodes[2][1].values())  # Terceiro sufixo

    def test_build_arvore_de_sufixos(self):
        arvore = ArvoreDeSufixos()
        arvore.build_arvore_de_sufixos("ACT")
        self.assertIn('A', arvore.nodes[0][1])
        self.assertIn('C', arvore.nodes[0][1])
        self.assertIn('T', arvore.nodes[0][1])
        self.assertIn('A', arvore.nodes[3][1])  # Nodo de 'ACT'

    def test_encontrar_padrao(self):
        arvore = ArvoreDeSufixos()
        arvore.build_arvore_de_sufixos("TACTA")
        self.assertEqual(arvore.encontrar_padrao("TA"), [0, 3])
        self.assertEqual(arvore.encontrar_padrao("ACG"), None)
        self.assertEqual(arvore.encontrar_padrao("T"), [0, 2, 4])

    def test_obter_folhas_abaixo(self):
        arvore = ArvoreDeSufixos()
        arvore.build_arvore_de_sufixos("TACTA")
        self.assertEqual(arvore.obter_folhas_abaixo(0), [5, 0, 3, 1, 4, 2])


if __name__ == '__main__':
    unittest.main()
