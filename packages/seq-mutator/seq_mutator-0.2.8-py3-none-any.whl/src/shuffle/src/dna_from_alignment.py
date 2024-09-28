from Bio import SeqIO
from tqdm import tqdm

from .utils import iter_coherent_overlaps
from .reverse_translate import ReverseTranslate
from .restriction_site_finder import RestrictionSiteFinder
from .codon_table import CodonTable


class DNAFromAlignment:

    def __init__(self, alignment_fasta, codon_table_csv, restriction_batch, min_fraction=0.05, min_overlap=2, margin=0):

        self.codon_table = CodonTable(codon_table_csv, min_fraction=min_fraction)
        self.restriction_site_finder = RestrictionSiteFinder(self.codon_table, restriction_batch)
        records = list(SeqIO.parse(alignment_fasta, "fasta"))

        self.protein_a = str(records[0].seq)
        self.protein_b = str(records[1].seq)
        self.min_overlap = min_overlap
        self.margin = margin
        self.reverse_translate = ReverseTranslate(self.codon_table)

    def get_total_hits(self):

        total_hits = []

        iter = iter_coherent_overlaps(self.protein_a, self.protein_b, self.min_overlap, self.margin)
        iter_total = iter_coherent_overlaps(self.protein_a, self.protein_b, self.min_overlap)
        total = len(list(iter_total))

        for start, end in tqdm(iter, total=total, desc="Finding restriction sites"):

            # retrieve the protein overlap
            protein_overlapping_regions = self.protein_a[start:end]

            # find the best codons for the protein overlap
            hits = self.restriction_site_finder.find_enzyme_hits(
                protein_overlapping_regions, start)

            if hits:
                total_hits.extend(hits)

        return total_hits

    def __call__(self, hits=None):
        if not hits:
            hits = self.get_total_hits()

        proteins = [self.protein_a, self.protein_b]
        [dna_a, dna_b] = self.reverse_translate(proteins, hits)

        return dna_a, dna_b, hits

