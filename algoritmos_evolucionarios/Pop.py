from algoritmos_evolucionarios import Individuos


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
        return best_indiv

    # Retorna o melhor indivíduo da população
    def best_fitness(self):
        return self.best_indiv().get_fitness()

    def selection(self, num_indivs, indivs=None):

        if not indivs:
            indivs = self.indivs

        list_selection = []

        # Lista de fitenesses de cada indivíduo da população
        fitnesses = list(self.get_fitnesses(indivs))

        for i in range(num_indivs):
            selection = self.roullete(fitnesses)

            fitnesses[selection] = 0.0

            list_selection.append(selection)

            return list_selection

    # Roleta seletora
    def roullete(self, fitnesses):
        """

        Parâmetros:
            fitnesses (list): A lista de aptidões dos indivíduos.

        """

        # Calcula o total de aptidoes
        total_fitness = sum(fitnesses)

        # Seleciona um valor aleatório
        random_value = random.uniform(0, total_fitness)

        running_sum = 0.0

        # Itera sobre o total de aptidoes e seleciona o indivíduo correspondente ao valor aleatório
        for i in range(len(fitnesses)):
            running_sum += fitnesses[i]
            if running_sum >= random_value:
                return i

        pass

    # Recombinação
    def recombination(self, progenitores, num_desc):

        desc = []
        num = 0

        while num < num_desc:

            prog1 = self.indivs[progenitores[num]]
            prog2 = self.indivs[progenitores[num + 1]]

            # Perform a simple crossover operation
            desc_1 = prog1.genome[:self.indiv_size // 2] + prog2.genome[self.indiv_size // 2:]
            desc_2 = prog2.genome[:self.indiv_size // 2] + prog1.genome[self.indiv_size // 2:]

            # Apply mutation to the desc
            desc_1 = desc_1.mutation(desc_1)
            desc_2 = desc_1.mutation(desc_2)

            desc.append(desc_1)
            desc.append(desc_2)
            num += 2

        return desc

    def reinsercao(self, desc):

        sobreviventes = self.selection(self.pop_size - len(desc))
        self.indivs = [ind if i in sobreviventes else d for i, (ind, d) in enumerate(zip(self.indivs, desc))]

        pass

    pass
