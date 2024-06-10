# Add parent dir to path to ensure module is found
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import unittest
from unittest.mock import patch, MagicMock
from gibbs_sampling import gibbs_sampling  # Adjust the import to match your module path

import unittest
from gibbs_sampling import escolhe_seq, gerar_snips, pwm, prob_snip, best_pos, gibbs_sampling


class TestYourFunctions(unittest.TestCase):

    def setUp(self):
        # Define any necessary setup for your tests
        pass

    def tearDown(self):
        # Define any necessary cleanup after your tests
        pass

    def test_escolhe_seq(self):
        # Test escolhe_seq function
        seqs = ['ATCG', 'CGTA', 'GCTA']
        result = escolhe_seq(seqs)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], int)
        self.assertIsInstance(result[1], str)

    def test_gerar_snips(self):
        # Test gerar_snips function
        seqs = ['ATCG', 'CGTA', 'GCTA']
        tam_motif = 2
        indice = 0 # equivalente a escolher 'ATCG'
        offsets, snips = gerar_snips(seqs, tam_motif, indice)
        self.assertIsInstance(offsets, list)
        self.assertIsInstance(snips, list)
        self.assertEqual(len(offsets), 2)
        self.assertEqual(len(snips), 2)

    def test_pwm(self):
        # Test pwm function
        snips = [['A', 'T'], ['C', 'G'], ['G', 'C'], ['T', 'A']]
        result = pwm(snips)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], dict)
        self.assertEqual(len(result[0]), 4)

    def test_prob_snip(self):
        # Test prob_snip function
        snip = 'AT'
        P = [{'A': 0.3, 'C': 0.2, 'G': 0.2, 'T': 0.3}, {'A': 0.2, 'C': 0.3, 'G': 0.3, 'T': 0.2}]
        result = prob_snip(snip, P)
        self.assertIsInstance(result, float)
        self.assertTrue(result >= 0.0)

    def test_best_pos(self):
        # Test best_pos function
        snips = [['A', 'T'], ['C', 'G'], ['G', 'C'], ['T', 'A']]
        offsets = [0, 1, 2, 3]
        P = [{'A': 0.3, 'C': 0.2, 'G': 0.2, 'T': 0.3}, {'A': 0.2, 'C': 0.3, 'G': 0.3, 'T': 0.2}]
        result = best_pos(snips, offsets, P)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], float)
        self.assertIsInstance(result[1], int)

    def test_gibbs_sampling(self):
        # Test gibbs_sampling function
        seqs = ['ATCG', 'CGTA', 'GCTA']
        tam_motif = 2
        iter = 10
        threshold = 0.5
        result = gibbs_sampling(seqs, tam_motif, iter, threshold)
        self.assertIsInstance(result, list)
        self.assertTrue(all(isinstance(item, tuple) for item in result))
        self.assertTrue(all(len(item) == 4 for item in result))


if __name__ == '__main__':
    unittest.main(verbosity=2)
