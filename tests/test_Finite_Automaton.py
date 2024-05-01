import unittest

class TestDNASequenceAutomaton(unittest.TestCase):
    def setUp(self):
        self.dna_automaton = DNASequenceAutomaton()

    def test_accept_valid_sequence(self):
        dna_sequence = "AGTATGCGATGTTAAGCG"
        self.assertTrue(self.dna_automaton.accept(dna_sequence))

    def test_accept_invalid_sequence_with_spaces(self):
        dna_sequence = "AG TA TGC GAT GTTA AGCG"
        with self.assertRaises(ValueError):
            self.dna_automaton.accept(dna_sequence)

    def test_accept_invalid_sequence_with_lowercase_letters(self):
        dna_sequence = "agtatgcgatgttaagcg"
        with self.assertRaises(ValueError):
            self.dna_automaton.accept(dna_sequence)

    def test_accept_invalid_sequence_with_spaces_and_lowercase_letters(self):
        dna_sequence = "ag tA TgC gAT gTTa AgCg"
        with self.assertRaises(ValueError):
            self.dna_automaton.accept(dna_sequence)

    def test_accept_invalid_sequence_with_invalid_characters(self):
        dna_sequence = "AGTATGCGATGTTAAGCZ"
        with self.assertRaises(ValueError):
            self.dna_automaton.accept(dna_sequence)

if __name__ == '__main__':
    unittest.main()
