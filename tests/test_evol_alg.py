"""
Funcionalidades chave de algoritmos evolucionários:

* criação de população inicial de forma aleatória
* avaliação de população inicial
* avaliação de individuos
* seleção de progenitores
* criação de novas soluções (mutações, cruzamento)
* determinar nova população a partir da população anterior e novas soluções




"""

import unittest
import algoritmos_evolucionarios


class TestEvolAlgo(unittest.TestCase):

    # Testar a iniciação de população
    # Começando pelos indivíduos
    def test_init_indiv(self):

        # Padrão
        tam_motif = 10
        indiv = init_indiv(tam_motif)

        # Verificar que está a adquirir o tamanho correto
        self.assertEqual(len(indiv), tam_motif)

        # Garante que está a usar o dicionário correto
        valid_bases = set('ACGT')
        self.assertTrue(all(base in valid_bases for base in indiv))

        # Negativo
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
        tam_pop = 50
        tam_motif = 5

        pop = init_pop(tam_pop, tam_motif)

        # Verificar que está a adquirir o tamanho correto
        self.assertEqual(len(pop), tam_pop)

        # Garantir que todos os indivíduos são "legais"
        valid_bases = set('ACGT')
        for indiv in pop:
            self.assertTrue(all(base in valid_bases for base in indiv))

        # negativo

        tam_pop = -5
        tam_motif = 5
        
        with self.assertRaises(ValueError):
            init_pop(tam_pop, tam_motif)
        
        # float
        tam_pop = 0.5
        tam_motif = 5
        
        with self.assertRaises(ValueError):
            init_pop(tam_pop, tam_motif)

        # motif maior que a pop
        tam_pop = 5
        tam_motif = 8
        
        with self.assertRaises(ValueError):
            init_pop(tam_pop, tam_motif) 

        # vazio
        tam_pop = 0
        tam_motif = 5

        with self.assertRaises(ValueError):
            init_pop(tam_pop, tam_motif)

    def test_fitness(self):

        # Padrão
        indiv = ['A','A','A','A']
        pwm = { 'A': [0.5, 0.25, 0.75, 0.75],
                'C': [0.25, 0.25, 0.25, 0.25],
                'G': [0.25, 0.25, 0.25, 0.25],
                'T': [0.25, 0.25, 0.25, 0.25] }
        
        fitness_score = fitness(indiv, pwm)
        self.assertEqual(2.25, fitness_score)

        # "ilegais"
        indiv = ['A','B','C','A']
        with self.assertRaises(ValueError):
            fitness_score(indiv, pwm)

        # discrepância de tamanhos
        indiv = ['A', 'A', 'A', 'A', 'A ']
        with self.assertRaises(ValueError):
            fitness_score(indiv, pwm)

        # vazio
        indiv = []
        with self.assertRaises(ValueError):
            fitness_score(indiv, pwm)

    
if __name__ == '__main__':
    unittest.main(verbosity=2)
    
