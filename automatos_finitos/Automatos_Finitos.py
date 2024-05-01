if __name__ == "__main__":

    from Auxiliares import sobreposicao

    class Automato:

        def __init__(self, padrao):
            self.amino = {'A', 'C', 'T', 'G'}
            self.verificar_seq(seq)
            self.verificar_padrao(padrao)
            self.padrao = padrao.upper()
            self.seq = seq.upper()
            self.num_estados = len(padrao) + 1
            self.tabela_transicao = {}
            self.construir_tabela_transicao(padrao)

        def verificar_seq(self, seq):
            """
            Verifica se a sequência contém apenas aminoácidos válidos

            Parâmetros:
                seq (str): A sequência a ser verificada

            Retorna:
                None
            """

            if not all(s in self.amino for s in seq):
                raise ValueError("A sequência contém caracteres inválidos.")

        def verificar_padrao(self, padrao):
            """
            Verifica se o padrão contém apenas aminoácidos válidos.

            Parâmetros:
                padrao (str): O padrão a ser verificado.

            Retorna:
                None
            """

            if not all(s in self.amino for s in padrao):
                raise ValueError("O padrão contém caracteres inválidos.")

        def construir_tabela_transicao(self, padrao):

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

        def proximo_estado(self, atual, simbolo):

            """
            Retorna o próximo estado com base no estado atual e no símbolo.

            Parâmetros:
                atual (int): O estado atual.
                simbolo (str): O símbolo de entrada.

            Retorna:
                int: O próximo estado.
            """

            return self.tabela_transicao.get((atual, simbolo.upper()), -1)

        def aplicar_sequencia(self, seq):

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

        def encontrar_ocorrencias(self, seq):

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

padrao = "ATG"
seq = "ATGCGCATGATG"

automato = Automato(padrao)
indices = automato.encontrar_ocorrencias(seq)

print("O Padrão aparece nos índices:", indices)
