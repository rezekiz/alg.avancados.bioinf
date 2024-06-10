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
# Add parent dir to path to ensure module is found
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from algoritmos_evolucionarios.AlgEvol import *
from algoritmos_evolucionarios.Ind import *
from algoritmos_evolucionarios.Pop import *
from unittest.mock import patch

class TestEvolAlgo(unittest.TestCase):

    # Testar a iniciação de população
    # Começando pelos indivíduos
    def test_init_indiv(self):

        # Padrão
        seqs = ['AAA', 'AAA', 'AAA', 'AAA']
        genes = [0,1,2]
        tam_motif = len(seqs)
        indiv = init_indiv(tam_motif, seqs)

        # Verificar que está a adquirir o tamanho correto
        self.assertEqual(len(indiv), tam_motif)

        # Garante que está dentro dos valores possíveis
        valid_indexes = [_ for _ in range(len(seqs[0]))]
        self.assertTrue(all(ind in valid_indexes for ind in indiv))

        # Fora do range possível ( < ou > que len(seqs) )
        tam_motif = -5
        with self.assertRaises(ValueError):
            init_indiv(tam_motif)

        # Float
        tam_motif = 1.5
        with self.assertRaises(ValueError):
            init_indiv(tam_motif)

        # Vazio
        tam_motif = 0
        with self.assertRaises(ValueError):
            init_indiv(tam_motif)

      
    # Testando a geração de população

    def test_init_pop(self):

        # Padrao
        seqs = ['AAA','AAA','AAA']
        tam_pop = 50
        tam_motif = 3
        pop = init_pop(tam_pop, tam_motif)

        # Verificar que está a adquirir o tamanho correto
        self.assertEqual(len(pop), tam_pop)

        # negativo
        tam_pop = -5
        tam_motif = 3
        with self.assertRaises(ValueError):
            init_pop(tam_pop, tam_motif)
        
        # float
        tam_pop = 0.5
        tam_motif = 3
        
        with self.assertRaises(ValueError):
            init_pop(tam_pop, tam_motif)

        # vazio
        tam_pop = 0
        tam_motif = 3

        with self.assertRaises(ValueError):
            init_pop(tam_pop, tam_motif)

    def test_fitness(self):

        """
        Como imagino que isto possa ser:

        1 - individuos são vetores de posições;
        2 - para testar a fitness criamos um subset de cada sequência;
        3 - geramos um PWM para esse subset;
        4 - somamos a probabilidade dos mais prováveis em cada posição;
        5 - a melhor fitness possível será o N * ((C+P) / (N*4P)) 
            N: nº seqs
            C: contagem da mesma base em todas
            P: pseudocontagem
            exemplo: [0,0,0] para ['AAA','AAA','AAA'] terá de ter um fitness de 3 * (4/7)
        """
        # Versão com PWM (mais complexa)
        seqs = ['AAGT', 'TAAG', 'CCAA' , 'AAAA']
        indiv = [0,1,2,0]
        
        """
        O PWM será:

        pwm = { 'A': [0.625, 0.625],
                'C': [0.125, 0.125],
                'G': [0.125, 0.125],
                'T': [0.125, 0.125]}
        """
        
        fitness_score = fitness(seqs, indiv) # Assumi que o fitness faz o subsetting e cria os PWMs
        self.assertEqual(1.25, fitness_score)
   
    def test_selection(self):
        
        """
        Provavelmente isto vai ficar completamente diferente pois
        funciona bastante melhor é mais lean com classes, no que respeita
        as fitnesses, mas esta pode ser uma abordagem possível?
        """
        indivs = [
            ([0,1,2,0],1.25),
            ([0,1,2,1],1.25),
            ([1,1,2,2],1.15),
            ([0,1,0,1],1.00)] 
        
        num_indivs = 2 # número de individuos a selecionar
        thresh = 1.1 # fitness mínima - elitismo
        selected = selection(indivs, num_indivs, thresh)
        self.assertEqual([[0,1,2,0], [0,1,2,1]], selected)

    def test_crossover(self):
        # Padrão
        indiv_1 = [0,1,2,0,5,6]
        indiv_2 = [0,3,3,1,0,1]
        x_pt    = 3
        offspring = crossover(indiv_1, indiv_2, x_pt)
        self.assertEqual([[0,1,2,1,0,1],[0,3,3,0,5,6]], offspring)

        # Inválidos - fora de range, vazio, negativo
        x_pt = 10
        with self.assertRaises(AssertionError):
            crossover(indiv_1, indiv_2, x_pt)

        # Inválidos - fora de range, vazio, negativo
        x_pt = -1
        with self.assertRaises(AssertionError):
            crossover(indiv_1, indiv_2, x_pt)

    import random
    @patch('random.randint', side_effect=[3, 5])             
    def test_mutation(self, mock_randint):
        # Padrão
        indiv = [0,4,2,0,0,1]
        mutated = mutate(indiv)
        self.assertEqual(mutated, [0,4,2,5,0,1])
    
    def test_termination(self):
        # Função que determina que o algoritmo acaba ao fim de X gerações
        # E que o resultado final é o que tem melhor fitness (num caso simples como os que temos vindo a demonstrar)
        pass

    def test_evol_algo_completo(self):
        # Testar todo o pipeline desde a geração de indivs, pop, mutações e gerações

        seqs = 'aaa act agt taa gaa aac'.upper().split()
        pop = 20
        gens = 10
        tam_motif = 2 # isto define o valor máximo que cada gene pode adotar 
        pass
    
if __name__ == '__main__':
    unittest.main(verbosity=2)
    
