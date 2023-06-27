# Green Information Retrieval

Reduce, Reuse, Recycle: Green IR Research

Welcome to the code and data repository for [ielab's](https://ielab.io) research on [Green Information Retrieval](https://ielab.io/green-ir). This repository contains information and material for our papers:

* Scells, Zhuang, Zuccon. [Reduce, Reuse, Recycle: Green Information Retrieval Research](https://ielab.io/green-ir), SIGIR 2022 (best paper award, honourable mention)
* Zuccon, Scells, Zhuang. [Beyond CO2 Emissions: The Overlooked Impact of Water Consumption of Information Retrieval Models](https://ielab.io/green-ir), ICTIR 2023

For the SIGIR 2022 perspective paper [Reduce, Reuse, Recycle: Green Information Retrieval Research](https://ielab.io/green-ir), this repository contains the raw data (see: [experiments.toml](experiments.toml)) that we collected for each of the end-to-end ad-hoc retrieval pipeline (using the [CodeCarbon](https://github.com/mlco2/codecarbon) library) and the additional emission data for household appliances and travel as seen in the paper. The code in this repository can be used to recreate all the tables and plots, and we also have the scripts used to capture the power and running times for the retrieval experiments.

## Recreate tables

 - `python create_tables.py`
 - Creates both the main experiment table and the comparison table containing additional data.
 - Outputs the two tables into the `output` folder.
 - This script generates a csv file for generating the two figures below.

## Recreate figures

 - `python create_query_usage_plot.py` (creates Figure 1)
 - `python create_effectiveness_plot.py` (creates Figure 2)
 - Separately creates the two figures, and outputs them into the `output` folder.

## Power usage scripts

 - These scripts (prefixed with `ex_` to indicate the experiments) are available in the [scripts](scripts) folder.
 - Please see the [Pipfile](Pipfile) for the exact versions of pyserini used.
 - There is also the script used to create the synthetic letor dataset, and a script for downloading the msmarco unicoil vectors.

## WandC: a WandB Plug-in for Metering Energy, Carbon and Water
Our plug-in that allows you to metering Energy and Water consumption along with carbon emmissions associated with your experiment is available at [https://github.com/ielab/wandc](https://github.com/ielab/wandc).
