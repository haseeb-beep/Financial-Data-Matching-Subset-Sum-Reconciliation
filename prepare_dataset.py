import pandas as pd
import random

# File paths
ledger_path = "C:\\Users\\Haseeb Haider\\Desktop\\Financial-Data-Matching-and-Subset-Sum-Analysis-main (1)\\Customer_Ledger_Entries_FULL.xlsx"
bank_path = "C:\\Users\\Haseeb Haider\\Desktop\\Financial-Data-Matching-and-Subset-Sum-Analysis-main (1)\\KH_Bank.xlsx"

# Load ledger file (transactions)
ledger_df = pd.read_excel(ledger_path, sheet_name="Customer Ledger Entries")

# --- Extract Transactions ---
# Find amount column
ledger_amount_col = None
for col in ledger_df.columns:
    if "amount" in col.lower():
        ledger_amount_col = col
        break

# Description column
ledger_description_col = "Description" if "Description" in ledger_df.columns else ledger_df.columns[0]

# Keep only needed columns
ledger_clean = ledger_df[[ledger_amount_col, ledger_description_col]].rename(
    columns={ledger_amount_col: "Transaction Amount", ledger_description_col: "Description"}
)

# Drop missing
ledger_clean = ledger_clean.dropna(subset=["Transaction Amount"])

# Sample 15 transactions
transactions_sample = ledger_clean.sample(15, random_state=42).reset_index(drop=True)

# --- Create Targets (smart way) ---
targets = []

# 1. Exact matches (pick 3 transactions and reuse amounts as targets)
for i in range(3):
    amt = transactions_sample.loc[i, "Transaction Amount"]
    targets.append({"Target Amount": amt, "Reference ID": f"REF_EXACT_{i+1}"})

# 2. Subset matches (sum of 2–3 random transactions)
for i in range(3):
    rows = random.sample(range(len(transactions_sample)), 2)
    amt = transactions_sample.loc[rows[0], "Transaction Amount"] + transactions_sample.loc[rows[1], "Transaction Amount"]
    targets.append({"Target Amount": amt, "Reference ID": f"REF_SUBSET_{i+1}"})

# 3. Random unmatched targets
for i in range(4):
    amt = round(random.uniform(1000, 5000), 2)
    targets.append({"Target Amount": amt, "Reference ID": f"REF_UNMATCHED_{i+1}"})

# Convert to DataFrame
targets_df = pd.DataFrame(targets)

# --- Save Final Assignment Dataset ---
output_path = "financial_reconciliation_dataset.xlsx"
with pd.ExcelWriter(output_path) as writer:
    transactions_sample.to_excel(writer, index=False, sheet_name="Transactions")
    targets_df.to_excel(writer, index=False, sheet_name="Targets")

print(f"✅ Assignment dataset saved to {output_path}")
