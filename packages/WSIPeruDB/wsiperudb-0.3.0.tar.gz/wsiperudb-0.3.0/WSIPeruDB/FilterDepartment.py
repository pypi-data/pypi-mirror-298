import ipywidgets as widgets
import pandas as pd
import requests
from IPython.display import display


def department_information():
    url = "https://github.com/karoru23/WSI-PeruDB/raw/main/site_information_numeral.geojson"
    response = requests.get(url)
    data_json = response.json()

    if "features" in data_json:

        siteinformation_df = pd.json_normalize(data_json["features"])
    else:
        siteinformation_df = pd.json_normalize(data_json)

    if "properties" in siteinformation_df.columns:
        siteinformation_df = pd.json_normalize(siteinformation_df["properties"])

    data = {
        "Department": siteinformation_df.get(
            "properties.Department", pd.Series([None] * len(siteinformation_df))
        ),
        "Sample_Type": siteinformation_df.get(
            "properties.Sample_Type", pd.Series([None] * len(siteinformation_df))
        ),
        "ID": siteinformation_df.get(
            "properties.ID", pd.Series([None] * len(siteinformation_df))
        ),
        "Number_of_O18_d2H_dataset": siteinformation_df.get(
            "properties.Number_of_O18_data", pd.Series([None] * len(siteinformation_df))
        ),
        "Sampling_Frequency": siteinformation_df.get(
            "properties.Sampling_Frequency", pd.Series([None] * len(siteinformation_df))
        ),
        "Project_ID": siteinformation_df.get(
            "properties.Project_ID", pd.Series([None] * len(siteinformation_df))
        ),
        "Database": siteinformation_df.get(
            "properties.Database", pd.Series([None] * len(siteinformation_df))
        ),
    }

    siteinformation_df = pd.DataFrame(data)

    department_dropdown = widgets.Dropdown(
        options=siteinformation_df["Department"].dropna().unique().tolist(),
        description="Search Department:",
    )

    def filter_dataframe(department):
        filtered_df = siteinformation_df[siteinformation_df["Department"] == department]
        display(filtered_df)

    interact = widgets.interactive(filter_dataframe, department=department_dropdown)

    return interact


if __name__ == "__main__":
    department_information()
