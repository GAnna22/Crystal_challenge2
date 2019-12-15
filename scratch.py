import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from matplotlib import cm
from scipy.interpolate import interp2d

path_gas_test = 'C:/Users/dorom/OneDrive/Рабочий стол/challenge2/challenge2/Geochemistry Data/CNS_gas_test.csv'
path_gas_train = 'C:/Users/dorom/OneDrive/Рабочий стол/challenge2/challenge2/Geochemistry Data/CNS_gas_train.csv'
path_rock_samples = 'C:/Users/dorom/OneDrive/Рабочий стол/challenge2/challenge2/Geochemistry Data/CNS_rock_samples.csv'
path_oil_samples = 'C:/Users/dorom/OneDrive/Рабочий стол/challenge2/challenge2/Geochemistry Data/CNS_oil.csv'
path_gas_external = 'C:/Users/dorom/OneDrive/Рабочий стол/challenge2/challenge2/Geochemistry Data/OGA_Field_Production_Points_PPRS_WGS84.csv'
prod_data = 'C:/Users/dorom/OneDrive/Рабочий стол/challenge2/challenge2/Production Data/CNS_Field_Production.csv'

df_test = pd.read_csv(path_gas_test, skiprows = [1], header = 0, engine='python')
df_train = pd.read_csv(path_gas_train, skiprows = [1], header = 0, engine='python')
df_rock = pd.read_csv(path_rock_samples, skiprows = [1], header = 0, engine='python')
df_oil = pd.read_csv(path_oil_samples, skiprows = [1], header = 0, engine='python')
df_prod = pd.read_csv(prod_data, skiprows = [1], header = 0, engine='python')

df_train['WH_LONG'].values[-5] = df_train['WH_LONG'].values[-4]
coord = df_train.iloc[:, [1, 6, 7, 18, 19, 31]].dropna(axis = 0)
coord['WH_LONG'] = coord['WH_LONG'].astype('float64')
import plotly.graph_objects as go

years = ['88', '98', '99', '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18']
for i in range(len(coord['WH_LONG'].values)):
    coord['SH_CDATE'].values[i] = coord['SH_CDATE'].values[i].split()[0].split('-')[2]

# make figure
fig_dict = {
    "data": [],
    "layout": {},
    "frames": []
}

# fill in most of layout
fig_dict["layout"]["xaxis"] = {"title": "Longitude"}
fig_dict["layout"]["yaxis"] = {"title": "Latitude"}
fig_dict["layout"]["hovermode"] = "closest"
fig_dict["layout"]["sliders"] = {
    "args": [
        "transition", {
            "duration": 400,
            "easing": "cubic-in-out"
        }
    ],
    "initialValue": "88",
    "plotlycommand": "animate",
    "values": years,
    "visible": True
}
fig_dict["layout"]["updatemenus"] = [
    {
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 500, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "Play",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
            }
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top"
    }
]

sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {
        "font": {"size": 20},
        "prefix": "Year:",
        "visible": True,
        "xanchor": "right"
    },
    "transition": {"duration": 300, "easing": "cubic-in-out"},
    "pad": {"b": 10, "t": 50},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": []
}

data_dict = {
    "x": list(coord["WH_LONG"]),
    "y": list(coord["WH_LAT"]),
    "mode": "markers",
    "text": list(coord["WELL_NAME"]),
    }
fig_dict["data"].append(data_dict)

for year in years:
    frame = {"data": [], "name": str(year)}
    dataset_by_year = coord[coord["SH_CDATE"] == year]

    data_dict = {
        "x": list(dataset_by_year["WH_LONG"]),
        "y": list(dataset_by_year["WH_LAT"]),
        "mode": "markers",
        "text": list(dataset_by_year["WELL_NAME"]),

    }
    frame["data"].append(data_dict)
    fig_dict["frames"].append(frame)
    slider_step = {"args": [
        [year],
        {"frame": {"duration": 300, "redraw": False},
         "mode": "immediate",
         "transition": {"duration": 300}}
    ],
        "label": year,
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)

fig_dict["layout"]["sliders"] = [sliders_dict]
fig = go.Figure(fig_dict)
fig.show()
