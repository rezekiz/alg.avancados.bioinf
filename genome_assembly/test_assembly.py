import unittest

from genome_assembly.genomeassembly import *

class TestAssemblyGraph(unittest.TestCase):
    """
    Suite de testes para a classe AssemblyGraph e
    respetivas funções auxiliares
    """

    def test_k_merify(self):
        seq = 'ACGT'
        k = 3
        self.assertEqual(k_merify(k, seq), ['ACG','CGT'])



if __name__ == '__main__':
    unittest.main(verbosity=2
                  )

# Test valid_path()
path = 'ACC-2 CCA-8 CAT-5 ATG-3'.split()
path2 = 'ACC-2 CCA-8 CAT-5 ATG-3 TGG-13 GGC-10 GCA-9 CAT-6 ATT-4 TTT-15 TTC-14 TCA-12 CAT-7 ATA-1 TAA-11'.split()


