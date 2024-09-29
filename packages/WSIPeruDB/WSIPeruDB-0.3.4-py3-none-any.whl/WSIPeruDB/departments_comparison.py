from io import BytesIO

import ipywidgets as widgets
import pandas as pd
import plotly.graph_objects as go
import requests


def compare_departments():

    url = "https://github.com/karoru23/WSI-PeruDB/raw/main/dataset_information_numeral.xlsx"
    response = requests.get(url)

    xlsx_content = BytesIO(response.content)
    datasetinformation_df = pd.read_excel(xlsx_content, sheet_name="dataset")

    datasetinformation_df["Sample_Collection_Date"] = pd.to_datetime(
        datasetinformation_df["Sample_Collection_Date"]
    )
    datasetinformation_df["Month"] = datasetinformation_df[
        "Sample_Collection_Date"
    ].dt.month

    department_dropdown_1 = widgets.Dropdown(
        options=datasetinformation_df["Department"].unique().tolist(), description="D1:"
    )

    department_dropdown_2 = widgets.Dropdown(
        options=datasetinformation_df["Department"].unique().tolist(), description="D2:"
    )

    sample_type_dropdown_1 = widgets.Dropdown(options=[], description="ST1:")

    sample_type_dropdown_2 = widgets.Dropdown(options=[], description="ST2:")

    season_dropdown_1 = widgets.Dropdown(
        options=["All", "Summer", "Winter"], description="Season 1:"
    )

    season_dropdown_2 = widgets.Dropdown(
        options=["All", "Summer", "Winter"], description="Season 2:"
    )

    def filter_dataframe(
        department, department_2, sample_type, sample_type_2, season, season_2
    ):
        summer_months = [12, 1, 2, 3]
        winter_months = [6, 7, 8]

        filtered_df_1 = datasetinformation_df[
            (datasetinformation_df["Department"] == department)
            & (datasetinformation_df["Sample_Type"] == sample_type)
            & (
                (
                    (season == "Summer")
                    & datasetinformation_df["Month"].isin(summer_months)
                )
                | (
                    (season == "Winter")
                    & datasetinformation_df["Month"].isin(winter_months)
                )
                | (season == "All")
            )
        ]

        filtered_df_2 = datasetinformation_df[
            (datasetinformation_df["Department"] == department_2)
            & (datasetinformation_df["Sample_Type"] == sample_type_2)
            & (
                (
                    (season_2 == "Summer")
                    & datasetinformation_df["Month"].isin(summer_months)
                )
                | (
                    (season_2 == "Winter")
                    & datasetinformation_df["Month"].isin(winter_months)
                )
                | (season_2 == "All")
            )
        ]

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=filtered_df_1["Month"],
                y=filtered_df_1["O18"],
                mode="markers",
                name=department,
                marker=dict(
                    color="darkorchid", size=8, line=dict(color="black", width=2)
                ),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=filtered_df_2["Month"],
                y=filtered_df_2["O18"],
                mode="markers",
                name=department_2,
                marker=dict(color="blue", size=8, line=dict(color="black", width=2)),
            )
        )

        fig.update_layout(
            title="Comparison of &#948;<sup>18</sup>O between Departments",
            xaxis_title="Month",
            yaxis_title=r"δ¹⁸O(VSMOW ‰)$",
            showlegend=True,
            yaxis=dict(autorange="reversed"),
            height=600,
        )

        fig.show()

    def update_sample_type_dropdown_1(*args):
        department = department_dropdown_1.value
        sample_type_dropdown_1.options = (
            datasetinformation_df[datasetinformation_df["Department"] == department][
                "Sample_Type"
            ]
            .unique()
            .tolist()
        )

    def update_sample_type_dropdown_2(*args):
        department = department_dropdown_2.value
        sample_type_dropdown_2.options = (
            datasetinformation_df[datasetinformation_df["Department"] == department][
                "Sample_Type"
            ]
            .unique()
            .tolist()
        )

    department_dropdown_1.observe(update_sample_type_dropdown_1, "value")
    department_dropdown_2.observe(update_sample_type_dropdown_2, "value")

    interactive_plot = widgets.interactive(
        filter_dataframe,
        department=department_dropdown_1,
        department_2=department_dropdown_2,
        sample_type=sample_type_dropdown_1,
        sample_type_2=sample_type_dropdown_2,
        season=season_dropdown_1,
        season_2=season_dropdown_2,
    )
    return interactive_plot


if __name__ == "__main__":
    compare_departments()
