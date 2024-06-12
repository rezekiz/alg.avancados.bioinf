# Add parent dir to path to ensure module is found
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest

from boyer_moore.BoyerMoore import BoyerMoore

class TestBoyerMoore(unittest.TestCase):
    
    def test_search_pattern_2(self):
        # Teste com um padrão que não está presente
        bm = BoyerMoore("ACTG", "GTC")
        result = bm.search_pattern("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC")
        self.assertEqual(result, [])
    
    def test_search_pattern_3(self):
        # Teste com sequência vazia
        bm = BoyerMoore("ACTG", "ACCA")
        result = bm.search_pattern("")
        self.assertEqual(result, [])

    def test_search_pattern_4(self):
        # Teste com padrão vazio
        bm = BoyerMoore("ACTG", "")
        result = bm.search_pattern("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC")
        self.assertEqual(result, list(range(len("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC") + 1)))


if __name__ == '__main__':
    unittest.main(verbosity=2)
