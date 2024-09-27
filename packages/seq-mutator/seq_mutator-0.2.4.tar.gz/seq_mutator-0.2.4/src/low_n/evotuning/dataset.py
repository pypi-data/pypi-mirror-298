import torch
import pandas as pd
from Bio import SeqIO
from torch.utils.data import Dataset
from Levenshtein import distance


class BaseEvotuneDataset(Dataset):

    def __init__(self, df, transform=None):
        self.df = df
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):

        if torch.is_tensor(idx):
            idx = idx.tolist()

        sample = self.df.iloc[idx]

        if self.transform:
            sample = self.transform(sample)

        return sample


class EvotuneDataset(BaseEvotuneDataset):

    def __init__(self, csv_path, target_path, max_evalue,
                 transform=None, take=1.0, df=None):
        super().__init__(df, transform)

        self.df = pd.read_csv(csv_path).sample(frac=take)

        # check that the columns id, sequence and evalue are present
        assert 'id' in self.df.columns
        assert 'sequence' in self.df.columns
        assert 'evalue' in self.df.columns

        # filter by evalue
        self.df = self.df[self.df['evalue'] < max_evalue]

        # check that
        self.target_sequence = self._parse_fasta_sequence(target_path)

    def _parse_fasta_sequence(self, fasta_path):
        with open(fasta_path) as fasta_file:
            for record in SeqIO.parse(fasta_file, "fasta"):
                return str(record.seq)

    def _metric(self, sequence):
        levenshtein = distance(sequence, self.target_sequence)
        return levenshtein**4

    def _apply_metric(self):
        self.df['metric'] = self.df['sequence'].apply(self._metric)
        self.df['metric'] = self.df['metric'] / self.df['metric'].sum()

    def train_test_split(self, test_size=0.2):

        self._apply_metric()

        test_random = self.df.sample(frac=test_size / 2)
        test_metric = self.df.sample(frac=test_size / 2, weights='metric')

        # get the total test set
        test = pd.concat([test_random, test_metric])
        train = self.df.drop(test.index)

        test_dataset = BaseEvotuneDataset(test, self.transform)
        train_dataset = BaseEvotuneDataset(train, self.transform)
        return train_dataset, test_dataset













