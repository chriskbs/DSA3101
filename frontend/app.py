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

app = dash.Dash(__name__, suppress_callback_exceptions = True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(children = [dcc.Location(id = "url", refresh = False),
                                       html.Div(id = "output-div")
                                       ])

# callbacks for input page 
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
    Output('submission-name-input-error', 'hidden'),
    Output('submission-name-modal', 'is_open', allow_duplicate=True),
    Input('confirm-button', 'n_clicks'),
    State('submission-name-input', 'value'),
    prevent_initial_call=True
)
def confirm_submission(n_clicks, filename):
    # checks inputs folder if any file has the same name
    for fname in os.listdir(ip.inputs_directory):
        if os.path.isfile(os.path.join(ip.inputs_directory, fname)):
            name, extension = os.path.splitext(fname)
            if name == filename and extension == '.json':
                # prompt user to change name
                return False, True
    # if no, save the file to inputs folder
    filepath = os.path.join(ip.inputs_directory, f"{filename}.json")
    
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

    return True, False

# Callbacks for past_simulations_page
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

# callback for run_simulation page
@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'))
def update_output(list_of_contents):
    if list_of_contents is not None:
        content = list_of_contents[0]
        return content

# Callbacks for simulation_page.py -------------------------------------------------------------------------------------(not working yet)
# For 'full graph' button of level 3
@app.callback(
        Output('popup-content', 'style'),
        Output('popup', 'is_open'),
        Input('button_lvl3','n_clicks'),
        State('popup', 'is_open')
)

def toggle_popup(n1, is_open):
    if n1:
        return {"display":"block"},not is_open
    return {"display":"none"}, is_open

# For 'full graph' button of level 4'
@app.callback(
        Output('popup-content2', 'style'),
        Output('popup2', 'is_open'),
        Input('button_lvl4','n_clicks'),
        State('popup2', 'is_open')
)

def toggle_popup(n1, is_open):
    if n1:
        return {"display":"block"},not is_open
    return {"display":"none"}, is_open

# For full graph button of level 5
@app.callback(
        Output('popup-content3', 'style'),
        Output('popup3', 'is_open'),
        Input('button_lvl5','n_clicks'),
        State('popup3', 'is_open')
)

def toggle_popup(n1, is_open):
    if n1:
        return {"display":"block"},not is_open
    return {"display":"none"}, is_open

# For full graph button of level 5
@app.callback(
        Output('popup-content4', 'style'),
        Output('popup4', 'is_open'),
        Input('button_lvl6','n_clicks'),
        State('popup4', 'is_open')
)

def toggle_popup(n1, is_open):
    if n1:
        return {"display":"block"},not is_open
    return {"display":"none"}, is_open

@app.callback(
    Output('tab-content', 'children'),
    Output('tab-oo-layout', 'figure'),
    Input('tabs', 'value'),
    Input('level-3-button', 'n_clicks'),
    Input('level-4-button', 'n_clicks'),
    Input('level-5-button', 'n_clicks'),
    Input('level-6-button', 'n_clicks')
)
def update_content_and_trace(tab, level3_clicks, level4_clicks, level5_clicks, level6_clicks):
    to_show = []
    if tab == 'tab-1':  
        for i in sp.levels:
            if i == 3:
                to_show.append(sp.tab_bp_layout_level3)
            if i == 4:
                to_show.append(sp.tab_bp_layout_level4)
            if i == 5:
                to_show.append(sp.tab_bp_layout_level5)
            if i == 6:
                to_show.append(sp.tab_bp_layout_level6)
        tab_content = html.Div(to_show)
    else:  
        tab_content = sp.tab_oo_layout

    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]  

    for trace in sp.traces:
        trace['opacity'] = 1

    if button_id == 'level-3-button':
        sp.traces[0]['opacity'] = 1
        sp.traces[1]['opacity'] = 0.2
        sp.traces[2]['opacity'] = 0.2
        sp.traces[3]['opacity'] = 0.2
    elif button_id == 'level-4-button':
        sp.traces[0]['opacity'] = 0.2
        sp.traces[1]['opacity'] = 1
        sp.traces[2]['opacity'] = 0.2
        sp.traces[3]['opacity'] = 0.2
    elif button_id == 'level-5-button':
        sp.traces[0]['opacity'] = 0.2
        sp.traces[1]['opacity'] = 0.2
        sp.traces[2]['opacity'] = 1
        sp.traces[3]['opacity'] = 0.2
    elif button_id == 'level-6-button':
        sp.traces[0]['opacity'] = 0.2
        sp.traces[1]['opacity'] = 0.2
        sp.traces[2]['opacity'] = 0.2
        sp.traces[3]['opacity'] = 1

    trace_figure = {'data': sp.traces, 'layout': sp.layout}
    
    return tab_content, trace_figure

# Callback for homepage 
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
    else:
        return hp.homepage_layout

    
if __name__ == '__main__':
    app.run_server(debug=True)