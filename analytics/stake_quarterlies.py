import math

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from analytics.data import *


STANDARDS_2024 = {
    "stake.membership": 2000,
    "stake.melchizedek priesthood.leadership": 150,
    "stake.active.adults": 500,
    "stake.active.youth": 100,
    "stake.wards": 5,
    "ward.membership": 250,
    "ward.melchizedek priesthood.leadership": 20,
    "ward.participating.adults": 100,
    "ward.participating.youth": 20,
}
"""Unit Standards starting in 2024.

In late 2023, the church released standards for unit sizes that would take effect in 2024. 
The summary of these changes can be seen in on the [church newsroom](https://newsroom.churchofjesuschrist.org/article/first-presidency-announces-uniform-worldwide-standards-for-ward-and-stake-boundaries).
This variable reflects what those new minimums are and is used when drawing min lines for reports."""
RENDER_ENGINE = "png"


DEFAULT_LDS_PALETTE = [
    "#007DA5",
    "#A6004E",
    "#E66A1F",
    "#50A83E",
]

ATTENDANCE_PALETTE = ["#318D43", "#D45311"]


def ward_standards_table_md():
    header = "| Standard | Value |\n| --- | --- |\n"
    ward_standards = {
        key: value for key, value in STANDARDS_2024.items() if "ward." in key
    }
    rows = []
    for key, value in ward_standards.items():
        name = key.replace(".", " ")
        name = name.replace("ward ", "").title()
        rows.append(f"| {name} | {value} |")
    return header + "\n".join(rows)


def __show_and_save_html_report(report_title: str, fig):
    """Saves the html report"""
    html_report_name = f"{report_title}.html"
    fig.write_html(create_and_get_output_path(html_report_name))
    # print(f"{report_title} - Saved.")
    fig.show(renderer=RENDER_ENGINE)


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


def clean_legend_entry(entry: str) -> str:
    entry = (
        entry.replace("ward.", "")
        .replace(".", " ")
        .replace("melch", "melchizedek priesthood")
        .title()
    )
    return entry


def make_bar_chart_per_ward_in_grid(
    df: pd.DataFrame,
    min_line: int = None,
    title: str = "",
    plot_variable: [str] = None,
    color_scheme: [str] = DEFAULT_LDS_PALETTE,
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
                    marker_color=color_scheme[j],
                    showlegend=show_legend,
                    text=subset[variable],
                    textposition="auto",
                ),
                row=row,
                col=col,
            )
            fig.update_traces(
                name=clean_legend_entry(variable), selector=dict(name=variable)
            )

        if min_line:
            fig.add_hline(y=min_line, line_dash="dash", row=row, col=col)
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
    )

    fig.update_layout(
        title={
            "text": title,
        },
        barmode="stack",
    )
    __show_and_save_html_report(title, fig)


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
    __show_and_save_html_report(title, fig)


def chart_melch_per_ward(df: pd.DataFrame):
    df["melch.not.attending"] = df["adult.male.melch"] - df["melch.attending"]
    make_bar_chart_per_ward_in_grid(
        df,
        min_line=STANDARDS_2024["ward.melchizedek priesthood.leadership"],
        title="Melchizedek Priesthood Attendance",
        plot_variable=["melch.attending", "melch.not.attending"],
        color_scheme=ATTENDANCE_PALETTE,
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
        title="Adults Attending Sunday Meetings",
        plot_variable=["melch.attending", "women.attending.meetings"],
        min_line=STANDARDS_2024["ward.participating.adults"],
    )


def chart_adult_temple_recommends_per_ward(df: pd.DataFrame):
    make_bar_chart_per_ward_in_grid(
        df,
        title="Adults with Temple Recommend",
        plot_variable=["endowed.adults.with.recommend"],
    )


def chart_youth_temple_recommends_per_ward(df: pd.DataFrame):
    make_bar_chart_per_ward_in_grid(
        df,
        title="Youth with Temple Recommend",
        plot_variable=["youth.with.recommend"],
    )


def chart_all_temple_recommends_per_ward(df: pd.DataFrame):
    make_bar_chart_per_ward_in_grid(
        df,
        title="All Members with Temple Recommends",
        plot_variable=["endowed.adults.with.recommend", "youth.with.recommend"],
    )


def chart_sacrament_meeting_attendance_per_ward(df: pd.DataFrame):
    make_bar_chart_per_ward_in_grid(
        df,
        title="Sacrament Meeting Attendance",
        plot_variable=["sacrament.attendance"],
    )


def chart_youth_active_per_ward(df: pd.DataFrame):
    make_bar_chart_per_ward_in_grid(
        df,
        title="Participating Youth",
        plot_variable=["young.men.attending", "young.women.attending"],
        min_line=STANDARDS_2024["ward.participating.youth"],
    )


