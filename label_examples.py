import json

filename = "DeltaBench/data/Deltabench_v1.jsonl"
output_filename = "examples_for_labeling.json"

# Step 1: Load the full dataset
dataset = []
with open(filename, "r", encoding="utf-8") as f:
    for line in f:
        dataset.append(json.loads(line.strip()))

# Step 2: Grab the first 10 examples
selected_examples = dataset[:10]

# Step 3: Export to JSON
with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(selected_examples, f, indent=2)

print("Exported 10 examples to 'examples_for_labeling.json'")
