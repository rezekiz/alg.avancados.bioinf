class EvolAlgorithm:

    def __init__(self, pop_size, numits, desc, indiv_size):
        self.pop_size = pop_size
        self.numits = numits
        self.desc = desc
        self.indiv_size = indiv_size

    def initPop(self, indiv_size):
        self.pop = Populacao(self.pop_size, indiv_size)

    def iteracao(self):
        progenitores = self.pop.selection(self.desc)
        desc = self.pop.recombination(progenitores, self.desc)
        #Falta evaluate
        self.pop.reinsercao(desc)

    def run(self):
        self.initPop(self.indiv_size)
        #self.evaluate(self.popul.indivs)
        self.bestsol = self.pop.best_indiv()
        for i in range(self.num + 1):
            self.iteracao()
        bs = self.pop.best_indiv()
        if bs > self.bestsol:
            self.bestsol = bs
        print("Iteration:", i, " ", "Best: ", self.bestsol)




