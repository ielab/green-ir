from decimal import Decimal
from typing import Any

import toml
import pandas as pd
import numpy as np


def calculate_pt(omega: float, t: float, p: float):
    return (omega * t * p) / 1000


def generate_table(data: dict, table: str = "experiment", use_pue=True):
    experiments = data[table]
    PUE = 1.0
    if use_pue:
        PUE = data["PUE"]
    equivalent_emissions = data["equivalent_emissions"]
    for experiment in experiments:
        if "running_time" not in experiment:
            experiment["running_time"] = 0
        if "watts" not in experiment:
            experiment["watts"] = 0
        if "include" not in experiment:
            experiment["include"] = True
        if "usage" not in experiment:
            experiment["usage"] = False
        if "id" not in experiment:
            experiment["id"] = None

        pt = calculate_pt(PUE,
                          experiment["running_time"],
                          experiment["watts"])
        experiment["Power (kWh)"] = pt
        emissions = equivalent_emissions * pt
        experiment["Emissions (\\COtt)"] = emissions
        experiment["Running Time (hours)"] = experiment["running_time"]
        experiment["Experiment"] = experiment["name"]
        experiment["Hardware"] = experiment["hardware"] if "hardware" in experiment else "-"
        experiment["Batch Size"] = experiment["batch_size"] if "batch_size" in experiment else "-"
        experiment["Updates"] = experiment["updates"] if "updates" in experiment else "-"
    df = pd.DataFrame(experiments)[["usage",
                                    "include",
                                    "Experiment",
                                    # "Hardware",
                                    # "Batch Size",
                                    # "Updates",
                                    "Running Time (hours)",
                                    "Power (kWh)",
                                    "Emissions (\\COtt)",
                                    "id"]]
    df.rename(columns={
        "Power Consumption (kWh)": "{\\raggedright Power Consumption\\\\ (kWh)}"
    },
        inplace=True)
    return df


def format_thing(thing) -> Any:
    if type(thing) is str:
        return thing
    if thing < 1e-4:
        return str(Decimal(round(thing, 5)))[:7]
    if thing > 999:
        return f"{thing:,.0f}"
    if thing > 1:
        return round(thing, 2)
    return round(thing, 4)


