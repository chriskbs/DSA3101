import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import csv

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

qualities = [
    "Privacy",
    "Crowd level",
    "Comfort",
    "Scenery",
    "Lighting",
    "Ease of finding seats",
    ]

data_input = pd.read_csv("...") #Fill in link to data
test = data_input["Simulation"].unique()
options = [{"label": i, "value": i} for i in test]

def total_score(model):
    return sum(model["changeInOccupancy"])


app.layout = html.Div([
    html.H1("Model Score Comparison"),
    
    html.Div([
        # Dropdown for selecting the first model
        dcc.Dropdown(
            id='model-dropdown-1',
            options = options,
        ),
        # Dropdown for selecting the second model
        dcc.Dropdown(
            id='model-dropdown-2',
            options = options,
        ),
    ], style={'display': 'flex', 'width': '50%'}),
    
    # Display the scores and the difference
    html.Div(id='score-difference')
])

@app.callback(
    Output('score-difference', 'children'),
    [Input('model-dropdown-1', 'value'), Input('model-dropdown-2', 'value')]
)
def update_score_difference(model1, model2):
    score1 = data_input.get(model1, 0)
    score2 = data_input.get(model2, 0)
    
    if score1 > score2:
        best_model = model1
    elif score1 < score2:
        best_model = model2
    else:
        best_model = "None (Tie)"
    
    difference = abs(score1 - score2)
    
    return f"{model1} score: {score1}, {model2} score: {score2}, Difference: {difference}, Best Model: {best_model}"

if __name__ == '__main__':
    app.run_server(debug=True)
