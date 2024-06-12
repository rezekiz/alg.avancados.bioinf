"""
Código base retirado dos powerpoints das aulas (da autoria de Rui Mendes) com pequenas alterações.
Utilização do stack overflow e de LLMs (GPT 3.5/ BlackboxAI) para algumas correções
"""

def bwt_transf(seq : str) -> str:
    """
    -Realiza a transformação de Burrows-Wheeler em uma sequência dada.

    -Parâmetros:
    seq (str): A sequência de entrada.

    -Retorna:
    tuple: Uma tupla contendo a sequência transformada de Burrows-Wheeler e o índice original da sequência na lista de rotações.
    """

    # Adiciona o caractere de terminação '$' à sequência
    seq += '$'
    
    # Gera todas as rotações da sequência
    rotations = [seq[i:] + seq[:i] for i in range(len(seq))]
    # Ordena as rotações
    rotations.sort()

    # Concatena os últimos caracteres de cada rotação para formar a BWT
    bwt = ''.join(rotation[-1] for rotation in rotations)
    # Retorna a BWT e o índice original da sequência na lista de rotações

    return bwt, rotations.index(seq)

def bwt_reverse(bwt : str) -> str:
    """
    -Reverte a transformação de Burrows-Wheeler em uma sequência original.
    
    -Parâmetros:
    bwt (str): A sequência de Burrows-Wheeler.
    
    -Retorna:
    str: A sequência original.
    """

    # Cria uma lista vazia do tamanho da sequência BWT
    table = [None] * len(bwt)

    # Executa o processo inverso de construção da tabela
    for _ in range(len(bwt)):
        table = [bwt[i] + (table[i] if table[i] is not None else '') for i in range(len(bwt))]
        table.sort()

    # Retorna a sequência original encontrada na tabela na posição do caractere de terminação '$'

    return table[bwt.index('$')][:-1]
