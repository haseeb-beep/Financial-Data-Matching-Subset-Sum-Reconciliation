import pandas as pd

# Load the prepared dataset
file_path = "financial_reconciliation_dataset.xlsx"

transactions_df = pd.read_excel(file_path, sheet_name="Transactions")
targets_df = pd.read_excel(file_path, sheet_name="Targets")

# ---- Task 1.1: Examine Data ----
print("=== Transactions Sheet (First 5 rows) ===")
print(transactions_df.head())
print("\n=== Targets Sheet (First 5 rows) ===")
print(targets_df.head())

print("\nTransactions Info:")
print(transactions_df.info())
print("\nTargets Info:")
print(targets_df.info())

# ---- Task 1.2: Data Preparation ----

# Handle missing values
transactions_df = transactions_df.dropna(subset=["Transaction Amount"])
targets_df = targets_df.dropna(subset=["Target Amount"])

# Standardize amounts (remove currency symbols, ensure float)
transactions_df["Transaction Amount"] = transactions_df["Transaction Amount"].replace('[\$,]', '', regex=True).astype(float)
targets_df["Target Amount"] = targets_df["Target Amount"].replace('[\$,]', '', regex=True).astype(float)

# Create unique identifiers for tracking matches
transactions_df["Transaction ID"] = ["T" + str(i+1) for i in range(len(transactions_df))]
targets_df["Target ID"] = ["G" + str(i+1) for i in range(len(targets_df))]

print("\n=== Transactions After Cleaning ===")
print(transactions_df.head())

print("\n=== Targets After Cleaning ===")
print(targets_df.head())

# Save cleaned data for Part 2
with pd.ExcelWriter("cleaned_financial_data.xlsx") as writer:
    transactions_df.to_excel(writer, index=False, sheet_name="Transactions")
    targets_df.to_excel(writer, index=False, sheet_name="Targets")

print("\n✅ Cleaned dataset saved as 'cleaned_financial_data.xlsx'")
