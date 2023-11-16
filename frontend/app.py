import os
import csv
import json
import dash
import base64
import requests
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, ctx, dcc, dash_table
from dash.dependencies import Input, Output, State 
from datetime import datetime 
import requests
import pandas as pd

import input_page.input_page as ip
import home_page.home_page as hp
import past_simulations_page.past_simulations_page as psp
import run_simulation.runsimulation as rs 
import simulation_page.simulation_page as sp 
import loading_page.loading as load
import comparison.comparison as compare

inputs_directory = r'data/seat arrangement/'

app = dash.Dash(__name__, suppress_callback_exceptions = True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config['prevent_initial_callbacks'] = 'initial_duplicate'

app.layout = html.Div(children = [dcc.Location(id = "url", refresh = False),
                                    html.Div(id = "output-div")
                                ])
simulation_csv_fname = os.path.join('simulation_page/dummy_data','trial_data_1lvl.csv')

# Callbacks for input page --------------------------------------------------------------------------------------------------------------------------------------------
@app.callback(
    [Output(f'count-text-{seat_type}', 'value', allow_duplicate=True) for seat_type in ip.seat_types_ip],
    Output('table_balanced_seats', 'data', allow_duplicate=True),
    Output('total_seats', 'children', allow_duplicate=True),
    [Input(f'plus-button-{seat_type}', 'n_clicks') for seat_type in ip.seat_types_ip],
    [Input(f'minus-button-{seat_type}', 'n_clicks') for seat_type in ip.seat_types_ip],
    [Input(f'count-text-{seat_type}', 'value') for seat_type in ip.seat_types_ip],
    prevent_initial_call=True
)
def update_counts(*clicks_and_data):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    # raise Exception(changed_id)
    seat_type = ''
    if changed_id.startswith('plus-button-'):
        seat_type = changed_id.replace('plus-button-', '').replace('.n_clicks', '')
    elif changed_id.startswith('minus-button-'):
        seat_type = changed_id.replace('minus-button-', '').replace('.n_clicks', '')
    elif changed_id.startswith('count-text-'):
        seat_type = changed_id.replace('count-text-', '').replace('.value', '')
    # else:
    #     return (0, 0, 0, 0, 0, 0, 0, 0, 0, data[title], f'Total seats: {find_total_seats(title, data, seats)}')
    count = ctx.inputs[f'count-text-{seat_type}.value']
    new_count, new_data = ip.update_count(title, count, seat_type)
    ctx.inputs[f'count-text-{seat_type}.value'] = new_count
    count_text_values = [v for k, v in ctx.inputs.items() if k.startswith('count-text-')]
    count_text_values.append(new_data)
    count_text_values.append(f'Total seats: {ip.find_total_seats(title, ip.data, ip.seats)}')
    # raise Exception(count_text_values)
    return tuple(count_text_values)

def update_level():
    global title
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    next_button = False
    back_button = False
    submit_button = True
    if changed_id == 'next-button.n_clicks':
        if title == "Level 3":
            title = "Level 4"
        elif title == "Level 4":
            title = "Level 5"
        elif title == "Level 5":
            title = "Level 6 Central Library"
        elif title == "Level 6 Central Library":
            title = "Level 6 Chinese Library"
            next_button = True
            submit_button = False
    elif changed_id == 'back-button.n_clicks':
        if title == "Level 6 Chinese Library":
            title = "Level 6 Central Library"
        elif title == "Level 6 Central Library":
            title = "Level 5"
        elif title == "Level 5":
            title = "Level 4"
        elif title == "Level 4":
            title = "Level 3"
            back_button = True
    return next_button, back_button, submit_button

title = ip.title
@app.callback(
    Output("title", "children"),
    [Output(f'count-text-{seat_type}', 'value', allow_duplicate=True) for seat_type in ip.seat_types_ip],
    Output('table_balanced_seats', 'data', allow_duplicate=True),
    Output('total_seats', 'children', allow_duplicate=True),
    Output('total_seats_title', 'children'),
    Output("next-button", "hidden"),
    Output("back-button", "hidden"),
    Output("submit-button", "hidden"),
    Input("next-button", "n_clicks"),
    Input("back-button", "n_clicks"),
    # Input("title", "children"),
    prevent_initial_call=True
)
def update_title(n_clicks, n_clicks2):
    output = []
    global title
    next_button, back_button, submit_button = update_level()
    output.append(title)
    for seat_type in ip.seat_types_ip:
        output.append(ip.find_seat_count(title, seat_type, ip.data))
    output.append(ip.data[title])
    output.append(f'Total seats: {ip.find_total_seats(title, ip.data, ip.seats)}')
    output.append(f'Seats selected for {title}')
    output.append(next_button)
    output.append(back_button)
    output.append(submit_button)
    return output

@app.callback(
    Output('submission-name-modal', 'is_open', allow_duplicate=True),
    Input('submit-button', 'n_clicks'),
    State('submit-button', 'hidden'),
    prevent_initial_call=True
)
def toggle_modal(submit_clicks, submit_button_hidden):
    if submit_button_hidden == True:
        return False
    else:
        return True

@app.callback(
    Output('url', 'pathname'),
    Output('submission-name-input-error', 'hidden'),
    Output('submission-name-modal', 'is_open', allow_duplicate=True),
    Input('confirm-button', 'n_clicks'),
    State('submission-name-input', 'value'),
    prevent_initial_call=True
)
def confirm_submission(n_clicks, filename):
    # checks inputs folder if any file has the same name
    for fname in os.listdir(inputs_directory):
        if os.path.isfile(os.path.join(inputs_directory, fname)):
            name, extension = os.path.splitext(fname)
            if extension != '.json':
                continue
            elif name == filename:
                # prompt user to change name
                return dash.no_update, False, True
    # if no, save the file to inputs folder
    if not n_clicks:
        return dash.no_update, True, False
    filepath = os.path.join(inputs_directory, f"{filename}.json")
    new_data = {}
    for level in ip.data:
        new_data[level] = []
        for seat in ip.data[level]:
            new_data[level].append({
                "seat_type": seat["Seat Type"],
                "count": seat["Count"]
            })
    
    output = {
        "submission_name": filename,
        "levels": [
            {
                "level": 'Level 3',
                "sections": new_data['Level 3']
            },
            {
                "level": 'Level 4',
                "sections": new_data['Level 4']
            },
            {
                "level": 'Level 5',
                "sections": new_data['Level 5']
            },
            {
                "level": 'Level 6 Central Library',
                "sections": new_data['Level 6 Central Library']
            },
            {
                "level": 'Level 6 Chinese Library',
                "sections": new_data['Level 6 Chinese Library']
            }
        ]
    }
    with open(filepath, 'w') as f:
        json.dump(output, f, indent=4)
    return '/run_simulation', True, False

# Connecting APIs

@app.callback(
    Output('url', 'pathname', allow_duplicate=True),
    Input('run_sim', 'n_clicks'),
    Input('submission-dropdown', 'value'),
    Input('period-dropdown', 'value'),
    Input('upload-data', 'contents'),
    prevent_initial_call=True
)

def submit_inputs(n_clicks, seat_arrangement_file, period_file, uploaded_file):
    print(n_clicks)
    if not n_clicks:
        return dash.no_update
    seat_arrangement_file_path = os.path.join(rs.json_files_path, seat_arrangement_file)
    if period_file:
        period_file_path = os.path.join(rs.csv_files_path, period_file)
    elif uploaded_file:
        content_type, content_string = uploaded_file.split(',')
        decoded = base64.b64decode(content_string)
        period_file_path = os.path.join(rs.json_files_path, 'custom_period.csv')
        with open(period_file_path, 'wb') as file:
            file.write(decoded)
    else:
        return dash.no_update

    upload_url = 'http://server-container:5000/upload'
    download_url = 'http://server-container:5000/download'
    files = {
        'json': ('submission.json', open(seat_arrangement_file_path, 'rb')),
        'csv': ('entries.csv', open(period_file_path, 'rb'))
    }
    download_csv_path = r"data/simulation csv"
    download_json_path = r"data/simulation json"
    os.makedirs(download_csv_path, exist_ok=True)
    os.makedirs(download_json_path, exist_ok=True)
    simulation_file_name = os.path.splitext(seat_arrangement_file)[0] + '@' + os.path.splitext(period_file)[0]
    response = requests.post(upload_url, params={'exam_period': 'False'}, files=files)
    print(response.status_code)
    print(response)
    if response.status_code == 200:
        result = response.json()
        result_csv = result['result_csv']
        result_json = result['result_json']
        download_csv = requests.get(download_url + "/" + result_csv)
        download_json = requests.get(download_url + "/" + result_json)
        if download_csv.status_code == 200 and download_json.status_code == 200:
            with open(os.path.join(download_csv_path, f"{simulation_file_name}.csv"), 'wb') as file:
                file.write(download_csv.content)
            with open(os.path.join(download_json_path, f"{simulation_file_name}.json"), 'wb') as file:
                file.write(download_json.content)
            simulation_csv_fname = os.path.join(download_csv_path, f"{simulation_file_name}.csv")
        return '/simulation_page'
    else:
        print(f'Error: {response.status_code}\n{response.json()}')
        return dash.no_update
    

# Callbacks for past_simulations_page ------------------------------------------------------------------------------------------------------------------------------
# Add a callback to show the delete modal when a delete button is clicked
@app.callback(
    Output("delete-modal", "is_open", allow_duplicate=True),
    Output("current-simulation-name", "data", allow_duplicate=True), 
    [Input(f"delete-button-{simulation_name}", "n_clicks") for simulation_name in psp.simulation_names],
    prevent_initial_call=True
)
def toggle_modal(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        return False, None
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    for simulation_name in psp.static_simulation_names:
        if button_id == f'delete-button-{simulation_name}':
            return True, simulation_name
    return False, None

@app.callback(
    [Output(f'row-{simulation_name}', 'hidden') for simulation_name in psp.simulation_names],
    Output('dropdown_left', 'options'),
    Output('dropdown_right', 'options'),
    Output('current-simulation-name', 'data', allow_duplicate=True),
    Output("delete-modal", "is_open", allow_duplicate=True),
    Input("confirm-delete-button", "n_clicks"),
    Input("cancel-delete-button", "n_clicks"),
    [State(f'row-{simulation_name}', 'hidden') for simulation_name in psp.simulation_names],
    State('current-simulation-name', 'data'),
    prevent_initial_call=True
)
def delete_rows(*args):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    output = []
    new_simulation_names = []
    current_simulation_name = args[-1]
    if button_id == "confirm-delete-button":
        for simulation_name in psp.static_simulation_names:
            if os.path.exists(os.path.join(psp.data_directory, simulation_name + '.json')):
                if simulation_name == current_simulation_name:
                    os.remove(os.path.join(psp.data_directory, simulation_name + '.json'))
                    output.append(True)
                else:
                    new_simulation_names.append(simulation_name)
                    output.append(False)
            else:
                output.append(True)
    if button_id == "cancel-delete-button":
        for simulation_name in psp.static_simulation_names:
            if os.path.exists(os.path.join(psp.data_directory, simulation_name + '.json')):
                new_simulation_names.append(simulation_name)
                output.append(False)
            else:
                output.append(True)
    new_options = [{'label': name, 'value': name} for name in new_simulation_names]
    global simulation_names
    simulation_names = new_simulation_names.copy()
    output.append(new_options)
    output.append(new_options)
    output.append(None)
    output.append(False)
    return output

# Callback for run_simulation page----------------------------------------------------------------------------------------------------------------------------
@app.callback(Output('output-data-upload', 'children', allow_duplicate=True),
              Input('upload-data', 'contents'),
              prevent_initial_call=True)
def update_output(list_of_contents):
    if list_of_contents is not None:
        content = list_of_contents[0]
        return content

# Connecting APIs
upload_url = 'http://127.0.0.1:5000/upload'

@app.callback(
    Output('slider-output-container', 'children', allow_duplicate=True),
    [Input('url', 'pathname')],
    prevent_initial_call=True
)
def update_output(pathname):
    # Your logic for updating the layout when the app is loaded
    data = pd.read_csv(simulation_csv_fname)
    levels = list(data['level'].unique()) # identifying the levels that users have chosen to simulate
    return [sp.level_layouts[level] for level in sp.levels]

# Callbacks for simulation_page.py -----------------------------------------------------------------------------------------------------------------------------
# Create callback functions for the "Full Graph" buttons for each level
for level in sp.levels:
    @app.callback(
        Output(f'popup-content{level}', 'style'),
        Output(f'popup{level}', 'is_open'),
        Input(f'button_lvl{level}', 'n_clicks'),
        State(f'popup{level}', 'is_open')
    )
    def toggle_popup(n1, is_open, level=level):
        if n1:
            return {"display": "block"}, not is_open
        return {"display": "none"}, is_open
    
# added this callback 
@app.callback(
    Output('slider-output-container', 'children'),
    Input('my-slider', 'value')
)
def update_output(value):
    return [sp.level_layouts[level] for level in sp.levels]

@app.callback(
    Output('tab-content', 'children', allow_duplicate=True),
    Input('tabs', 'value'),
    prevent_initial_call=True)
def update_content(tab):
    if tab == 'tab-1':
        return sp.tab1_content
    else:
        return sp.tab_oo_layout
    
# Callback for comparison page --------------------------------------------------------------------------------------------------------------------------------------
@app.callback(
    Output('model-differences', 'figure'),
    Input('toggle-button', 'n_clicks')
)
def toggle_models(n_clicks):
    global selected_model
    if n_clicks and n_clicks % 2 == 0:
        selected_model = compare.model_2
        button_text = "Toggle to Model 3"
    else:
        selected_model = compare.model_3
        button_text = "Toggle to Model 2"

    fig = compare.create_bar_graph()

    return fig, button_text

# Callback for homepage ----------------------------------------------------------------------------------------------------------------------------------------------------
@app.callback(Output('output-div', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/input':
        return ip.layout
    if pathname == '/past_simulations':
        return psp.psp_layout
    if pathname == '/run_simulation':
        return rs.rs_layout
    if pathname == '/simulation_page':
        return sp.sp_layout
    if pathname == '/compare':
        return compare.app.layout
    if pathname == '/loading_page':
        return load.load_layout
    else:
        return hp.homepage_layout

    
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
