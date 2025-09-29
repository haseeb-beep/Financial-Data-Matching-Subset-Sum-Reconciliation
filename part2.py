import pandas as pd
import itertools
import time

# Load cleaned data from Part 1
file_path = "cleaned_financial_data.xlsx"
transactions_df = pd.read_excel(file_path, sheet_name="Transactions")
targets_df = pd.read_excel(file_path, sheet_name="Targets")

# ---- Task 2.1: Exact Matching ----
print("=== Exact Matches ===")
exact_matches = []
for _, target in targets_df.iterrows():
    matches = transactions_df[transactions_df["Transaction Amount"] == target["Target Amount"]]
    for _, match in matches.iterrows():
        exact_matches.append({
            "Target ID": target["Target ID"],
            "Reference ID": target["Reference ID"],
            "Target Amount": target["Target Amount"],
            "Transaction ID": match["Transaction ID"],
            "Description": match["Description"],
            "Transaction Amount": match["Transaction Amount"]
        })

exact_matches_df = pd.DataFrame(exact_matches)
print(exact_matches_df if not exact_matches_df.empty else "No exact matches found.")

# ---- Task 2.2: Subset Sum Brute Force ----
def subset_sum_bruteforce(transactions, target_amount):
    """Find subsets of transactions that sum exactly to target_amount."""
    results = []
    n = len(transactions)
    # Check all possible combinations (1 to n elements)
    for r in range(1, n + 1):
        for combo in itertools.combinations(transactions, r):
            if abs(sum(combo) - target_amount) < 1e-9:  # Floating point tolerance
                results.append(combo)
    return results

print("\n=== Subset Sum Results ===")
subset_results = []
start_time = time.time()
for _, target in targets_df.iterrows():
    combos = subset_sum_bruteforce(transactions_df["Transaction Amount"].tolist(), target["Target Amount"])
    if combos:
        subset_results.append({
            "Target ID": target["Target ID"],
            "Target Amount": target["Target Amount"],
            "Combinations Found": combos
        })
end_time = time.time()

subset_results_df = pd.DataFrame(subset_results)
print(subset_results_df if not subset_results_df.empty else "No subset sums found.")

# ---- Task 2.3: Performance Analysis ----
execution_time = end_time - start_time
print(f"\nExecution time for brute force subset sum: {execution_time:.4f} seconds")

# Save results to Excel
with pd.ExcelWriter("part2_bruteforce_results.xlsx") as writer:
    exact_matches_df.to_excel(writer, index=False, sheet_name="Exact Matches")
    subset_results_df.to_excel(writer, index=False, sheet_name="Subset Sum Results")

print("\n✅ Results saved to 'part2_bruteforce_results.xlsx'")
