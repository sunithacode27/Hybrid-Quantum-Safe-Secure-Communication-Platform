import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("performance_results1.csv")

print(df)

plt.figure(figsize=(8,5))

plt.plot(
    df["Operation"],
    df["Time"],
    marker="o",
    linewidth=2
)

plt.title("Kyber Performance Analysis")
plt.xlabel("Operation")
plt.ylabel("Time (seconds)")

plt.grid(True)

plt.savefig("kyber_performance_line_graph.png")

plt.show()