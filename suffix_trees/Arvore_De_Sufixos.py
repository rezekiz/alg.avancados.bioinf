"""
Código base retirado dos powerpoints das aulas (da autoria de Rui Mendes) com pequenas alterações.
Utilização do stack overflow e de LLMs (GPT 3.5 e Gemini 1.5) para algumas correções
"""

class ArvoreDeSufixos:
    """
    Classe para representar uma árvore de sufixos.

    Atributos:
        nodes (dict): Um dicionário que mapeia cada nodo da árvore para seus filhos.
        num (int): O número total de nodos na árvore.
    """
    def __init__(self) -> None:
        """
        Inicializa uma árvore de sufixos.

        Parâmetros:
            None

        Retorna:
            None
        """
        self.nodes = {0: (-1, {})}  # Node raiz
        self.num = 0

    def print_arvore(self) -> None:

        """
        Imprime a árvore de sufixos.

        Parâmetros:
            None

        Retorna:
            None
        """

        for k, v in self.nodes.items():
            if v[0] < 0:
                print(f"{k} -> {v[1]}")
            else:
                print(f"{k} : {v[0]}")

    def add_node(self, origem : int, simbolo : str, num_folha: int = -1) -> None:

        """
        Adiciona um nodo à árvore de sufixos.

        Parâmetros:
            origem (int): O nódulo de origem.
            simbolo (str): O símbolo da transição.
            num_folha (int): O número da folha associada ao nódulo, se houver. Padrão é -1.

        Retorna:
            None
        """

        self.num += 1
        self.nodes[origem][1][simbolo] = self.num
        self.nodes[self.num] = (num_folha, {})

    def add_sufixo(self, p : str, num_sufixo : int) -> None:

        """
        Adiciona um sufixo à árvore

        Parâmetros:
            p (str): Sufixo a ser adicionado.
            num_sufixo (int): Número do sufixo.

        Retorna:
            None

        """

        pos = 0
        node = 0
        while pos < len(p):
            if p[pos] not in self.nodes[node][1]:
                self.add_node(node, p[pos], num_sufixo if pos == len(p) - 1 else -1)
            node = self.nodes[node][1][p[pos]]
            pos += 1


    def build_arvore_de_sufixos(self, seq : str) -> None:

        """
        Constrói a árvore de sufixos a partir de uma sequência

        Parâmetros:
            seq (str): Sequência de aminoácidos

        Retorna:
            None
        """

        t = seq + "$"
        for i in range(len(t)):
            self.add_sufixo(t[i:], i)

    def encontrar_padrao(self, padrao : str) -> list:
        """
        Encontra o padrão na árvore de sufixos.

        Parâmetros:
            padrao (str): Padrão a ser procurado

        Retorna:
            list: Lista de índices onde o padrão aparece na sequência
        """

        pos = 0
        node = 0
        while pos < len(padrao):
            if padrao[pos] in self.nodes[node][1]:
                node = self.nodes[node][1][padrao[pos]]
                pos += 1
            else:
                return None
        return self.obter_folhas_abaixo(node)

    def obter_folhas_abaixo(self, node : int) -> list:

        """
        Obtém as folhas abaixo de um nodo.

        Parâmetros:
            nodo (int): Nodo de início

        Retorna:
            list: Lista de folhas abaixo do node
        """
        res = []
        if self.nodes[node][0] >= 0:
            res.append(self.nodes[node][0])
        else:
            for k in self.nodes[node][1]:
                novo_node = self.nodes[node][1][k]
                folhas = self.obter_folhas_abaixo(novo_node)
                res.extend(folhas)
        return res


