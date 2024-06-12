# Add parent dir to path to ensure module is found
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest

from arvore_sufixos.Arvore_De_Sufixos import *

class TestArvoreDeSufixos(unittest.TestCase):
    """
    Testes para a classe ArvoreDeSufixos.
    """

    def test_add_sufixo(self):
        """
        Verifica se os sufixos são adicionados corretamente à árvore.
        """
        arvore = ArvoreDeSufixos()
        arvore.add_sufixo("ACT", 0)
        self.assertIn(1, arvore.nodes[0][1].values())  # Primeiro sufixo
        self.assertIn(2, arvore.nodes[1][1].values())  # Segundo sufixo
        self.assertIn(3, arvore.nodes[2][1].values())  # Terceiro sufixo

    def preparar_arvore_de_teste(self):
        """
        Prepara uma instância da classe ArvoreDeSufixos para ser usada nos testes.
        """
        self.arvore = ArvoreDeSufixos()

    def test_adicionar_sufixo_e_encontrar_padrao(self):
        """
        Verifica se o padrão "ana" é encontrado corretamente na sequência "banana".
        """
        self.preparar_arvore_de_teste()
        self.arvore.build_arvore_de_sufixos("banana")
        resultado = self.arvore.encontrar_padrao("ana")
        self.assertEqual(resultado, [1, 3])

    def test_encontrar_padrao_inexistente(self):
        """
        Verifica se o método retorna None quando o padrão "xyz" não é encontrado na árvore.
        """
        self.preparar_arvore_de_teste()
        self.arvore.build_arvore_de_sufixos("banana")
        resultado = self.arvore.encontrar_padrao("xyz")
        self.assertIsNone(resultado)

    def test_adicionar_sufixo_e_imprimir_arvore(self):
        """
        Verifica se a função de imprimir a árvore não gera erros para a sequência "banana".
        """
        self.preparar_arvore_de_teste()
        self.arvore.build_arvore_de_sufixos("banana")
        # Verifica se a função de imprimir a árvore não gera erros
        try:
            self.arvore.print_arvore()
        except Exception as e:
            self.fail(f"Erro ao imprimir a árvore: {e}")

 
if __name__ == '__main__':
    unittest.main()
