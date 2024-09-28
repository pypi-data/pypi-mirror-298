from .codon_table import CodonTable
import numpy as np


class ReverseTranslate:

    def __init__(self, codon_table):
        self.codon_table = codon_table

    def _init_dnas(self, sequence_length, num_sequences):
        dnas = np.empty((num_sequences, sequence_length * 3), dtype=str)
        return dnas

    def _fill_hit(self, dnas, hit):
        start = hit.start * 3
        dna_sequence = self.codon_table.get_best_dna(hit.dna_sequences)
        dnas[:, start:start + len(dna_sequence)] = np.array(list(dna_sequence))

    def _sequences_are_same(self, sequences):
        """
        check if all sequences are the same

        :param sequences: list of sequences [str]
        """
        return all(sequence == sequences[0] for sequence in sequences)

    def __call__(self, sequences: [str], hits):
        """
        reverse translate a set of protein sequences to a dna sequences,
        which are most optimal for the codon table. The hits are used to lock in certain codons.

        :param codon_table: codon table
        :param sequence: protein sequence
        :param hits: list of hits
        """
        sequences = np.array([list(sequence) for sequence in sequences])

        # create a list of bases for the dna sequencs
        dnas = self._init_dnas(sequences.shape[1], sequences.shape[0])

        # fill in the dna sequence with the hits
        for hit in hits:
            self._fill_hit(dnas, hit)

        for i in range(sequences.shape[1]):
            dna_idx = i * 3

            # skip if the dna is already filled in with a hit
            if dnas[0, dna_idx]:
                continue

            # if all codons are same for all sequences, set the codon to the same for all sequences
            if self._sequences_are_same(sequences[:, i]):
                codon = self.codon_table.get_random_codon(sequences[0, i])
                dnas[:, dna_idx:dna_idx + 3] = list(codon)

            for j, sequence in enumerate(sequences):
                aa = sequence[i]

                # skip if the amino acid is a gap
                if aa == '-':
                    continue

                # set random codon for the amino acid
                codon = self.codon_table.get_random_codon(aa)
                dnas[j, dna_idx:dna_idx + 3] = list(codon)

        return [''.join(dna) for dna in dnas]


if __name__ == "__main__":
    codon_table = CodonTable("data/ecoli_codon_table.csv")

    protein = "MA-GG-"
    protein2 = "M-MGGM"

    dna = ReverseTranslate(codon_table)([protein, protein2], [])
    print(dna)

























