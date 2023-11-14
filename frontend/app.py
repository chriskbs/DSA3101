import os
import csv
import json
import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, ctx, dcc, dash_table
from dash.dependencies import Input, Output, State 
from datetime import datetime 

import input_page.input_page as ip
import home_page.home_page as hp
import past_simulations_page.past_simulations_page as psp
import run_simulation.runsimulation as rs 
import simulation_page.simulation_page as sp 
import loading_page.loading as load

inputs_directory = r'data/seat arrangement/'

app = dash.Dash(__name__, suppress_callback_exceptions = True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(children = [dcc.Location(id = "url", refresh = False),
                                       html.Div(id = "output-div")
                                       ])

# callbacks for input page --------------------------------------------------------------------------------------------------------------------------------------------
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

title = "Level 3"
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
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
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
    [Output('output-data-upload', 'children'),
     Output('some-other-output', 'children')],  # Add any other relevant outputs
    [Input('submit-button', 'n_clicks')],
    [State('filename-input', 'value'),  # Assuming you have an input for the filename
     State('data', 'data')]  # Assuming you have a component storing data in the app layout
)

def submit_inputs(n_clicks, filename, data):
    if n_clicks is None:
        raise PreventUpdate

    if not filename:
        return html.Label("Please provide a submission name."), None

    submission_data = {
        "submission_name": filename,
        "levels": []
    }

    for level in data:
        level_data = {
            "level": level,
            "sections": [{"seat_type": seat["Seat Type"], "count": seat["Count"]} for seat in data[level]]
        }
        submission_data["levels"].append(level_data)

    submission_json = json.dumps(submission_data)

    upload_url = 'http://127.0.0.1:5000/upload'

    files = {
        'json': ('submission.json', submission_json),
    }

    response = requests.post(upload_url, params={'exam_period': 'False'}, files=files)

    if response.status_code == 200:
        result = response.json()
        return html.Label(f'Files processed successfully. Result JSON file: {result["result_json"]}'), None
    else:
        return html.Label(f'Error: {response.status_code}. {response.json()}'), None

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

# callback for run_simulation page----------------------------------------------------------------------------------------------------------------------------
@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'))
def update_output(list_of_contents):
    if list_of_contents is not None:
        content = list_of_contents[0]
        return content


# Connecting APIs
upload_url = 'http://127.0.0.1:5000/upload'

@app.callback(
    Output('some-other-output-component', 'children'),  # Change the output component
    Input('upload-data', 'contents'),
    prevent_initial_call=True
)
def update_output2(list_of_contents):
    if list_of_contents is None:
        raise PreventUpdate

    content = list_of_contents[0]

    files = {
        'json': ('submission.json', content),
    }
    response = requests.post(upload_url, params={'exam_period': 'False'}, files=files)

    if response.status_code == 200:
        result = response.json()
        message = f'Files processed successfully. Result JSON file: {result["result_json"]}'
    else:
        message = f'Error: {response.status_code}\n{response.json()}'

    return html.Div(message)



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
    Output('tab-content', 'children'),
    Input('tabs', 'value')
)
def update_content(tab):
    if tab == 'tab-1':
        # return [sp.level_layouts[level] for level in sp.levels]
        return sp.tab1_content
    else:
        return sp.tab_oo_layout

# Connecting APIs
@app.callback(
    [Output('tab-content', 'children'),
     Output('some-other-output-3', 'children')],
    [Input('tabs', 'value'),
     Input('run-simulation-button', 'n_clicks')],
    prevent_initial_call=True
)
def update_tab_and_output(tab, n_clicks):
    if n_clicks is None:
        raise PreventUpdate

    if tab == 'tab-1':
        return [sp.level_layouts[level] for level in sp.levels], None
    else:
        results_url2 = 'http://127.0.0.1:5000/download'

        # Make a GET request to the API
        response = requests.get(results_url2)

        if response.status_code == 200:
            result = response.json()

            return [
                sp.tab_oo_layout,
                html.Div(f"Result CSV file: {result['result_csv']}", style={'color': 'navy', 'font-size': '18px'}),
                html.Div(f"Result JSON file: {result['result_json']}", style={'color': 'navy', 'font-size': '18px'})
            ], None
        else:
            return [html.Div(f"Error: {response.status_code}\n{response.json()}", style={'color': 'red', 'font-size': '18px'})], None
    
# Callback for comparison page --------------------------------------------------------------------------------------------------------------------------------------


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
        return html.H1("Working in progress")
    if pathname == '/loading_page':
        return load.load_layout
    else:
        return hp.homepage_layout

    
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False)
