from Ind import Individuos
import random


# Classe população

class Populacao:

    def __init__(self, pop_size: int, indiv_size: int, indivs: list = None):
        """
            Inicializa um novo objeto da classe população.

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

        # Cria a lista de indivíduos
        self.indivs = []

        # Itera sobre o intervalo de 0 a (pop_size - 1)
        for i in range(self.pop_size):
            # Cria um novo objeto da classe Individuos com o tamanho do genoma especificado
            # e adiciona-o à lista de indivíduos
            self.indivs.append(Individuos(self.indiv_size))
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
            fitnesses.append(indiv.get_fitness())
        return fitnesses

    # Retorna o número do melhor indivíduo
    def best_indiv(self):
        """
            Retorna o melhor indivíduo da população.

            Parâmetros:
                None

            Retorno:
                Individuos: O melhor indivíduo da população.
        """
        best_indiv = self.indivs[0]
        for indiv in self.indivs:
            if indiv.get_fitness() > best_indiv.get_fitness():
                best_indiv = indiv

        best_ind = self.indivs.index(best_indiv) + 1

        return best_ind

    # Retorna a aptidão do melhor indivíduo
    def best_fitness(self):
        """
            Retorna a aptidão do melhor indivíduo da população.

            Parâmetros:
                None

            Retorno:
                int: A aptidão do melhor indivíduo da população.
        """
        return self.indivs[self.best_indiv() - 1].get_fitness()

    @staticmethod
    def linscaling(fitnesses):
        """
        Realiza o escalonamento linear das aptidões.

        Parâmetros:
            fitnesses (list): A lista de aptidões dos indivíduos.

        Retorno:
            list: A lista de aptidões escalonadas linearmente.
        """
        maximo = max(fitnesses)
        minimo = min(fitnesses)

        # Evita divisão por zero quando todos os fitnesses são iguais
        if maximo == minimo:
            return [1.0] * len(fitnesses)
        res = []
        for f in fitnesses:
            val = (f - minimo) / (maximo - minimo)
            res.append(val)
        return res

    def roulette(self, n):
        """
        Realiza a seleção de n indivíduos da população utilizando o método de roleta.

        Parâmetros: n (int): O número de indivíduos a serem selecionados. indivs (list): A lista de indivíduos da
        população. Se não for fornecida, utiliza os indivíduos da própria população.

        Retorno:
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

    # Recombinação
    def recombination(self, progenitores, num_desc):

        desc = []
        num = 0

        len(progenitores)

        while num < num_desc:

            for num_progenitores in range(0, len(progenitores) - 1):
                prog1 = self.indivs[progenitores[num_progenitores]]
                prog2 = self.indivs[progenitores[num_progenitores + 1]]

                # Perform a simple crossover operation
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

    def reinsertion(self, offspring):
        """
        Realiza a reinserção dos descendentes na população.

        Parâmetros:
            offspring (list): A lista de novos descendentes.

        Retorno:
            None
        """
        # Índice dos índividuos da população a manter
        tokeep = self.roulette(self.pop_size - len(offspring))

        # Lista da população final
        final_pop = []

        # Adiciona os índividuos da população a manter
        for i in tokeep:
            final_pop.append(self.indivs[i].genome)

        # Adiciona os descendentes
        for i in range(len(offspring)):
            final_pop.append(offspring[i])

        return final_pop

    pass
