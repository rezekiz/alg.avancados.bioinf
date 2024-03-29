# Instanciação do método de identificação de motifs com recurso
# ao MCMC Gibbs Sampling
#
#

# Funções auxiliares

def gerar_seqs(n,t):
  from random import choice
  return [''.join(choice('ACGT') for p in range(n)) for i in range(t)]

#

def escolhe_seq(seqs):
  from random import choice
  return choice(list(enumerate(seqs)))

#

def gerar_snips(seqs , L , offset_max, indice):

  from random import randint as ri

  offsets = [ri(0,offset_max) for pos, seq in enumerate(seqs) if pos != indice]
  snips = [seq[pos: pos + L] for seq, pos in zip(seqs,offsets) if seq != seq[indice]]

  return offsets, snips

#

def pwm(seqs , pseudo = 1):
  # Criamos uma lista por compreensão que contém 1 dicionário de P(base) por sequência
  return [
      {base: (seq.count(base) + pseudo) / (len(seq) + 4 * pseudo) for base in 'ACGT'} for seq in zip(*seqs)
      ]

# Esta função tem de ser atualizada para encadear com a verificação de todas as posições

def prob_snip(snip, P):
  '''
  Função que calcula a P(snip|P), para determinar a probabilidade
  deste ser gerado pelo perfil P

  Parametros:

  snip : str
    strings correspondente a bases de DNA

  P : list[dict]
    perfil probabilistico para um conjunto de sub-sequências de DNA

  Devolve:

  float
    P(snip|P)
  '''
  score = 1
  for pos , base in enumerate(snip):
    score *= P[pos][base]
  return score

# Código a ser implementado para isto:

'''
res = []
for offset in range(len(escolhida) - L + 1):

    motif = escolhida[offset : offset + L]

    prob = 1

    for pos in range(L):

        prob *= P[pos][motif[pos]] / 10 # -> será o nosso T

    res.append(prob)

res

'''

# Esta função tem de ser atualizada
# Concretamente é preciso substituir o max() do return por um random.choices() com
# as probs geradas pela função acima

def best_pos(snips, offsets, P):

  from random import choices

  # Calculamos P(snip|P) para cada snip
  probs = [prob_snip(snip, P) for snip in snips]

  # Calculamos a probabilidade combinada para cada snip
  prob_comb = [round(prob/sum(probs),5) for prob in probs]

  # Garantimos que a soma totaliza 1
  assert round(sum(prob_comb),0) == 1

  # Devolve a melhor probabilidade e o offset associado a este
  return max(list(zip(prob_comb,offsets)))

# Função principal
# Talvez seja melhor converter isto tudo num objecto GibssSampler

def gibbs_sampler(seqs,L,iter, threshold):
  '''
  Add docstrings
  '''
  i_zero = iter
  # Garantir que todas as sequências têm o mesmo tamanho
  assert all(len(seq) == len(seqs[0]) for seq in seqs)

  # Definir n como o tamanho das nossas sequências
  n = len(seqs[0])

  # Definir o valor de posição máximo possível (n - L)
  offset_max = n - L

  # Inicialização das variáveis-resultado
  best_so_far = -1
  best_offset_so_far = -1
  best_motif_so_far = ''
  best_motifs = []

  # Iniciamos o loop de iterações em função do número indicado ou do threshold
  while iter > 0 and best_so_far <= threshold:
    #print(best_motif_so_far, best_so_far, best_offset_so_far)

    # Escolhemos uma sequência aleatória
    indice, escolhida = escolhe_seq(seqs)

    # Determinamos snips e offsets para as restantes
    offsets, snips = gerar_snips(seqs, L, offset_max, indice)
    #print(snips)

    # Geramos a matriz PWM
    P = pwm(snips)

    # Vemos a posição p com maior probabilidade e respetivo offset
    best_p, best_o = best_pos(snips, offsets, P)
    #print(best_p, best_o)

    # Comparamos com o "best so far" e atualizamos
    if best_p > best_so_far:
      best_so_far = best_p
      best_offset_so_far = best_o
      best_motif_so_far = escolhida[best_o:best_o+L]

      # Adicionamos o motif à lista de motifs candidatos
      best_motifs.append((
        f'S{str(indice)}',
        f'p = {str(best_offset_so_far)}',
        best_motif_so_far,
        best_so_far))



    iter -=1

  print(f'Threshold {threshold} atingido ao fim de {i_zero-iter} iterações.')
  return best_motifs