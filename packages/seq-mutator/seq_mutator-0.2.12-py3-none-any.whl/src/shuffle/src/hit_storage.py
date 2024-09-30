import pandas as pd
import os

from .restriction_enzyme_hit import RestrictionEnzymeHit


class HitStorage:

    def __init__(self, csv_path):
        self.csv_path = csv_path

    def path_exists(self):
        return os.path.exists(self.csv_path)

    def load_hits(self):
        """
        Load restriction enzyme hits from the input csvs

        :return: list of RestrictionEnzymeHit objects
        """
        df = pd.read_csv(self.csv_path)
        return [RestrictionEnzymeHit(**r) for r in df.to_dict(orient="records")]

    def save_hits(self, hits):
        df = pd.DataFrame([h.to_dict() for h in hits])
        # check that "start" is in the first column
        df = df[["start"] + [col for col in df.columns if col != "start"]]
        df.to_csv(self.csv_path, index=False)




