from Bio.Restriction import RestrictionBatch, AllEnzymes
from Bio import Seq
import pandas as pd


class RestrictionEnzymeBatch(RestrictionBatch):

    def __init__(self, csv_file, filter_blunt=True):
        """
        :param csv_file: csv file containing restriction enzyme names.
        The csv file should have a column named "Name"
        """
        df = pd.read_csv(csv_file)
        df = df.dropna(subset=["Name"])
        names = df["Name"].tolist()

        recognized_enzymes, unrecognized_enzymes = self._filter_breaking_enzymes(names)
        print(
            f"Loaded {len(recognized_enzymes)} valid restriction enzymes. Original number of enzymes: {len(names)}")

        super().__init__(recognized_enzymes)

        if filter_blunt:
            self._filter_blunt_enzymes()

    def _filter_blunt_enzymes(self):
        blunt_enzymes = [e for e in self if e.is_blunt()]
        for e in blunt_enzymes:
            self.remove(e)

    def _filter_breaking_enzymes(self, names):
        """
        filter out all enzymes that have "(" or ")" in their names
        """
        # filter out all enzymes that have "(" or ")" in their names
        recognized_enzymes = [name for name in names if "(" not in name and ")" not in name]

        # filter out all enzymes that are not recognized by Biopython
        recognized_enzymes = [name for name in recognized_enzymes if name in AllEnzymes]

        unrecognized_enzymes = [name for name in names if name not in recognized_enzymes]
        return recognized_enzymes, unrecognized_enzymes


class AllEnzymesBatch(RestrictionBatch):

    def __init__(self):
        super().__init__(AllEnzymes)
        self._filter_blunt_enzymes()

    def _filter_blunt_enzymes(self):
        blunt_enzymes = [e for e in self if e.is_blunt()]
        for e in blunt_enzymes:
            self.remove(e)

    def __sub__(self, other):
        enzymes_in_other = [e for e in self if e in other]
        for e in enzymes_in_other:
            self.remove(e)


if __name__ == "__main__":
    rb = RestrictionEnzymeBatch("data/restriction_enzymes.csv")
    print(rb.search(Seq.Seq("GATCTCTAGA")))









