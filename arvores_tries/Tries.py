class TrieNode:
    def __init__(self, letra : str = None) -> None:
        """
        Inicializa um nó da Trie.

        Parâmetros:
            letra (str, opcional): A letra representada pelo nó.

        Retorna:
            None
        """
        self.letra = letra
        self.children = {}
        self.fim_palavra = False

    def pprint(self) -> None:
        """
        Imprime a estrutura da Trie a partir deste nó, com formatação para facilitar a visualização.

        Parâmetros:
            None

        Retorna:
            None
        """
        print(" +", end="")
        self._pprint()

    def _pprint(self, ind_str : str = "") -> None:
        """
        Método auxiliar para imprimir a estrutura da Trie com formatação adequada

        Parâmetros:

        Retorna:
            None
        """
        indentacao = False

        if self.fim_palavra:
            print(".")
            indentacao = True

        for ix, letra in enumerate(sorted(self.children.keys())):
            ult_child = ix == len(self.children) - 1

            if indentacao:
                print(ind_str + " +", end="")
            print("-" + letra, end="")

            child_indent = ind_str + ("  " if ult_child else " |")
            self.children[letra]._pprint(child_indent)
            indentacao = True


class Trie:
    def __init__(self) -> None:
        """
        Inicializa uma Trie vazia.

        Parâmetros:
            None

        Retorna:
            None
        """
        self.root = TrieNode()

    def insert(self, palavra : str) -> None:
        """
        Insere uma palavra na Trie.

        Parâmetros:
            palavra (str): A palavra a ser inserida.

        Retorns:
            None
        """
        nodulo = self.root

        for letra in palavra:
            if letra not in nodulo.children:
                nodulo.children[letra] = TrieNode(letra)
            nodulo = nodulo.children[letra]

        nodulo.fim_palavra = True

    def procura(self, palavra : str) -> bool:
        """
        Procura uma palavra na Trie.

        Parâmetros:
            palavra (str): A palavra a ser procurada.

        Retorna:
            bool: True se a palavra estiver na Trie, False caso contrário.
        """
        nodulo = self.root

        for letra in palavra:
            if letra not in nodulo.children:
                return False
            else:
                nodulo = nodulo.children[letra]

        return nodulo.fim_palavra

    def comeca(self, prefixo : str) -> None:
        """
        Verifica se existe alguma palavra na Trie que começa com um determinado prefixo.

        Parâmetros:
            prefixo (str): O prefixo a ser procurado.

        Retorna:
            bool: True se existe alguma palavra na Trie que começa com o prefixo, False caso contrário.
        """
        nodulo = self.root

        for letra in prefixo:
            if letra not in nodulo.children:
                return False
            else:
                nodulo = nodulo.children[letra]
        return True

    def pprint(self) -> None:
        """
        Imprime a estrutura da Trie a partir da raiz, com formatação para facilitar a visualização.

        Parâmetros:
            None

        Retorna:
            None
        """
        self.root.pprint()




