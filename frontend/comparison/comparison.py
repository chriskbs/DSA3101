import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import csv
import json
import os

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {"graphBackground": "#F5F5F5", "background": "#ffffff", "text": "#000000"}


model_2 = {
    "name": "random submission2",
    "score": 50,
    "privacy": 20,
    "crowd level": 80,
    "comfort": 60,
    "scenery": 76,
    "lighting": 89,
    "ease of access": 90
}

model_3 = {
    "name": "random submission3",
    "score": 55,
    "privacy": 30,
    "crowd level": 70,
    "comfort": 65,
    "scenery": 72,
    "lighting": 85,
    "ease of access": 88
}

models_data = [model_2, model_3]

criteria = [key for key in model_2.keys() if key != 'name']

differences = {criterion: model_2[criterion] - model_3[criterion] for criterion in criteria}

def create_bar_graph():
    fig = px.bar(
        x=criteria,
        y=[differences[criterion] for criterion in criteria],
        labels={'x': 'Criteria', 'y': 'Difference'},
        title=f"{model_2['name']} vs. {model_3['name']} Differences"
    )
    return fig

app.layout = html.Div([
    html.H1("Model Comparison"),
    html.Table([
        html.Tr([html.Th("Criterion"), html.Th("Model 2"), html.Th("Model 3"), html.Th("Difference")]),
    ] + [
        html.Tr([html.Td(criterion), html.Td(model_2[criterion]), html.Td(model_3[criterion]), html.Td(differences[criterion])])
        for criterion in criteria
    ]),
    # Button to toggle between models
    html.Button("Toggle Model", id="toggle-button"),

    # Bar graph
    dcc.Graph(id='model-differences', figure= create_bar_graph()),

    dcc.Input(style={"margin-left": "15px"})
])

@app.callback(
    Output('model-differences', 'figure')
)
def toggle_models(n_clicks):
    global selected_model
    if n_clicks and n_clicks % 2 == 0:
        selected_model = model_2
        button_text = "Toggle to Model 3"
    else:
        selected_model = model_3
        button_text = "Toggle to Model 2"

    fig = create_bar_graph()

    return fig, button_text

if __name__ == '__main__':
    app.run_server(debug=False)
