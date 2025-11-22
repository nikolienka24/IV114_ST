#!/usr/bin/env python3
import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser(description="Compare SOMDE and SpatialDE resource usage.")
parser.add_argument("dataset", type=str, help="Dataset folder name (e.g., SN123_A938797_Rep1_X)")
args = parser.parse_args()

dataset = args.dataset
print(f"Using dataset: {dataset}")

# ----------------------
# 1. Load CSV files
# ----------------------
# Method requirements
method1_file = f"somde_results/{dataset}/requirements.csv"
method2_file = f"spatialde_results/{dataset}/requirements.csv"

# System info
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
method2['System'] = 'System2_spatialDE'
system1['System'] = 'System1_somde'
system2['System'] = 'System2_spatialDE'

# ----------------------
# 3. Normalize RAM units
# ----------------------
for df in [method1, method2]:
    if 'Total_RAM_GB' in df.columns:
        df['Total_RAM_MB'] = df['Total_RAM_GB'] * 1024
    else:
        df['Total_RAM_MB'] = df['RAM_used_MB']

# Ensure CPU usage percent exists
if 'CPU_usage_percent' not in method2.columns:
    cpu_col = [c for c in method2.columns if 'CPU' in c.lower() and 'time' in c.lower()][0]
    wall_col = [c for c in method2.columns if 'Wall' in c and 'time' in c][0]
    method2['CPU_usage_percent'] = (method2[cpu_col] / method2[wall_col]) * 100
    method2 = method2.rename(columns={cpu_col: 'CPU_time', wall_col: 'Wall_time'})

# ----------------------
# 4. Aggregate SOMDE tasks
# ----------------------
somde_summary = pd.DataFrame({
    'Task': ['SOMDE node initialization + SOMDE analysis'],
    'CPU_time': [method1['CPU_time'].sum()],
    'Wall_time': [method1['Wall_time'].sum()],
    'RAM_used_MB': [method1['RAM_used_MB'].sum()],
    'System': ['System1_somde']
})

# ----------------------
# 5. Merge with system info
# ----------------------
somde_summary = somde_summary.merge(system1, on='System', how='left')
method2 = method2.merge(system2, on='System', how='left')

# ----------------------
# 6. Compute normalized efficiencies
# ----------------------
for df in [somde_summary, method2]:
    df['CPU_efficiency'] = df['CPU_time'] / (df['CPU_cores'] * df['Wall_time'])
    df['RAM_efficiency'] = df['RAM_used_MB'] / (df['Total_RAM_GB'] * 1024)

# Compute CPU usage percent for SOMDE
somde_summary['CPU_usage_percent'] = (somde_summary['CPU_time'] / somde_summary['Wall_time']) * 100

# ----------------------
# 7. Combine for comparison
# ----------------------
cols_to_show = ['Task','CPU_time','Wall_time','CPU_usage_percent','RAM_used_MB','CPU_efficiency','RAM_efficiency','System']
comparison = pd.concat([
    somde_summary[cols_to_show],
    method2[cols_to_show]
], ignore_index=True)

# ----------------------
# 8. Print and save
# ----------------------
print("\n===== Resource Usage Comparison =====\n")
print(comparison)

# Ensure output folder exists
output_dir = f"method_comparison/{dataset}"
os.makedirs(output_dir, exist_ok=True)
output_file = f"{output_dir}/requirements_comparison.csv"

comparison.to_csv(output_file, index=False)
print(f"\nComparison saved to {output_file}")
