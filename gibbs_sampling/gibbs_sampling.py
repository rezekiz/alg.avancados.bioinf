"""
Módulo de funções auxiliares da função de Gibbs Sampling.
Código escrito por Rui Sousa com apoio a nível meta de LLM (GPT 3.5)
para afinações de pseudo-código em certos casos.

Documentação gerada por Rui Sousa
"""

from typing import List, Tuple, Dict
from random import choice, randint

def escolhe_seq(seqs : List[str]) -> Tuple[int, str]:
    '''
    Seleciona aleatoriamente uma sequência do conjunto de sequências.

    Parâmetros:
        seqs (List[str]): Lista de sequências de DNA.

    Retorna:
        Tuple[int, str]: Tuplo contendo o índice da sequência selecionada e a própria sequência.
    '''
    assert isinstance(seqs, list) and all(isinstance(seq,str) for seq in seqs),\
        "Devem ser listas de strings"
    assert all((char in 'ATCG') for seq in seqs for char in seq), \
        "Devem conter bases válidas - ATCG"

    return choice(list(enumerate(seqs)))

def gerar_snips(seqs: List[str], tam_motif: int, indice: int) -> Tuple[List[int], List[str]]:
    '''
    Gera snips para todas as sequências, exceto uma sequência escolhida aleatoriamente.

    Parâmetros:
        seqs (List[str]): Lista de sequências de DNA.
        tam_motif (int): Tamanho do motif a ser gerado.
        indice (int): Índice da sequência que será excluída da geração de snips.

    Retorna:
        Tuple[List[int], List[str]]: Tuplo contendo a lista de offsets e a lista de snips gerados.
    '''
    assert seqs, \
        "Não pode ser lista vazia."
    assert all(seq for seq in seqs), \
        "Não podem existir sequências vazias"
    assert tam_motif < len(seqs[0]), \
        "Tamanho do motif tem de ser no limite do tamanho da sequência"

    # Removemos a escolhida da lista
    seqs_copy = seqs[:]
    seqs_copy.pop(indice)

    # Calculamos o offset máximo possível
    offset_max = len(seqs[0]) - tam_motif

    # Geramos a lista de offsets
    offsets = [randint(0, offset_max) for pos, seq in enumerate(seqs_copy)]

    # Geramos a lista de snips
    snips = [seq[pos: pos + tam_motif] for seq, pos in zip(seqs_copy, offsets)]

    return offsets, snips


def pwm(snips : List[str]) -> List[Dict[str, float]]:
    '''
    Calcula a matriz de PWM (Position Weight Matrix) para uma lista de snips.

    Parâmetros:
        snips (List[str]): Lista de snips de DNA.

    Retorna:
        List[Dict[str, float]]: Lista de dicionários representando a matriz PWM.
    '''
    return [
        {base: (seq.count(base) + 1) / (len(seq) + 4) for base in 'ACGT'} for seq in zip(*snips)
    ]

def prob_snip(snip: str, pwm_matrix: float) -> float:
    '''
    Calcula a probabilidade de um snip ser gerado pelo perfil P (matriz PWM).

    Parâmetros:
        snip (str): Snip de DNA a ser avaliado.
        pwm_matrix (List[Dict[str, float]]): Matriz PWM representando o perfil probabilístico.

    Retorna:
        float: Probabilidade do snip dado o perfil P.
    '''
    score = 1
    for pos, base in enumerate(snip):
        score *= pwm_matrix[pos][base]
    return score

def best_pos(snips: List[str], offsets: List[int], pwm_matrix: float) -> Tuple[float, int]:
    '''
    Encontra a melhor posição e offset baseado na matriz PWM.

    Parâmetros:
        snips (List[str]): Lista de snips de DNA.
        offsets (List[int]): Lista de offsets correspondentes aos snips.
        pwm_matrix (List[Dict[str, float]]): Matriz PWM representando o perfil probabilístico.

    Retorna:
        Tuple[float, int]: Tuplo contendo a melhor probabilidade encontrada e o offset correspondente.
    '''
    probs = [prob_snip(snip, pwm_matrix) for snip in snips]
    prob_sum = sum(probs)
    prob_comb = [round(prob / prob_sum, 5) for prob in probs]
    return max(zip(prob_comb, offsets))

def gibbs_sampling(seqs: List[str], tam_motif: int, num_iteracoes: int, threshold: float) -> List[str]:
    '''
    Executa o algoritmo de amostragem de Gibbs para encontrar motifs nas sequências fornecidas.

    Parâmetros:
        seqs (List[str]): Lista de sequências de DNA.
        tam_motif (int): Tamanho do motif a ser encontrado.
        num_iteracoes (int): Número máximo de iterações para executar o algoritmo.
        threshold (float): Limite de probabilidade para encerrar o algoritmo.

    Retorna:
        List[str]: Lista dos melhores motifs encontrados durante as iterações.
    '''

    i_zero = num_iteracoes
    # Garantir que todas as sequências têm o mesmo tamanho
    assert all(len(seq) == len(seqs[0]) for seq in seqs)
    assert len(seqs[0]) > tam_motif

    # Inicialização das variáveis-resultado
    best_so_far = -1
    best_motifs = []

    # Iniciamos o loop de iterações em função do número indicado ou do threshold
    while num_iteracoes > 0 and best_so_far <= threshold:
        # Escolhemos uma sequência aleatória
        indice, escolhida = escolhe_seq(seqs)

        # Determinamos snips e offsets para as restantes
        offsets, snips = gerar_snips(seqs, tam_motif, indice)

        # Geramos a matriz PWM
        pwm_matrix = pwm(snips)

        # Vemos a posição p com maior probabilidade e respetivo offset
        best_p, best_o = best_pos(snips, offsets, pwm_matrix)

        # Comparamos com o "best so far" e atualizamos
        if best_p > best_so_far:
            best_so_far = best_p
            best_offset_so_far = best_o
            best_motif_so_far = escolhida[best_o:best_o + tam_motif]

        # Adicionamos o motif à lista de motifs candidatos
        best_motifs.append((
            f'S{str(indice)}',
            f'p = {str(best_offset_so_far)}',
            best_motif_so_far,
            best_so_far))

        num_iteracoes -= 1

    print(f'Threshold {threshold} atingido ao fim de {i_zero - num_iteracoes} iterações.')
    return best_motifs
