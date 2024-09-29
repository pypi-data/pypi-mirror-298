from io import BytesIO

import ipywidgets as widgets
import pandas as pd
import plotly.graph_objects as go
import requests


def analyze_temporal_series():

    url = "https://github.com/karoru23/WSI-PeruDB/raw/main/dataset_information_numeral.xlsx"
    response = requests.get(url)

    xlsx_content = BytesIO(response.content)
    datasetinformation_df = pd.read_excel(xlsx_content, sheet_name="dataset")

    if datasetinformation_df.empty:
        raise ValueError(
            "El DataFrame está vacío. Verifica los datos en el archivo JSON."
        )

    department_dropdown = widgets.Dropdown(
        options=datasetinformation_df["Department"].unique().tolist(),
        description="Department:",
    )

    sample_type_dropdown = widgets.Dropdown(options=[], description="Sample Type:")

    id_dropdown = widgets.Dropdown(options=[], description="ID:")

    def filter_dataframe(department, sample_type, ID):
        if ID == "All":
            filtered_df_1 = datasetinformation_df[
                (datasetinformation_df["Department"] == department)
                & (datasetinformation_df["Sample_Type"] == sample_type)
            ]

            layout = go.Layout(title="Histogram of &#948;<sup>18</sup>O")
            fig = go.Figure(
                data=[
                    go.Histogram(
                        x=filtered_df_1["O18"],
                        marker_color="pink",
                        marker_line_color="black",
                        marker_line_width=1,
                    )
                ],
                layout=layout,
            )
            fig.update_xaxes(title_text=r"δ¹⁸O(VSMOW ‰)$")
            fig.update_yaxes(title_text="Frequency")
            fig.show()

        else:
            filtered_df_1 = datasetinformation_df[
                (datasetinformation_df["Department"] == department)
                & (datasetinformation_df["Sample_Type"] == sample_type)
                & (datasetinformation_df["ID"] == ID)
            ]

            layout = go.Layout(title="Temporal Series of &#948;<sup>18</sup>O")
            temporal_series_1 = go.Scatter(
                x=filtered_df_1["Sample_Collection_Date"],
                y=filtered_df_1["O18"],
                mode="markers",
                marker=dict(size=12, color="pink", line=dict(width=2, color="black")),
                name="Series 1",
            )
            fig = go.Figure(data=temporal_series_1, layout=layout)
            fig.update_xaxes(title_text="Sample Collection Date", title_standoff=16)
            fig.update_yaxes(
                title_text=r"δ¹⁸O(VSMOW ‰)$",
                title_standoff=16,
                autorange="reversed",
            )
            fig.show()

    def update_sample_type_dropdown(*args):
        department = department_dropdown.value
        sample_type_dropdown.options = (
            datasetinformation_df[datasetinformation_df["Department"] == department][
                "Sample_Type"
            ]
            .unique()
            .tolist()
        )

    def update_id_dropdown(*args):
        department = department_dropdown.value
        sample_type = sample_type_dropdown.value
        id_dropdown.options = ["All"] + datasetinformation_df[
            (datasetinformation_df["Department"] == department)
            & (datasetinformation_df["Sample_Type"] == sample_type)
        ]["ID"].unique().tolist()

    department_dropdown.observe(update_sample_type_dropdown, "value")
    department_dropdown.observe(update_id_dropdown, "value")
    sample_type_dropdown.observe(update_id_dropdown, "value")

    interact = widgets.interactive(
        filter_dataframe,
        department=department_dropdown,
        sample_type=sample_type_dropdown,
        ID=id_dropdown,
    )

    return interact


if __name__ == "__main__":
    analyze_temporal_series()
