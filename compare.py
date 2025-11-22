import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import seaborn as sns

# ================================
# 1. Load Results
# ================================

# Předpokládejme:
# somde_res: dataframe s kolonkou 'gene' a jednou metrikou (např. FSV)
# spatialde_res: dataframe s 'gene' a třeba 'qval' nebo 'LLR'

somde_res = pd.read_csv("somde_results.csv")
spatialde_res = pd.read_csv("spatialde_results.csv")

# Podmínky pro významné geny (uprav dle svého datasetu)
somde_sig = somde_res[somde_res["qval"] < 0.05]["gene"]
spatialde_sig = spatialde_res[spatialde_res["qval"] < 0.05]["gene"]

set_somde = set(somde_sig)
set_spatialde = set(spatialde_sig)

# ================================
# 2. Venn Diagram
# ================================

plt.figure(figsize=(6, 6))
venn2([set_somde, set_spatialde], set_labels=("SOMDE", "SpatialDE"))
plt.title("Overlap of Significant Genes")
plt.show()

# ================================
# 3. Scatter Plot of Statistics
# ================================

merged = pd.merge(somde_res, spatialde_res, on="gene", suffixes=("_somde", "_spatialde"))

plt.figure(figsize=(7, 6))
sns.scatterplot(
    data=merged,
    x="FSV_somde",        # změň názvy podle své metriky
    y="LLR_spatialde",    # nebo qval_spatialde
    hue=merged["gene"].isin(set_somde & set_spatialde),
    palette=["gray", "red"]
)
plt.title("Scatter: SOMDE vs SpatialDE statistics")
plt.xlabel("SOMDE Statistic (e.g., FSV)")
plt.ylabel("SpatialDE Statistic (e.g., LLR)")
plt.show()

# ================================
# 4. Rank–Rank Plot
# ================================

# Seřazení genů podle statistiky
somde_res["rank_somde"] = somde_res["FSV"].rank(ascending=False)
spatialde_res["rank_spatialde"] = spatialde_res["LLR"].rank(ascending=False)

merged_ranks = pd.merge(somde_res, spatialde_res, on="gene")

plt.figure(figsize=(7, 6))
sns.scatterplot(
    data=merged_ranks,
    x="rank_somde",
    y="rank_spatialde",
    alpha=0.6
)
plt.title("Rank–Rank Plot (SOMDE vs SpatialDE)")
plt.xlabel("SOMDE Rank")
plt.ylabel("SpatialDE Rank")
plt.gca().invert_xaxis()
plt.gca().invert_yaxis()
plt.show()

# ================================
# 5. Optional: Plot pro konkrétní gen
# ================================

gene_to_check = "GeneX"

if gene_to_check in merged.index:
    row = merged.set_index("gene").loc[gene_to_check]
    print("SOMDE:", row["FSV_somde"])
    print("SpatialDE:", row["LLR_spatialde"])
else:
    print("Tento gen nebyl nalezen.")
