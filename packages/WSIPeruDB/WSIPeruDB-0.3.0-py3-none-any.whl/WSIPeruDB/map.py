import random

import folium
import geopandas as gpd
from branca.element import Figure
from folium.plugins import Search


def random_color(feature):
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    return {"fillColor": color, "color": "black", "weight": 1.5, "fillOpacity": 0.3}


def generate_map():

    SI = gpd.read_file(
        "https://github.com/karoru23/WSI-PeruDB/raw/main/site_information_numeral.geojson"
    )
    SI["ID"] = SI.ID
    SI["station"] = SI.Station
    SI["Latitude"] = SI.Latitude
    SI["Longitude"] = SI.Longitude
    SI["Altitude"] = SI.Altitude
    SI["Department"] = SI.Department
    SI["Start_Date"] = SI.Start_Date
    SI["End_Date"] = SI.End_Date
    SI["Sampling_Frequency"] = SI.Sampling_Frequency
    SI["Sample_Type"] = SI.Sample_Type
    SI["Number_of_O18_data"] = SI.Number_of_O18_data
    SI["Number_of_D_data"] = SI.Number_of_D_data
    SI["O18_analytical_precision"] = SI.O18_analytical_precision
    SI["D_analytical_precision"] = SI.D_analytical_precision
    SI["Contact"] = SI.Contact
    SI["Contact_Email"] = SI.Contact_Email
    SI["References"] = SI.References
    SI["Database"] = SI.Database
    SI["Project_ID"] = SI.Project_ID

    for col in ["Start_Date", "End_Date"]:
        if col in SI.columns:
            SI[col] = SI[col].astype(str)

    fig = Figure(width=1000, height=1000)
    estaciones = folium.Map(location=(-10, -75), zoom_start=6)
    m = fig.add_child(estaciones)

    stateperu = folium.GeoJson(
        SI,
        name="Peru Site Information",
        tooltip=folium.GeoJsonTooltip(fields=["ID", "station"]),
        popup=folium.GeoJsonPopup(
            fields=[
                "ID",
                "Station",
                "Latitude",
                "Longitude",
                "Altitude",
                "Department",
                "Start_Date",
                "End_Date",
                "Sampling_Frequency",
                "Sample_Type",
                "Number_of_O18_data",
                "Number_of_D_data",
                "O18_analytical_precision",
                "D_analytical_precision",
                "Contact",
                "Contact_Email",
                "References",
                "Database",
                "Project_ID",
            ]
        ),
        zoom_on_click=True,
    ).add_to(estaciones)

    departamento = gpd.read_file(
        "https://github.com/juaneladio/peru-geojson/raw/master/peru_departamental_simple.geojson"
    )

    perudepartment = folium.GeoJson(
        departamento, name="Peru Department", style_function=random_color
    ).add_to(estaciones)

    statesearch = Search(
        layer=perudepartment,
        geom_type="Polygon",
        placeholder="Search for a Peru Department",
        collapsed=False,
        search_label="NOMBDEP",
        weight=5,
    ).add_to(estaciones)

    return estaciones


if __name__ == "__main__":
    generate_map()
