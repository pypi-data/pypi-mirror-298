import torch
import random


class TokenizeAndMask:

    def __init__(self, tokenizer, max_length):
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __call__(self, sample):
        # get the sequence from the sample
        sequence = sample['sequence']

        # encode the sequence with the tokenizer. padd and truncate the sequece to the max length specified
        encoding = self.tokenizer(sequence, return_tensors='pt', padding='max_length',
                                  truncation=True, max_length=self.max_length)

        # create a copy of the input_ids tensor to use as labels
        labels = encoding.input_ids.clone()

        # create a random mask token index in 15 % of the cases
        length = min(len(sequence), self.max_length)
        mask_idx = random.sample(range(1, length - 1), int(length * 0.15))

        # replace the mask token index with the mask token id
        encoding.input_ids[0, mask_idx] = self.tokenizer.mask_token_id

        # replace all the tokens that are not the mask token with -100
        labels = torch.where(encoding.input_ids == self.tokenizer.mask_token_id, labels, -100)

        # squeeze the tensor
        encoding["input_ids"] = encoding["input_ids"].squeeze()
        encoding["attention_mask"] = encoding["attention_mask"].squeeze()
        labels = labels.squeeze()

        encoding["labels"] = labels
        return encoding



