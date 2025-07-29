import json
import os
import spacy
from nltk.corpus import wordnet as wn
import pandas as pd

# Step 1: Load the SpaCy English model for sentence splitting and POS tagging
nlp = spacy.load("en_core_web_sm")

# Step 2: Load your labeled examples from a JSON file
filename = "examples_for_labeling.json"
with open(filename, "r", encoding="utf-8") as f:
    examples = json.load(f)

results = []

# Step 3: Process each example
for example in examples:
    cot = example["long_cot"]  
    doc = nlp(cot)  
    flagged_steps = []

    # Step 4: Iterate through each sentence in the CoT
    for i, sent in enumerate(doc.sents):
        # Extract lemmas of tokens that are either nouns or verbs
        tokens = [token.lemma_ for token in sent if token.pos_ in ("NOUN", "VERB")]

        # Step 5: Check which tokens are unknown (not found in WordNet)
        unknown_tokens = [t for t in tokens if not wn.synsets(t)]

        # Step 6: If there are unknown tokens, add info about this sentence to flagged steps
        if unknown_tokens:
            flagged_steps.append({
                "step_number": i + 1,        
                "sentence": sent.text,        
                "unknown_tokens": unknown_tokens 
            })

    # Step 7: Append results for this example including question, CoT, and flagged steps
    results.append({
        "input": example["question"],
        "cot": cot,
        "flagged_steps": json.dumps(flagged_steps, ensure_ascii=False),  
        "human_drift": example.get("drift", False)  
    })

# Step 8: Convert results list to a DataFrame and save as CSV for analysis
df = pd.DataFrame(results)
df.to_csv("flagged_cot_steps.csv", index=False)

print("Ontology check complete. Results saved to flagged_cot_steps.csv")
