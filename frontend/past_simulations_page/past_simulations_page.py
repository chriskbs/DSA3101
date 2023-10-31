import dash
from dash import Dash, html, dcc, Input, Output, ctx, dcc, State, dash_table
import dash_daq as daq
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import os
import json

data_directory = '../data'

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

simulation_names = []

for fname in os.listdir(data_directory):
    if os.path.isfile(os.path.join(data_directory, fname)):
        name, extension = os.path.splitext(fname)
        if extension == '.json':
            simulation_names.append(name)

print(simulation_names)        
def create_dropdown(position="left"):
    dropdown = dcc.Dropdown(
        id=f'dropdown_{position}',
        options=[{'label': name, 'value': name} for name in simulation_names],
        value=simulation_names[0],
        style={'display': 'inline-block', 'width': '30%'}
    )
    return dropdown

compare_banner = html.Div([
    create_dropdown("left"),
    html.H3('VS', style={'display': 'inline-block', 'width': '10%'}),
    create_dropdown("right"),
    html.Button('Compare', id='compare-button', n_clicks=0, style={'display': 'inline-block', 'width': '10%'}),
])
"""
{
    "name": "dummy",
    "score": 95,
    "privacy": 70,
    "crowd level": 80,
    "comfort": 90,
    "scenery": 100,
    "lighting": 80,
    "ease of access": 90,
}
"""
def simulation_scores(simulation_name):
    with open(os.path.join(data_directory, simulation_name + '.json')) as f:
        simulation_scores = json.load(f)
    scores_style = {'display': 'inline-block', 'width': '33%', 'text-align': 'left'}
    return html.Div([
        html.H5(f'Score:{simulation_scores["score"]}', style=scores_style),
        html.H5(f'Privacy:{simulation_scores["privacy"]}', style=scores_style),
        html.H5(f'Crowd Level:{simulation_scores["crowd level"]}', style=scores_style),
        html.H5(f'Comfort:{simulation_scores["comfort"]}', style=scores_style),
        html.H5(f'Scenery:{simulation_scores["scenery"]}', style=scores_style),
        html.H5(f'Lighting:{simulation_scores["lighting"]}', style=scores_style),
        html.H5(f'Ease of Access:{simulation_scores["ease of access"]}', style=scores_style),
    ],
    style={'display': 'inline-block', 'width': '100%', 'padding': '10px'})
    
    
def create_row(simulation_name):
    simulation = html.Div(
        children=[
            html.H3(simulation_name, style={'padding': '10px'}),
            simulation_scores(simulation_name),
        ],
        style={'display': 'inline-block', 'width': '80%', 'margin': '10px auto', 'border': '1px solid black'}
    )
    delete_button = html.Button(
        children='Delete',
        id=f'delete-button-{simulation_name}',
        n_clicks=0,
        style={'display': 'inline-block', 'width': '20%'}
    )
    new_row = html.Div(
        children=[
            simulation,
            delete_button,
        ]
    )
    return new_row

past_simulations = html.Div(
    children=[create_row(simulation_name) for simulation_name in simulation_names]
)

app.layout = html.Div([
        html.Div([
        compare_banner,
        past_simulations,
    ],
    style={'display': 'inline-block', 'width': '100%', 'margin': '10px auto', 'border': '1px solid black'})
], 
style={'height': '100vh', 'width': '100vw', 'overflow': 'scroll'})
if __name__ == '__main__':
    app.run_server(debug=True)