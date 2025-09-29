import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
from itertools import chain, combinations
import random

# --- Subset Sum Algorithms ---
def subset_sum_bruteforce(transactions, target):
    for subset in chain.from_iterable(combinations(transactions, r) for r in range(len(transactions) + 1)):
        if abs(sum(subset) - target) < 1e-9:
            return True
    return False

def subset_sum_dp(transactions, target):
    n = len(transactions)
    target = round(target, 2)
    scale = 100
    trans_scaled = [int(round(x * scale)) for x in transactions]
    target_scaled = int(round(target * scale))

    if target_scaled < 0 or n == 0:
        return False

    dp = [[False] * (target_scaled + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = True

    for i in range(1, n + 1):
        for j in range(1, target_scaled + 1):
            if trans_scaled[i - 1] <= j:
                dp[i][j] = dp[i - 1][j] or dp[i - 1][j - trans_scaled[i - 1]]
            else:
                dp[i][j] = dp[i - 1][j]

    return dp[n][target_scaled]

# --- Performance Testing ---
dataset_sizes = [10, 15, 20, 22, 24]  # keep small for brute force
repeats = 3
target = 100  # fixed target to search for

brute_times = []
dp_times = []

for size in dataset_sizes:
    times_b = []
    times_d = []

    for _ in range(repeats):
        # Generate random positive integers (to enlarge complexity)
        expanded_transactions = [random.randint(1, 50) for _ in range(size)]

        # Brute Force
        start = time.time()
        subset_sum_bruteforce(expanded_transactions, target)
        times_b.append(time.time() - start)

        # DP
        start = time.time()
        subset_sum_dp(expanded_transactions, target)
        times_d.append(time.time() - start)

    brute_times.append(np.mean(times_b))
    dp_times.append(np.mean(times_d))

# --- Save results ---
results = pd.DataFrame({
    "Dataset Size": dataset_sizes,
    "Brute Force Time (s)": brute_times,
    "DP Time (s)": dp_times
})
results.to_excel("part4_evaluation_results.xlsx", index=False)

# --- Plot ---
plt.plot(dataset_sizes, brute_times, marker='o', label="Brute Force")
plt.plot(dataset_sizes, dp_times, marker='o', label="Dynamic Programming")
plt.xlabel("Dataset Size (#transactions)")
plt.ylabel("Average Runtime (seconds)")
plt.title("Algorithm Performance Comparison")
plt.legend()
plt.grid(True)
plt.savefig("part4_performance_plot.png")
plt.show()

print("\n✅ Part 4 results saved to 'part4_evaluation_results.xlsx' and 'part4_performance_plot.png'")
