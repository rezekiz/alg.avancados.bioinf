# Add parent dir to path to ensure module is found
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest

from bwt.bwt import *

class TestBWT(unittest.TestCase):
    def test_bwt_transf(self):
        # Teste básico
        seq = "banana"
        bwt, index = bwt_transf(seq)
        self.assertEqual(bwt, "annb$aa")
        self.assertEqual(index, 4)

        # Teste com uma sequência diferente
        seq = "mississippi"
        bwt, index = bwt_transf(seq)
        self.assertEqual(bwt, "ipssm$pissii")
        self.assertEqual(index, 5)

        # Teste com uma sequência vazia
        seq = ""
        bwt, index = bwt_transf(seq)
        self.assertEqual(bwt, "$")
        self.assertEqual(index, 0)


    def test_bwt_reverse(self):
        # Teste básico
        bwt = "annb$aa"
        original = bwt_reverse(bwt)
        self.assertEqual(original, "banana")

        # Teste com uma sequência diferente
        bwt = "ipssm$pissii"
        original = bwt_reverse(bwt)
        self.assertEqual(original, "mississippi")

        # Teste com uma sequência vazia
        bwt = "$"
        original = bwt_reverse(bwt)
        self.assertEqual(original, "")

if __name__ == '__main__':
    unittest.main(verbosity=2)
