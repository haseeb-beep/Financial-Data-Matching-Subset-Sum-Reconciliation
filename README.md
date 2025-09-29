his project implements a multi-part assignment analyzing financial transaction data against target amounts. It covers dataset preparation, exact and approximate matching, dynamic programming solutions, machine learning integration, and performance benchmarking.

The main problem revolves around Subset Sum Matching:

Given a list of transactions (credits/debits), determine whether a combination matches a target (e.g., invoice or payment request).

⚙️ Requirements

Python 3.8+

Libraries:pip install pandas numpy matplotlib scikit-learn openpyxl

Assignment Parts
Part 1 – Dataset Preparation

Input: Raw ledger & bank data

Output: cleaned_financial_data.xlsx with two sheets:

Transactions (Transaction ID, Amount)

Targets (Target ID, Amount)

Ensures data is standardized and ready for matching.

Part 2 – Brute Force Subset Sum

Implements exhaustive search for:

Exact matches (Transaction sums == Target)

Subset sum combinations

Saves results to part2_bruteforce_results.xlsx

Reports execution time for brute force.

Part 3 – Dynamic Programming Approach

Efficient, memory-optimized DP subset sum solution

Handles larger datasets without memory issues

Saves results to part3_dp_results.xlsx.

Part 4 – Machine Learning Integration

Feature engineering of transactions vs. targets

Trains ML models to predict match likelihood

Evaluates with accuracy and confusion matrix

Outputs graphs + ml_results.xlsx.

Part 5 – Benchmarking & Visualization

Compares brute force vs. DP on:

Execution time

Scalability

Generates bar charts, line plots, and benchmarking reports.

✨ Key Learnings

Difference in complexity between brute force and DP

How ML can approximate subset sum problems

Benchmarking algorithms with real-world financial data

Preprocessing and cleaning datasets for analysis

👨‍💻 Author

Syed Haseeb Haider
