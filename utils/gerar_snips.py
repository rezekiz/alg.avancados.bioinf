def gerar_snips(seqs, tam_snip, offset_max, indice):
        indice , escolhida = self.escolhe_seq()
        offsets = [randint(0,self.offset_max) for pos, seq in enumerate(self.seqs) if pos != indice]
        snips = [seq[pos : pos + self.tam_motif] for seq, pos in zip(self.seqs, offsets) if seq != escolhida]

        return offsets, snips