if __name__ == '__main__':
    _danger_str = """% ------------------------------------------------------
% !!!!!!!!!!!!!!!!!!!!!!!!
% ! CAREFUL: DO NOT EDIT !
% !!!!!!!!!!!!!!!!!!!!!!!!
% THIS TABLE WAS AUTOMATICALLY GENERATED.
% ANY CHANGES YOU MAKE HERE ARE LIKELY TO BE OVERRIDDEN!
% PROCEED WITH CAUTION.
% ------------------------------------------------------
"""
    with open("experiments.toml", "r") as f:
        _data = toml.load(f)
    _df_experiments = generate_table(_data)
    _df_appliances = generate_table(_data, "appliance", use_pue=False)
    with open("query_power_usage.csv", "w") as f:
        f.write(_df_experiments.to_csv(index=False, header=False))
    _df_experiments = _df_experiments[_df_experiments["include"] == True].drop(["include", "usage"], axis=1)
    _df_appliances = _df_appliances[_df_appliances["include"] == True].drop(["include", "usage"], axis=1)
    _df_appliances = _df_appliances.round(4)
    # pd.options.display.float_format = '{:20,.2f}'.format
    # midrule_indexes = [1, 3, 6, 9, 13, 15]
    sum_running_time = 0.0
    sum_kwh = 0.0
    sum_emissions = 0.0
    _result_table = _danger_str + r"""
\begin{tabular}{lp{1cm}p{1cm}p{1cm}}
\toprule
"""
    equivalent_emissions = _data["equivalent_emissions"]
    tilde_expansion_experiment = list(filter(lambda x: x["id"] == "TILDE_expansion", _data["experiment"]))[0]
    docTquery_expansion_experiment = list(filter(lambda x: x["id"] == "docTquery_expansion", _data["experiment"]))[0]

    tilde_expansion_running_time = tilde_expansion_experiment["running_time"]
    tilde_expansion_kwh = calculate_pt(_data["PUE"], tilde_expansion_experiment["running_time"], tilde_expansion_experiment["watts"])
    tilde_expansion_emissions = equivalent_emissions * tilde_expansion_kwh

    docTquery_expansion_running_time = docTquery_expansion_experiment["running_time"]
    docTquery_expansion_kwh = calculate_pt(_data["PUE"], docTquery_expansion_experiment["running_time"], docTquery_expansion_experiment["watts"])
    docTquery_expansion_emissions = equivalent_emissions * docTquery_expansion_kwh

    _result_table += " & ".join(_df_experiments.columns[:-1]) + "\\\\\\midrule\n"
    records = _df_experiments.to_records()
    next_id = None
    for i, record in enumerate(records):
        if i < len(records) - 1:
            next_id = records[i + 1]["id"]
        else:
            next_id = ""
        sum_running_time += record[2]
        sum_kwh += record[3]
        sum_emissions += record[4]
        _result_table += " & ".join([str(format_thing(x)) for x in list(record)[1:-1]])
        _result_table += " \\\\\n"
        if next_id is not None and next_id != record["id"]:
            print(i, record)
            if record["id"] in ["TILDEv2", "uniCOIL"]:
                print("####################### hi #################")
                _result_table += f"{tilde_expansion_experiment['name']} & {format_thing(tilde_expansion_running_time)} & {format_thing(tilde_expansion_kwh)} & {format_thing(tilde_expansion_emissions)} \\\\\n"
                _result_table += f"\\cmidrule{{2-4}}\\vspace{{8pt}} & \\textbf{{{format_thing(sum_running_time + tilde_expansion_running_time)}}} & \\textbf{{{format_thing(sum_kwh + tilde_expansion_kwh)}}} & \\textbf{{{format_thing(sum_emissions + tilde_expansion_emissions)}}} \\\\\n"
                _result_table += f"{docTquery_expansion_experiment['name']} & {format_thing(docTquery_expansion_running_time)} & {format_thing(docTquery_expansion_kwh)} & {format_thing(docTquery_expansion_emissions)} \\\\\n"
                _result_table += f"\\cmidrule{{2-4}} & \\textbf{{{format_thing(sum_running_time + docTquery_expansion_running_time)}}} & \\textbf{{{format_thing(sum_kwh + docTquery_expansion_kwh)}}} & \\textbf{{{format_thing(sum_emissions + docTquery_expansion_emissions)}}} \\\\\\midrule\n"
            else:
                _result_table += f"\\cmidrule{{2-4}} & \\textbf{{{format_thing(sum_running_time)}}} & \\textbf{{{format_thing(sum_kwh)}}} & \\textbf{{{format_thing(sum_emissions)}}} \\\\\\midrule\n"
            sum_running_time = 0.0
            sum_kwh = 0.0
            sum_emissions = 0.0
    _result_table += r"""\end{tabular}"""
    print(_result_table)
    with open("output/experiments.tex", "w") as f:
        f.write(_result_table)

    _df_appliances.rename(columns={"Experiment": "Appliance"}, inplace=True)
    _df_appliances.drop(["id"], axis=1, inplace=True)
    _appliance_table = "\n".join((_danger_str + _df_appliances.to_latex(index=False, escape=False, column_format="lp{1.8cm}p{1.8cm}p{1.7cm}")).split("\n")[:-3]) + "\\midrule\n"
    # _appliance_table += "\\toprule Flight & & & Emissions (\\COtt)\\\\\\midrule\n"
    _appliance_table += f"\\multicolumn{{3}}{{l}}{{Flight from Frankfurt to Madrid}} & {format_thing(_data['plane_fra_mad'])}\\\\\n"
    _appliance_table += f"\\multicolumn{{3}}{{l}}{{Flight from New York to Madrid}} & {format_thing(_data['plane_jfk_mad'])}\\\\\n"
    _appliance_table += f"\\multicolumn{{3}}{{l}}{{Flight from Shanghai to Madrid}} & {format_thing(_data['plane_pvg_mad'])}\\\\\n"
    _appliance_table += f"\\multicolumn{{3}}{{l}}{{Flight from Melbourne to Madrid}} & {format_thing(_data['plane_mel_mad'])}\\\\\\midrule\n"
    _appliance_table += f"\\multicolumn{{3}}{{l}}{{Driving 10,00km by car}} & {format_thing(_data['car_kg_per_km'] * 10000)}\\\\\n"
    _appliance_table += r"""\bottomrule
\end{tabular}"""
    print(_appliance_table)
    with open("output/appliances.tex", "w") as f:
        f.write(_appliance_table)
