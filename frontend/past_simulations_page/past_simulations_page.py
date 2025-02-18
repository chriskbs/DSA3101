import dash
from dash import Dash, html, dcc, Input, Output, ctx, dcc, State, dash_table
import dash_daq as daq
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import os
import json

# data_directory = os.path.join(os.path.dirname(__file__), 'data') #'../data'
data_directory = r"data/simulation json/" 

# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# we need this to keep track of the names that were deleted
static_simulation_names = []
# add names inside the data directory that are not in the current list
def add_json_filenames(current_list, directory):
    for fname in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, fname)):
            name, extension = os.path.splitext(fname)
            if extension == '.json':
                if name not in current_list:
                    current_list.append(name)
    return current_list

static_simulation_names = add_json_filenames(static_simulation_names, data_directory)
simulation_names = static_simulation_names.copy()
      
def create_dropdown(position="left"):
    dropdown = dcc.Dropdown(
        id=f'dropdown_{position}',
        options=[{'label': name, 'value': name} for name in simulation_names],
        placeholder='Select a simulation...',
        style={'vertical-align': 'middle'}
    )
    return html.Div([
        dropdown,
    ],
    style={'display': 'inline-block', 'width': '40%', 'vertical-align': 'middle'})

compare_banner = html.Div([
    create_dropdown("left"),
    html.H3('VS', style={'display': 'inline-block', 'text-align': 'center', 'width': '5%', 'vertical-align': 'middle'}),
    create_dropdown("right"),
    html.Div([
        html.A(html.Button('Compare', 
                     id='compare-button', n_clicks=0, style={'width': '100%'}),href = '/compare', style = {'text-decoration':'none'}),
    ],
    style={'padding': '5px', 'width': '15%', 'vertical-align': 'middle', 'height': '10%', 'display': 'inline-block'})
    
],
style={'border': '1px solid black', 'padding': '10px'})
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
    scores_style = {'display': 'inline-block', 'width': '33.3%', 'text-align': 'left'}
    formatted_score = "{:.2f}".format(simulation_scores["score"])
    formatted_privacy = "{:.2f}".format(simulation_scores["privacy"])
    formatted_crowd_level = "{:.2f}".format(simulation_scores["crowd level"])
    formatted_comfort = "{:.2f}".format(simulation_scores["comfort"])
    formatted_scenery = "{:.2f}".format(simulation_scores["scenery"])
    formatted_lighting = "{:.2f}".format(simulation_scores["lighting"])
    formatted_ease_of_access = "{:.2f}".format(simulation_scores["ease of access"])
    return html.Div([
        html.H5(f'Score: {formatted_score}', style=scores_style),
        html.H5(f'Privacy: {formatted_privacy}', style=scores_style),
        html.H5(f'Crowd Level: {formatted_crowd_level}', style=scores_style),
        html.H5(f'Comfort: {formatted_comfort}', style=scores_style),
        html.H5(f'Scenery: {formatted_scenery}', style=scores_style),
        html.H5(f'Lighting: {formatted_lighting}', style=scores_style),
        html.H5(f'Ease of Access: {formatted_ease_of_access}', style=scores_style),
    ],
    style={'display': 'inline-block', 'width': '100%', 'padding': '10px'})
    
    
def create_row(simulation_name, actual):
    hidden = simulation_name not in actual
    delete_button = html.Button(
        children=[html.Img(src='assets/delete.svg', alt='Button Image', style={'width': '50px', 'height': '100px'})],
        id=f'delete-button-{simulation_name}',
        style={'width': '100%', 'height': '100%'}
    )
    if hidden:
        return html.Div([delete_button],
                    style={'vertical-align': 'middle'},
                    id=f'row-{simulation_name}',
                    hidden=hidden
                )
    simulation = html.Div(
        children=[
            html.Div([
                html.H3(dcc.Link(f"{simulation_name}", href = f'/simulation_page/{simulation_name}'), style={'padding': '10px', "text-decoration": "underline"}), # changed 6/11 linking to simulation page 
                simulation_scores(simulation_name),
            ], style={'display': 'inline-block', 'width': '85%', 'vertical-align': 'middle'}),
            html.Div([
                html.Button(
                    dcc.Link(children=[html.Img(src='assets/view.png', style={'width': '100px', 'height': '100px'})], href = f'/simulation_page/{simulation_name}'), # changed 6/11 linking to simulation page 
                    id=f'view-button-{simulation_name}',
                    style={'width': '90%', 'height': '100%'}
                )
            ], style={'display': 'inline-block', 'width': '15%', 'vertical-align': 'middle', 'height': '100%'})
        ],
        style={'display': 'inline-block', 'width': '85%', 'margin': '0 auto', 'border': '1px solid black', 'vertical-align': 'middle'}
    )
    new_row = html.Div(
        children=[
            simulation,
            html.Div([
                dbc.Col(
                    delete_button,
                    width={"size": 8, "offset": 2}
                )
            ], style={'display': 'inline-block', 'width': '15%', 'vertical-align': 'middle'}),
        ],
        style={'vertical-align': 'middle'}
    )
    new_row_with_Br = html.Div(
        children=[
            new_row,
            html.Br()
        ],
        style={'vertical-align': 'middle'},
        id=f'row-{simulation_name}',
    )
    return new_row_with_Br

