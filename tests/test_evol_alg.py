"""
Testes escritos por Rui Sousa (QA) e Mariana Oliveira (dev)

Funcionalidades chave de algoritmos evolucionários:

* criação de população inicial de forma aleatória
* avaliação de população inicial
* avaliação de individuos
* seleção de progenitores
* criação de novas soluções (mutações, cruzamento)
* determinar nova população a partir da população anterior e novas soluções

"""
import os
# Add parent dir to path to ensure module is found
import sys
import unittest

# Adicionar o diretório superior ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar as classes necessárias
from algoritmos_evolucionarios import EvolAlgorithm, Individuos, Populacao


class TestEvolAlgo(unittest.TestCase):

    # Testar a classe Individuos
    def test_individuos_init(self):
        """
        Testa o método __init__ da classe Individuos para garantir que o genoma é inicializado com o tamanho correto
        e que os genes estão dentro do intervalo [0, 1].
        """
        indiv = Individuos(size=10)
        self.assertEqual(len(indiv.genome), 10, "Tamanho do genoma incorreto.")
        self.assertTrue(all(gene in [0, 1] for gene in indiv.genome), "Genes fora do intervalo [0, 1].")

    def test_individuos_mutation(self):
        """
        Testa o método mutation da classe Individuos para garantir que a mutação altera pelo menos um gene do genoma.
        """
        indiv = Individuos(size=10)
        original_genome = indiv.genome[:]
        indiv.mutation()
        self.assertNotEqual(indiv.genome, original_genome, "Mutação não alterou o genoma.")
        self.assertTrue(any(indiv.genome[i] != original_genome[i] for i in range(10)),
                        "Mutação não alterou um gene corretamente.")

    def test_individuos_crossover(self):
        """
        Testa o método crossover da classe Individuos para garantir que o crossover produz um filho com pelo menos um
        gene de cada genoma dos pais.
        """
        indiv1 = Individuos(size=10)
        indiv2 = Individuos(size=10)
        child1, child2 = indiv1.crossover(indiv2)
        self.assertEqual(len(child1.genome), 10, "Tamanho do genoma do filho 1 está incorreto.")
        self.assertEqual(len(child2.genome), 10, "Tamanho do genoma do filho 2 está incorreto.")
        # Verifica se os filhos têm partes dos pais
        self.assertTrue(
            any(child1.genome[i] == indiv1.genome[i] for i in range(10)) and
            any(child1.genome[i] == indiv2.genome[i] for i in range(10)),
            "Filho 1 não contém partes de ambos os pais."
        )
        self.assertTrue(
            any(child2.genome[i] == indiv1.genome[i] for i in range(10)) and
            any(child2.genome[i] == indiv2.genome[i] for i in range(10)),
            "Filho 2 não contém partes de ambos os pais."
        )

    def test_individuos_get_fitness(self):
        """
        Verifica se a aptidão é calculada corretamente para um indivíduo com genoma conhecido.
        """
        indiv = Individuos(size=10, genome=[1, 1, 1, 0, 0, 1, 0, 1, 1, 1])
        self.assertEqual(indiv.get_fitness(), 7, "Aptidão calculada incorretamente.")

    def test_individuos_set_fitness(self):
        """"
        Verifica se a aptidão é configurada corretamente para um indivíduo.
        """
        indiv = Individuos(size=10)
        indiv.set_fitness(5)
        self.assertEqual(indiv.fitness, 5, "Aptidão não foi configurada corretamente.")

    # Testar a classe Populacao
    def test_populacao_init(self):
        """
        Testa o método __init__ da classe Populacao para garantir que o tamanho da população e o tamanho dos genomas
        dos indivíduos estejam corretos.
        """
        pop = Populacao(pop_size=5, indiv_size=10)
        self.assertEqual(len(pop.indivs), 5, "Tamanho da população incorreto.")
        for indiv in pop.indivs:
            self.assertEqual(len(indiv.genome), 10, "Tamanho do genoma do indivíduo incorreto.")

    def test_populacao_get_fitnesses(self):
        """
        Testa se a função get_fitnesses retorna uma lista de aptidões corretamente calculadas
        """
        pop = Populacao(pop_size=5, indiv_size=10)
        fitnesses = pop.get_fitnesses()
        self.assertEqual(len(fitnesses), 5, "Tamanho da lista de aptidões incorreto.")
        for i in range(5):
            indiv = pop.get_indiv(i)
            expected_fitness = sum(indiv.genome)  # Calcula a aptidão esperada
            self.assertEqual(fitnesses[i], expected_fitness, "A aptidão calculada está incorreta.")

    def test_populacao_best_fitness(self):
        """
        Testa se a função best_fitness retorna a aptidão do melhor indivíduo na população
        """
        pop = Populacao(pop_size=5, indiv_size=10)
        best_fitness = pop.best_fitness()
        best_indiv = pop.best_indiv()
        expected_fitness = sum(pop.get_indiv(best_indiv - 1).genome)  # Calcula a aptidão esperada
        self.assertEqual(best_fitness, expected_fitness, "A aptidão do melhor indivíduo está incorreta.")

    def test_populacao_reinsertion(self):
        """
        Testa se a função reinsertion insere corretamente os descendentes na população
        """
        pop = Populacao(pop_size=5, indiv_size=10)
        offspring = [[0] * 10] * 3  # Exemplo de descendentes
        final_pop = pop.reinsertion(offspring)
        self.assertEqual(len(final_pop), 5, "Tamanho da população final incorreto.")
        for indiv in final_pop:
            self.assertIsInstance(indiv, list, "O objeto na população final não é uma lista.")
            self.assertEqual(len(indiv), 10, "Tamanho do genoma do indivíduo na população final incorreto.")

    def test_populacao_roulette(self):
        """
        Testa se a função roulette seleciona os indivíduos de forma adequada
        """
        pop = Populacao(pop_size=10, indiv_size=10)

        # Realiza a seleção de 5 indivíduos
        selected_indices = pop.roulette(5)

        # Verifica se os índices selecionados estão dentro do intervalo correto
        for index in selected_indices:
            self.assertTrue(0 <= index < 10, "O índice selecionado está fora do intervalo.")

        # Verifica se a soma das aptidões dos indivíduos selecionados é maior que zero
        sum(pop.get_fitnesses())
        selected_fitnesses = [pop.get_fitnesses()[i] for i in selected_indices]
        self.assertGreater(sum(selected_fitnesses), 0,
                           "A soma das aptidões dos indivíduos selecionados deve ser maior que zero.")

        # Verifica se a função roulette está a selecionar indivíduos de forma aleatória
        random_selected_indices = pop.roulette(5)
        self.assertNotEqual(selected_indices, random_selected_indices,
                            "A seleção de indivíduos não está sendo feita de forma aleatória.")

    # Testar a classe EvolAlgorithm
    def test_evol_algorithm_init(self):
        """
        Testa se o algoritmo inicializa corretamente
        """
        algo = EvolAlgorithm(pop_size=5, numits=10, desc=2, indiv_size=10)
        self.assertEqual(algo.pop_size, 5, "Tamanho da população incorreto no algoritmo.")
        self.assertEqual(algo.numits, 10, "Número de iterações incorreto no algoritmo.")
        self.assertEqual(algo.desc, 2, "Número de descendentes incorreto no algoritmo.")
        self.assertEqual(algo.indiv_size, 10, "Tamanho do genoma do indivíduo incorreto no algoritmo.")

    def test_evol_algorithm_evaluate(self):
        """
        Testa se o método evaluate retorna as aptidões corretamente
        """
        algo = EvolAlgorithm(pop_size=5, numits=10, desc=2, indiv_size=10)
        indivs = [[0, 1, 0, 1, 1, 0, 0, 1, 1, 1], [1, 0, 1, 0, 0, 1, 1, 0, 0, 0], [0, 1, 1, 1, 0, 0, 0, 1, 1, 1]]
        fitnesses = algo.evaluate(indivs)
        expected_fitnesses = [6, 4, 6]
        self.assertEqual(fitnesses, expected_fitnesses, "As aptidões calculadas estão incorretas.")


if __name__ == '__main__':
    unittest.main(verbosity=2)
