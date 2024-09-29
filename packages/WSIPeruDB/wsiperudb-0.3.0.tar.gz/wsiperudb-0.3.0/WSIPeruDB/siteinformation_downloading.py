import os
from io import BytesIO

import ipywidgets as widgets
import pandas as pd
import requests
from IPython.display import display


def download_site_information():

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
        "ID": siteinformation_df.get(
            "properties.ID", pd.Series([None] * len(siteinformation_df))
        ),
        "Station": siteinformation_df.get(
            "properties.Station", pd.Series([None] * len(siteinformation_df))
        ),
        "Department": siteinformation_df.get(
            "properties.Department", pd.Series([None] * len(siteinformation_df))
        ),
        "Sample_Type": siteinformation_df.get(
            "properties.Sample_Type", pd.Series([None] * len(siteinformation_df))
        ),
        "Latitude": siteinformation_df.get(
            "properties.Latitude", pd.Series([None] * len(siteinformation_df))
        ),
        "Longitude": siteinformation_df.get(
            "properties.Longitude", pd.Series([None] * len(siteinformation_df))
        ),
        "Altitude": siteinformation_df.get(
            "properties.Altitude", pd.Series([None] * len(siteinformation_df))
        ),
        "Start_Date": siteinformation_df.get(
            "properties.Start_Date", pd.Series([None] * len(siteinformation_df))
        ),
        "End_Date": siteinformation_df.get(
            "properties.End_Date", pd.Series([None] * len(siteinformation_df))
        ),
        "Number_of_O18_data": siteinformation_df.get(
            "properties.Number_of_O18_data", pd.Series([None] * len(siteinformation_df))
        ),
        "Number_of_D_data": siteinformation_df.get(
            "properties.Number_of_D_data", pd.Series([None] * len(siteinformation_df))
        ),
        "O18_analytical_precision": siteinformation_df.get(
            "properties.O18_analytical_precision",
            pd.Series([None] * len(siteinformation_df)),
        ),
        "D_analytical_precision": siteinformation_df.get(
            "properties.D_analytical_precision",
            pd.Series([None] * len(siteinformation_df)),
        ),
        "Sampling_Frequency": siteinformation_df.get(
            "properties.Sampling_Frequency", pd.Series([None] * len(siteinformation_df))
        ),
        "Sample_Type": siteinformation_df.get(
            "properties.Sample_Type", pd.Series([None] * len(siteinformation_df))
        ),
        "Contact": siteinformation_df.get(
            "properties.Contact", pd.Series([None] * len(siteinformation_df))
        ),
        "Contact_Email": siteinformation_df.get(
            "properties.Contact_Email", pd.Series([None] * len(siteinformation_df))
        ),
        "References": siteinformation_df.get(
            "properties.References", pd.Series([None] * len(siteinformation_df))
        ),
        "Project_ID": siteinformation_df.get(
            "properties.Project_ID", pd.Series([None] * len(siteinformation_df))
        ),
        "Database": siteinformation_df.get(
            "properties.Database", pd.Series([None] * len(siteinformation_df))
        ),
    }

    siteinformation_df = pd.DataFrame(data)

    def filter_and_show(department, sample_type, ID):
        if ID == "All":
            filtered_df = siteinformation_df[
                (siteinformation_df["Department"] == department)
                & (siteinformation_df["Sample_Type"] == sample_type)
            ]
        else:
            filtered_df = siteinformation_df[
                (siteinformation_df["Department"] == department)
                & (siteinformation_df["Sample_Type"] == sample_type)
                & (siteinformation_df["ID"] == ID)
            ]

        display(filtered_df)

    def download_data(button):
        department = department_dropdown.value
        sample_type = sample_type_dropdown.value
        ID = id_dropdown.value

        try:
            if ID == "All":
                filtered_df = siteinformation_df[
                    (siteinformation_df["Department"] == department)
                    & (siteinformation_df["Sample_Type"] == sample_type)
                ]
            else:
                filtered_df = siteinformation_df[
                    (siteinformation_df["Department"] == department)
                    & (siteinformation_df["Sample_Type"] == sample_type)
                    & (siteinformation_df["ID"] == ID)
                ]

            current_directory = os.getcwd()
            file_name = "filtered_data_siteinfo.xlsx"
            save_path = os.path.join(current_directory, file_name)

            with pd.ExcelWriter(save_path, engine="openpyxl") as writer:
                filtered_df.to_excel(writer, index=False, sheet_name="Filtered Data")

            status_label.value = f"File has been saved to: {save_path}"
        except Exception as e:
            status_label.value = f"Error: {e}"

    department_dropdown = widgets.Dropdown(
        options=siteinformation_df["Department"].unique().tolist(),
        description="Department:",
    )

    sample_type_dropdown = widgets.Dropdown(options=[], description="Sample Type:")

    id_dropdown = widgets.Dropdown(options=[], description="ID:")

    download_button = widgets.Button(description="Download Excel")
    download_button.on_click(download_data)

    status_label = widgets.Label(value="")

    def update_sample_type_dropdown(*args):
        department = department_dropdown.value
        sample_type_dropdown.options = (
            siteinformation_df[siteinformation_df["Department"] == department][
                "Sample_Type"
            ]
            .unique()
            .tolist()
        )

    def update_id_dropdown(*args):
        department = department_dropdown.value
        sample_type = sample_type_dropdown.value
        id_dropdown.options = ["All"] + siteinformation_df[
            (siteinformation_df["Department"] == department)
            & (siteinformation_df["Sample_Type"] == sample_type)
        ]["ID"].unique().tolist()

    department_dropdown.observe(update_sample_type_dropdown, "value")
    department_dropdown.observe(update_id_dropdown, "value")
    sample_type_dropdown.observe(update_id_dropdown, "value")

    display(
        widgets.interactive(
            filter_and_show,
            department=department_dropdown,
            sample_type=sample_type_dropdown,
            ID=id_dropdown,
        )
    )
    display(download_button)
    display(status_label)


if __name__ == "__main__":
    download_site_information()
