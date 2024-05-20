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

    # Inicialização de operador de mutação que altera um único gene
    def mutation(self):
        """
            Altera um gene aleatório do genoma do indivíduo.

            Parâmetros:
                None

            Retorno:
                None
        """

        tamanho = len(self.genome)
        pos_gene = random.randint(0, tamanho - 1)

        if self.genome[pos_gene] != 0:
            self.genome[pos_gene] = 0
        else:
            self.genome[pos_gene] = 1

        pass

    # Crossover em vários pontos
    def crossover(self, indiv2):
        """
            Realiza o crossover entre dois indivíduos.

            Parâmetros:
                indiv2 (Individuos): O segundo indivíduo.

            Retorno:
                Individuos: O novo indivíduo.
        """

        novo_indiv = Individuos(self.size, 0, self.lim_sup, self.lim_inf)

        # Crossover entre genomas
        for i in range(self.size):
            if random.randint(0, 1) == 1:
                novo_indiv.genome.append(self.genome[i])
            else:
                novo_indiv.genome.append(indiv2.genome[i])

        return novo_indiv

    pass