# Add parent dir to path to ensure module is found
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from utils import pwm

# TODO testar gerador_seqs

class TestarUtils(unittest.TestCase):

    def test_pwm(self):

        seqs = ['ACGT','ACGT','ACGT','ACGT']
        mpwm = pwm(seqs)

        self.assertEqual(
            {'A': [0.625, 0.125, 0.125, 0.125], 'C': [0.125, 0.625, 0.125, 0.125], 'G': [0.125, 0.125, 0.625, 0.125], 'T': [0.125, 0.125, 0.125, 0.625]} , mpwm
            )
        
        seqs = []

        # Ilegais
        seqs = ['ARGT' , 'ACGT', 'ACGT', 'ACGT']
        with self.assertRaises(AssertionError):
            pwm(seqs)

        # Tamanhos diferentes
        seqs = ['ASEREJE', 'ACGT', 'ACGT', 'ACGT']
        with self.assertRaises(AssertionError):
            pwm(seqs)

        # vazia
        seqs = []
        with self.assertRaises(AssertionError):
            pwm(seqs)

if __name__ == '__main__':
    unittest.main(verbosity=2)

