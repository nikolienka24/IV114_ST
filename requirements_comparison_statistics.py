import os
import pandas as pd

# -------------------------------
# Parameters
# -------------------------------
root_folder = "method_comparison/"  # Change to your folder
output_folder = "statistics_requirements/"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

task_stats_csv = os.path.join(output_folder, "combined_statistics_by_task.csv")

# -------------------------------
# Step 1: Collect all CSVs
# -------------------------------
all_dfs = []

for subdir, dirs, files in os.walk(root_folder):
    for file in files:
        if file == "requirements_comparison.csv":
            file_path = os.path.join(subdir, file)
            df = pd.read_csv(file_path)
            # Optional: keep subfolder info
            df['Subfolder'] = os.path.basename(subdir)
            all_dfs.append(df)

if not all_dfs:
    raise FileNotFoundError("No 'requirements_comparison.csv' files found in subfolders.")

# Combine all data
combined_df = pd.concat(all_dfs, ignore_index=True)
print(f"Collected {len(combined_df)} rows from {len(all_dfs)} files.")

# -------------------------------
# Step 2: Define aggregation (skip std to avoid nulls if single row)
# -------------------------------
agg_dict = {
    "CPU_time": ["mean", "min", "max"],
    "Wall_time": ["mean", "min", "max"],
    "CPU_usage_percent": ["mean", "min", "max"],
    "RAM_used_MB": ["mean", "min", "max"],
    "CPU_efficiency": ["mean", "min", "max"],
    "RAM_efficiency": ["mean", "min", "max"]
}

# -------------------------------
# Step 3: Compute statistics by Task
# -------------------------------
stats_by_task = combined_df.groupby("Task").agg(agg_dict).reset_index()

# Flatten MultiIndex columns
stats_by_task.columns = ['_'.join(col).strip('_') for col in stats_by_task.columns.values]

# Fill NaN (optional)
stats_by_task = stats_by_task.fillna(0)

# Save CSV
stats_by_task.to_csv(task_stats_csv, index=False)
print(f"Statistics by Task saved to '{task_stats_csv}'")
