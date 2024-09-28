from Bio import SearchIO
import pandas as pd
from tqdm import tqdm

from .database import Database


class JackHMMERParser:

    def __init__(self, hmmer_file, db_name):
        self.hmmer_file = hmmer_file
        self.db = Database(db_name)

    def _parse_hmmer(self):
        with open(self.hmmer_file) as f:
            for query in SearchIO.parse(f, "hmmer3-tab"):
                yield query

    def create_csv(self, path, max_evalue=10.):

        print("Creating CSV file with max evalue of {}".format(max_evalue))

        ids = []
        evalues = []

        # iterate through hmmer output
        for query in tqdm(self._parse_hmmer()):
            for hit in query.hits:

                # filter by evalue
                if hit.evalue > max_evalue:
                    continue

                ids.append(hit.id)
                evalues.append((hit.id, hit.evalue))

        # get sequences from database
        print("Getting sequences from database")
        sequences = self.db.get_sequences(ids)

        # create dataframe
        print("Creating CSV file")
        df = pd.DataFrame(sequences, columns=["id", "sequence"])
        evalue_df = pd.DataFrame(evalues, columns=["id", "evalue"])

        df = df.merge(evalue_df, on="id")
        df.to_csv(path, index=False)


