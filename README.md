# IV114 Spatial Transcriptomics Project
**Work done for IV114 course at FI MUNI fall semester 2025**

## Introduction

## Data

## Quality Control

## Identification of SVGd with SpatialDE

## Identification of SVGs with SOMDE
### Environment setup GUIDE

This guide explains how to set up a Python virtual environment and install all required dependencies to run **[SOMDE](https://github.com/zhanglabtools/SOMDE)** (Self-Organizing Map for Differential Expression).

---

### Overview

SOMDE is a spatial transcriptomics analysis tool that uses Self-Organizing Maps (SOM) to detect spatially variable genes efficiently.  
This part helps you create a reliable environment to reproduce SOMDE results with compatible package versions.

**Tested on:** Python **3.9**

---

### Step 1: Create and Activate a Virtual Environment

```bash
# Create a virtual environment
python -m venv somde-env

# Activate it
source somde-env/bin/activate      # On macOS/Linux
# OR
somde-env\Scripts\activate         # On Windows
```

### Step 2: make sure you have all libraries in correct versions
* numpy 1.21.6
* pandas 1.3.5
* scipy 1.7.3
* **somde**
``` bash
pip install -r SOMDE/requirements.txt
```

