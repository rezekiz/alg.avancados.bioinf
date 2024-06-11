from Pop import Populacao
from Ind import Individuos


class EvolAlgorithm:

    def __init__(self, pop_size, numits, desc, indiv_size):
        self.pop_size = pop_size
        self.numits = numits
        self.desc = desc
        self.indiv_size = indiv_size
        pass

    def init_pop(self, indiv_size):
        self.pop = Populacao(self.pop_size, indiv_size)
        pass

    def evaluate(self, indivs):
        for i in range(len(indivs)):
            indiv = indivs[i]
            fit = 0
            for x in indiv.genome:
                if x == 1:
                    fit += 1
            indiv.set_fitness(fit)
        pass

    def iteration(self):
        parents = self.pop.roulette(self.desc)
        descendentes = self.pop.recombination(parents, self.desc)
        self.evaluate(descendentes)
        self.pop.reinsertion(descendentes)

    def run(self):
        self.init_pop(self.indiv_size)
        self.evaluate(self.pop.indivs)
        self.best_sol = self.pop.best_indiv()

        for i in range(self.numits + 1):
            self.iteration()
            best_s = self.pop.best_indiv()
            if best_s > self.best_sol:
                self.best_sol = best_s

            print(f"Iteration {i}: Best solution = {self.best_sol}")

