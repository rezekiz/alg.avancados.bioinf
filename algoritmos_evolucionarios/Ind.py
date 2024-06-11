# Classe de individuos
import random


class Individuos:

    def __init__(self, size: int, lim_sup: int = 1, lim_inf: int = 0, genome: object = None) -> object:
        """
            Inicializa um novo objeto da classe individuos.

            Parâmetros:
                size (int): O tamanho do genoma do indivíduo.
                fitness (float): A aptidão do indivíduo.
                lim_sup (int): O limite superior do genoma do indivíduo.
                lim_inf (int): O limite inferior do genoma do indivíduo.
                genome (list): O genoma do indivíduo.

            Opcional:
                genome (list): O genoma do indivíduo. Se o genoma for vazio inicializa com valores aleatórios.

        """
        if genome is None:
            genome = []

        self.size = size
        self.genome = genome
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

    # Crossover num único ponto
    def crossover(self, other):
        """
            Realiza crossover entre o indivíduo atual (self) e outro indivíduo para gerar dois novos indivíduos.

            Parâmetros:
                other (Individuos): O outro indivíduo.

            Retorno:
                (Individuos, Individuos): Dois novos indivíduos resultantes do crossover.
        """
        if self.size != other.size:
            raise ValueError("Os indivíduos devem ter tamanhos de genoma iguais para realizar o crossover.")

        crossover_point = random.randint(1, self.size - 1)

        new_genome1 = self.genome[:crossover_point] + other.genome[crossover_point:]
        new_genome2 = other.genome[:crossover_point] + self.genome[crossover_point:]

        return Individuos(size=self.size, genome=new_genome1), Individuos(size=other.size, genome=new_genome2)

        pass

    def crossover_multi(self, other, num_points):
        """
            Realiza crossover entre o indivíduo atual (self) e outro indivíduo para gerar dois novos indivíduos.

            Parâmetros:
                other (Individuos): O outro indivíduo.
                num_points (int): O número de pontos de crossover.

            Retorno:
                (Individuos, Individuos): Dois novos indivíduos resultantes do crossover.
        """
        if self.size != other.size:
            raise ValueError("Os indivíduos devem ter tamanhos de genoma iguais para realizar o crossover.")
        if num_points >= self.size - 1:
            raise ValueError("O número de pontos de crossover deve ser menor que o tamanho do genoma - 1.")

        # Seleciona pontos de crossover aleatórios
        crossover_points = sorted(random.sample(range(1, self.size), num_points))

        # Realiza o crossover nos pontos selecionados
        new_genome1 = []
        new_genome2 = []
        current_parent = self
        for i in range(self.size):
            if i in crossover_points:
                # Troca o pai atual
                current_parent = other if current_parent is self else self
            new_genome1.append(current_parent.genome[i])
            new_genome2.append(other.genome[i])

        return Individuos(size=self.size, genome=new_genome1), Individuos(size=other.size, genome=new_genome2)

        pass

    def get_fitness(self):
        """
            Retorna a aptidão do indivíduo.

            Parâmetros:
                None

            Retorno:
                int: A aptidão do indivíduo.
        """

        return sum(self.genome)
    
    def get_genes(self):
        #for i in range(len(self.genome)):
        #    return self.genome[i]
        return self.genome

    def set_fitness(self, fit):
        self.fitness = fit

    pass
