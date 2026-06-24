# graphs/pqc_graph.py

import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file
data = pd.read_csv("Analysis/pqc_compare.csv")

# Convert speed words to values
speed_map = {
    "Slow": 1,
    "Medium": 2,
    "Fast": 3,
    "Very Fast": 4
}

values = [speed_map[x] for x in data["Speed"]]

# Graph
plt.figure(figsize=(9,5))
plt.bar(data["Algorithm"], values)

plt.title("Post-Quantum Cryptography Algorithm Comparison")
plt.xlabel("PQC Algorithms")
plt.ylabel("Relative Speed")

# Show values on bars
for i, v in enumerate(values):
    plt.text(i, v + 0.05, str(v), ha='center')

plt.tight_layout()
plt.savefig("results/pqc_graph.png")
plt.show()