import random


# Classe de individuos
class Individuos:

    def __init__(self, size: int, fitness=None, lim_sup: int = 1, lim_inf: int = 0, genome=None):
        """
            Inicializa um novo objeto da classe individuos.

            Parâmetros:
                size (int): O tamanho do genoma do indivíduo.
                fitness (float): A aptidão do indivíduo.
                lim_sup (int): O limite superior do genoma do indivíduo.
                lim_inf (int): O limite inferior do genoma do indivíduo.

            Opcional:
                genome (list): O genoma do indivíduo. Se o genoma for vazio inicializa com valores aleatórios.

        """
        if genome is None:
            genome = []

        self.size = size
        self.genome = genome
        self.fitness = fitness
        self.lim_sup = lim_sup
        self.lim_inf = lim_inf

        # Se objeto genome for vazio inicializa com valores aleatórios
        if not self.genome:
            self.init_aleat_indiv(size)

        pass

    # Inicialização aleatória de um indivíduo
    def init_aleat_indiv(self, size: int):
        """
            Inicializa um novo objeto da classe individuos com valores aleatórios determinados
            pelo parâmetro size.

            Parâmetros:
                size (int): O tamanho do genoma do indivíduo.
        """

        for i in range(size):
            self.genome.append(random.randint(self.lim_inf, self.lim_sup))

    pass


# Classe população

class Populacao:

    def __init__(self, pop_size: int, indiv_size: int, indivs: int):
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

        self.indivs = []

        for i in range(self.pop_size):
            self.indivs.append(Individuos(self.indiv_size))

    pass
