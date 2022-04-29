import csv
import toml
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
import numpy as np

NUM_QUERIES = 6980
NUM_ESTIMATE = 200
query_estimates = [1_000, 1_0_000, 1_00_000, 1_000_000, 10_000_000]

# %
with open("experiments.toml", "r") as f:
    experiment_data = toml.load(f)

equivalent_emissions = experiment_data["equivalent_emissions"]
# %
s_emissions = "Emissions (kgC$0_2$e)"
s_queries = "Number of Queries (per hour)"
s_experiment = "Experiment"
emissions_equivalent_per_query = {s_emissions: [], s_queries: [], s_experiment: []}
with open("query_power_usage.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        if row[0] == "True":
            if "(*)" in row[2]:
                emissions_equivalent_per_query[s_emissions] += [q * ((float(row[4]) / NUM_ESTIMATE) * equivalent_emissions) for q in query_estimates]
            else:
                emissions_equivalent_per_query[s_emissions] += [q * ((float(row[4]) / NUM_QUERIES) * equivalent_emissions) for q in query_estimates]
            emissions_equivalent_per_query[s_queries] += [q for q in query_estimates]
            emissions_equivalent_per_query[s_experiment] += [row[2] for q in query_estimates]

# %
sns.set()
sns.set_style("whitegrid")
df = pd.DataFrame(emissions_equivalent_per_query)
fig, ax = plt.subplots()
sns.pointplot(data=df, y=s_emissions, x=s_queries, hue=s_experiment, palette="colorblind", ax=ax, log_scale=10)
ax.tick_params(which="both", bottom=True, left=True)
plt.rc("axes", labelsize=16)
plt.rc("ytick", labelsize=12)
plt.rc("xtick", labelsize=12)
plt.yscale("log")
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: np.format_float_positional(y, trim='-')))
ax.yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=np.arange(2, 10) * .1, numticks=12))
ax.set_xticklabels([f"{x:,.0f}" for x in query_estimates])
plt.tick_params(axis="x", labelrotation=45)
ax.set_clip_on(False)
ax.annotate("log10", (0.01, 0.95), annotation_clip=False, xycoords="axes fraction", fontsize=8)
ax.yaxis.set_minor_formatter(ticker.NullFormatter())
plt.legend(bbox_to_anchor=(0, 1, 1, 0), mode="expand", ncol=2)
plt.tight_layout()
plt.savefig("output/query_emissions_per_hour.pdf", bbox_inches='tight')
plt.show()

# %%
