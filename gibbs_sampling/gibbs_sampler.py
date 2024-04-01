from random import randint, choice
from utils.auxiliares import GibbsSamplerFunctions

def GibbsSampler(seqs, tam_motif, iter, threshold):
    '''
    Executa o algoritmo de amostragem de Gibbs para encontrar motifs.

    Retorna:
    - List: lista de melhores motifs encontrados
    '''
    aux = GibbsSamplerFunctions()

    i_zero = iter
    # Garantir que todas as sequências têm o mesmo tamanho
    assert all(len(seq) == len(seqs[0]) for seq in seqs)

    # Inicialização das variáveis-resultado
    best_so_far = -1
    best_motifs = []

    # Definir o valor de posição máximo possível (n - L)
    offset_max = len(seqs[0]) - tam_motif

    # Iniciamos o loop de iterações em função do número indicado ou do threshold
    while iter > 0 and best_so_far <= threshold:
        # Escolhemos uma sequência aleatória
        indice, escolhida = aux.escolhe_seq(seqs)

        # Determinamos snips e offsets para as restantes
        offsets, snips = aux.gerar_snips(seqs, tam_motif, offset_max, indice, escolhida)

        # Geramos a matriz PWM
        P = aux.pwm(snips)

        # Vemos a posição p com maior probabilidade e respetivo offset
        best_p, best_o = aux.best_pos(snips, offsets, P)

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
