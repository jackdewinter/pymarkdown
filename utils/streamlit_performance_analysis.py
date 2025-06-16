"""
Streamlit application to visualize performance data.
"""

import csv
import json
from typing import Any, Dict

import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")


def __load_tally_map(file_to_load: str) -> Dict[str, Any]:
    tally_map = {}
    with open(file_to_load, "r", encoding="utf-8") as requirement_filex:
        csv_reader = csv.reader(requirement_filex)
        for next_row in csv_reader:
            num_repeats = next_row[0]
            test_duration = float(next_row[2])

            if num_repeats in tally_map:
                tally_list = tally_map[num_repeats]
            else:
                tally_list = []
                tally_map[num_repeats] = tally_list
            tally_list.append(test_duration)

    average_tally_map = {
        num_repeats: {
            "Complete Duration (s)": sum(list_of_samples) / len(list_of_samples),
            "repeats": int(num_repeats),
        }
        for num_repeats, list_of_samples in tally_map.items()
    }

    data_columns = ["repeats", "Complete Duration (s)"]
    columnized_datax = {i: [] for i in data_columns}
    for next_aggregated_sample in average_tally_map.values():
        columnized_datax["repeats"].append(int(next_aggregated_sample["repeats"]))
        columnized_datax["Complete Duration (s)"].append(
            float(next_aggregated_sample["Complete Duration (s)"])
        )
    return columnized_datax


if show_current := st.checkbox("Show current", value=True):
    columnized_data = __load_tally_map("build/series.csv")
    if show_source_table := st.checkbox("Show source table", value=True):
        st.table(columnized_data)

    data = pd.DataFrame.from_dict(columnized_data, orient="columns")
    st.line_chart(data, x="repeats")

    with open("build/series.json", "r", encoding="utf-8") as requirement_file:
        gg = json.load(requirement_file)
    data = pd.DataFrame(gg)
    st.table(data)
else:
    columnized_data = __load_tally_map("publish/perf-with-rules.csv")
    columnized_data2 = __load_tally_map("publish/perf-without-rules.csv")

    old_value = columnized_data["Complete Duration (s)"]
    del columnized_data["Complete Duration (s)"]
    columnized_data["Duration With Rules (s)"] = old_value

    old_value = columnized_data2["Complete Duration (s)"]
    columnized_data["Duration Without Rules (s)"] = old_value

    if show_source_table := st.checkbox("Show source tables", value=False):
        st.table(columnized_data)

    data = pd.DataFrame.from_dict(columnized_data, orient="columns")
    st.line_chart(data, x="repeats")

    col1, col2 = st.columns(2)

    with col1:
        with open(
            "publish/perf-with-rules.json", "r", encoding="utf-8"
        ) as requirement_file:
            gg = json.load(requirement_file)
        data = pd.DataFrame(gg)
        st.text("with rules")
        st.table(data)
    with col2:
        with open(
            "publish/perf-without-rules.json", "r", encoding="utf-8"
        ) as requirement_file:
            gg = json.load(requirement_file)
        data = pd.DataFrame(gg)
        st.text("without rules")
        st.table(data)
