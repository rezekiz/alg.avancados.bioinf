import unittest
from utils import pwm

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

