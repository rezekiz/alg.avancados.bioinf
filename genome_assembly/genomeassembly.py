from grafos.grafos import Graph
from typing import List
"""

Aux funcs

"""

def k_merify(seq: str, k: int = 3) -> List[str]:
    """

    Args:
        k: size of k-mers
        seq: target sequence

    Returns:
        list: list of k-mers

    """
    assert k > 0 and k < len(seq)
    return sorted([seq[i:i+k] for i in range(len(seq)-k+1)])


def suffix(seq):
    return(seq[1:])

def prefix(seq):
    return(seq[:-1])

def identify(frags: List[str]) -> List[str]:
    """

    Args:
        frags: list of fragments

    Returns:
        list: list of tagged fragments

    """
    ident = 1
    res = []
    for frag in frags:
        res.append(f'{frag}-{ident}')
        ident += 1
    return res

class AssemblyGraph(Graph):
    def __init__(self, frags):
        super().__init__()
        self.assemble(frags)

    def assemble(self, frags):
        idA = 1 # adiciona um tag por ordem de aparição do fragmento
        for A in frags:
            suf = suffix(A)
            idB = 1
            #print(f'{A}-{idA}')
            for B in frags:
                #print(f'{B}-{idB}')
                if prefix(B) == suf:
                    self.add_edges(f'{A}-{idA} -> {B}-{idB}')
                idB += 1
            idA += 1

    def valid_path(self, path):
        if path[0] not in self.g.keys():
            return False
        for i in range(1, len(path)):
            if path[i] not in self.g.keys():
                return False
        return True

    def is_hamiltonian(self, path):
        # Check if path is valid
        if self.valid_path(path):
            # Initiate list of destinations
            dests = list(self.g.keys())

            # If path size is less than number of destinations, it can't be hamiltonian
            if len(path) != len(dests):
                return False

            # Traverse the path
            for i in range(len(path)):
                if path[i] in dests:
                    dests.remove(path[i])
                else: return False

            # Check if we visited all destinations
            if not dests:
                return True
            else:
                return False


frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA" , "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
grafo = AssemblyGraph(frags)
grafo.show().render()
#print(grafo.g)

# Test valid_path()
path = 'ACC-2 CCA-8 CAT-5 ATG-3'.split()
path2 = 'ACC-2 CCA-8 CAT-5 ATG-3 TGG-13 GGC-10 GCA-9 CAT-6 ATT-4 TTT-15 TTC-14 TCA-12 CAT-7 ATA-1 TAA-11'.split()
print(
    'Teste ao valid_path()',
    grafo.valid_path(path),
    grafo.valid_path(path2),
    sep='\n'
)

# Test hamiltonian
print(
    "Teste ao is_hamiltonian()",
    grafo.is_hamiltonian(path),
    grafo.is_hamiltonian(path2),
    sep='\n'
)


