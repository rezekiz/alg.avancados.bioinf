
# Classe população

class Populacao:

    def __init__(self, pop_size: int, indiv_size: int, indivs: list = None):
        """
            Inicializa um novo objeto da classe populacao.

            Parâmetros:
                pop_size (int): O número de indivíduos na população.
                indiv_size (int): O tamanho do genoma de cada indivíduo.
                indivs (list): A lista de indivíduos. Se a lista for vazia inicializa com valores aleatórios.

        """

        self.pop_size = pop_size
        self.indiv_size = indiv_size

        # Caso indivs seja vazio inicializa com valores aleatórios
        if indivs:
            self.indivs = indivs
        else:
            self.init_aleat_pop()
        pass

    # Inicialização aleatória da população
    def init_aleat_pop(self):
        """
            Inicializa um novo objeto da classe populacao com valores aleatórios.

            Parâmetros:
                None

            Retorno:
                None
        """

        self.indivs = []

        for i in range(self.pop_size):
            self.indivs.append(Individuos(self.indiv_size, [], 1, 0))

        pass

    # Retorna o indivíduo da população com o parâmetro index
    def get_indiv(self, index: int):
        """
            Retorna o indivíduo da população com o parâmetro index.

            Parâmetros:
                index (int): O indice do indivíduo da população.

            Retorno:
                Individuos: O indivíduo da população.
        """
        return self.indivs[index]

    # Retorna lista de aptidões de todos os indivíduos da população
    def get_fitnesses(self):
        """
            Retorna a lista de aptidões de todos os indivíduos da população.

            Parâmetros:
                None

            Retorno:
                list: A lista de aptidões de todos os indivíduos da população.
        """
        fitnesses = []
        for indiv in self.indivs:
            fitnesses.append(indiv.fitness)
        return fitnesses

    # Seleciona o melhor score de entre os indivíduos da população
    def get_best_indiv(self):
        """
            Retorna o melhor indivíduo da população.

            Parâmetros:
                None

            Retorno:
                Individuos: O melhor indivíduo da população.
        """

        return max(self.indivs, key=lambda x: x.fitness)

    pass
