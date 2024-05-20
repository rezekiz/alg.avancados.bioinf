from Ind import Individuos

if __name__ == "__main__":
    # Criar dois indivíduos
    ind1 = Individuos(size=10)
    ind2 = Individuos(size=10)

    print("Genoma do Indivíduo 1:", ind1.genome)
    print("Genoma do Indivíduo 2:", ind2.genome)

    # Mutação do primeiro indivíduo
    ind1.mutation()
    print("Genoma do Indivíduo 1 após mutação:", ind1.genome)

    # Crossover entre os dois indivíduos
    ind1, ind2 = Individuos.crossover(ind1, ind2)
    print("Genoma do Indivíduo 1 após crossover:", ind1.genome)
    print("Genoma do Indivíduo 2 após crossover:", ind2.genome)

    # Crossover entre os dois indivíduos em 3 pontos
    ind1, ind2 = Individuos.crossover_multi(ind1, ind2, 3)
    print("Genoma do Indivíduo 1 após crossover:", ind1.genome)
    print("Genoma do Indivíduo 2 após crossover:", ind2.genome)