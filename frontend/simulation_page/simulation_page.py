import os
import sys
import dash 
import random
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc 

from dash import html, dcc, Input, Output, State
from datetime import datetime, timedelta

current_directory = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_directory, '..', 'data', 'simulation csv', '234@normal.csv')
data = pd.read_csv(csv_path)
data['timestamp'] = pd.to_datetime(data['timestamp'])
levels = list(data['level'].unique()) # identifying the levels that users have chosen to simulate

# If the user only inputs data for one level, the graph would occupy the whole screen else just half the screen
if len(levels) == 1:
    x = '100%'
    y = '100%'
else:
    x = "48%"
    y = "48%"

# For the slider
hour_map = {
    0: '00:00',
    1: '01:00',
    2: '02:00',
    3: '03:00',
    4: '04:00',
    5: '05:00',
    6: '06:00',
    7: '07:00', 
    8: '08:00',
    9: '09:00',
    10: '10:00',
    11: '11:00',
    12: '12:00',
    13: '13:00',
    14: '14:00',
    15: '15:00',
    16: '16:00',
    17: '17:00',
    18: '18:00',
    19: '19:00',
    20: '20:00',
    21: '21:00',
    22: '22:00',
    23: '23:00'
}

# Bar Graphs for 'Overall Change in Occupancy'
# def create_level_layout(level, data):
#     indexes_level = [index for index, value in enumerate(data['level']) if value == level]
#     df_level = data.iloc[indexes_level].sort_values(by='section')
#     fig_level = px.bar(df_level, x='section', y='utilization_rate', title=f'Level {level}', color='utilization_rate',
#                        color_discrete_sequence='rgb(77, 232, 232)',
#                        text=df_level['utilization_rate'],
#                        hover_data={'utilization_rate': True})
#     fig_level.update_traces(marker=dict(color='rgb(77, 232, 232)')) # To ensure that the graph color would be red and green
#     fig_level.update_layout(hovermode='closest')

#     # Create the layout for the given level
#     tab_bp_layout_level = html.Div([
#         dcc.Graph(id=f'Graph_{level}', figure=fig_level),
#         dbc.Button(f"Full Graph (Level {level})", id=f"button_lvl{level}", n_clicks=0, style={'float': 'right', 'background-color': '#003D7C'}),
#         html.Div(id=f"popup-content{level}", children=[
#             dbc.Modal([
#                 dbc.ModalHeader(f"Level {level}", style={'background-color': '#003D7C', 'font-size': '24px', 'font-weight': 'bold'}),
#                 dbc.ModalBody([
#                     dcc.Graph(id=f'Graph_{level}', figure=fig_level, style={'width': '100%', 'height': '100%'}),
#                 ], style={'background-color': 'white'}),
#             ], id=f"popup{level}", fullscreen=True, centered=True)
#         ])
#     ], style={'width': x, 'height': y, 'display': 'inline-block'})
#     return tab_bp_layout_level

def create_level_layout(level, hour, data):
    indexes_level = [index for index, value in enumerate(data['level']) if value == level and data['timestamp'][index].hour == hour]
    df_level = data.iloc[indexes_level].sort_values(by='section')
    df_level = df_level.dropna(subset=['utilization_rate'])
    grouped_data = df_level.groupby(['section'])['utilization_rate'].mean().reset_index()
    fig_level = px.bar(grouped_data, x='section', y='utilization_rate', title=f'Level {level} - Hour {hour}', color='utilization_rate',
                       color_discrete_sequence='rgb(77, 232, 232)',
                       text=grouped_data['utilization_rate'],
                       hover_data={'utilization_rate': True})
    fig_level.update_traces(marker=dict(color='rgb(77, 232, 232)'))  # To ensure that the graph color would be red and green
    fig_level.update_layout(yaxis_range=[0, 1])
    fig_level.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_level.update_layout(hovermode='closest')

    # Create the layout for the given level and hour
    tab_bp_layout_level = html.Div([
        dcc.Graph(id=f'Graph_{level}', figure=fig_level),
        dbc.Button(f"Full Graph (Level {level} - Hour {hour})", id=f"button_lvl{level}", n_clicks=0,
                   style={'float': 'right', 'background-color': '#003D7C'}),
        html.Div(id=f"popup-content{level}", children=[
            dbc.Modal([
                dbc.ModalHeader(f"Level {level} - Hour {hour}", style={'background-color': '#003D7C', 'font-size': '24px', 'font-weight': 'bold'}),
                dbc.ModalBody([
                    dcc.Graph(id=f'Graph_{level}', figure=fig_level, style={'width': '100%', 'height': '100%'}),
                ], style={'background-color': 'white'}),
            ], id=f"popup{level}", fullscreen=True, centered=True)
        ])
    ], style={'width': x, 'height': y, 'display': 'inline-block'})
    return tab_bp_layout_level


