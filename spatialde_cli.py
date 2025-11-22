import click
import numpy as np
import pandas as pd

import NaiveDE
import SpatialDE
import os

# cpu usage and time statistics
import csv
import psutil
import time
import platform

def main(expression_csv, coordinate_csv, results_csv, model_selection_csv=None):
    """
    Perform SpatialDE test on data in input files.
    """
    # Determine base directory for saving files (same as results_csv folder)
    base_dir = os.path.dirname(results_csv)
    os.makedirs(base_dir, exist_ok=True)
    
    # ---- System info ----
    cpu_model = platform.processor()
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count(logical=True)

    total_ram = psutil.virtual_memory().total / (1024**3)  # GB

    print("CPU model:", cpu_model)
    print("CPU cores:", cpu_cores)
    print("CPU threads:", cpu_threads)
    print("Total RAM: {:.2f} GB".format(total_ram))

    # ---------------- SAVE TO CSV -----------------
    csv_file = os.path.join(base_dir, "system_info.csv")

    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["CPU_model", "CPU_cores", "CPU_threads", "Total_RAM_GB"])
        writer.writerow([cpu_model, cpu_cores, cpu_threads, round(total_ram, 2)])

    print(f"System info saved to {csv_file}")
    

    # Load expression matrix
    df = pd.read_csv(expression_csv, index_col=0)
    df = df.T[df.sum(0) >= 3].T  # Filter practically unobserved genes

    # Load coordinates
    sample_info = pd.read_csv(coordinate_csv, index_col=0)
    sample_info['total_counts'] = df.sum(1)
    sample_info = sample_info.query('total_counts > 5')  # Remove empty features

    # Align
    df = df.loc[sample_info.index]
    X = sample_info[['x', 'y']]

    print("Min / max v df:", df.values.min(), df.values.max())
    print("Jsou v df nějaké NaNy?", np.isnan(df.values).any())

    # Variance-stabilizing transform
    dfm = NaiveDE.stabilize(df.T).T

    print("Min / max v dfm:", dfm.values.min(), dfm.values.max())
    print("Jsou v dfm NaNy?", np.isnan(dfm.values).any())

    # Regression out sequencing depth
    res = NaiveDE.regress_out(sample_info, dfm.T, 'np.log(total_counts)').T

    # ---------- SAVE res (normalized expression) ----------
    res_csv = os.path.join(base_dir, "res.csv")
    print(f"Saving res matrix to: {res_csv}")
    res.to_csv(res_csv)
    # ------------------------------------------------------

    # ---------- SAVE filtered sample_info ----------
    sample_info_csv = os.path.join(base_dir, "sample_info.csv")
    print(f"Saving sample_info to: {sample_info_csv}")
    sample_info.to_csv(sample_info_csv)
    # ------------------------------------------------
    
    print("SpatialDE analysis")

    process = psutil.Process(os.getpid())
    process.cpu_percent(interval=None)   # reset counters

    start_cpu = time.process_time()
    start_wall = time.time()

    # -------- code to measure -----------
    # Perform Spatial DE test with default settings
    # Run SpatialDE
    results = SpatialDE.run(X, res)
    # ------------------------------------

    end_cpu = time.process_time()
    end_wall = time.time()

    cpu_time = end_cpu - start_cpu
    wall_time = end_wall - start_wall
    cpu_usage = process.cpu_percent(interval=None)
    ram_usage = process.memory_info().rss / (1024**2)  # MB

    print("CPU time: {:.6f} seconds".format(cpu_time))
    print("Wall time: {:.6f} seconds".format(wall_time))
    print("CPU usage (%):", cpu_usage)
    print("RAM used by process: {:.2f} MB".format(ram_usage))

    # ---------------- SAVE TO CSV -----------------
    with open(os.path.join(base_dir,  "requirements.csv"), "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Task","CPU_model", "CPU_cores", "CPU_threads", "Total_RAM_GB"])
        writer.writerow(["SpatialDE analysis", cpu_time, wall_time, cpu_usage, ram_usage])
    
    # Save results.csv
    print(f"Saving SpatialDE results to: {results_csv}")
    results.to_csv(results_csv)
    
    # Optional: model selection file
    #if model_selection_csv:
        #de_results = results[(results.qval < 0.05)].copy()
        #ms_results = SpatialDE.model_search(X, res, de_results)

        #print(f"Saving model selection to: {model_selection_csv}")
        #ms_results.to_csv(model_selection_csv)

        #return results, ms_results

    return results


if __name__ == "__main__":
    main(
        expression_csv="data_after_qc/SN124_A938797_Rep2/count.not_normalized.csv",
        coordinate_csv="data_after_qc/SN124_A938797_Rep2/idx.not_normalized.csv",
        results_csv="data_after_qc/SN124_A938797_Rep2/results_spatialDE/results.csv",
    )
