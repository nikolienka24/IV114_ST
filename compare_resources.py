#!/usr/bin/env python3
"""
Compare SOMDE vs SpatialDE resource usage with normalization.

Usage: python script.py <folder_name>
Example: python script.py SN048_A121573_Rep1

Input folder needs to contain 2 CSVs with following structure:
  requirements.csv: CPU_time, Wall_time, RAM_used_MB, CPU_usage_percent
  system_info.csv: Total_RAM_GB, CPU_cores

Output: method_comparison/<folder_name>/requirements_comparison.csv

Note: RAM metrics are normalized by system specs since methods run on different hardware.
"""

import pandas as pd
import os
import argparse

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
# 2. Extract system specs
# ----------------------
somde_ram_gb = float(system1['Total_RAM_GB'].iloc[0])
somde_cores = int(system1['CPU_cores'].iloc[0])
spatialde_ram_gb = float(system2['Total_RAM_GB'].iloc[0])
spatialde_cores = int(system2['CPU_cores'].iloc[0])

print(f"\nSystem specs:")
print(f"  SOMDE: {somde_cores} cores, {somde_ram_gb} GB RAM")
print(f"  SpatialDE: {spatialde_cores} cores, {spatialde_ram_gb} GB RAM")

# ----------------------
# 4. Normalize RAM and CPU time to reference system
# ----------------------
# Normalize to 8GB RAM and 8 CPU cores for fair comparison
reference_ram_gb = 8
reference_cores = 8

somde_ram_norm_factor = reference_ram_gb / somde_ram_gb
spatialde_ram_norm_factor = reference_ram_gb / spatialde_ram_gb

somde_cpu_norm_factor = reference_cores / somde_cores
spatialde_cpu_norm_factor = reference_cores / spatialde_cores

somde_summary = pd.DataFrame({
    'Task': ['SOMDE node initialization + analysis'],
    'CPU_time': [method1['CPU_time'].sum()],
    'CPU_time_normalized': [method1['CPU_time'].sum() * somde_cpu_norm_factor],  # Normalized to 8 cores
    'Wall_time': [method1['Wall_time'].sum()],
    'Wall_time_normalized': [method1['Wall_time'].sum() * somde_cpu_norm_factor],  # Normalized to 8 cores
    'RAM_used_MB': [method1['RAM_used_MB'].max()],  # peak RAM
    'RAM_used_normalized_MB': [method1['RAM_used_MB'].max() * somde_ram_norm_factor],  # Normalized to 8GB system
})

# ----------------------
# 5. Compute metrics for SOMDE
# ----------------------
somde_summary['CPU_usage_percent'] = (somde_summary['CPU_time'] / somde_summary['Wall_time']) * 100
somde_summary['CPU_efficiency'] = somde_summary['CPU_time'] / (somde_cores * somde_summary['Wall_time'])
somde_summary['RAM_efficiency'] = somde_summary['RAM_used_MB'] / (somde_ram_gb * 1024)
somde_summary['RAM_percent'] = (somde_summary['RAM_used_MB'] / (somde_ram_gb * 1024)) * 100
somde_summary['System'] = 'SOMDE'
somde_summary['CPU_cores'] = somde_cores
somde_summary['Total_RAM_GB'] = somde_ram_gb

# ----------------------
# 6. Compute metrics for SpatialDE with normalization
# ----------------------
if 'CPU_usage_percent' not in method2.columns:
    method2['CPU_usage_percent'] = (method2['CPU_time'] / method2['Wall_time']) * 100

method2['CPU_time_normalized'] = method2['CPU_time'] * spatialde_cpu_norm_factor
method2['Wall_time_normalized'] = method2['Wall_time'] * spatialde_cpu_norm_factor
method2['RAM_used_normalized_MB'] = method2['RAM_used_MB'] * spatialde_ram_norm_factor
method2['CPU_efficiency'] = method2['CPU_time'] / (spatialde_cores * method2['Wall_time'])
method2['RAM_efficiency'] = method2['RAM_used_MB'] / (spatialde_ram_gb * 1024)
method2['RAM_percent'] = (method2['RAM_used_MB'] / (spatialde_ram_gb * 1024)) * 100
method2['System'] = 'SpatialDE'
method2['CPU_cores'] = spatialde_cores
method2['Total_RAM_GB'] = spatialde_ram_gb

# ----------------------
# 7. Combine for comparison
# ----------------------
cols = ['Task', 'CPU_time', 'CPU_time_normalized', 'Wall_time', 'Wall_time_normalized',
        'CPU_usage_percent', 'RAM_used_MB', 'RAM_used_normalized_MB', 'RAM_percent',
        'CPU_efficiency', 'RAM_efficiency', 'System', 'CPU_cores', 'Total_RAM_GB']

comparison = pd.concat([somde_summary[cols], method2[cols]], ignore_index=True)

# ----------------------
# 8. Print and save
# ----------------------
print("\n===== Resource Usage Comparison =====\n")
print(comparison.to_string(index=False))

output_dir = f"method_comparison/{dataset}"
os.makedirs(output_dir, exist_ok=True)
output_file = f"{output_dir}/requirements_comparison.csv"
comparison.to_csv(output_file, index=False)

print(f"\n✓ Comparison saved to {output_file}")