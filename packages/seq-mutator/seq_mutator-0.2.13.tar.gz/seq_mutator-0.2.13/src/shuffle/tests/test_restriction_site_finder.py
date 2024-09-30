from unittest import TestCase
from Bio.Restriction import RestrictionBatch, EcoRI

from ..src.restriction_site_finder import RestrictionSiteFinder
from ..src.codon_table import CodonTable


class TestRestrictionSiteFinder(TestCase):

    def setUp(self):
        self.codon_table = CodonTable("data/ecoli_codon_table.csv", min_fraction=0.0)
        self.restriction_batch = RestrictionBatch([EcoRI])
        self.restriction_site_finder = RestrictionSiteFinder(
            self.codon_table, self.restriction_batch)

    def test_get_all_possible_dna(self):
        sites = ["GAV", "NTC", "AYA", "AAAAR"]
        expected = [
            ["GAC", "GAG", "GAA"],
            ["ATC", "GTC", "TTC", "CTC"],
            ["ATA", "ACA"],
            ["AAAAA", "AAAAG"]]
        for site, exp in zip(sites, expected):
            result = self.restriction_site_finder._get_all_possible_dna(site)
            self.assertEqual(set(result), set(exp))

    def test_make_translatable(self):
        sites = ["GAVG", "NTC", "AY"]
        exptected = [
            ["NNGAVG", "NGAVGN", "GAVGNN"],
            ["NTC"],
            ["NAY", "AYN"]]
        for site, exp in zip(sites, exptected):
            result = self.restriction_site_finder._make_translatable(site)

            # check that all elements in result have length devidable by 3
            self.assertTrue(all(len(e) % 3 == 0 for e in result))

            # check that the result is the same as expected
            self.assertEqual(set(result), set(exp))

    def test_find_enzyme_hits_single(self):
        enzyme = EcoRI
        site = enzyme.site
        restriction_batch = RestrictionBatch([enzyme])

        restriction_site_finder = RestrictionSiteFinder(self.codon_table, restriction_batch)
        translated = self.codon_table.translate(site)
        hits = restriction_site_finder.find_enzyme_hits(translated)

        self.assertTrue(hits)
        self.assertTrue(all(h.enzyme == enzyme for h in hits))
        self.assertTrue(all(h.aa_sequence == translated for h in hits))

    def test_find_enzyme_hits_multiple(self):
        for enzyme in self.restriction_batch:
            site = enzyme.site

            for base in site:
                if base in ["N", "R", "Y", "V"]:
                    new_base = self.restriction_site_finder.ambiguity_codes[base][0]
                    site = site.replace(base, new_base)

            missing = 3 - len(site) % 3
            missing = 0 if missing == 3 else missing

            site += "A" * missing
            translated = self.codon_table.translate(site)

            self.assertTrue(translated)

            hits = self.restriction_site_finder.find_enzyme_hits(translated)

            # check that the hits are not empty
            self.assertTrue(hits)

            # check that hits contain the enzyme
            self.assertTrue(any(h.enzyme == enzyme for h in hits))

            # check that hits contain the translated site
            self.assertTrue(any(h.aa_sequence == translated for h in hits))

            # check that the dna sequences are valid and can be tranlated
            for hit in hits:
                self.assertTrue(all(self.codon_table.translate(dna)
                                for dna in hit.dna_sequences))








