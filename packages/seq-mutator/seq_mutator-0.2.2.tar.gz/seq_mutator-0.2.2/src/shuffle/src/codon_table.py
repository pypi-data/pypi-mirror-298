import pandas as pd
import random


class CodonTable:

    def __init__(self, csv_path, min_fraction=0.05):
        """
        retrieve the codon table from a csv file

        fields: [triplet] [amino acid] [fraction] [fraction]

        :return forward_table, back_table
        """
        df = pd.read_csv(csv_path)
        df = df[["triplet", "amino acid", "fraction"]]
        self.df = df[df["fraction"] >= min_fraction]

        # back_table
        back_table = self.df.sort_values(by="fraction", ascending=False)
        self.back_table = back_table.groupby("amino acid")["triplet"].apply(list).to_dict()

        # forward_table
        self.forward_table = self.df.set_index("triplet")["amino acid"].to_dict()

    def best_codon(self, aa):
        """
        retrieve the best codon for a given amino acid

        :param aa: amino acid

        :return codons: list of codons
        """
        if aa not in self.back_table:
            raise ValueError(f"amino acid {aa} not found in codon table")

        codons = self.back_table[aa]
        return codons[0]

    def get_random_codon(self, aa):
        """
        retrieve a random codon for a given amino acid

        :param aa: amino acid

        :return codon: codon
        """
        if aa not in self.back_table:
            raise ValueError(f"amino acid {aa} not found in codon table")

        # get all codons for the amino acid
        df = self.df[self.df["amino acid"] == aa]

        # get a random codon with the propability of the fraction
        codon = random.choices(df["triplet"].values, df["fraction"].values)[0]

        return codon


    def get_best_dna(self, dna_sequences):
        """
        return the dna sequence with the highest fraction
        """
        best_dna = None
        best_score = 0

        for dna in dna_sequences:
            assert len(dna) % 3 == 0, "DNA sequence must be a multiple of 3"
            score = 0
            for i in range(0, len(dna), 3):
                codon = dna[i:i + 3]

                if codon not in self.forward_table:
                    continue

                fraction = self.df[self.df["triplet"] == codon]["fraction"].values[0]
                score += fraction

            if score > best_score:
                best_score = score
                best_dna = dna

        return best_dna

    def translate(self, dna, raise_error=False):
        """
        translate a DNA sequence to a protein sequence

        :param dna: DNA sequence

        :return protein: protein sequence
        """

        assert len(dna) % 3 == 0, "DNA sequence must be a multiple of 3"

        protein = ""
        for i in range(0, len(dna), 3):
            codon = dna[i:i + 3]

            if codon not in self.forward_table:
                if raise_error:
                    raise ValueError(f"codon {codon} not found in codon table")
                return

            protein += self.forward_table[codon]

        return protein


if __name__ == "__main__":
    codon_table = CodonTable("data/ecoli_codon_table.csv", min_fraction=0.05)
    print("Back Table: ", codon_table.back_table)
    print("Forward Table: ", codon_table.forward_table)
