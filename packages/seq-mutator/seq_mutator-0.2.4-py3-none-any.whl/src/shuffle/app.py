from typer import Typer, Option
from typing import Annotated
import os

from .src.dna_from_alignment import DNAFromAlignment
from .src.hit_storage import HitStorage
from .src.restriction_enzymes import RestrictionEnzymeBatch

app = Typer(help="This is the cli used for codon optimization and restriction site finding")


@app.command(help="Find all restriction sites in the alignment in the overlapping regions.")
def find_hits(
    alignment: Annotated[str, Option(help="The path to the alignment fasta file. It should"
                                     "contain 2 sequences.")],
    restriction_enzymes: Annotated[str,
                                   Option(help="The path to the csv file containing the restriction"
                                          "enzymes. It must have the column 'Name'.")],
    codon_table: Annotated[str,
                           Option(help="The path to the csv file containing the codon table. It "
                                  "must have the columns 'triplet', 'amino acid', 'fraction'.")],
    hits_path: Annotated[str,
                         Option('-h', '--hits', help="The path to "
                                "the csv file the hits will be stored in.")] = "hits.csv",
):
    if not os.path.exists(alignment):
        raise FileNotFoundError(f"Alignment file {alignment} not found.")

    if not os.path.exists(restriction_enzymes):
        raise FileNotFoundError(f"Restriction enzymes file {restriction_enzymes} not found.")

    if not os.path.exists(codon_table):
        raise FileNotFoundError(f"Codon table file {codon_table} not found.")

    hit_sotrage = HitStorage(hits_path)
    restriction_batch = RestrictionEnzymeBatch(restriction_enzymes)
    dna_from_alignment = DNAFromAlignment(alignment, codon_table, restriction_batch)
    _, __, hits = dna_from_alignment()

    print(f'Found {len(hits)} hits.')

    hit_sotrage.save_hits(hits)

    print(f'Saved hits to {hits_path}.')


@app.command(help="This command performs a codon optimization on the alignment for the given"
             "codon table. The given restriction enzyme hits will be included into the sequence")
def optimize(
    alignment: Annotated[str, Option(help="The path to the alignment fasta file. It should contain"
                                     "2 sequences.")],
    restriction_enzymes: Annotated[str,
                                   Option(help="The path to the csv file containing the restriction"
                                          "enzymes. It must have the column 'Name'.")],
    codon_table: Annotated[str,
                           Option(help="The path to the csv file containing the codon table. It "
                                  "must have the columns 'triplet', 'amino acid', 'fraction'.")],
    hits_path: Annotated[str,
                         Option('-h', '--hits', help="The path to "
                                "the csv file the hits will be stored in.")] = None,
):
    if not os.path.exists(alignment):
        raise FileNotFoundError(f"Alignment file {alignment} not found.")

    if not os.path.exists(restriction_enzymes):
        raise FileNotFoundError(f"Restriction enzymes file {restriction_enzymes} not found.")

    if not os.path.exists(codon_table):
        raise FileNotFoundError(f"Codon table file {codon_table} not found.")

    if hits_path is not None and os.path.exists(hits_path):
        hit_sotrage = HitStorage(hits_path)
        hits = hit_sotrage.load_hits()

    dna_from_alignment = DNAFromAlignment(alignment, codon_table, restriction_enzymes)
    dna_a, dna_b, _ = dna_from_alignment(hits)

    print(f'Here are the codon optimized sequences including {len(hits)}'
          f'restriction sites: \n1: {dna_a}\n2: {dna_b}')


if __name__ == "__main__":
    app()




