import unittest


class TestBoyerMoore(unittest.TestCase):

    def test_search_pattern(self):
        # Teste básico
        bm = BoyerMoore("ACTG", "ACCA")
        result = bm.search_pattern("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC")
        self.assertEqual(result, [5, 13, 22, 36])

        # Teste com um padrão diferente
        bm = BoyerMoore("ACTG", "TG")
        result = bm.search_pattern("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC")
        self.assertEqual(result, [1, 14, 22, 26, 33])

        # Teste com um padrão que não está presente
        bm = BoyerMoore("ACTG", "GTC")
        result = bm.search_pattern("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC")
        self.assertEqual(result, [])

        # Teste com sequência vazia
        bm = BoyerMoore("ACTG", "ACCA")
        result = bm.search_pattern("")
        self.assertEqual(result, [])

        # Teste com padrão vazio
        bm = BoyerMoore("ACTG", "")
        result = bm.search_pattern("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC")
        self.assertEqual(result, list(range(len("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC") + 1)))


if __name__ == '__main__':
    unittest.main()
