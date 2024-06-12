import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import unittest

from automatos_finitos.Automatos_Finitos import *
from automatos_finitos.Automatos_Finitos import *

class TestAutomaton(unittest.TestCase):
    """
    Classe de testes para validar o funcionamento da classe Automato.
    """

    def test_verificar_seq(self):
        """
        Verifica se o método lança uma exceção ValueError quando a sequência contém caracteres inválidos.
        """
        automato = Automato("ATG", "ATGCGCATGATG")
        self.assertIsNone(automato.verificar_seq("ATGCGCATGATG"))

        with self.assertRaises(ValueError):
            automato.verificar_seq("ATGXCATGATG")  # Sequência inválida

    def test_verificar_padrao(self):
        """
        Verifica se o método lança uma exceção ValueError quando o padrão contém caracteres inválidos.
        """
        automato = Automato("ATG", "ATGCGCATGATG")
        self.assertIsNone(automato.verificar_padrao("ATG"))

        with self.assertRaises(ValueError):
            automato.verificar_padrao("AXG")  # Padrão inválido

    def test_construir_tabela_transicao(self):
        """
        Verifica se a tabela de transição foi construída corretamente para o padrão "ATG".
        """
        automato = Automato("ATG", "ATGCGCATGATG")
        automato.construir_tabela_transicao("ATG")
        # Verificar se a tabela de transição foi construída corretamente
        self.assertEqual(automato.tabela_transicao[(0, 'A')], 1)
        self.assertEqual(automato.tabela_transicao[(1, 'T')], 2)
        self.assertEqual(automato.tabela_transicao[(2, 'G')], 3)
        self.assertEqual(automato.tabela_transicao[(3, 'C')], 0)

    def test_encontrar_ocorrencias(self):
        """
        Verifica se o método encontra corretamente as ocorrências do padrão na sequência fornecida.
        """
        automato = Automato("ATG", "ATGCGCATGATG")
        ocorrencias = automato.encontrar_ocorrencias("ATGCGCATGATG")
        self.assertEqual(ocorrencias, [0, 6, 9])  # Corrigido
        ocorrencias_vazio = automato.encontrar_ocorrencias("")
        self.assertEqual(ocorrencias_vazio, [])


if __name__ == "__main__":
    unittest.main()
