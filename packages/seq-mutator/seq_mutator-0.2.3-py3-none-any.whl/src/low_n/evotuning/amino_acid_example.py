from transformers import AutoTokenizer, EsmForMaskedLM
import torch
import random

tokenizer = AutoTokenizer.from_pretrained("facebook/esm2_t6_8M_UR50D")
model = EsmForMaskedLM.from_pretrained("facebook/esm2_t6_8M_UR50D")


input_sequence = "MERPWGAADGLSRWPHGLGLLLLLQLLPPSTLSQDRLDAPPPPAAPLPRWSGPIGVSWGLRAAAAGGAFPRGGRWRRSAPGEDEECGRVRDFVAKLANNTHQHVFDDLRGSVSLSWVGDSTGVILVLTTFHVPLVIMTFGQSKLYRSEDYGKNFKDITDLINNTFIRTEFGMAIGPENSGKVVLTAEVSGGSRGGRIFRSSDFAKNFVQTDLPFHPLTQMMYSPQNSDYLLALSTENGLWVSKNFGGKWEEIHKAVCLAKWGSDNTIFFTTYANGSCKADLGALELWRTSDLGKSFKTIGVKIYSFGLGGRFLFASVMADKDTTRRIHVSTDQGDTWSMAQLPSVGQEQFYSILAANDDMVFMHVDEPGDTGFGTIFTSDDRGIVYSKSLDRHLYTTTGGETDFTNVTSLRGVYITSVLSEDNSIQTMITFDQGGRWTHLRKPENSECDATAKNKNECSLHIHASYSISQKLNVPMAPLSEPNAVGIVIAHGSVGDAISVMVPDVYISDDGGYSWTKMLEGPHYYTILDSGGIIVAIEHSSRPINVIKFSTDEGQCWQTYTFTRDPIYFTGLASEPGARSMNISIWGFTESFLTSQWVSYTIDFKDILERNCEEKDYTIWLAHSTDPEDYEDGCILGYKEQFLRLRKSSVCQNGRDYVVTKQPSICLCSLEDFLCDFGYYRPENDSKCVEQPELKGHDLEFCLYGREEHLTTNGYRKIPGDKCQGGVNPVREVKDLKKKCTSNFLSPEKQNSKSNSVPIILAIVGLMLVTVVAGVLIVKKYVCGGRFLVHRYSVLQQHAEANGVDGVDALDTASHTNKSGYHDDSDEDLLE"


inputs = tokenizer(input_sequence, return_tensors="pt", padding=True)
labels = inputs.input_ids.clone()

# mask random amino acids
mask_index = random.sample(range(1, len(input_sequence)), int(len(input_sequence) * 0.15))
inputs.input_ids[0, mask_index] = tokenizer.mask_token_id

# mask labels of non-<mask> tokens
labels = torch.where(inputs.input_ids == tokenizer.mask_token_id, labels, -100)

# calc output
outputs = model(**inputs, labels=labels, output_hidden_states=True)

# print infos about the input sequence
# print(mask_index, inputs, labels, tokenizer.mask_token_id)
print("labels shape: ", labels.shape)

print("output keys: ", outputs.keys())
print("loss: ", outputs.loss)

# print hidden states
print("hidden states shape: ", outputs.hidden_states[-1].shape)




