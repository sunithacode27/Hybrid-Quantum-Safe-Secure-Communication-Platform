import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file
data = pd.read_csv("results/performance_results.csv")

# Bar Graph
plt.figure(figsize=(8,5))
plt.bar(data["Algorithm"], data["Execution Time (seconds)"])

plt.title("Classical vs PQC vs Hybrid Performance")
plt.xlabel("Algorithms")
plt.ylabel("Key Generation Time (seconds)")

# show values on bars
for i, v in enumerate(data["Execution Time (seconds)"]):
    plt.text(i, v + 0.0001, str(round(v,6)), ha='center')

plt.tight_layout()
plt.savefig("results/graph.png")
plt.show()