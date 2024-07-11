"""
Código inspirado nos slides de Algoritmos Evolutivos
"""
import random

# Classe de individuos
class Individuos:
    """
    Classe que representa um indivíduo em um algoritmo evolutivo.

    Atributos:
        size (int): O tamanho do genoma do indivíduo.
        genome (list[int]): O genoma do indivíduo.
        lim_sup (int): O limite superior dos valores dos genes.
        lim_inf (int): O limite inferior dos valores dos genes.
        fitness (int): A aptidão do indivíduo.
    """

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

# Classe população
class Populacao:
    """
    Classe que representa uma população em um algoritmo evolutivo.

    Atributos:
        pop_size (int): O número de indivíduos na população.
        indiv_size (int): O tamanho do genoma de cada indivíduo.
        indivs (list): A lista de indivíduos na população.
    """

    def __init__(self, pop_size: int, indiv_size: int, indivs: list[Individuos] = None) -> None:
        """
        Inicializa um novo objeto da classe população.

        Parâmetros:
            pop_size (int): O número de indivíduos na população.
            indiv_size (int): O tamanho do genoma de cada indivíduo.
            indivs (list): A lista de indivíduos. Se a lista for vazia inicializa com valores aleatórios.

        Retorna:
            None
        """
        self.pop_size = pop_size
        self.indiv_size = indiv_size

        if indivs:
            self.indivs = indivs
        else:
            self.init_aleat_pop()
        pass

    def init_aleat_pop(self) -> None:
        """
        Inicializa um novo objeto da classe populacao com valores aleatórios.

        Parâmetros:
            None

        Retorna:
            None
        """
        self.indivs = []

        for i in range(self.pop_size):
            self.indivs.append(Individuos(self.indiv_size))
        pass

    def get_indiv(self, index: int) -> Individuos:
        """
        Retorna o indivíduo da população na posição especificada pelo parâmetro index.

        Parâmetros:
            index (int): O índice do indivíduo da população desejado.

        Retorna:
            Individuos: O indivíduo na posição especificada.
        """
        return self.indivs[index]

    def get_fitnesses(self) -> list[float]:
        """
        Retorna a lista de aptidões de todos os indivíduos da população.

        Parâmetros:
            None

        Retorna:
            list: A lista de aptidões de todos os indivíduos da população.
        """
        fitnesses = []

        for indiv in self.indivs:
            fitnesses.append(indiv.get_fitness())
        return fitnesses

    def best_indiv(self) -> int:
        """
        Retorna o índice do melhor indivíduo na população.

        Parâmetros:
            None

        Retorna:
            int: O índice do melhor indivíduo.
        """
        best_indiv = self.indivs[0]
        for indiv in self.indivs:
            if indiv.get_fitness() > best_indiv.get_fitness():
                best_indiv = indiv

        best_ind = self.indivs.index(best_indiv) + 1

        return best_ind

    def best_fitness(self) -> float:
        """
        Retorna a aptidão do melhor indivíduo da população.

        Parâmetros:
            None

        Retorna:
            int: A aptidão do melhor indivíduo da população.
        """
        return self.indivs[self.best_indiv() - 1].get_fitness()

    @staticmethod
    def linscaling(fitnesses: list[float]) -> list[float]:
        """
        Realiza o escalonamento linear das aptidões.

        Parâmetros:
            fitnesses (list): A lista de aptidões dos indivíduos.

        Retorna:
            list: A lista de aptidões escalonadas linearmente.
        """
        maximo = max(fitnesses)
        minimo = min(fitnesses)

        if maximo == minimo:
            return [1.0] * len(fitnesses)
        res = []
        for f in fitnesses:
            val = (f - minimo) / (maximo - minimo)
            res.append(val)
        return res

    def roulette(self, n: int) -> list[int]:
        """
        Realiza a seleção de n indivíduos da população utilizando o método de roleta.

        Parâmetros:
            n (int): O número de indivíduos a serem selecionados.

        Retorna:
            list: Uma lista contendo os índices dos indivíduos selecionados.
        """
        res = []
        fitnesses = self.linscaling(self.get_fitnesses())
        tot_fitness = sum(fitnesses)

        for _ in range(n):
            val = random.random() * tot_fitness
            acum = 0.0
            ind = 0

            while acum < val:
                acum += fitnesses[ind]
                ind += 1

            res.append(ind - 1)
            tot_fitness -= fitnesses[ind - 1]
            fitnesses.pop(ind - 1)

        return res

    def recombination(self, progenitores: list[int], num_desc: int) -> list[list[int]]:
        """
        Realiza a recombinação dos indivíduos selecionados.

        Parâmetros:
            progenitores (list): Lista de índices dos indivíduos selecionados como progenitores.
            num_desc (int): Número de descendentes a serem gerados.

        Retorna:
            list: Lista contendo os descendentes gerados.
        """

        desc = []
        num = 0

        len(progenitores)

        while num < num_desc:

            for num_progenitores in range(0, len(progenitores) - 1):
                prog1 = self.indivs[progenitores[num_progenitores]]
                prog2 = self.indivs[progenitores[num_progenitores + 1]]

                desc1, desc2 = prog1.crossover(prog2)

                desc1.mutation()
                desc2.mutation()

                desc.append(desc1)
                desc.append(desc2)

                num += 2

        gene_desc = []

        for indiv in desc:
            ind = indiv.genome
            gene_desc.append(ind)

        if num_desc % 2 == 0:
            return gene_desc
        else:
            return gene_desc[:-1]

    def reinsertion(self, offspring: list[list[int]]) -> list[list[int]]:
        """
        Realiza a reinserção dos descendentes na população.

        Parâmetros:
            offspring (list): A lista de novos descendentes.

        Retorna:
            list: Lista da população final após a reinserção dos descendentes.
        """
        tokeep = self.roulette(self.pop_size - len(offspring))
        final_pop = []

        for i in tokeep:
            final_pop.append(self.indivs[i].genome)

        for i in range(len(offspring)):
            final_pop.append(offspring[i])

        return final_pop

    pass

