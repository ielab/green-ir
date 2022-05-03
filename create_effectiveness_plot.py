import csv
import toml
from adjustText import adjust_text
from matplotlib import pyplot as plt, ticker
import matplotlib as mpl
import seaborn as sns
import pandas as pd
import numpy as np

# This causes matplotlib to use Type 42 (a.k.a. TrueType) fonts for PostScript and PDF files.
# This allows you to avoid Type 3 fonts without limiting yourself to the stone-age technology
# of Type 1 fonts.
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42


NUM_QUERIES = 6980
NUM_ESTIMATE = 200
ids = ["BM25","TILDEv2", "DPR", "uniCOIL", "monoBERT"]
# query_estimates = [100, 200, 300, 400, 6980]

# %
with open("experiments.toml", "r") as f:
    experiment_data = toml.load(f)

equivalent_emissions = experiment_data["equivalent_emissions"]
# %
s_emissions = "Emissions (kg$C0_2$e)"
s_queries = "Number of Queries (per hour)"
s_experiment = "Experiment"
emissions_equivalent_per_query = {s_emissions: [], s_queries: [], s_experiment: []}

emissions_data = {}
time_data = {}
tilde_expansion_emissions = 0.0
tilde_expansion_time = 0.0
docTquery_expansion_emissions = 0.0
docTquery_expansion_time = 0.0
with open("query_power_usage.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        experiment_id = row[6]

        if experiment_id == "TILDE_expansion":
            tilde_expansion_emissions = float(row[5])
            tilde_expansion_time = float(row[3])

        if experiment_id == "docTquery_expansion":
            docTquery_expansion_emissions = float(row[5])
            docTquery_expansion_time = float(row[3])

        experiment_emissions = row[5]
        # Emissions.
        if experiment_id in ids:
            if experiment_id not in emissions_data:
                emissions_data[experiment_id] = 0.0
            emissions_data[experiment_id] += float(experiment_emissions)

        # Time.
        experiment_time = row[3]
        if experiment_id in ids:
            if experiment_id not in time_data:
                time_data[experiment_id] = 0.0
            time_data[experiment_id] += float(experiment_time)

time_data["TILDEv2 (TILDE expansion)"] = time_data["TILDEv2"]
emissions_data["TILDEv2 (TILDE expansion)"] = emissions_data["TILDEv2"]
time_data["TILDEv2 (docTquery expansion)"] = time_data["TILDEv2"]
emissions_data["TILDEv2 (docTquery expansion)"] = emissions_data["TILDEv2"]
time_data["TILDEv2 (TILDE expansion)"] += tilde_expansion_time
emissions_data["TILDEv2 (TILDE expansion)"] += tilde_expansion_emissions
time_data["TILDEv2 (docTquery expansion)"] += docTquery_expansion_time
emissions_data["TILDEv2 (docTquery expansion)"] += docTquery_expansion_emissions

time_data["uniCOIL (TILDE expansion)"] = time_data["uniCOIL"]
emissions_data["uniCOIL (TILDE expansion)"] = emissions_data["uniCOIL"]
time_data["uniCOIL (docTquery expansion)"] = time_data["uniCOIL"]
emissions_data["uniCOIL (docTquery expansion)"] = emissions_data["uniCOIL"]
time_data["uniCOIL (TILDE expansion)"] += tilde_expansion_time
emissions_data["uniCOIL (TILDE expansion)"] += tilde_expansion_emissions
time_data["uniCOIL (docTquery expansion)"] += docTquery_expansion_time
emissions_data["uniCOIL (docTquery expansion)"] += docTquery_expansion_emissions

del time_data["TILDEv2"]
del time_data["uniCOIL"]
del emissions_data["TILDEv2"]
del emissions_data["uniCOIL"]

mrr_data = {}
for result in experiment_data["result"]:
    mrr_data[result["id"]] = result["mrr_10"]

plot_data = {}
for k, v in emissions_data.items():
    plot_data[k] = {"Emissions": v, "Effectiveness": mrr_data[k], "Running Time": time_data[k]}

plot_df = pd.DataFrame(plot_data).T.reset_index().rename({"index": "Method"}, axis=1)
# %
sns.set()
sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(6, 4))
sns.regplot(data=plot_df, x="Emissions", y="Effectiveness", ax=ax,
            n_boot=500, x_estimator=np.median, logx=True, ci=None)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.rc("axes", labelsize=16)
plt.rc("ytick", labelsize=12)
plt.rc("xtick", labelsize=12)
ax.tick_params(which="both", bottom=True, left=True)
texts = [plt.text(x=record["Emissions"], y=record["Effectiveness"], s=record["Method"], ha='center', va='center') for record in plot_df.to_records()]
adjust_text(texts, arrowprops=dict(arrowstyle='-', color='black', lw=1.5),
            autoalign='xy', lim=1000)
ax.set_xlabel("Emissions (kgC$0_2$e)")
ax.set_ylabel("Effectiveness (MRR@10)")
plt.tight_layout()
plt.savefig("output/effectiveness_emissions_tradeoff.pdf", bbox_inches='tight')
plt.show()

# %%
