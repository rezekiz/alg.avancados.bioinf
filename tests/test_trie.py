import os
# Add parent dir to path to ensure module is found
import sys
import unittest

# Adicionar o diretório superior ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar as classes necessárias
from arvores_tries import TrieNode, Trie

class TestTrie(unittest.TestCase):

    def initialize_trie(self):
        """
        Inicializa a Trie e insere palavras antes de cada teste.
        """
        self.trie = Trie()
        self.words = ["casa", "casaco", "casinha", "carro", "camisa", "computador"]
        for word in self.words:
            self.trie.insert(word)

    def test_insert_and_search(self):
        """
        Testa a inserção e procura de palavras na Trie.
        """
        self.initialize_trie()
        for word in self.words:
            self.assertTrue(self.trie.procura(word), f"A palavra '{word}' deveria estar na Trie.")
        self.assertFalse(self.trie.procura("camisola"), "A palavra 'camisola' não deveria estar na Trie.")
        self.assertFalse(self.trie.procura("car"), "A palavra 'car' não deveria estar na Trie.")
        self.assertFalse(self.trie.procura("c"), "A palavra 'c' não deveria estar na Trie.")

    def test_prefix(self):
        """
        Testa a verificação de prefixos na Trie.
        """
        self.initialize_trie()
        self.assertTrue(self.trie.comeca("ca"), "Deveria existir uma palavra que começa com 'ca'.")
        self.assertTrue(self.trie.comeca("cas"), "Deveria existir uma palavra que começa com 'cas'.")
        self.assertTrue(self.trie.comeca("co"), "Deveria existir uma palavra que começa com 'co'.")
        self.assertFalse(self.trie.comeca("cai"), "Não deveria existir uma palavra que começa com 'cai'.")
        self.assertTrue(self.trie.comeca("cam"), "Deveria existir uma palavra que começa com 'cam'.")

    def test_empty_trie(self):
        """
        Testa a procura e verificação de prefixos numa Trie vazia.
        """
        empty_trie = Trie()
        self.assertFalse(empty_trie.procura("qualquer"), "A Trie vazia não deveria conter palavras.")
        self.assertFalse(empty_trie.comeca("q"), "A Trie vazia não deveria conter prefixos.")

    def test_partial_word(self):
        """
        Testa se substrings de palavras não são reconhecidas como palavras completas.
        """
        self.initialize_trie()
        self.assertFalse(self.trie.procura("cas"), "A substring 'cas' não deveria ser reconhecida como uma palavra "
                                                   "completa.")

    def test_insert_duplicate_words(self):
        """
        Testa a inserção de palavras duplicadas na Trie.
        """
        self.initialize_trie()
        self.trie.insert("casa")
        self.trie.insert("casa")
        self.assertTrue(self.trie.procura("casa"),
                        "A palavra 'casa' deveria estar na Trie mesmo após inserções duplicadas.")

    def test_non_existent_prefix(self):
        """
        Testa a verificação de prefixos não existentes na Trie.
        """
        self.initialize_trie()
        self.assertFalse(self.trie.comeca("xyz"), "Não deveria existir uma palavra que começa com 'xyz'.")

    def test_word_with_common_prefix(self):
        """
        Testa a inserção e procura de palavras com prefixos comuns.
        """
        self.initialize_trie()
        self.trie.insert("caminho")
        self.assertTrue(self.trie.procura("caminho"), "A palavra 'caminho' deveria estar na Trie.")
        self.assertTrue(self.trie.comeca("camin"), "Deveria existir uma palavra que começa com 'camin'.")
        self.assertFalse(self.trie.procura("camin"),
                         "A substring 'camin' não deveria ser reconhecida como uma palavra completa.")


if __name__ == "__main__":
    unittest.main()
