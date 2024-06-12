"""
Código inspirado nos slides de Algoritmos Evolutivos
"""
import random

# Classe de individuos
class Individuos:

    def __init__(self, size: int, lim_sup: int = 1, lim_inf: int = 0, genome: list[int] = None) -> None:
        """
        Inicializa um novo objeto da classe individuos.

        Parâmetros:
            size (int): O tamanho do genoma do indivíduo.
            lim_sup (int): O limite superior do genoma do indivíduo.
            lim_inf (int): O limite inferior do genoma do indivíduo.
            genome (list): O genoma do indivíduo.

        Retorna:
            None
        """
        if genome is None:
            genome = []

        self.size = size
        self.genome = genome
        self.lim_sup = lim_sup
        self.lim_inf = lim_inf
        self.fitness = None

        if not self.genome:
            self.init_aleat_indiv(size)
        pass

    def init_aleat_indiv(self, size: int) -> None:
        """
        Inicializa um novo objeto da classe individuos com valores aleatórios determinados pelo parâmetro size.

        Parâmetros:
            size (int): O tamanho do genoma do indivíduo.

        Retorna:
            None
        """
        for i in range(size):
            self.genome.append(random.randint(self.lim_inf, self.lim_sup))

        pass

    def mutation(self) -> None:
        """
        Altera um gene aleatório do genoma do indivíduo.

        Parâmetros:
            None

        Retorna:
            None
        """
        tamanho = len(self.genome)
        pos_gene = random.randint(0, tamanho - 1)

        if self.genome[pos_gene] != 0:
            self.genome[pos_gene] = 0
        else:
            self.genome[pos_gene] = 1

        pass

    def crossover(self, other: 'Individuos') -> tuple['Individuos', 'Individuos']:
        """
        Realiza crossover entre o indivíduo atual (self) e outro indivíduo (other) para gerar dois novos indivíduos.

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

    def crossover_multi(self, other: 'Individuos', num_points: int) -> tuple['Individuos', 'Individuos']:
        """
        Realiza crossover entre o indivíduo atual (self) e outro indivíduo para gerar dois novos indivíduos.

        Parâmetros:
            other (Individuos): O outro indivíduo.
            num_points (int): O número de pontos de crossover.

        Retorna:
            (Individuos, Individuos): Dois novos indivíduos resultantes do crossover.
        """
        if self.size != other.size:
            raise ValueError("Os indivíduos devem ter tamanhos de genoma iguais para realizar o crossover.")
        if num_points >= self.size - 1:
            raise ValueError("O número de pontos de crossover deve ser menor que o tamanho do genoma - 1.")

        crossover_points = sorted(random.sample(range(1, self.size), num_points))

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

    def get_fitness(self) -> int:
        """
        Retorna a aptidão do indivíduo.

        Parâmetros:
            None

        Retorno:
            int: A aptidão do indivíduo.
        """
        if self.fitness is None:
            self.fitness = sum(self.genome)  # Calcula a fitness se ainda não estiver definida
        return self.fitness

    def get_genes(self) -> list[int]:
        """
        Retorna os genes do indivíduo.

        Parâmetros:
            None

        Retorno:
            list[int]: Lista dos genes do indivíduo.
        """
        genes_list = []

        for i in range(len(self.genome)):
            genes_list.append(self.genome[i])

        return genes_list

    def set_fitness(self, fit: int) -> int:
        """
        Configura a aptidão do indivíduo.

        Parâmetros:
            fit (int): A aptidão do indivíduo.

        Retorno:
            int: A aptidão do indivíduo.
        """
        self.fitness = fit
        return self.fitness

    pass