# Classe Algoritmo Evolutivo
class EvolAlgorithm:
    """
    Classe que implementa um algoritmo evolutivo simples.

    Atributos:
        pop_size (int): O tamanho da população.
        numits (int): O número de iterações do algoritmo.
        desc (int): O número de descendentes a serem gerados em cada iteração.
        indiv_size (int): O tamanho do genoma de cada indivíduo na população.
        pop (Populacao): A população atual do algoritmo.
        best_sol (int): A melhor solução encontrada pelo algoritmo.
    """

    def __init__(self, pop_size: int, numits : int, desc: int, indiv_size: int) -> None:
        """
        Inicializa um novo objeto da classe EvolAlgorithm.

        Parâmetros:
            pop_size (int): O tamanho da população.
            numits (int): O número de iterações.
            desc (int): O número de descendentes a serem gerados em cada iteração.
            indiv_size (int): O tamanho do genoma de cada indivíduo.

        Retorna:
            None

        """
        self.best_sol = None
        self.pop_size = pop_size
        self.numits = numits
        self.desc = desc
        self.indiv_size = indiv_size
        self.pop = None

    def init_pop(self, indiv_size : int) -> Populacao:
        """
        Inicializa uma nova população.

        Parâmetros:
            indiv_size (int): O tamanho do genoma de cada indivíduo.

        Retorna:
            Populacao: A população inicializada.
        """
        self.pop = Populacao(self.pop_size, indiv_size)
        return self.pop

    def evaluate(self, indivs : list[list[int]]) -> list[int]:
        """
        Avalia a aptidão de uma lista de indivíduos.

        Parâmetros:
            indivs (List[List[int]]): Uma lista de indivíduos representados por seus genomas.

        Retorna:
            List[int]: Uma lista contendo as aptidões correspondentes a cada indivíduo.
        """
        fit_ind = []
        for i in range(len(indivs)):
            indiv = indivs[i]
            fit = 0
            for x in indiv:
                if x == 1:
                    fit += 1
            fit_ind.append(fit)
        return fit_ind

    def iteration(self) -> None:
        """
        Executa uma iteração do algoritmo evolutivo.

        Realiza seleção dos pais, recombinação, avaliação dos descendentes e reinserção na população.

        Parâmetros:
            None

        Retorna:
            None
        """
        parents = self.pop.roulette(self.desc)
        descendentes = self.pop.recombination(parents, self.desc)
        self.evaluate(descendentes)
        self.pop.reinsertion(descendentes)

    def run(self) -> None:
        """
        Executa o algoritmo evolutivo.

        Realiza a inicialização da população, avaliação dos descendentes e reinserção na população.

        Parâmetros:
            None

        Retorna:
            None
        """
        self.init_pop(self.indiv_size)
        indivs = []

        for indiv in self.pop.indivs:
            indivs.append(indiv.get_genes())

        self.evaluate(indivs)

        self.best_sol = self.pop.best_indiv()

        for i in range(self.numits + 1):
            self.iteration()
            best_s = self.pop.best_indiv()
            if best_s > self.best_sol:
                self.best_sol = best_s

            print(f"Iteration {i}: Best solution = {self.best_sol}")
