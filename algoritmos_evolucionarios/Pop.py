"""
Código inspirado nos slides de Algoritmos Evolutivos
"""
import random
from Ind import Individuos

# Classe população
class Populacao:

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
