from transformers import AutoTokenizer, EsmForMaskedLM
from peft import get_peft_model, LoraConfig, TaskType
import torch
import pandas as pd
from sklearn.linear_model import RidgeCV, Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from scipy.stats import ttest_rel
import pickle
import numpy as np
from tqdm import tqdm


class Topmodel:

    def __init__(self, esm_model, topmodel_path, tokenizer, cache_dir, load=False, sparse_refit=False, pval_cutoff=0.01, lora=False):
        """
        :param topmodel_path: str
            Path to store the top model.
        :param esm_model: str
            The ESM model to use. It should be a valid Identifiert for a huggingface ESM2 model or
            a path to a ESM2 Hugging Face checkpoint.
        """

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.esm_model = EsmForMaskedLM.from_pretrained(
            esm_model, cache_dir=cache_dir).to(self.device)

        if lora:
            print("Using LORA")
            peft_config = LoraConfig(
                task_type=TaskType.TOKEN_CLS,
                inference_mode=False,
                r=2,
                lora_alpha=1,
                target_modules=["query", "key", "value"],
                bias="none",
                lora_dropout=0.2
            )
            self.esm_model = get_peft_model(self.esm_model, peft_config)

        self.esm_model.eval()
        self.tokenizer = AutoTokenizer.from_pretrained(
            tokenizer, cache_dir=cache_dir, clean_up_tokenization_spaces=True)
        self.topmodel_path = topmodel_path
        self.topmodel = make_pipeline(StandardScaler(), RidgeCV(
            alphas=np.logspace(-6, 6, 1000), store_cv_results=True))
        self.sparse_refit = sparse_refit
        self.pval_cutoff = pval_cutoff

        if load:
            self.topmodel = pickle.load(open(topmodel_path, "rb"))

    def train(self, data_csv):
        """
        Train the top model.

        :param data_csv: str
            Path to a CSV file containing sequences to train on.
        """
        df = pd.read_csv(data_csv)

        # assert csv contains the right columns
        assert 'label' in df.columns, "The csv file must contain a 'label' column."
        assert 'sequence' in df.columns, "The csv file must contain a 'sequence' column."

        data = df["sequence"].to_list()

        X = []
        for sequence in tqdm(data):
            X.append(self._get_hidden_states(sequence))
        X = np.array(X)
        y = df["label"].values
        self.topmodel.fit(X, y)

        if self.sparse_refit:
            best_alpha_idx = np.argwhere(
                self.topmodel[1].alphas == self.topmodel[1].alpha_).reshape(-1)[0]

            sparse_alpha_idx = -1
            for i in range(best_alpha_idx + 1, len(self.topmodel[1].alphas)):
                pval = ttest_rel(self.topmodel[1].cv_results_[
                                 :, best_alpha_idx], self.topmodel[1].cv_results_[:, i]).pvalue
                print(i)
                print(pval)

                if pval < self.pval_cutoff:
                    sparse_alpha_idx = i - 1
                    break

            model_sparse = make_pipeline(StandardScaler(), Ridge(
                alpha=self.topmodel[1].alphas[sparse_alpha_idx]))
            model_sparse.fit(X, y)

            model_sparse[1].best_alpha = self.topmodel[1].alpha_
            model_sparse[1].sparse_alpha = self.topmodel[1].alphas[sparse_alpha_idx]
            model_sparse[1].alpha_ = self.topmodel[1].alphas[sparse_alpha_idx]
            model_sparse[1].alphas = self.topmodel[1].alphas
            self.topmodel = model_sparse

        # print score
        score = self.topmodel.score(X, y)
        print("Score: {:.2E}".format(score))
        print("Alpha: {:.2E}".format(self.topmodel[1].alpha_))

    def save(self):
        # store the model
        pickle.dump(self.topmodel, open(self.topmodel_path, "wb"))

    def _get_hidden_states(self, x):
        inputs = self.tokenizer(x, return_tensors="pt", padding=True).to(self.device)
        if len(inputs["input_ids"]) > 1:
            input_lens = [len(sequence) for sequence in x]
            with torch.no_grad():
                esm_output = self.esm_model(**inputs, output_hidden_states=True)
            output = []
            for i, tokens_len in enumerate(input_lens):
                output.append(
                    esm_output.hidden_states[-1][i, 1: tokens_len + 1].mean(dim=0).detach().cpu().numpy())
            return np.array(output)
        else:
            with torch.no_grad():
                esm_output = self.esm_model(**inputs, output_hidden_states=True)
            return esm_output.hidden_states[-1][0, 1:-1, :].mean(dim=0).detach().cpu().numpy()

    def predict(self, x):
        """
        Predict the label for a given sequence.

        :param x: str | [str]
            The sequence(s) to predict the label for.
        :return: float
            The predicted label.
        """
        last_hidden_layer = self._get_hidden_states(x)
        if len(last_hidden_layer.shape) == 1:
            last_hidden_layer = last_hidden_layer.reshape(1, -1)
        return self.topmodel.predict(last_hidden_layer)


if __name__ == "__main__":
    topmodel = Topmodel("facebook/esm2_t6_8M_UR50D", "topmodel.pkl")
    topmodel.train("data.csv")
    topmodel.save()
    data = ["MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG",
            "MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG"]
    print(topmodel.predict(data))
    data = "MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG"
    print(topmodel.predict(data))









