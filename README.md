Financial Data Subset Sum Analysis

## 📌 Project Overview
This project implements a **multi-part assignment** that analyzes financial transaction data against target amounts.  
The tasks include dataset preparation, exact/approximate matching, dynamic programming solutions, machine learning integration, and performance benchmarking.

The main problem revolves around **Subset Sum Matching**:
- Given a list of transactions (credits/debits), determine whether a combination of them matches a target (e.g., invoice or payment request).
## ⚙️ Requirements
- Python 3.8+
- Libraries:
  ```bash
  pip install pandas numpy matplotlib scikit-learn openpyxl
  📝 Assignment Parts
Part 1 – Dataset Preparation

Input: Raw ledger & bank data.

Output: cleaned_financial_data.xlsx with two sheets:

Transactions (Transaction ID, Transaction Amount)

Targets (Target ID, Target Amount)

Ensures the data format is clean and ready for matching.

Part 2 – Brute Force Subset Sum

Implements exhaustive search to find:

Exact matches (Transaction sums == Target)

Subset sum results.

Outputs results to part2_bruteforce_results.xlsx.

Provides execution time for brute force.

Part 3 – Dynamic Programming Approach

Implements DP-based Subset Sum (efficient memory-optimized version).

Handles large transaction datasets without memory errors.

Saves results to part3_ml_results.xlsx.

Part 4 – Machine Learning Integration

Creates a feature-engineered dataset of transactions vs. targets.

Trains ML models to predict likelihood of matches.

Uses classification metrics and visualizations (accuracy, confusion matrix).

Output: Graphs and ml_results.xlsx.

Part 5 – Benchmarking & Visualization

Compares Brute Force vs Dynamic Programming in terms of:
Execution time
Scalability
Generates bar charts & line plots for performance visualization.

Output: Benchmarking plots + benchmark_results.xlsx.


✨ Key Learnings

How brute force and DP differ in computational complexity.
How ML can approximate subset sum problems.
How to benchmark algorithms with real-world data.
Data cleaning and preprocessing for financial analysis.

👨‍💻 Author

Maryam Ijaz

