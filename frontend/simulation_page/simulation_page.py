import dash
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from datetime import datetime, timedelta
import random
import plotly.graph_objs as go
import os
import numpy as np
import requests
import sys
app_dir_path = os.path.dirname(__file__)
sys.path.append(app_dir_path)


data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'dummy_data','trial_data_1lvl.csv'))
# data = app.state['simulation_data']
levels = list(data['level'].unique()) # identifying the levels that users have chosen to simulate
timestamps_column = data['timestamp']
timestamps_column = pd.to_datetime(timestamps_column)
timestamps_column = timestamps_column.dt.time
data['timestamp'] = timestamps_column
current = datetime.strptime('10:20:00', '%H:%M:%S') # update 10:20:00 accordingly to slider value
current_time = current.time()
# print(data['timestamp'][1] == current_time)

# If the user only inputs data for one level, the graph would occupy the whole screen else just half the screen
if len(levels) == 1:
    x = '100%'
    y = '100%'
else:
    x = "48%"
    y = "48%"

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
    24: '23:00',
    25: '00:00',
}

def create_level_layout(level, data):
    indexes_level = [index for index, value in enumerate(data['level']) if value == level]
    df_level = data.iloc[indexes_level].sort_values(by='section')
    fig_level = px.bar(df_level, x='section', y='utilization_rate', title=f'Level {level}', color='utilization_rate',
                       color_discrete_sequence='rgb(77, 232, 232)',
                       text=df_level['utilization_rate'],
                       hover_data={'utilization_rate': True})
    fig_level.update_traces(marker=dict(color='rgb(77, 232, 232)')) # To ensure that the graph color would be red and green
    fig_level.update_layout(hovermode='closest')

    # Create the layout for the given level
    tab_bp_layout_level = html.Div([
        dcc.Graph(id=f'Graph_{level}', figure=fig_level),
        dbc.Button(f"Full Graph (Level {level})", id=f"button_lvl{level}", n_clicks=0, style={'float': 'right', 'background-color': '#003D7C'}),
        html.Div(id=f"popup-content{level}", children=[
            dbc.Modal([
                dbc.ModalHeader(f"Level {level}", style={'background-color': '#003D7C', 'font-size': '24px', 'font-weight': 'bold'}),
                dbc.ModalBody([
                    dcc.Graph(id=f'Graph_{level}', figure=fig_level, style={'width': '100%', 'height': '100%'}),
                ], style={'background-color': 'white'}),
            ], id=f"popup{level}", fullscreen=True, centered=True)
        ])
    ], style={'width': x, 'height': y, 'display': 'inline-block'})
    return tab_bp_layout_level


level_layouts = {level: create_level_layout(level, data) for level in levels}
tab1_content = html.Div([
    dcc.Slider(
        id = 'my-slider',
        marks = hour_map,
        value = 0, 
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


button_style = {'backgroundColor': 'black', 'color': 'white', 'borderRadius': '15px', 'margin': '5px'}
tab_style = {'padding': '10px', 'background-color': '#003D7C', 'color':'white', 'fontWeight':'bold', 'fontSize':'20px'}
# # The overall skeleton
sp_layout = html.Div([
    html.Button(dcc.Link("Home", href = '/', style = {'text-decoration':'none'}), 
                id="button_home", n_clicks=0, style={'background-color': 'light grey', 'border-radius': '5px'}),
    html.Button(dcc.Link(children=[html.Img(src='assets/close.png', style={'width': '17px', 'height': '17px'})], href = '/run_simulation', style = {'text-decoration':'none'}), 
                id="button_close", n_clicks=0, style={'border-radius': '5px', 'float': 'right'}),
    html.Div([
        dcc.Tabs(id='tabs', value='tab-1', children=[
            dcc.Tab(label='Overall Change in Occupancy', value='tab-1', style= tab_style),
            dcc.Tab(label='Occupancy overtime', value='tab-2', style= tab_style)
        ]),
        html.Div(id='tab-content')
    ])], style={'padding': '10px'})

# # Create callback functions for the "Full Graph" buttons for each level
# for level in levels:
#     @app.callback(
#         Output(f'popup-content{level}', 'style'),
#         Output(f'popup{level}', 'is_open'),
#         Input(f'button_lvl{level}', 'n_clicks'),
#         State(f'popup{level}', 'is_open')
#     )
#     def toggle_popup(n1, is_open, level=level):
#         if n1:
#             return {"display": "block"}, not is_open
#         return {"display": "none"}, is_open

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

# Callback for switching between tabs and displaying the full graphs
# @app.callback(
#     Output('tab-content', 'children'),
#     Input('tabs', 'value')
# )
# def update_content(tab):
#     if tab == 'tab-1':
#         return [level_layouts[level] for level in levels]
#     else:
#         return tab_oo_layout


# Callback for connecting API and switching between graphs
# @app.callback(
#     Output('tab-content', 'children'),
#     Input('tabs', 'value'),
#     Input('run-simulation-button', 'n_clicks'),
#     prevent_initial_call=True
# )
# def update_content(tab, n_clicks):
#     if n_clicks is None:
#         raise PreventUpdate

#     if tab == 'tab-1':
#         return [level_layouts[level] for level in levels]
#     else:
#         results_url = 'http://127.0.0.1:5000/results'

#         # Make a GET request to the API
#         response = requests.get(results_url)

#         if response.status_code == 200:
#             # Assume the API returns a JSON object with the necessary information
#             result = response.json()

#             return [
#                 tab_oo_layout,
#                 html.Div(f"Result CSV file: {result['result_csv']}", style={'color': 'navy', 'font-size': '18px'}),
#                 html.Div(f"Result JSON file: {result['result_json']}", style={'color': 'navy', 'font-size': '18px'})
#             ]
#         else:
#             return [html.Div(f"Error: {response.status_code}\n{response.json()}", style={'color': 'red', 'font-size': '18px'})]

# if __name__ == '__main__':
#     app.run_server(debug=True)
