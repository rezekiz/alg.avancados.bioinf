"""
A module for generation of Position-Weighted Matrices
"""

def pwm(seqs: list[str], pseudo: int = 1) -> dict:
    """
    Calculate the Position Weight Matrix (PWM) from a list of DNA sequences.

    Args:
    - seqs (list): A list of DNA sequences represented as strings.
    - pseudo (int, optional): The pseudo count to add to each frequency count. Default is 1.

    Returns:
    - dict: A dictionary representing the PWM.
            Each key corresponds to a DNA base ('A', 'C', 'G', 'T'),
            and each value a list with the frequency of that base at each position in the motif.

    Example:
    >>> sequences = ['ACGT', 'ATGC', 'AGTC', 'AGTC']
    >>> pwm_matrix = pwm(sequences)
    >>> print(pwm_matrix)
    {'A': [0.5, 0.25, 0.75, 0.75], 
     'C': [0.25, 0.25, 0.0, 0.0], 
     'G': [0.25, 0.25, 0.25, 0.25], 
     'T': [0.0, 0.25, 0.0, 0.0]}
    """

    # Verificações
    assert isinstance(seqs, list), \
        "Não é uma lista de sequências"

    assert all(isinstance(seq, str) for seq in seqs), \
        "Todas as sequências têm de ser strings"

    assert isinstance(pseudo, int), \
        "Pseudocontagem tem de ser um número inteiro"

    assert seqs, \
        "É uma lista vazia"

    assert all(len(seq) == len(seqs[0]) for seq in seqs), \
        "Tamanhos discrepantes"

    assert all(set(seq).issubset({'A','C','G','T'}) for seq in seqs), \
        "Contém bases inválidas"


    pwm_matrix = {'A': [], 'C': [], 'G': [], 'T': []}

    for base in 'ACGT':
        for pos in range(len(seqs[0])):
            count = sum(seq[pos] == base for seq in seqs)
            pwm_matrix[base].append((count + pseudo) / (len(seqs) + 4 * pseudo))

    return pwm_matrix
