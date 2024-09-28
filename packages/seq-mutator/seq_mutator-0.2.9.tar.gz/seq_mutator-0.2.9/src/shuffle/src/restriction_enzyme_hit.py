from dataclasses import dataclass, asdict


@dataclass
class RestrictionEnzymeHit:
    aa_sequence: str
    enzyme: str
    dna_sequences: list
    start: int

    def __init__(self, aa_sequence, enzyme, dna_sequences, start):
        self.aa_sequence = aa_sequence
        self.enzyme = enzyme
        self.dna_sequences = dna_sequences

        if type(dna_sequences) is str:
            self.dna_sequences = dna_sequences.split(",")

        self.start = start

    def to_dict(self):
        self.dna_sequences = ",".join(self.dna_sequences)
        return asdict(self)






