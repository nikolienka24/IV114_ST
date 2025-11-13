# IV114 Spatial Transcriptomics Project
**Work done for IV114 course at FI MUNI fall semester 2025**

## Introduction
This project focuses on the analysis of **Spatial Transcriptomics (ST)** data to identify **Spatially Variable Genes (SVGs)**.

---

## Project Overview

Spatial Transcriptomics allows researchers to measure gene expression while preserving spatial context within tissues.  
In this project, we implement a full analysis workflow that includes:

1. **Data visualization**
2. **Quality Control (QC)** + filtering out low-quality spots
3. **SOMDE** — applying *Self-Organizing Map for Differential Expression* to efficiently identify spatially variable genes.
4. **SpatialDE** — performing statistical modeling to detect to efficiently identify spatially variable genes.

---

## Data Description

The spatial transcriptomics datasets used in this project are publicly available from **Zenodo**:

🔗 **Dataset source:** [https://zenodo.org/records/7760264](https://zenodo.org/records/7760264)

These data originate from **SpaceRanger**-processed outputs and correspond to multiple biological replicates and samples.

---

## Running notebook from command line
To run the `.ipynb` notebook from the command line with custom input values, follow these steps:

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
---

```
## Quality Control
**Quality Control (QC)** ensures that only high-quality spots and reliably expressed genes are included in downstream analyses.  
This step removes potential artifacts caused by low sequencing depth, high mitochondrial gene content, or low transcript counts.

### Overview
During this step, the dataset was loaded using **`scanpy.read_visium`**, and several quality metrics were computed to evaluate spot quality.  
Spots and genes not meeting defined thresholds were filtered out to improve data reliability and minimize noise in spatial analyses.

The following filtering criteria were applied (default thresholds can be adjusted by the user according to dataset characteristics):

- Spots with **total counts below 1000** were removed.  
- Spots with **fewer than 200 detected genes** were removed.  
- Spots with **more than 20% mitochondrial transcripts** were removed.  
- Spots with **more than 10 estimated cells** were considered outliers and excluded.  

If no cell count information was available, a constant value of **8 cells per spot** was assigned based on literature estimates.

After filtering, the data were **normalized and log-transformed** using the following commands:

```python
sc.pp.normalize_total(adata_qc, target_sum=1e6)
sc.pp.log1p(adata_qc)
```

Several **visualizations** were generated to evaluate the filtering process, including histograms, spatial plots highlighting low-quality spots, and summary plots of discarded spots.  
The filtered dataset was saved as:  
`DATA_PATH/qc_filtered/adata_QC_filtered.h5ad`

---

## Identification of SVGs with SpatialDE
**SpatialDE** is a statistical framework designed to identify **Spatially Variable Genes (SVGs)** — genes whose expression levels exhibit significant spatial patterns across tissue sections.

### Overview
SpatialDE applies **Gaussian Process regression** to model gene expression as a function of spatial coordinates (x, y).  
For each gene, it compares a **spatial model** against a **non-spatial model** and performs a **likelihood ratio test** to evaluate whether spatial variation is statistically significant.

### Workflow
1. **Input preparation:**  
   QC-filtered and normalized data (`adata_QC_filtered.h5ad`) were used as input for the analysis.  

2. **Model fitting:**  
   Each gene was fitted with both spatial and non-spatial models to assess spatial variability.  

3. **Statistical testing:**  
   SpatialDE computed *p*-values and applied **FDR correction** to identify statistically significant SVGs.  

4. **Visualization:**  
   The most significant SVGs were visualized as spatial expression maps to confirm biologically meaningful patterns.

### Implementation
SpatialDE was implemented in Python using the official package available at:  
**[SpatialDE GitHub Repository](https://github.com/Teichlab/SpatialDE)**

**Recommended versions:**
- `spatialde` ≥ 1.1.3  
- `numpy` ≥ 1.21  
- `pandas` ≥ 1.3  

It is recommended to preselect **highly variable genes** before running SpatialDE to improve computational efficiency on large datasets.

---

## Identification of SVGs with SOMDE
**SOMDE (Self-Organizing Map for Differential Expression)** is a computational method designed to identify **spatially variable genes (SVGs)** from spatial transcriptomics data.  
It combines **self-organizing maps (SOMs)** — an unsupervised neural network algorithm — with statistical modeling to efficiently detect genes that exhibit spatial expression patterns across tissue sections.  

### Overview

SOMDE is a spatial transcriptomics analysis tool that uses Self-Organizing Maps (SOM) to detect spatially variable genes efficiently.  
This part helps you create a reliable environment to reproduce SOMDE results with compatible package versions.

Link to the SOMDE github: **[SOMDE](https://github.com/zhanglabtools/SOMDE)**

### Environment Setup Guide

**Tested with:** Python **3.9**  

It is recommended to run this notebook within an isolated virtual environment to ensure all required dependencies are correctly installed and to avoid conflicts with other Python packages.

### Required Libraries and Versions

Please make sure the following libraries are installed with the specified versions:

- `numpy` 1.21.6  
- `pandas` 1.3.5  
- `scipy` 1.7.3  
- `somde`

Alternatively, you can configure your virtual environment with the provided `requirements.txt` file:

```bash
pip install -r SOMDE/requirements.txt
```
