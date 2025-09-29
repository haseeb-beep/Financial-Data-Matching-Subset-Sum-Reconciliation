# part5.py (fixed timing & bar chart visibility)
import pandas as pd
import time
import matplotlib.pyplot as plt
import random

# =========================
# Subset Sum Implementations
# =========================
def subset_sum_bruteforce(transactions, target):
    from itertools import combinations
    n = len(transactions)
    for r in range(1, n + 1):
        for combo in combinations(transactions, r):
            if abs(sum(combo) - target) < 1e-6:
                return True
    return False

def subset_sum_dp(transactions, target):
    """Memory-efficient set-based DP"""
    scale = 100
    trans_scaled = [int(round(x * scale)) for x in transactions]
    target_scaled = int(round(target * scale))

    reachable = {0}
    for val in trans_scaled:
        new_reachable = set(reachable)
        for s in reachable:
            if s + val == target_scaled:
                return True
            if s + val < target_scaled:
                new_reachable.add(s + val)
        reachable = new_reachable

    return target_scaled in reachable


# =========================
# Benchmarking Function
# =========================
def timed_run(func, *args, repeats=5):
    """Run function multiple times and return average execution time (high precision)."""
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        func(*args)
        end = time.perf_counter()
        times.append(end - start)
    return sum(times) / repeats

def benchmark_by_size(transactions, targets, sizes=[50, 100, 200, 400]):
    results = []
    for size in sizes:
        sample_trans = random.sample(transactions, min(len(transactions), size))
        target = random.choice(targets)

        # Brute Force timing (only on small sizes)
        if size <= 100:  
            brute_time = timed_run(subset_sum_bruteforce, sample_trans, target)
        else:
            brute_time = None  # skip brute force for large sizes

        # DP timing
        dp_time = timed_run(subset_sum_dp, sample_trans, target)

        results.append({"Size": size, "BruteForce": brute_time, "DP": dp_time})
    return pd.DataFrame(results)


# =========================
# Main Script
# =========================
if __name__ == "__main__":
    file_path = "cleaned_financial_data.xlsx"
    transactions_df = pd.read_excel(file_path, sheet_name="Transactions")
    targets_df = pd.read_excel(file_path, sheet_name="Targets")

    transactions = transactions_df["Transaction Amount"].tolist()
    targets = targets_df["Target Amount"].tolist()

    # Run benchmark
    results_df = benchmark_by_size(transactions, targets, sizes=[50, 100, 200, 400])
    print("\n=== Benchmarking Results ===")
    print(results_df)

    # Save results
    results_df.to_excel("part5_performance_results.xlsx", index=False)
    print("\n✅ Part 5 results saved to 'part5_performance_results.xlsx'")

    # =========================
    # Visualization
    # =========================
    plt.figure(figsize=(8, 5))
    plt.plot(results_df["Size"], results_df["DP"], marker="o", label="DP (Set-based)")
    if results_df["BruteForce"].notna().any():
        plt.plot(results_df["Size"], results_df["BruteForce"], marker="s", label="Brute Force")
    plt.xlabel("Dataset Size (#Transactions)")
    plt.ylabel("Execution Time (s)")
    plt.title("Subset Sum Performance vs Dataset Size")
    plt.legend()
    plt.grid(True)
    plt.savefig("part5_performance_plot.png")
    plt.show()

    # Bar chart comparison (fixed dataset, size=100)
    fixed_size_df = results_df[results_df["Size"] == 100]
    if not fixed_size_df.empty:
        fixed = fixed_size_df.iloc[0]
        plt.figure(figsize=(6, 4))
        bars = {
            "BruteForce": max(fixed["BruteForce"], 1e-6),  # avoid disappearing
            "DP": max(fixed["DP"], 1e-6)
        }
        plt.bar(bars.keys(), bars.values(), color=["red", "green"])
        plt.ylabel("Execution Time (s)")
        plt.title("Brute Force vs DP on 100 Transactions")
        plt.savefig("part5_bar_chart.png")
        plt.show()
        print("✅ Comparison bar chart saved as 'part5_bar_chart.png'")
