import torch
print(torch.cuda.is_available())
import wandb
import random
import numpy as np

from datasets import load_dataset
from transformers import AutoTokenizer,AutoModelForMaskedLM, pipeline
from transformers import DataCollatorForLanguageModeling, Trainer, TrainingArguments
import math


seed_val = 42
random.seed(seed_val)
np.random.seed(seed_val)
torch.manual_seed(seed_val)
torch.cuda.manual_seed_all(seed_val)

wandb.init(project="", name="")


train_file_path = ""
val_file_path = ""


datasets = load_dataset("text", data_files={"train": train_file_path, "validation": val_file_path}, sample_by="paragraph")
print(datasets["train"][10])



#model_checkpoint = "deepset/gbert-large"
model_checkpoint = "" #trained model from a previous dataset
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint, use_fast=True)


def tokenize_function(examples):
    return tokenizer(examples["text"], max_length=256, truncation=True, padding='max_length')

print("Beginning text tokenization")

tokenized_datasets = datasets.map(tokenize_function, batched=True, num_proc=4, remove_columns=["text"])

block_size = 256

def group_texts(examples):
    # Concatenate all texts.
    concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
    total_length = len(concatenated_examples[list(examples.keys())[0]])
    # We drop the small remainder, we could add padding if the model supported it instead of this drop, you can
        # customize this part to your needs.
    total_length = (total_length // block_size) * block_size
    # Split by chunks of max_len.
    result = {
        k: [t[i : i + block_size] for i in range(0, total_length, block_size)]
        for k, t in concatenated_examples.items()
    }
    result["labels"] = result["input_ids"].copy()
    return result

print("Beginning text grouping")
lm_datasets = tokenized_datasets.map(
    group_texts,
    batched=True,
    batch_size=1000,
    num_proc=4,
)


print(tokenizer.decode(lm_datasets["train"][1]["input_ids"]))
print("\n\n")
print(tokenizer.decode(lm_datasets["train"][2]["input_ids"]))
print("\n\n")
print(tokenizer.decode(lm_datasets["train"][30]["input_ids"]))
print("\n\n")
print(tokenizer.decode(lm_datasets["train"][41]["input_ids"]))
print("\n\n")
print(tokenizer.decode(lm_datasets["train"][52]["input_ids"]))
print("\n\n")
model = AutoModelForMaskedLM.from_pretrained(model_checkpoint)

model_name = model_checkpoint.split("/")[-1]
training_args = TrainingArguments(
    f"{model_name}",
    evaluation_strategy = "epoch",
    learning_rate=3e-5,
    weight_decay=1e-3,
    save_steps=500,
    num_train_epochs=5,
    push_to_hub=False,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=8,
)

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm_probability=0.15)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=lm_datasets["train"],
    eval_dataset=lm_datasets["validation"],
    data_collator=data_collator,
)

trainer.train()
model.save_pretrained("")
tokenizer.save_pretrained("")

eval_results = trainer.evaluate()
print(f"Perplexity: {math.exp(eval_results['eval_loss']):.2f}")



model =AutoModelForMaskedLM.from_pretrained("./cardioNET/models/gbert_large_ggponc_bronco_dgk_cardio_mieDEEP2")
tokenizer =AutoTokenizer.from_pretrained("./cardioNET/models/gbert_large_ggponc_bronco_dgk_cardio_mieDEEP2")
mlm_pipeline = pipeline("fill-mask", model=model, tokenizer=tokenizer, top_k=5)


sentence = (
    "In der Kardiologie, [MASK] Pectoris ist eine Krankenheit")
result = mlm_pipeline(sentence)

print(f"{sentence=}")
print("\nresults:")
for r in result:
    print(f"{r['token_str']}: {r['score']}")

sentence = (
    "Die [MASK] sollte als erstes bildgebendes Verfahren zur Detektion von Lebermetastasen eingesetzt werden."
)
result = mlm_pipeline(sentence)

print(f"{sentence=}")
print("\nresults:")
for r in result:
    print(f"{r['token_str']}: {r['score']}")

sentence = (
    "Es erfolgte eine multiple RV-Biopsieentnahme. "
    "Der postinterventionelle Verlauf gestaltete sich komplikationslos.  "
    "Am Folgetag wurde ein Perikarderguss echokardiographisch ausgeschlossen. "
    "In der histopathologischen Aufarbeitung der RV-Biopsie konnte eine Vaskulitis und eine Speichererkrankung ausgeschlossen werden, "
    "typische Zeichen einer hypertrophen [MASK] waren nicht präsent.  Es fand sich in einem Biopsiepartikel jedoch eine deutlich erhöhte Zahl Adipozyten, "
    "die in Gesamtschau und in Kenntnis des MRT-Befundes bei hypertrabekularisiertem RV und dort leichtgradig eingeschränkter Pumpfunktion differenzialdiagnostisch an eine ARVC denken lassen."
    "Wir haben deshalb u.a. ambulanten Termin zur Anbindung an unsere Spezialambulanz für Kardiomyopathie vereinbart."
)

result = mlm_pipeline(sentence)

print(f"{sentence=}")
print("\nresults:")
for r in result:
    print(f"{r['token_str']}: {r['score']}")
