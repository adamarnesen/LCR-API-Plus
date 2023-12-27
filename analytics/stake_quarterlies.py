import math

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from analytics.data import *


STANDARDS_2024 = {
    "stake.membership": 2000,
    "stake.melch.leadership": 150,
    "stake.active.adults": 500,
    "stake.active.youth": 100,
    "stake.wards": 5,
    "ward.membership": 250,
    "ward.melch.leadership": 20,
    "ward.active.adults": 100,
    "ward.active.youth": 20,
}
"""Unit Standards starting in 2024.

In late 2023, the church released standards for unit sizes that would take effect in 2024. 
The summary of these changes can be seen in on the [church newsroom](https://newsroom.churchofjesuschrist.org/article/first-presidency-announces-uniform-worldwide-standards-for-ward-and-stake-boundaries).
This variable reflects what those new minimums are and is used when drawing min lines for reports."""


def get_section_by_label(qrp, section_id):
    section = next(
        (item for item in qrp["sections"] if item.get("nameResourceId") == section_id),
        None,
    )
    return section


def get_row_by_label(section, row_id):
    row = next(
        (item for item in section["rows"] if item.get("nameResourceId") == row_id), None
    )
    return row


def get_value_for_field(qrp, section_id, row_id):
    section = get_section_by_label(qrp, section_id)
    row = get_row_by_label(section, row_id)
    return row_id, row["actualValue"]


def make_bar_chart_per_ward_in_grid(
    df: pd.DataFrame, min_line: int = None, title: str = "", plot_variable: [str] = None
):
    wards = df["unitName"].unique()
    grid_size = math.ceil(math.sqrt(len(wards)))
    fig = make_subplots(
        rows=grid_size, cols=grid_size, subplot_titles=wards, shared_yaxes="all"
    )
    legend_added = set()
    for i, ward in enumerate(wards):
        row = i // grid_size + 1
        col = i % grid_size + 1
        subset = df[df["unitName"] == ward]
        for j, variable in enumerate(plot_variable):
            show_legend = False
            if (variable not in legend_added) and len(plot_variable) > 1:
                show_legend = True
                legend_added.add(variable)
            fig.add_trace(
                go.Bar(
                    x=subset["quarter"],
                    y=subset[variable],
                    name=variable,
                    marker_color=px.colors.qualitative.D3[j],
                    showlegend=show_legend,
                ),
                row=row,
                col=col,
            )

        if min_line:
            fig.add_hline(y=min_line, line_dash="dash", row=row, col=col)
    fig.update_layout(
        title={
            "text": title,
        },
        barmode="stack",
    )
    fig.show()


def make_charts_colum_per_ward(df: pd.DataFrame, rows, title):
    wards = df["unitName"].unique()
    fig = make_subplots(
        rows=len(rows), cols=len(wards), shared_yaxes=True, subplot_titles=wards
    )
    legend_added = {}
    for column_index, ward in enumerate(wards, start=1):
        ward_data = df[df["unitName"] == ward]
        for row_index, row in enumerate(rows, start=1):
            for variable in row["variables"]:
                show_legend = False
                if variable not in legend_added:
                    show_legend = True
                    entries = len(legend_added)
                    legend_added[variable] = entries
                fig.add_trace(
                    go.Bar(
                        x=ward_data["quarter"],
                        y=ward_data[variable],
                        name=variable,
                        marker_color=px.colors.qualitative.D3[legend_added[variable]],
                        showlegend=show_legend,
                    ),
                    row=row_index,
                    col=column_index,
                )
            fig.update_yaxes(title_text=row["name"], row=row_index, col=1)
            if "standard" in row.keys():
                fig.add_hline(
                    y=row["standard"], line_dash="dash", row=row_index, col=column_index
                )
    fig.update_layout(
        barmode="stack",
        title={
            "text": title,
        },
    )
    fig.show()


def chart_melch_per_ward(df: pd.DataFrame):
    df["melch.not.attending"] = df["adult.male.melch"] - df["melch.attending"]
    make_bar_chart_per_ward_in_grid(
        df,
        min_line=STANDARDS_2024["ward.melch.leadership"],
        title="Melchizedek Priesthood Attendance",
        plot_variable=["melch.attending", "melch.not.attending"],
    )


def chart_primary_per_ward(df: pd.DataFrame):
    make_bar_chart_per_ward_in_grid(
        df,
        title="Primary Attendance",
        plot_variable=["children.attending.primary.2019.1"],
    )


def chart_membership_per_ward(df: pd.DataFrame):
    make_bar_chart_per_ward_in_grid(
        df,
        title="Ward Membership",
        plot_variable=["total.members"],
        min_line=STANDARDS_2024["ward.membership"],
    )


def chart_adult_active_per_ward(df: pd.DataFrame):
    make_bar_chart_per_ward_in_grid(
        df,
        title="Active Adults",
        plot_variable=["melch.attending", "women.attending.meetings"],
        min_line=STANDARDS_2024["ward.active.adults"],
    )


def chart_youth_active_per_ward(df: pd.DataFrame):
    make_bar_chart_per_ward_in_grid(
        df,
        title="Active Youth",
        plot_variable=["young.men.attending", "young.women.attending"],
        min_line=STANDARDS_2024["ward.active.youth"],
    )


def make_individual_charts(df: pd.DataFrame):
    chart_melch_per_ward(df)
    chart_primary_per_ward(df)
    chart_membership_per_ward(df)
    chart_adult_active_per_ward(df)
    chart_youth_active_per_ward(df)


def create_quarterly_analytics(data_file: str, starting_year: int, unit_name: str):
    df = pd.read_csv(data_file)
    df = df[df["year"] >= starting_year]
    make_individual_charts(df)
    rows = [
        {
            "name": "Membership",
            "variables": ["total.members"],
            "standard": STANDARDS_2024["ward.membership"],
        },
        {
            "name": "Melchizedek Priesthood",
            "variables": ["melch.attending"],
            "standard": STANDARDS_2024["ward.melch.leadership"],
        },
        {
            "name": "Adults",
            "variables": ["melch.attending", "women.attending.meetings"],
            "standard": STANDARDS_2024["ward.active.adults"],
        },
        {
            "name": "Youth",
            "variables": ["young.men.attending", "young.women.attending"],
            "standard": STANDARDS_2024["ward.active.youth"],
        },
        {
            "name": "Sacrament",
            "variables": ["sacrament.attendance"],
        },
        {
            "name": "Primary",
            "variables": ["children.attending.primary.2019.1"],
        },
    ]
    make_charts_colum_per_ward(df, rows, unit_name)
