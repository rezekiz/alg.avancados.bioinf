import unittest
from Auxiliares import sobreposicao
from Automato import Automato

class TestAutomaton(unittest.TestCase):

    def test_verify_valid_seq(self):
        seq = "ATGC"
        automaton = Automato("ATG")
        automaton.verify_seq(seq)

    def test_verify_invalid_seq(self):
        seq = "ATGX"
        automaton = Automato("ATG")
        with self.assertRaises(ValueError):
            automaton.verify_seq(seq)

    def test_verify_valid_pattern(self):
        pattern = "ATG"
        automaton = Automato(pattern)
        automaton.verify_pattern(pattern)

    def test_verify_invalid_pattern(self):
        pattern = "ATGX"
        automaton = Automato("ATG")
        with self.assertRaises(ValueError):
            automaton.verify_pattern(pattern)

    def test_build_transition_table(self):
        pattern = "ATG"
        automaton = Automato(pattern)
        expected = {
            (0, 'A'): 1, (0, 'T'): 0, (0, 'G'): 0, (0, 'C'): 0,
            (1, 'A'): 1, (1, 'T'): 2, (1, 'G'): 0, (1, 'C'): 0,
            (2, 'A'): 1, (2, 'T'): 0, (2, 'G'): 3, (2, 'C'): 0,
            (3, 'A'): 1, (3, 'T'): 2, (3, 'G'): 0, (3, 'C'): 0
        }
        self.assertEqual(automaton.transition_table, expected)

    def test_apply_sequence(self):
        pattern = "ATG"
        seq = "ATGCGC"
        automaton = Automato(pattern)
        expected = [0, 1, 2, 3, 0, 0, 0]
        result = automaton.apply_sequence(seq)
        self.assertEqual(result, expected)

    def test_find_occurrences(self):
        pattern = "ATG"
        seq = "ATGCGCATGATG"
        automaton = Automato(pattern)
        expected = [0, 6, 9]
        result = automaton.find_occurrences(seq)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