delete_modal = dbc.Modal(
    [
        dbc.ModalHeader("Delete Confirmation"),
        dbc.ModalBody("Are you sure you want to delete this simulation?"),
        dbc.ModalFooter([
            dbc.Button("Delete", id="confirm-delete-button", color="danger"),
            dbc.Button("Cancel", id="cancel-delete-button"),
        ]),
        dcc.Store(id='current-simulation-name')
    ],
    id="delete-modal",
    is_open=False,
)

past_simulations = html.Div(
    id='past-simulations',
    children=[html.Hr()]+[create_row(simulation_name, simulation_name) for simulation_name in simulation_names],
    style={'overflow': 'scroll', 'height': '90%', 'width': '100%'}
)

psp_layout = html.Div([
    html.Div([
        html.A(html.Button("Home", className="home-btn", id="home-button"), href="/"),
    ], style={'position': 'absolute', 'top': '20px', 'left': '20px'}),  # changed 6/11 included home page button 

    delete_modal,
    html.Div([
        compare_banner,
        past_simulations,
    ],
    style={'width': '1200px', 
           'margin': '0 auto',
           'border': '1px solid black',
           'padding': '10px',
           'height': '100%',}) 
], 
style={'padding': '40px', 'height': '100vh', 'width': '100vw', 'overflow': 'scroll'})

# # Add a callback to show the delete modal when a delete button is clicked
# @app.callback(
#     Output("delete-modal", "is_open", allow_duplicate=True),
#     Output("current-simulation-name", "data", allow_duplicate=True), 
#     [Input(f"delete-button-{simulation_name}", "n_clicks") for simulation_name in simulation_names],
#     prevent_initial_call=True
# )
# def toggle_modal(*args):
#     ctx = dash.callback_context
#     if not ctx.triggered:
#         return False, None
#     button_id = ctx.triggered[0]["prop_id"].split(".")[0]
#     for simulation_name in static_simulation_names:
#         if button_id == f'delete-button-{simulation_name}':
#             return True, simulation_name
#     return False, None

# @app.callback(
#     [Output(f'row-{simulation_name}', 'hidden') for simulation_name in simulation_names],
#     Output('dropdown_left', 'options'),
#     Output('dropdown_right', 'options'),
#     Output('current-simulation-name', 'data', allow_duplicate=True),
#     Output("delete-modal", "is_open", allow_duplicate=True),
#     Input("confirm-delete-button", "n_clicks"),
#     Input("cancel-delete-button", "n_clicks"),
#     [State(f'row-{simulation_name}', 'hidden') for simulation_name in simulation_names],
#     State('current-simulation-name', 'data'),
#     prevent_initial_call=True
# )
# def delete_rows(*args):
#     ctx = dash.callback_context
#     button_id = ctx.triggered[0]['prop_id'].split('.')[0]
#     output = []
#     new_simulation_names = []
#     current_simulation_name = args[-1]
#     if button_id == "confirm-delete-button":
#         for simulation_name in static_simulation_names:
#             if os.path.exists(os.path.join(data_directory, simulation_name + '.json')):
#                 if simulation_name == current_simulation_name:
#                     os.remove(os.path.join(data_directory, simulation_name + '.json'))
#                     output.append(True)
#                 else:
#                     new_simulation_names.append(simulation_name)
#                     output.append(False)
#             else:
#                 output.append(True)
#     if button_id == "cancel-delete-button":
#         for simulation_name in static_simulation_names:
#             if os.path.exists(os.path.join(data_directory, simulation_name + '.json')):
#                 new_simulation_names.append(simulation_name)
#                 output.append(False)
#             else:
#                 output.append(True)
#     new_options = [{'label': name, 'value': name} for name in new_simulation_names]
#     global simulation_names
#     simulation_names = new_simulation_names.copy()
#     output.append(new_options)
#     output.append(new_options)
#     output.append(None)
#     output.append(False)
#     return output

# if __name__ == '__main__':
#     app.run_server(debug=True)