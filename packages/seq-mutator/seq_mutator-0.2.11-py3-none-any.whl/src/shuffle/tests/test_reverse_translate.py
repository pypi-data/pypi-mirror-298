from unittest import TestCase
from Bio.Restriction import EcoRI

from ..src.reverse_translate import ReverseTranslate
from ..src.restriction_enzyme_hit import RestrictionEnzymeHit
from ..src.codon_table import CodonTable


class TestReverseTranslate(TestCase):

    def setUp(self):
        self.codon_table = CodonTable("data/ecoli_codon_table.csv", min_fraction=0.0)
        self.reverse_translate = ReverseTranslate(self.codon_table)

    def test_call(self):
        protein = "MA-AGG-"
        protein2 = "M-MAGGM"

        # # perfect_dna_sequence = "ATGGCGGGGGGG"
        rh_1 = RestrictionEnzymeHit("A", EcoRI, ["GCA"], 3)
        rh_2 = RestrictionEnzymeHit("GG", EcoRI, ["GGAGGA"], 4)
        hits = [rh_1, rh_2]

        proteins = [protein, protein2]
        [dna_1, dna_2] = self.reverse_translate(proteins, hits)

        protein = protein.replace("-", "")
        protein2 = protein2.replace("-", "")

        self.assertEqual(len(dna_1), len(protein) * 3)
        self.assertEqual(protein, self.codon_table.translate(dna_1))

        self.assertEqual(len(dna_2), len(protein2) * 3)
        self.assertEqual(protein2, self.codon_table.translate(dna_2))









