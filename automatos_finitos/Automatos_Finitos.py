"""
Código base retirado dos powerpoints das aulas (da autoria de Rui Mendes) com pequenas alterações.
Utilização do stack overflow e de LLMs (GPT 3.5 e Gemini 1.5) para algumas correções
"""
import sys
import os

from .Auxiliares import sobreposicao

class Automato:
    """
    Representa um autômato que procura um padrão específico em uma sequência de aminoácidos.

    Atributos:
        amino (set): Conjunto de aminoácidos válidos ('A', 'C', 'T', 'G').
        padrao (str): O padrão a ser procurado na sequência, convertido para maiúsculas.
        seq (str): A sequência de aminoácidos na qual o padrão será procurado, convertida para maiúsculas.
        num_estados (int): O número de estados do autômato, que é igual ao comprimento do padrão mais um.
        tabela_transicao (dict): Tabela de transição do autômato, representada como um dicionário que mapeia (estado, símbolo) para o próximo estado.
    """

    def __init__(self, padrao: str, seq) -> None:
        """
        Inicializa o autômato com o padrão especificado.

        Parâmetros:
            padrao (str): O padrão a ser procurado na sequência.

        Retorna:
            None
        """
        self.amino = {'A', 'C', 'T', 'G'}
        self.verificar_seq(seq)
        self.verificar_padrao(padrao)
        self.padrao = padrao.upper()
        self.seq = seq.upper()
        self.num_estados = len(padrao) + 1
        self.tabela_transicao = {}
        self.construir_tabela_transicao(padrao)

    def verificar_seq(self, seq: str) -> None:
        """
        Verifica se a sequência contém apenas aminoácidos válidos

        Parâmetros:
            seq (str): A sequência a ser verificada

        Retorna:
            None

        Raises:
            ValueError: Se a sequência contiver caracteres inválidos.
        """

        if not all(s in self.amino for s in seq):
            raise ValueError("A sequência contém caracteres inválidos.")

    def verificar_padrao(self, padrao: str) -> None:
        """
        Verifica se o padrão contém apenas aminoácidos válidos.

        Parâmetros:
            padrao (str): O padrão a ser verificado.

        Retorna:
            None

        Raises:
            ValueError: Se o padrão contiver caracteres inválidos.
        """

        if not all(s in self.amino for s in padrao):
            raise ValueError("O padrão contém caracteres inválidos.")

    def construir_tabela_transicao(self, padrao: str) -> None:

        """
        Constrói a tabela de transição com base no padrão de entrada.

        Parâmetros:
            padrao (str): O padrão usado para construir a tabela de transição.

        Retorna:
            None
        """

        k = 0
        for q in range(self.num_estados):
            for a in self.amino:
                if q < len(self.padrao) and a == self.padrao[q]:
                    k = q + 1
                else:
                    k = sobreposicao(self.padrao[:q] + a, self.padrao)
                self.tabela_transicao[(q, a)] = k

    def proximo_estado(self, atual: int, simbolo: str) -> int:

        """
        Retorna o próximo estado com base no estado atual e no símbolo.

        Parâmetros:
            atual (int): O estado atual.
            simbolo (str): O símbolo de entrada.

        Retorna:
            int: O próximo estado.
        """

        return self.tabela_transicao.get((atual, simbolo.upper()), -1)

    def aplicar_sequencia(self, seq: str) -> list:

        """
        Aplica uma sequência ao autômato e retorna os estados resultantes.

        Parâmetros:
            seq (str): A sequência.

        Retorna:
            list: Os estados resultantes.
        """

        q = 0
        res = [q]
        for a in self.seq:
            q = self.proximo_estado(q, a)
            res.append(q)
        return res

    def encontrar_ocorrencias(self, seq: str) -> list:

        """
        Encontra todas as ocorrências do padrão na sequência.

        Parâmetros:
            seq (str): A sequência na qual o padrão será procurado.

        Retorna:
            list: Uma lista de índices que representam as posições em que o padrão começa na sequência.
        """

        q = 0
        res = []
        for i, a in enumerate(seq):
            q = self.proximo_estado(q, a)
            if q == self.num_estados - 1:
                res.append(i - len(self.padrao) + 1)
        return res



if __name__ == "__main__":
    padrao = "ATG"
    seq = "ATGCGCATGATG"

    automato = Automato(padrao, seq)
    indices = automato.encontrar_ocorrencias(seq)

    print("O Padrão aparece nos índices:", indices)
