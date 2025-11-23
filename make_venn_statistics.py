import os
import pandas as pd
from pathlib import Path
from collections import defaultdict

"""
Aggregate venn diagram statistics across all datasets.

Scans subdirectories in method_comparison/ for venn count CSVs and computes 
summary statistics (sum, mean, median, min, max, std dev) across all datasets.

Input CSV structure (Category, Count):
  Category,Count
  Only SOMDE,17320
  Only SpatialDE,12
  Both,16

Output: statistics_all_datasets/venn_statistics_summary.csv
"""


# Configuration
base_dir = "method_comparison/"  # Change to your directory path
csv_files = ["venn_counts.fsv.csv", "venn_counts.qval+fsv.csv", "venn_counts.qval.csv"]

# Dictionary to store data: {csv_name: {category: [counts]}}
data = defaultdict(lambda: defaultdict(list))

# Walk through all subdirectories
for root, dirs, files in os.walk(base_dir):
    # Skip the base directory itself
    if root == base_dir:
        continue

    subdir_name = os.path.basename(root)

    for csv_file in csv_files:
        filepath = os.path.join(root, csv_file)

        if os.path.exists(filepath):
            try:
                df = pd.read_csv(filepath)
                for _, row in df.iterrows():
                    category = row['Category']
                    count = row['Count']
                    data[csv_file][category].append(count)
                print(f"✓ Loaded {subdir_name}/{csv_file}")
            except Exception as e:
                print(f"✗ Error reading {filepath}: {e}")
        else:
            print(f"✗ Not found: {subdir_name}/{csv_file}")

# Generate statistics
print("\n" + "=" * 80)
print("STATISTICS ACROSS ALL SUBDIRECTORIES")
print("=" * 80)

for csv_file in csv_files:
    print(f"\n{csv_file}")
    print("-" * 80)

    if csv_file not in data or not data[csv_file]:
        print("  No data found")
        continue

    for category in sorted(data[csv_file].keys()):
        counts = data[csv_file][category]

        print(f"\n  {category}:")
        print(f"    Count: {len(counts)} subdirectories")
        print(f"    Sum: {sum(counts):,}")
        print(f"    Mean: {sum(counts) / len(counts):.2f}")
        print(f"    Median: {pd.Series(counts).median():.2f}")
        print(f"    Min: {min(counts):,}")
        print(f"    Max: {max(counts):,}")
        print(f"    Std Dev: {pd.Series(counts).std():.2f}")

# Summary table
print("\n" + "=" * 80)
print("SUMMARY TABLE")
print("=" * 80)

summary_data = []
for csv_file in csv_files:
    for category in sorted(data[csv_file].keys()):
        counts = data[csv_file][category]
        summary_data.append({
            'File': csv_file,
            'Category': category,
            'Subdirs': len(counts),
            'Total': sum(counts),
            'Mean': f"{sum(counts) / len(counts):.2f}",
            'Min': min(counts),
            'Max': max(counts)
        })

if summary_data:
    summary_df = pd.DataFrame(summary_data)
    print(summary_df.to_string(index=False))

    # Optional: save to CSV
    summary_df.to_csv("statistics_all_datasets/venn_statistics_summary.csv", index=False)
    print(f"\n✓ Summary saved to venn_statistics_summary.csv")