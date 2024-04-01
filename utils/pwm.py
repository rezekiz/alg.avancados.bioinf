def pwm(seqs, pseudo = 1):
        return [
            {base: (seq.count(base) + pseudo) / (len(seq) + 4 * pseudo) for base in 'ACGT'} for seq in zip(*seqs)
            ]