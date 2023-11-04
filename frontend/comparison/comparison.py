import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import csv
import json
import os

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {"graphBackground": "#F5F5F5", "background": "#ffffff", "text": "#000000"}

criteria = [{'label': 'Score', 'value': 'Score'},
            {'label': 'Privacy', 'value': 'Privacy'},
            {'label': 'Crowd Level', 'value': 'Crowd Level'},
            {'label': 'Comfort', 'value': 'Comfort'},
            {'label': 'Scenery', 'value': 'Scenery'},
            {'label': 'Ease of Access', 'value': 'Ease of Access'}
]

### TO ADD TO past_simulations.py
# dcc.Location(id="url", refresh=False),  # Location component for URL handling
#     html.A("Go to Page 2", href="/comparison-page"),


app.layout = html.Div([
    dcc.Link(html.Button('Go Back to Previous Page', href='/past-simulation-page', refresh = True)), 
    html.H1("Model Score Comparison"),
    dcc.Location(id='/comparison-page', refresh=False),  # Location component for URL handling
    dcc.Dropdown(
        id='criteria-dropdown',
        options = criteria,
        value='Score'
    ),
    html.Div(id='comparison-results'),
])


@app.callback(Output('comparison-results', 'children'),
              Input('/past-simulation-page', 'search'),
              Input('criteria-dropdown', 'value'))

def perform_comparison(n_clicks, model1, model2, criteria):
    if n_clicks > 0 and model1 and model2 and criteria:
        # Load JSON data for the selected models
        with open(os.path.join(data_directory, model1 + '.json')) as f1:
            data1 = json.load(f1)
        with open(os.path.join(data_directory, model2 + '.json')) as f2:
            data2 = json.load(f2)
        # Extract the criteria scores
        score1 = data1.get(criteria, 0)
        score2 = data2.get(criteria, 0)

        # Create a comparison result message
        comparison_result = f"{model1} vs. {model2} based on {criteria}: {score1} vs. {score2}"

        return html.H2(comparison_result)

if __name__ == '__main__':
    app.run_server(debug=False)
