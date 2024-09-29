import os
from io import BytesIO

import ipywidgets as widgets
import pandas as pd
import requests
from IPython.display import display


def download_dataset():

    url = "https://github.com/karoru23/WSI-PeruDB/raw/main/dataset_information_numeral.xlsx"
    response = requests.get(url)

    xlsx_content = BytesIO(response.content)
    datasetinformation_df = pd.read_excel(xlsx_content, sheet_name="dataset")
    datasetinformation_df["Sample_Collection_Date"] = pd.to_datetime(
        datasetinformation_df["Sample_Collection_Date"]
    )
    department_dropdown = widgets.Dropdown(
        options=datasetinformation_df["Department"].unique().tolist(),
        description="Department:",
    )

    sample_type_dropdown = widgets.Dropdown(options=[], description="Sample Type:")

    id_dropdown = widgets.Dropdown(options=[], description="ID:")

    output = widgets.Output()
    display(output)

    def filter_and_show(department, sample_type, ID):
        if ID == "All":
            filtered_df = datasetinformation_df[
                (datasetinformation_df["Department"] == department)
                & (datasetinformation_df["Sample_Type"] == sample_type)
            ]
        else:
            filtered_df = datasetinformation_df[
                (datasetinformation_df["Department"] == department)
                & (datasetinformation_df["Sample_Type"] == sample_type)
                & (datasetinformation_df["ID"] == ID)
            ]

        display(filtered_df)

    def download_data(button):
        department = department_dropdown.value
        sample_type = sample_type_dropdown.value
        ID = id_dropdown.value

        try:
            if ID == "All":
                filtered_df = datasetinformation_df[
                    (datasetinformation_df["Department"] == department)
                    & (datasetinformation_df["Sample_Type"] == sample_type)
                ]
            else:
                filtered_df = datasetinformation_df[
                    (datasetinformation_df["Department"] == department)
                    & (datasetinformation_df["Sample_Type"] == sample_type)
                    & (datasetinformation_df["ID"] == ID)
                ]

            current_directory = os.getcwd()
            file_name = "filtered_datasetinfo.xlsx"
            save_path = os.path.join(current_directory, file_name)

            with pd.ExcelWriter(save_path, engine="openpyxl") as writer:
                filtered_df.to_excel(writer, index=False, sheet_name="Filtered Data")

            with output:
                output.clear_output()
                print(f"File has been saved to: {save_path}")
        except Exception as e:
            with output:
                output.clear_output()
                print(f"Error: {e}")

    download_button = widgets.Button(description="Download Excel")
    download_button.on_click(download_data)

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

    display(
        widgets.interactive(
            filter_and_show,
            department=department_dropdown,
            sample_type=sample_type_dropdown,
            ID=id_dropdown,
        )
    )
    display(download_button)


if __name__ == "__main__":
    download_dataset()
