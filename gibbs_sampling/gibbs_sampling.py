from typing import List, Tuple, Dict
"""
Módulo de funções auxiliares da função de Gibbs Sampling.
Código escrito por Rui Sousa com apoio a nível meta de LLM (GPT 3.5) para afinações de pseudo-código em certos casos.
Documentação gerada por Rui Sousa
"""

from random import choice, randint


def escolhe_seq(seqs : List[str]) -> Tuple[int, str]:
    '''
    Seleciona aleatoriamente uma sequência do conjunto de sequências.

    Retorna:
    - Tuple: (indice, escolhida), onde:
        * indice: índice da sequência selecionada
        * escolhida: sequência selecionada
    '''
    assert isinstance(seqs, list) and all(isinstance(seq,str) for seq in seqs), "Devem ser listas de strings"
    assert all((char in 'ATCG') for seq in seqs for char in seq), "Devem conter bases válidas - ATCG"

    return choice(list(enumerate(seqs)))


def gerar_snips(seqs: List[str], tam_motif: int, indice: int) -> Tuple[List[int], List[str]]:
    '''
    Gera snips para todas as sequências, exceto uma sequência escolhida aleatoriamente.

    Retorna:
    - Tuple: (offsets, snips), onde:
        * offsets: lista de offsets para cada sequência
        * snips: lista de snips para cada sequência
    '''
    assert seqs, "Não pode ser lista vazia."
    assert all(seq for seq in seqs), "Não podem existir sequências vazias"
    assert tam_motif < len(seqs[0]), "Tamanho do motif tem de ser no limite do tamanho da sequência"

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
    Esta função difere da utilizada nas auxiliares, utilizando uma abordagem de lista de dicionários.

    Calcula a matriz de PWM (Position Weight Matrix) para uma lista de snips.

    Retorna:
    - List[dict]: lista de dicionários representando a matriz PWM
    '''
    return [{base: (seq.count(base) + 1) / (len(seq) + 4) for base in 'ACGT'} for seq in zip(*snips)]


def prob_snip(snip: str, P: float) -> float:
    '''
    Função que calcula a P(snip|P), para determinar a probabilidade
    deste ser gerado pelo perfil P

    Parâmetros:

    snip : str
        strings correspondente a bases de DNA

    P : list[dict]
        perfil probabilistico para um conjunto de sub-sequências de DNA

    Retorna:

    float
        P(snip|P)
    '''
    score = 1
    for pos, base in enumerate(snip):
        score *= P[pos][base]
    return score


def best_pos(snips: List[str], offsets: List[int], P: float) -> Tuple[float, int]:
    '''
    Encontra a melhor posição e offset.

    Retorna:
    - Tuple: (melhor_prob, melhor_offset), onde:
        * melhor_prob: melhor probabilidade
        * melhor_offset: melhor offset
    '''
    probs = [prob_snip(snip, P) for snip in snips]
    prob_sum = sum(probs)
    prob_comb = [round(prob / prob_sum, 5) for prob in probs]
    return max(zip(prob_comb, offsets))


def gibbs_sampling(seqs: List[str], tam_motif: int, iter: int, threshold: float) -> List[str]:
    '''
    Executa o algoritmo de amostragem de Gibbs para encontrar motifs.

    Retorna:
    - List: lista de melhores motifs encontrados
    '''

    i_zero = iter
    # Garantir que todas as sequências têm o mesmo tamanho
    assert all(len(seq) == len(seqs[0]) for seq in seqs)
    assert len(seqs[0]) > tam_motif

    # Inicialização das variáveis-resultado
    best_so_far = -1
    best_motifs = []

    # Iniciamos o loop de iterações em função do número indicado ou do threshold
    while iter > 0 and best_so_far <= threshold:
        # Escolhemos uma sequência aleatória
        indice, escolhida = escolhe_seq(seqs)

        # Determinamos snips e offsets para as restantes
        offsets, snips = gerar_snips(seqs, tam_motif, indice)

        # Geramos a matriz PWM
        P = pwm(snips)

        # Vemos a posição p com maior probabilidade e respetivo offset
        best_p, best_o = best_pos(snips, offsets, P)

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

        iter -= 1

    print(f'Threshold {threshold} atingido ao fim de {i_zero - iter} iterações.')
    return best_motifs
