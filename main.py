from utils import gerador_seqs
from gibbs_sampling import GibbsSampler

seqs = gerador_seqs(50,5)
#print(seqs)

motifs = GibbsSampler(seqs, 4, 5, 0.5)
print(motifs)
# seqs, tam_motif, iter, threshold):
