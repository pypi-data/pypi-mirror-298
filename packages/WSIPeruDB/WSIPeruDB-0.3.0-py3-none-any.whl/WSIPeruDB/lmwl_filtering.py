from io import BytesIO

import ipywidgets as widgets
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests


def plot_lmwl():

    url = "https://github.com/karoru23/WSI-PeruDB/raw/main/dataset_information_numeral.xlsx"
    response = requests.get(url)

    xlsx_content = BytesIO(response.content)
    datasetinformation_df = pd.read_excel(xlsx_content, sheet_name="dataset")

    department_dropdown = widgets.Dropdown(
        options=datasetinformation_df["Department"].unique().tolist(),
        description="Department:",
    )

    sample_type_dropdown = widgets.Dropdown(options=[], description="Sample Type:")

    id_dropdown = widgets.Dropdown(options=[], description="ID:")

    def filter_dataframe(department, sample_type, ID):
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
        Oxy = filtered_df["O18"].values
        Hyd = filtered_df["D"].values
        Oxy = Oxy.reshape((-1, 1))
        H_gmwl = 8 * Oxy + 10

        data = pd.DataFrame({"Oxy": Oxy.flatten(), "Hyd": Hyd})

        if len(filtered_df) < 4:
            print(
                "Exploratory analysis charts will not be generated due to insufficient data quantity"
            )
            return

        fig = px.scatter(
            data,
            x="Oxy",
            y="Hyd",
            trendline="ols",
            title="Local Meteoric Water Line (LMWL)",
        )
        fig.update_traces(
            marker=dict(size=12, color="pink", line=dict(width=1.5, color="black")),
            showlegend=True,
        )
        fig.add_trace(
            go.Scatter(
                x=Oxy.flatten(),
                y=H_gmwl.flatten(),
                mode="lines",
                name=r"$\delta^{{2}}H = 8 \delta^{{18}}O + 10 $",
                line=dict(color="black"),
            )
        )
        model = px.get_trendline_results(fig)
        alpha = model.iloc[0]["px_fit_results"].params[0]
        beta = model.iloc[0]["px_fit_results"].params[1]
        fig.update_layout(
            title="Local Meteoric Water Line (LMWL)",
            xaxis_title=r"$\delta^{18}O$ (VSMOW ‰)",
            yaxis_title=r"$\delta^{2}H$ (VSMOW ‰)",
            legend=dict(
                x=0.01,
                y=0.98,
                traceorder="normal",
                font=dict(family="sans-serif", size=12, color="black"),
                bgcolor="LightSteelBlue",
                bordercolor="dimgray",
                borderwidth=2,
            ),
        )
        fig.data[0].name = "Data"
        fig.data[0].showlegend = True
        fig.data[1].name = (
            rf"$\delta^{{2}}H = {round(beta, 2)}\delta^{{18}}O + {round(alpha, 2)}$"
        )
        fig.data[1].showlegend = True
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
    plot_lmwl()
