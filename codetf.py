from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

checkpoint = "Salesforce/codet5p-770m"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint,
                                              torch_dtype=torch.float16,
                                              trust_remote_code=True).to(device)

print(model.get_memory_footprint())

python_function = "Write python code for summing a list of lists"

encoding = tokenizer(python_function, return_tensors="pt").to(device)
encoding["decoder_input_ids"] = encoding["input_ids"].clone()
outputs = model.generate(**encoding, max_length=750)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))