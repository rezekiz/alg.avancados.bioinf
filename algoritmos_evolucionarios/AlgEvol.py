from .Pop import Populacao

class EvolAlgorithm:

    def __init__(self, pop_size: int, numits, desc: int, indiv_size: int):
        self.best_sol = None
        self.pop_size = pop_size
        self.numits = numits
        self.desc = desc
        self.indiv_size = indiv_size
        self.pop = None

    def init_pop(self, indiv_size):
        self.pop = Populacao(self.pop_size, indiv_size)
        return self.pop

    def evaluate(self, indivs):
        fit_ind = []
        for i in range(len(indivs)):
            indiv = indivs[i]
            fit = 0
            for x in indiv:
                if x == 1:
                    fit += 1
            fit_ind.append(fit)
        return fit_ind

    def iteration(self):
        parents = self.pop.roulette(self.desc)
        descendentes = self.pop.recombination(parents, self.desc)

        # Tem de receber objetos do tipo Individuos e não recebe
        self.evaluate(descendentes)
        self.pop.reinsertion(descendentes)

    def run(self):
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
