import json
import os
import spacy
from nltk.corpus import wordnet as wn
import pandas as pd

# Load spacy model for sentence splitting and POS tagging
nlp = spacy.load("en_core_web_sm")

# Load your labeled examples (the 20 you prepared)
filename = "examples_for_labeling.json"
with open(filename, "r", encoding="utf-8") as f:
    examples = json.load(f)

results = []

for example in examples:
    cot = example["long_cot"]
    doc = nlp(cot)
    flagged_steps = []
    for i, sent in enumerate(doc.sents):
        tokens = [token.lemma_ for token in sent if token.pos_ in ("NOUN", "VERB")]
        unknown_tokens = [t for t in tokens if not wn.synsets(t)]
        if unknown_tokens:
            flagged_steps.append({
                "step_number": i + 1,
                "sentence": sent.text,
                "unknown_tokens": unknown_tokens
            })
    results.append({
        "input": example["question"],
        "cot": cot,
        "flagged_steps": json.dumps(flagged_steps, ensure_ascii=False),  # Convert list to JSON string
        "human_drift": example.get("drift", False)
    })

df = pd.DataFrame(results)
df.to_csv("flagged_cot_steps.csv", index=False)

print("✅ Ontology check complete. Results saved to flagged_cot_steps.csv")
