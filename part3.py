# part3.py
import os
import time
import pandas as pd

# --------------------------
# Paths / I/O
# --------------------------
BASE_DIR = r"C:\Users\HP\Desktop\code-gen-assignment"   # <- change if needed
os.makedirs(BASE_DIR, exist_ok=True)

INPUT_FILE = os.path.join(BASE_DIR, "cleaned_financial_data.xlsx")
OUTPUT_FILE = os.path.join(BASE_DIR, "part3_ml_results.xlsx")

# --------------------------
# Load data (from Part 1)
# --------------------------
transactions_df = pd.read_excel(INPUT_FILE, sheet_name="Transactions")
targets_df = pd.read_excel(INPUT_FILE, sheet_name="Targets")

# Make sure required columns exist; if IDs are missing (e.g., you ran Part 3 first), create them.
if "Transaction ID" not in transactions_df.columns:
    transactions_df["Transaction ID"] = [f"T{i+1}" for i in range(len(transactions_df))]
if "Target ID" not in targets_df.columns:
    targets_df["Target ID"] = [f"G{i+1}" for i in range(len(targets_df))]

# Ensure numeric types
transactions_df["Transaction Amount"] = pd.to_numeric(transactions_df["Transaction Amount"], errors="coerce")
targets_df["Target Amount"] = pd.to_numeric(targets_df["Target Amount"], errors="coerce")

transactions_df = transactions_df.dropna(subset=["Transaction Amount"]).reset_index(drop=True)
targets_df = targets_df.dropna(subset=["Target Amount"]).reset_index(drop=True)

# --------------------------
# Task 3.1: Feature Engineering
# --------------------------
pairs = []
for _, t in transactions_df.iterrows():
    for _, g in targets_df.iterrows():
        diff = abs(t["Transaction Amount"] - g["Target Amount"])
        pairs.append({
            "Transaction ID": t["Transaction ID"],
            "Target ID": g["Target ID"],
            "Transaction Amount": float(t["Transaction Amount"]),
            "Target Amount": float(g["Target Amount"]),
            "Amount Difference": float(diff),
            "Is_Exact_Match": 1 if diff < 1e-9 else 0
        })

pairs_df = pd.DataFrame(pairs)
print("=== Feature Engineered Dataset (first 10 rows) ===")
print(pairs_df.head(10))

# --------------------------
# Task 3.2: Optimized Subset Sum (works with negatives + gives one witness subset)
# --------------------------
def subset_sum_dp_witness(values, target, ids=None, scale=100):
    """
    Set/Dict-based DP that supports negative values and reconstructs one solution.

    values: list of floats (transaction amounts)
    target: float (target amount)
    ids:    parallel list of identifiers (same length as values), optional
    scale:  multiply by this factor and round to work in integers (100 = cents)

    Returns: (exists: bool, chosen_indices: list[int])
    """
    if ids is None:
        ids = list(range(len(values)))

    # Scale to integers to avoid floating errors
    vals = [int(round(v * scale)) for v in values]
    tgt = int(round(target * scale))

    # reachable: dict[int sum] -> (prev_sum, index_used)
    # Start with sum 0 reachable, with no predecessor
    reachable = {0: None}

    for i, val in enumerate(vals):
        # Take a snapshot of current sums to extend
        current_sums = list(reachable.keys())
        for s in current_sums:
            new_s = s + val
            if new_s not in reachable:
                reachable[new_s] = (s, i)  # we can reach new_s by using value at index i
        # Optional: early exit if we already reached target
        if tgt in reachable:
            break

    if tgt not in reachable:
        return False, []

    # Reconstruct indices by walking predecessors
    chosen_indices = []
    cur = tgt
    while cur != 0:
        prev_sum, idx = reachable[cur]
        chosen_indices.append(idx)
        cur = prev_sum
    chosen_indices.reverse()
    return True, chosen_indices

# Run DP for each target and collect a readable report
transactions = transactions_df["Transaction Amount"].tolist()
transaction_ids = transactions_df["Transaction ID"].tolist()
descriptions = transactions_df["Description"].tolist() if "Description" in transactions_df.columns else [""] * len(transactions)

dp_rows = []
start_t = time.time()
for _, g in targets_df.iterrows():
    exists, idxs = subset_sum_dp_witness(transactions, g["Target Amount"], ids=transaction_ids, scale=100)

    if exists:
        picked_ids = [transaction_ids[i] for i in idxs]
        picked_amts = [transactions[i] for i in idxs]
        picked_desc = [descriptions[i] for i in idxs]
        dp_rows.append({
            "Target ID": g["Target ID"],
            "Target Amount": float(g["Target Amount"]),
            "Subset Exists": True,
            "Num Items": len(idxs),
            "Picked Transaction IDs": ", ".join(picked_ids),
            "Picked Amounts": ", ".join(f"{a:.2f}" for a in picked_amts),
            "Picked Descriptions": " | ".join(picked_desc),
            "Sum(chosen)": round(sum(picked_amts), 2)
        })
    else:
        dp_rows.append({
            "Target ID": g["Target ID"],
            "Target Amount": float(g["Target Amount"]),
            "Subset Exists": False,
            "Num Items": 0,
            "Picked Transaction IDs": "",
            "Picked Amounts": "",
            "Picked Descriptions": "",
            "Sum(chosen)": 0.0
        })
end_t = time.time()

dp_results_df = pd.DataFrame(dp_rows)
print("\n=== Dynamic Programming Subset Sum Results (with witness) ===")
print(dp_results_df.head(10))
print(f"\nExecution time (DP subset sum): {end_t - start_t:.4f} seconds")

# --------------------------
# Task 3.3: (Optional) Simple ML Model
# --------------------------
ml_report_text = "scikit-learn not installed; skipping ML model."
try:
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import classification_report

    X = pairs_df[["Transaction Amount", "Target Amount", "Amount Difference"]]
    y = pairs_df["Is_Exact_Match"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    ml_report_text = classification_report(y_test, y_pred)
    print("\n=== Logistic Regression Model Performance ===")
    print(ml_report_text)
except Exception as e:
    print(f"\n⚠️ Skipping ML model: {e}")

# --------------------------
# Save outputs
# --------------------------
with pd.ExcelWriter(OUTPUT_FILE) as writer:
    pairs_df.to_excel(writer, index=False, sheet_name="Feature_Engineering")
    dp_results_df.to_excel(writer, index=False, sheet_name="DP_SubsetSum")
    # Save ML report as a one-cell sheet for convenience
    pd.DataFrame({"Report": [ml_report_text]}).to_excel(writer, index=False, sheet_name="ML_Report")

print(f"\n✅ Part 3 results saved to: {OUTPUT_FILE}")
