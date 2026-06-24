import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("analysis/classical_compare.csv")

speed_map = {
    "Slow": 1,
    "Medium": 2,
    "Fast": 3,
    "Very Fast": 4
}

values = [speed_map[x] for x in data["Speed"]]

plt.bar(data["Algorithm"], values)
plt.title("Classical Algorithm Speed Comparison")
plt.xlabel("Algorithms")
plt.ylabel("Relative Speed")

plt.savefig("results/classical_graph.png")
plt.show()