level_layouts = {level: create_level_layout(level, 9, data) for level in levels}
tab1_content = html.Div([
    dcc.Slider(
        id = 'my-slider',
        marks = hour_map,
        value = 9, 
        step = None
    ),
    html.Div(
        id = 'slider-output-container' # my-slider output should contain the graphs 
    )
])

# Sample data for four library floors
floors = ["Floor 3", "Floor 4", "Floor 5", "Floor 6"]
time_range = [datetime(2023, 1, 1, 9, 0), datetime(2023, 1, 2, 8, 0)]
time_interval = timedelta(minutes=15)
timestamps = [time_range[0] + i * time_interval for i in range(int((time_range[1] - time_range[0]).total_seconds() / time_interval.total_seconds()))]

def generate_bell_curve(center, std_dev, length, floor_name):
    x = np.linspace(center - 3 * std_dev, center + 3 * std_dev, length)
    y = 1 / (std_dev * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - center) / std_dev) ** 2)
    return y, floor_name

peak_times = [datetime(2023, 1, 1, 11, 0), datetime(2023, 1, 1, 10, 0), datetime(2023, 1, 1, 14, 0), datetime(2023, 1, 1, 16, 0)]
std_deviation = 2  

# Time series plot for 'Occupancy Overtime'
traces = []

for i, peak_time in enumerate(peak_times):
    curve_data, floor_name = generate_bell_curve(peak_time.timestamp(), std_deviation, len(timestamps), floors[i])
    trace = go.Scatter(
        x=timestamps,
        y=curve_data,
        mode='lines',
        name=floor_name,
        line_shape='spline',
        opacity=1  # Set the opacity to control visibility
    )
    traces.append(trace)

layout = go.Layout(
    title='Central Library TimeSeries Plot by Floor',
    xaxis=dict(
        title='Time',
        range=[time_range[0], time_range[1]],
        rangeselector=dict(
            buttons=list([
                dict(count=6, label='6H', step='hour', stepmode='backward'),
                dict(count=1, label='1D', step='day', stepmode='backward'),
            ])
        ),
        type='date',
        showline=False,
        hoverformat='%H:%M'
    ),
    yaxis=dict(
        title='Occupancy Rate'
    ),
    legend=dict(
        orientation='h'
    )
)

layout['xaxis']['tickformat'] = '%H:%M'

tab_oo_layout = html.Div([
    dcc.Graph(figure={'data': traces, 'layout': layout}, id='tab-oo-layout'),
])

# The overall skeleton
button_style = {'backgroundColor': 'black', 'color': 'white', 'borderRadius': '15px', 'margin': '5px'}
tab_style = {'padding': '10px', 'background-color': '#003D7C', 'color':'white', 'fontWeight':'bold', 'fontSize':'20px'}

sp_layout = html.Div([
    html.A(html.Button("Home", className="home-btn", id="home-button"), href="/"),
    html.Button(dcc.Link(children=[html.Img(src=r'assets/close.png', style={'width': '17px', 'height': '17px'})], href = '/run_simulation', style = {'text-decoration':'none'}), 
                id="button_close", n_clicks=0, style={'border-radius': '5px', 'float': 'right'}),
    html.Div([
        dcc.Tabs(id='tabs', value='tab-1', children=[
            dcc.Tab(label='Overall Change in Occupancy', value='tab-1', style= tab_style),
            dcc.Tab(label='Occupancy overtime', value='tab-2', style= tab_style)
        ]),
        html.Div(tab1_content, id='tab-content')
    ])], style={'padding': '10px'})

