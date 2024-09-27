import torch
from transformers import AutoTokenizer, EsmForMaskedLM
from tqdm import tqdm
import numpy as np


class ZeroShotModel:

    def __init__(self, esm_model, tokenizer, cache_dir):
        """
        :param esm_model: str
            The ESM model to use. It should be a valid identifier for a huggingface ESM2 model or
            a path to a ESM2 Hugging Face checkpoint.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.esm_model = EsmForMaskedLM.from_pretrained(esm_model, cache_dir=cache_dir).to(self.device)
        self.esm_model.eval()
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer, cache_dir=cache_dir)

        amino_acids = {'P': 0,'G': 1,'A': 2,'V': 3,'L': 4,'I': 5,'M': 6,'F': 7,'Y': 8,'W': 9,'C': 10,'S': 11,'T': 12,'N': 13,'Q': 14,'D': 15,'E': 16,'K':17,'R': 18,'H': 19}
        self.amino_acid_token_map = {residue: self.tokenizer.convert_tokens_to_ids(residue) for residue in amino_acids.keys()}

    def predict_point_mutations(self, sequence, positions):
        """
        Predict the label for a given sequence.

        :param sequence: str
            The sequence for which to predict the mutations.
        :param positions: [int]
            The positions for which alternative residues should be scored. First amino acid has position 1, not 0!!!
        :return: Tensor
            The predicted label.
        """
        input = self.tokenizer(sequence, return_tensors="pt", padding=False).to(self.device)
        all_residue_scores = []
        for index in tqdm(positions):
            input_masked = input.input_ids.clone()
            input_masked[0,index] = self.tokenizer.mask_token_id
            with torch.no_grad():
                logits = self.esm_model(input_masked.to(self.device)).logits
            residue_logits = torch.log_softmax(logits[0,index,:], -1)
            residue_logits -= float(residue_logits[self.amino_acid_token_map[sequence[index-1]]])
            residue_scores = {residue: float(residue_logits[self.amino_acid_token_map[residue]]) for residue in self.amino_acid_token_map.keys()}
            all_residue_scores.append(residue_scores)
        return all_residue_scores
    

if __name__ == "__main__":
    model = ZeroShotModel("facebook/esm2_t6_8M_UR50D","facebook/esm2_t6_8M_UR50D")
    print(model.predict_point_mutations("MASSQLEFNVERKQPELLGPAEPTPYELKELSDIDDQDGVRLFLTAIFIYPPPTKTSMPTRKTDPASDIRRGLSKAMVYYYPFAGRIREGPNRKLSVDCTGEGIVFCEADADIRLDGLGDVEVLRPPYPFIDKMTLGEGSAILGAPLVYVQVTRFACGGFIITGRFNHVMADAPGFTMFMKAAADLARGATVPMPLPVWERERYRSRVPPRVTFAHHEYMHVDDPPPRPTSEPWSLHSAFFTKADVATLRAQLPADLRKAATSFDIITACMWRCRVSALQYGPDEVVRLIVAVNSRTKFDPPLTGYYGNGLMLPAAVTEAGKLVGSDLGYAVELVREAKGKVTEEYVRSAADFLVLNGRVHFVVSNTFLVSDLRRLIDLANMDWGWGKAVSGGPVDVGENVISFLATSKNSAGEEGAVVPFCLPDSALGRFTSEVKKLVCFRPLENAAASNPDHGYMSRM",[2,3]))
