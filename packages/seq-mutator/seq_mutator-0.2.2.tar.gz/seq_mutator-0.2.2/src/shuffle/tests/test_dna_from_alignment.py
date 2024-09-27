from unittest import TestCase

from ..src.dna_from_alignment import DNAFromAlignment
from ..src.restriction_enzymes import RestrictionEnzymeBatch


class TestDNAFromAlignment(TestCase):

    def setUp(self):
        alignment_fasta = "tests/test_alignment.fasta"
        codon_table_csv = "tests/test_codon_table.csv"
        restrictoin_enzymes_csv = "tests/test_restriction_enzymes.csv"
        restriction_batch = RestrictionEnzymeBatch(restrictoin_enzymes_csv)
        self.dna_from_alignment = DNAFromAlignment(
            alignment_fasta, codon_table_csv, restriction_batch)

    def test_get_total_hits(self):
        hits = self.dna_from_alignment.get_total_hits()
        self.assertTrue(hits)

    def test_call(self):
        dna_a, dna_b, hits = self.dna_from_alignment()
        self.assertTrue(dna_a)
        self.assertTrue(dna_b)
        self.assertTrue(hits)

        protein_a = self.dna_from_alignment.protein_a.replace("-", "")
        protein_b = self.dna_from_alignment.protein_b.replace("-", "")

        self.assertEqual(len(dna_a), len(protein_a) * 3)
        self.assertEqual(len(dna_b), len(protein_b) * 3)

        codon_table = self.dna_from_alignment.codon_table

        codon_table.translate(dna_a, raise_error=True)
        codon_table.translate(dna_b, raise_error=True)

