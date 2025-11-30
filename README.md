# IV114 Spatial Transcriptomics Project
**Analysis of Spatial Transcriptomics data and identification of Spatially Variable Genes (SVGs)**
**Work completed for the IV114 course at FI MUNI — Fall Semester 2025**

## Introduction

This project focuses on the analysis of **Spatial Transcriptomics (ST)** data with the goal of **identifying Spatially Variable Genes (SVGs)**. A complete analysis workflow is implemented, including data visualization, quality control, and two independent SVG detection methods (SOMDE and SpatialDE).

---

## Project Overview

Spatial Transcriptomics allows researchers to measure gene expression while preserving spatial context within tissues.  
In this project, we implement a full analysis workflow that includes:

1. **Data visualization** (Python >3.11 is required)
2. **Quality Control (QC)** + filtering out low-quality spots (Python >3.11 is required)
3. **SOMDE** — applying *Self-Organizing Map for Differential Expression* to efficiently identify spatially variable genes. (Please refer to the *SOMDE Analysis* section for proper virtual environment setup.)
4. **SpatialDE** — performing statistical modeling to detect to efficiently identify spatially variable genes.

---

## Data Description

The spatial transcriptomics datasets used in this project are publicly available from **Zenodo**:

🔗 **Dataset source:** [https://zenodo.org/records/7760264](https://zenodo.org/records/7760264)

These data originate from **SpaceRanger**-processed outputs and correspond to multiple biological replicates and samples.

---

## Running notebook from command line
To run a jupyter notebook (`.ipynb`) from the command line with custom input values, follow these steps:

### 1. Register your virtual environment as a Jupyter kernel

First, activate your virtual environment and install the required packages:

```bash
source <your_venv_name>/bin/activate   # OPTIONAL: Activate your virtual environment
pip install ipykernel jupyter
python -m ipykernel install --user --name=iv114_venv
```

### 2. Install PAPERMILL library
```bash
pip install papermill
```

Example:
```bash
papermill data_overview.ipynb data_overview.results.ipynb \
  -k iv114_venv \
  -p input "data/SN048_A121573_Rep1" \
  -p show_gene "FAM41C"
```
## Quality Control
**Quality Control (QC)** ensures that only high-quality spots and reliably expressed genes are included in downstream analyses.
### Overview
During this step, the dataset is laoded using `scanpy` library, and several quality metrics are computed to evaluate spot quality. Spots and genes not meeting defined thresholds are filtered out to improve data reliability and minimize noise in spatial analyses.

The following filtering criteria are applied (default thresholds can be adjusted by the user according to dataset characteristics):

- spots with **total counts below 1000**
- spots with **fewer than 200 detected genes**
- spots with **more than 20% mitochondrial transcripts**
- spots with **more than 10 estimated cells**
  - If cell count estimates were unavailable, a constant value of 8 cells per spot was assigned based on literature

were removed.

### Post-Filtering Steps
- Data normalization
- Log-transformation

### Vizualizations
- Histograms of QC metrics
- Spatial plots marking removed and retained spots
- Summary plots comparing pre- and post-filter datasets
---

## Identification of SVGs with SpatialDE
**SpatialDE** is a statistical framework designed to identify **Spatially Variable Genes (SVGs)** — genes whose expression levels exhibit significant spatial patterns across tissue sections.

### Overview
SpatialDE applies **Gaussian Process regression** to model gene expression as a function of spatial coordinates (x, y). For each gene, it compares a **spatial model** against a **non-spatial model** and performs a **likelihood ratio test** to evaluate whether spatial variation is statistically significant.

### Workflow
1. **Input preparation:**  
   Use QC-filtered data.

2. **Model fitting:**  
   Each gene is fitted with both spatial and non-spatial models to assess spatial variability.  

3. **Statistical testing:**  
   SpatialDE computed *p*-values and applied **FDR correction** to identify statistically significant SVGs.  

4. **Visualization:**  
   The most significant SVGs are visualized as spatial expression maps to confirm biologically meaningful patterns.

**Outputs:**
res.csv, results.csv, sample_info.csv
These files contain per-gene statistics used later for manual SVG evaluation.

### Implementation
SpatialDE is implemented in Python using the official package available at:  
**[SpatialDE GitHub Repository](https://github.com/Teichlab/SpatialDE)**

**Recommended versions:**
- `spatialde` ≥ 1.1.3  
- `numpy` ≥ 1.21  
- `pandas` ≥ 1.3
---

## Identification of SVGs with SOMDE
**SOMDE (Self-Organizing Map for Differential Expression)** is a computational method designed to identify **spatially variable genes (SVGs)** from spatial transcriptomics data. It combines
- **self-organizing maps (SOMs)** — an unsupervised neural network algorithm 
- statistical modeling 

to efficiently detect genes that exhibit spatial expression patterns across tissue sections.  

### Overview
This part helps you create a reliable environment to reproduce SOMDE results with compatible package versions.

Link to the SOMDE GitHub: [Github repositary](https://github.com/zhanglabtools/SOMDE)

Link to the SOMDE paper: [Paper](https://academic.oup.com/bioinformatics/article/37/23/4392/6308937)

### Environment Setup Guide

**Tested with:** Python **3.8**  

It is recommended to run this notebook within an isolated virtual environment to ensure all required dependencies are correctly installed and to avoid conflicts with other Python packages.

### Required Libraries and Versions

Please make sure the following libraries are installed with the specified versions:

- `numpy` version 1.17.5
- `pandas` version 1.3.1
- `scipy` version 1.4.1
- `somoclu` version 1.7.5
- `somde` version 0.1.8

Alternatively, you can configure your **conda** virtual environment with the provided `somde-environment.yml` file:

```bash
conda env create -f somde_x86.yml
```

## Manual Identification of TRUE vs FALSE SVGs
Notebook: Identification_of_SVGs.ipynb

Purpose:
This notebook helps users manually inspect SVG candidates using volcano plots, spatial expression maps, and key statistical metrics (FSV, q-value, LLR, fraction_expressing, etc.).

Why we included this step:
During our analysis we found that relying only on q-value and FSV often led to false-positive SVGs – genes that were statistically significant but showed no meaningful spatial pattern.
Therefore, a manual inspection step is needed to:
- visually identify true vs false SVGs
- compare statistical metrics across genes
- determine which variables are most reliable for filtering false positives
This enables users to build more robust and biologically meaningful SVG selection criteria.

## Final analysis
**Scripts for requirements comparison** - contains documentation in the beginning og python file
- `compare_resources.py` - normalizes and aggregates resource usage data across multiple systems and machines
- `compare_resources.all_datasets.py` - computes summary statistics across multiple datasets
- `make_venn_statistics.py`

**Notebooks**
1. vizualization - FSV scatter plots, qval scatter plots, meta-expression heatmaps per SOM node 
   - `SOMDE_vizualizations.ipynb` - visualizes SOMDE results
   - `SpatialDE_visual.ipynb` - visualizes SpatialDE results
2. Method comparison - compares SOMDE and SpatialDE results
   - `method_comparison.ipynb`
   - scatter plots of FSV and q-values for both methods
   - highlighting method-specific, overlapping, and non-detected genes
   - Venn diagrams of significant gene overlap
   - resource usage comparison plots
