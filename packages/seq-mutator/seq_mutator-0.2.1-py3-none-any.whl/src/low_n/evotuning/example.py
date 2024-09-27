from transformers import AutoTokenizer, EsmForMaskedLM
import torch

tokenizer = AutoTokenizer.from_pretrained("facebook/esm2_t6_8M_UR50D")
model = EsmForMaskedLM.from_pretrained("facebook/esm2_t6_8M_UR50D")

input_sequence = "The capital of France is <mask>."
label_sequence = "The capital of France is Paris."

padded_sequence = tokenizer([input_sequence, label_sequence], return_tensors="pt", padding=True)

# get the input and label tensors
attention_mask = padded_sequence["attention_mask"]
input_ids = padded_sequence["input_ids"]

inputs = input_ids[0]
labels = input_ids[1]

# mask labels of non-<mask> tokens
labels = torch.where(inputs == tokenizer.mask_token_id, labels, -100)

inputs = inputs.unsqueeze(0)
labels = labels.unsqueeze(0)
attention_mask = attention_mask[0].unsqueeze(0)

outputs = model(inputs, labels=labels, attention_mask=attention_mask, output_hidden_states=True)

# print infos about the input sequence
print("input shape: ", inputs.shape)

print("output keys: ", outputs.keys())
print("loss: ", outputs.loss)

# print hidden states
print("hidden states shape: ", outputs.hidden_states[-1].shape)


