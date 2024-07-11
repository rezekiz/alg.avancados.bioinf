from alg_evol import Individuos, Populacao, EvolAlgorithm

if __name__ == "__main__":

    ## Ver classe Individuos

    # Criar dois indivíduos
    ind1 = Individuos(size=10)
    ind2 = Individuos(size=10)

    # Genoma dos dois indivíduos
    print("Genoma do Indivíduo 1:", ind1.genome)
    print("Genoma do Indivíduo 2:", ind2.genome)

    # Mutação do primeiro indivíduo
    ind1.mutation()
    print("Genoma do Indivíduo 1 após mutação:", ind1.genome)

    # Crossover entre os dois indivíduos
    ind1, ind2 = Individuos.crossover(ind1, ind2)
    print("Genoma do Indivíduo 1 após crossover entre eles:", ind1.genome)
    print("Genoma do Indivíduo 2 após crossover entre eles:", ind2.genome)

    # Crossover entre os dois indivíduos em 3 pontos
    ind1, ind2 = Individuos.crossover_multi(ind1, ind2, 3)
    print("Genoma do Indivíduo 1 após crossover em 3 pontos:", ind1.genome)
    print("Genoma do Indivíduo 2 após crossover em 3 pontos:", ind2.genome)

    # Avaliação dos dois indivíduos
    print("Aptidão do Indivíduo 1:", ind1.get_fitness())
    print("Aptidão do Indivíduo 2:", ind2.get_fitness())

    # Obter genoma dos indivíduos por função
    print("Genoma do Indivíduo 1:", ind1.get_genes())
    print("Genoma do Indivíduo 2:", ind2.get_genes())

    # Designar fitness de indivíduos
    print("Aptidão do Indivíduo 1:", ind1.set_fitness(10))
    print("Verificar alteração da aptidão do Indivíduo 1:", ind1.get_fitness())

    ## Ver classe Populacao

    # Criar uma população
    pop_size = 5  # Tamanho da população
    indiv_size = 5  # Tamanho do genoma de cada indivíduo
    populacao = Populacao(pop_size, indiv_size)

    # Mostrar os genomas iniciais da população
    print("\nGenomas iniciais da população:")
    for i, indiv in enumerate(populacao.indivs):
        print(f"Indivíduo {i + 1}: {indiv.genome}")

    # Obter indíviduo conforme o parâmetro index
    print("Indivíduo 2:", populacao.get_indiv(1))

    # Avaliação da aptidão da população
    print("Aptidão da População:", populacao.get_fitnesses())

    # Melhor indivíduo da população
    print("Melhor Indivíduo da População:", populacao.best_indiv())

    # Aptidão do melhor indivíduo da população
    print("Aptidão do Melhor Indivíduo da População:", populacao.best_fitness())

    # Escalonamento linear das apitidoes
    print("Aptidão escalonada:", populacao.linscaling(populacao.get_fitnesses()))

    # Seleção
    num_ind = 3
    print("Seleção de indivíduos por roleta:", populacao.roulette(2))

    # Recombinação
    print("Recombinação:", populacao.recombination([3, 4], 3))

    # Reinserção
    print("Reinserção:", populacao.reinsertion([[1, 1, 0, 1, 1], [0, 1, 0, 0, 0], [1, 0, 1, 1, 1]]))

    # Parâmetros para a inicialização da classe EvolAlgorithm
    pop_size = 10
    numits = 100
    desc = 5
    indiv_size = 5

    # Cria um objeto da classe EvolAlgorithm
    evol = EvolAlgorithm(pop_size, numits, desc, indiv_size)
    print("Avaliação do fit dos indivíduos:", evol.evaluate([[0, 0, 1, 0, 0], [1, 1, 0, 1, 1], [0, 0, 0, 1, 0]]))

    # Executa o algoritmo
    print("Algoritmo a correr:", evol.run())
