#!/usr/bin/env python3
import pandas as pd
import os
import argparse

"""
Compare SOMDE vs SpatialDE resource usage.

Usage: python script.py <folder_name>
Example: python script.py SN048_A121573_Rep1

Input folder needs to contains 2 CSVs with following structure:
  requirements.csv: CPU_time, Wall_time, RAM_used_MB, CPU_usage_percent
  system_info.csv: Total_RAM_GB, CPU_cores

Output: method_comparison/<dataset>/requirements_comparison.csv
"""

# ----------------------
# 0. Parse arguments
# ----------------------
parser = argparse.ArgumentParser(description="Compare SOMDE and SpatialDE resource usage.")
parser.add_argument("dataset", type=str, help="Dataset folder name (e.g., SN048_A121573_Rep1)")
args = parser.parse_args()
dataset = args.dataset
print(f"Using dataset: {dataset}")

# ----------------------
# 1. Load CSV files
# ----------------------
method1_file = f"somde_results/{dataset}/requirements.csv"
method2_file = f"spatialde_results/{dataset}/requirements.csv"

system1_file = f"somde_results/{dataset}/system_info.csv"
system2_file = f"spatialde_results/{dataset}/system_info.csv"

method1 = pd.read_csv(method1_file)
method2 = pd.read_csv(method2_file)
system1 = pd.read_csv(system1_file)
system2 = pd.read_csv(system2_file)

# ----------------------
# 2. Assign system names
# ----------------------
method1['System'] = 'System1_somde'
method2['System'] = 'System2_spatialde'
system1['System'] = 'System1_somde'
system2['System'] = 'System2_spatialde'

# ----------------------
# 3. Convert total RAM to MB for efficiency
# ----------------------
system1['Total_RAM_MB'] = system1['Total_RAM_GB'] * 1024
system2['Total_RAM_MB'] = system2['Total_RAM_GB'] * 1024

# ----------------------
# 4. Ensure CPU usage columns for SpatialDE
# ----------------------
if 'CPU_usage_percent' not in method2.columns:
    # Detect columns containing CPU_time and Wall_time
    cpu_cols = [c for c in method2.columns if 'cpu' in c.lower() and 'time' in c.lower()]
    wall_cols = [c for c in method2.columns if 'wall' in c.lower() and 'time' in c.lower()]
    if cpu_cols and wall_cols:
        method2 = method2.rename(columns={cpu_cols[0]: 'CPU_time', wall_cols[0]: 'Wall_time'})
        method2['CPU_usage_percent'] = (method2['CPU_time'] / method2['Wall_time']) * 100
    else:
        raise ValueError("Could not detect CPU_time or Wall_time in SpatialDE requirements.csv")

# ----------------------
# 5. Aggregate SOMDE tasks
# ----------------------
somde_summary = pd.DataFrame({
    'Task': ['SOMDE node initialization + analysis'],
    'CPU_time': [method1['CPU_time'].sum()],
    'Wall_time': [method1['Wall_time'].sum()],
    'RAM_used_MB': [method1['RAM_used_MB'].max()],  # peak RAM
    'System': ['System1_somde']
})

# ----------------------
# 6. Merge with system info safely
# ----------------------
somde_summary = somde_summary.merge(system1, on='System', how='left', suffixes=("", "_sys"))
method2 = method2.merge(system2, on='System', how='left', suffixes=("", "_sys"))

# ----------------------
# 7. Compute efficiencies
# ----------------------
def compute_efficiency(df, system_df):
    df['CPU_efficiency'] = df['CPU_time'] / (df['CPU_cores'] * df['Wall_time'])
    df['RAM_efficiency'] = df['RAM_used_MB'] / float(system_df['Total_RAM_MB'].iloc[0])
    if 'CPU_usage_percent' not in df.columns:
        df['CPU_usage_percent'] = (df['CPU_time'] / df['Wall_time']) * 100
    return df

somde_summary = compute_efficiency(somde_summary, system1)
method2 = compute_efficiency(method2, system2)

# ----------------------
# 8. Combine for comparison
# ----------------------
cols = ['Task','CPU_time','Wall_time','CPU_usage_percent','RAM_used_MB','CPU_efficiency','RAM_efficiency','System']
comparison = pd.concat([somde_summary[cols], method2[cols]], ignore_index=True)

# ----------------------
# 9. Print and save
# ----------------------
print("\n===== Resource Usage Comparison =====\n")
print(comparison)

output_dir = f"method_comparison/{dataset}"
os.makedirs(output_dir, exist_ok=True)
output_file = f"{output_dir}/requirements_comparison.csv"
comparison.to_csv(output_file, index=False)

print(f"\nComparison saved to {output_file}")
