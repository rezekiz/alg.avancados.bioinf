"""
Generate random sequences for testing purposes.
"""

from random import choice

def gerador_seqs(len_seqs : int , num_seqs : int) -> list[str]:
    """
    Função simples de geração de num_seqs número de sequências de DNA aleatórias
    de tamanho len_seqs utilizando a função choice do módulo random.

    Recebe dois números inteiros, len_seqs e num_seqs e devolve uma lista de num_seqs
    strings de tamanho len_seqs.
    """
    return [''.join(choice('ACGT') for p in range(len_seqs)) for i in range(num_seqs)]
