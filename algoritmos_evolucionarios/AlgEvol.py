"""
Código inspirado nos slides de Algoritmos Evolutivos
"""

from Pop import Populacao

# Classe Algoritmo Evolutivo
class EvolAlgorithm:

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
