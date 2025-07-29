import json
import os

# Step 1: Locate the correct file
filename = os.path.join("DeltaBench", "data", "Deltabench_v1.jsonl")

# Step 2: Read each line (each is a JSON object)
dataset = []
with open(filename, "r", encoding="utf-8") as f:
    for line in f:
        dataset.append(json.loads(line.strip()))

# Step 3: Print the first example
print("🔍 First Example:")
print(json.dumps(dataset[0], indent=2))