def aggregate_attendance_and_percentages(df: pd.DataFrame):
    """Aggregate attendance.

    Computes the aggregated attendance that includes both men and women attendance as well as the
    percentage of attendance in these aggregates compared to the potential.
    """

    df.loc[:, "sacrament.attending.percent"] = (
        df["sacrament.attendance"] / df["sacrament.attendance.potential"]
    )

    df.loc[:, "adults.attending"] = (
        df["melch.attending"]
        + df["prospective.elders.attending"]
        + df["women.attending.meetings"]
    )
    df.loc[:, "adults.attending.potential"] = (
        df["melch.attending.potential"]
        + df["prospective.elders.attending.potential"]
        + df["women.attending.meetings.potential"]
    )
    df.loc[:, "adults.attending.percent"] = (
        df["adults.attending"] / df["adults.attending.potential"]
    )

    df.loc[:, "youth.attending"] = (
        df["young.men.attending"] + df["young.women.attending"]
    )
    df.loc[:, "youth.attending.potential"] = (
        df["young.men.attending.potential"] + df["young.women.attending.potential"]
    )
    df.loc[:, "youth.attending.percent"] = (
        df["youth.attending"] / df["youth.attending.potential"]
    )

    df.loc[:, "children.attending.percent"] = (
        df["children.attending.primary.2019.1"]
        / df["children.attending.primary.2019.1.potential"]
    )

    df.loc[:, "adults.youth.submitted.names.percent"] = (
        df["adults.youth.submitted.names"]
        / df["adults.youth.submitted.names.potential"]
    )
    return df


def chart_attendance_percent_trend(df: pd.DataFrame):
    plots = [
        {
            "name": "Sacrament",
            "variable": "sacrament.attending.percent",
        },
        {
            "name": "Adults",
            "variable": "adults.attending.percent",
        },
        {
            "name": "Youth",
            "variable": "youth.attending.percent",
        },
        {
            "name": "Children",
            "variable": "children.attending.percent",
        },
    ]
    names = [d["name"] for d in plots]
    grid_size = math.ceil(math.sqrt(len(names)))
    fig = make_subplots(rows=grid_size, cols=grid_size, subplot_titles=names)
    for i, plot in enumerate(plots):
        grid_row = i // grid_size + 1
        grid_col = i % grid_size + 1
        fig_px = px.line(
            df,
            x=df["quarter"],
            y=df[plot["variable"]],
            color="unitName",
            markers=True,
            color_discrete_sequence=DEFAULT_LDS_PALETTE,
        )
        fig_go = go.Figure(fig_px)
        for trace in fig_go.data:
            if i > 0:
                trace.showlegend = False
            fig.add_trace(trace, row=grid_row, col=grid_col)
    fig.update_yaxes(tickformat=".2%")
    title = "Attendance Across Groups"
    fig.update_layout(
        title={
            "text": title,
        },
    )
    if len(df["unitName"].unique()) == 1:
        fig.update_layout(showlegend=False)
    __show_and_save_html_report(title, fig)


def chart_correlations(df: pd.DataFrame):
    corr_matrix = df.corr(numeric_only=True)
    corr_matrix.dropna(axis=1, how="all", inplace=True)
    corr_matrix.dropna(axis=0, how="all", inplace=True)
    cols = [i for i in corr_matrix.columns if (not "attend" in i)]
    rows = [
        i
        for i in corr_matrix.index
        if (not "potential" in i) and ("attend" in i) and ("percent" in i)
    ]
    corr_matrix = corr_matrix[cols]
    corr_matrix = corr_matrix.loc[rows]
    corr_matrix.sort_index(inplace=True)
    corr_matrix.sort_index(axis=1, inplace=True)
    fig = px.imshow(
        corr_matrix,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        color_continuous_scale="RdBu_r",
    )
    title = "Attendance Percentages Correlation to other metrics"
    fig.update_layout(title={"text": title})
    __show_and_save_html_report(title, fig)


def make_individual_charts(df: pd.DataFrame):
    chart_melch_per_ward(df)
    chart_primary_per_ward(df)
    chart_membership_per_ward(df)
    chart_adult_active_per_ward(df)
    chart_youth_active_per_ward(df)


def create_quarterly_analytics(data_file: str, starting_year: int, unit_name: str):
    df = pd.read_csv(data_file)
    df = aggregate_attendance_and_percentages(df)
    chart_correlations(df)
    df = df[df["year"] >= starting_year]
    make_individual_charts(df)
    chart_attendance_percent_trend(df)
    rows = [
        {
            "name": "Membership",
            "variables": ["total.members"],
            "standard": STANDARDS_2024["ward.membership"],
        },
        {
            "name": "Melchizedek Priesthood",
            "variables": ["melch.attending"],
            "standard": STANDARDS_2024["ward.melchizedek priesthood.leadership"],
        },
        {
            "name": "Adults",
            "variables": ["melch.attending", "women.attending.meetings"],
            "standard": STANDARDS_2024["ward.participating.adults"],
        },
        {
            "name": "Youth",
            "variables": ["young.men.attending", "young.women.attending"],
            "standard": STANDARDS_2024["ward.participating.youth"],
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
