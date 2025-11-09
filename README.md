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

```

## Quality Control

## Identification of SVGd with SpatialDE

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
