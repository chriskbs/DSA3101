import dash
from dash import Dash, html, dcc, Input, Output, ctx, dcc, State, dash_table
import dash_daq as daq
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import csv

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

simulated_period = dcc.RadioItems(
    ['Normal period', 'Exam period', 'Event day'], 
    'Normal period', 
    id='simulated_period',
    style={'display': 'inline-block'},
    labelStyle={'display': 'inline-block'}
)

upload_csv = dcc.Upload(
    id='upload_csv',
    children=html.Button('Upload CSV File'),
    style={
        'display': 'inline-block'
    },
    multiple=False  # Allow only single file upload
)

available_levels = dcc.Checklist(
    ['Level_1', 'Level_2', 'Level_3', 'Level_4', 'Level_5', 'Level_6'],
    ['Level_1', 'Level_2', 'Level_3', 'Level_4', 'Level_5', 'Level_6'],
    id='available_levels',
    labelStyle={'display': 'inline-block'}
)

seat_types = [
    'movable_seat',
    '4_man_seat',
    '8_man_seat',
    'cubicle',
    'diagonal_seat',
    'discussion_cubicle',
    'sofa',
    'soft_seat',
    'window_seat',
]

# seats per seat_type
seats = {
    'movable_seat': 5,
    '4_man_seat': 4,
    '8_man_seat': 8,
    'cubicle': 1,
    'diagonal_seat': 1,
    'd_cubicle': 2,
    'sofa': 1,
    'soft_seat': 4,
    'window_seat': 1,
}

data={
    "Level 3": [
        {'Seat Type': 'movable_seat', 'Count': 0},
        {'Seat Type': '4_man_seat', 'Count': 0},
        {'Seat Type': '8_man_seat', 'Count': 0},
        {'Seat Type': 'cubicle', 'Count': 0},
        {'Seat Type': 'diagonal_seat', 'Count': 0},
        {'Seat Type': 'd_cubicle', 'Count': 0},
        {'Seat Type': 'sofa', 'Count': 0},
        {'Seat Type': 'soft_seat', 'Count': 0},
        {'Seat Type': 'window_seat', 'Count': 0},
    ],
    "Level 4": [
        {'Seat Type': 'movable_seat', 'Count': 0},
        {'Seat Type': '4_man_seat', 'Count': 0},
        {'Seat Type': '8_man_seat', 'Count': 0},
        {'Seat Type': 'cubicle', 'Count': 0},
        {'Seat Type': 'diagonal_seat', 'Count': 0},
        {'Seat Type': 'd_cubicle', 'Count': 0},
        {'Seat Type': 'sofa', 'Count': 0},
        {'Seat Type': 'soft_seat', 'Count': 0},
        {'Seat Type': 'window_seat', 'Count': 0},
    ],
    "Level 5": [
        {'Seat Type': 'movable_seat', 'Count': 0},
        {'Seat Type': '4_man_seat', 'Count': 0},
        {'Seat Type': '8_man_seat', 'Count': 0},
        {'Seat Type': 'cubicle', 'Count': 0},
        {'Seat Type': 'diagonal_seat', 'Count': 0},
        {'Seat Type': 'd_cubicle', 'Count': 0},
        {'Seat Type': 'sofa', 'Count': 0},
        {'Seat Type': 'soft_seat', 'Count': 0},
        {'Seat Type': 'window_seat', 'Count': 0},
    ],
    "Level 6 Central Library": [
        {'Seat Type': 'movable_seat', 'Count': 0},
        {'Seat Type': '4_man_seat', 'Count': 0},
        {'Seat Type': '8_man_seat', 'Count': 0},
        {'Seat Type': 'cubicle', 'Count': 0},
        {'Seat Type': 'diagonal_seat', 'Count': 0},
        {'Seat Type': 'd_cubicle', 'Count': 0},
        {'Seat Type': 'sofa', 'Count': 0},
        {'Seat Type': 'soft_seat', 'Count': 0},
        {'Seat Type': 'window_seat', 'Count': 0},
    ],
    "Level 6 Chinese Library": [
        {'Seat Type': 'movable_seat', 'Count': 0},
        {'Seat Type': '4_man_seat', 'Count': 0},
        {'Seat Type': '8_man_seat', 'Count': 0},
        {'Seat Type': 'cubicle', 'Count': 0},
        {'Seat Type': 'diagonal_seat', 'Count': 0},
        {'Seat Type': 'd_cubicle', 'Count': 0},
        {'Seat Type': 'sofa', 'Count': 0},
        {'Seat Type': 'soft_seat', 'Count': 0},
        {'Seat Type': 'window_seat', 'Count': 0},
    ]
}

title = "Level 3"

def find_seat_count(level, seat_type, data):
    for seat in data[level]:
        if seat["Seat Type"] == seat_type:
            return seat["Count"]
    return 0

def find_total_seats(level, data, seats):
    total_seats = 0
    for seat_type in seats:
        total_seats += find_seat_count(level, seat_type, data) * seats[seat_type]
    return total_seats

# Define a component to display the total count of each seat type
table_balanced_seats = dash_table.DataTable(
    id='table_balanced_seats',
    columns=[
        {'name': 'Seat Type', 'id': 'Seat Type'},
        {'name': 'Count', 'id': 'Count'},
    ],
    data=data[title],
    style_table={'display': 'inline-block'}
    # style_table={'height': '300px', 'overflowY': 'auto'}  # Add vertical scroll if needed
)

def create_item(item_name, item_image):
    image = html.Img(src=item_image, style={'width': '100%', 'height': '100%'})
    plus_button = dbc.Button('+', color='primary', size='lg', style={'width': '100%', 'height': '100%', 'text-align': 'center'})
    minus_button = dbc.Button('-', color='primary', size='lg', style={'width': '100%', 'height': '100%', 'text-align': 'center'})
    count_text = dcc.Input(type='number', min=0, max=200, step=1, value = 0, style={'width': '100%', 'height': '100%', 'text-align': 'center'})
    item_title = html.H3(item_name, style={'text-align': 'center'})
    plus_button.id = f'plus-button-{item_name}'
    minus_button.id = f'minus-button-{item_name}'
    count_text.id = f'count-text-{item_name}'
    return html.Div([dbc.Card(
        dbc.CardBody(
            [
                image,
                item_title,
                dbc.Row(
                    [
                        dbc.Col(
                            minus_button,
                            width=2,
                            align='center'
                        ),
                        dbc.Col(
                            count_text,
                            width=4,
                            align='center'
                        ),
                        dbc.Col(
                            plus_button,
                            width=2,
                            align='center'
                        ),
                    ],
                    justify="center"
                ),
            ]
        ),
        style={'width': '100%', 'height': '100%', 'text-align': 'center'}
    )])

# Define the content for each tab
more_seats_content = dbc.Row(
    children=[
        dbc.Col(create_item('movable_seat', r'assets/movable_seat.png'), width=6, align='center'),
        dbc.Col(create_item('4_man_seat', r'assets/4_man_seat.png'), width=6, align='center'),
        dbc.Col(create_item('8_man_seat', r'assets/8_man_seat.png'), width=6, align='center'),
        dbc.Col(create_item('window_seat', r'assets/window_seat.png'), width=6, align='center'),
    ],
    justify="between",
)

more_comfort_content = dbc.Row(
    children=[
        dbc.Col(create_item('sofa', r'assets/sofa.png'), width=6, align='center'),
        dbc.Col(create_item('soft_seat', r'assets/soft_seat.png'), width=6, align='center'),
    ],
    justify="between",
)

more_privacy_content = dbc.Row(
    children=[
        dbc.Col(create_item('cubicle', r'assets/cubicle.png'), width=6, align='center'),
        dbc.Col(create_item('discussion_cubicle', r'assets/discussion_cubicle.png'), width=6, align='center'),
        dbc.Col(create_item('diagonal_seat', r'assets/diagonal_seat.png'), width=6, align='center'),
    ],
    justify="between",
)

app.layout = html.Div([
    html.Div([ # div for entire page
        html.Div(
            [
                html.H1(title, id="title", style={'text-align': 'center'}),
                html.I("The model will asume that the level is closed if there is no seat selected.", style={'text-align': 'center'}),
            ]
        ), # div for header
        html.Div([ # div for body
            html.Li( # div for left side
                [
                    # html.Div([
                    #     html.Li([
                    #         html.Label('Simulated period'),
                    #         html.Br(),
                    #         simulated_period, # dcc.RadioItems
                    #     ], style={'display': 'inline-block'}),
                    #     html.Li([
                    #             upload_csv # dcc.Upload
                    #     ], style={'display': 'inline-block'})
                    # ], style={'border': '1px solid #000', 'padding': '20px'}),
                    # html.Br(),
                    # html.Div([
                    #     html.Label('Levels Available'),
                    #     available_levels # dcc.Checklist
                    # ], style={'border': '1px solid #000', 'padding': '20px'}),
                    # html.Br(),
                    html.Div([
                        html.Label('Seats selected for Level 3', id="total_seats_title", style={'padding-top': '20px', 'padding-left': '20px', 'padding-right': '20px'}),
                        table_balanced_seats, # dcc.Checklist
                        html.Label(f'Total seats: {find_total_seats(title, data, seats)}', id="total_seats", style={'padding-left': '20px', 'padding-right': '20px'}),
                    ], style={'border': '1px solid #000'}),
                ],
                style={'width': '15%', 'display': 'inline-block', 'vertical-align': 'top'}
            ),
            html.Li(
                [
                    dcc.Tabs([
                        dcc.Tab(label='More Seats', children=more_seats_content),
                        dcc.Tab(label='More Comfort', children=more_comfort_content),
                        dcc.Tab(label='More Privacy', children=more_privacy_content),
                    ]),
                ],
                style={'width': '85%', 'display': 'inline-block', 'text-align': 'center', 'vertical-align': 'middle', 'border': '1px solid #000', 'padding': '20px'}
            ), # div for right side
        ]),
        html.Button('Back', id='back-button', hidden=True, style={
            "position": "fixed",
            "bottom": "50px",
            "left": "50px",
            "background-color": "#007BFF",
            "color": "white",
            "padding": "10px 20px",
            "border": "none",
            "border-radius": "5px",
            "cursor": "pointer",
        }),
        html.Button("Next", id="next-button", hidden=False, style={
            "position": "fixed",
            "bottom": "50px",
            "right": "50px",
            "background-color": "#007BFF",
            "color": "white",
            "padding": "10px 20px",
            "border": "none",
            "border-radius": "5px",
            "cursor": "pointer",
        }),
        html.Button("Submit", id="submit-button", hidden=True, style={
            "position": "fixed",
            "bottom": "50px",
            "right": "50px",
            "background-color": "#007BFF",
            "color": "white",
            "padding": "10px 20px",
            "border": "none",
            "border-radius": "5px",
            "cursor": "pointer",
        }),
        dbc.Modal([
                html.Div([
                    html.Label("Give a name to this submission:"),
                    dcc.Input(id='submission-name-input', type='text', value=''),
                    html.Button('Confirm', id='confirm-button'),
                ])
            ],
             id='submission-name-modal',
        ),
        # html.Div([
        #     html.Div([
        #         html.Label("Give a name to this submission:"),
        #         dcc.Input(id='submission-name-input', type='text', value=''),
        #         html.Button('Confirm', id='confirm-button'),
        #     ])
        # ],
        # id='submission-name-modal',
        # style={'display': 'none'}),
    ], style={'width': '1200px', 'margin': '0 auto'})
], style={'padding': '40px', 'height': '100vh', 'width': '100vw', 'overflow': 'scroll'}) # div for entire page

def update_count(level, count, item_name):
    # Calculate the new counts
    count = int(count)
    if f'plus-button-{item_name}' == ctx.triggered_id:
        count = min(200, count + 1)
    elif f'minus-button-{item_name}' == ctx.triggered_id:
        count = max(0, count - 1)
    if item_name == "discussion_cubicle":
        item_name = "d_cubicle"
    for seat in data[level]:
        if seat["Seat Type"] == item_name:
            seat["Count"] = count
    return str(count), data[level]

# Define a callback to update seat counts and the table data
@app.callback(
    [Output(f'count-text-{seat_type}', 'value', allow_duplicate=True) for seat_type in seat_types],
    Output('table_balanced_seats', 'data', allow_duplicate=True),
    Output('total_seats', 'children', allow_duplicate=True),
    [Input(f'plus-button-{seat_type}', 'n_clicks') for seat_type in seat_types],
    [Input(f'minus-button-{seat_type}', 'n_clicks') for seat_type in seat_types],
    [Input(f'count-text-{seat_type}', 'value') for seat_type in seat_types],
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
    new_count, new_data = update_count(title, count, seat_type)
    ctx.inputs[f'count-text-{seat_type}.value'] = new_count
    count_text_values = [v for k, v in ctx.inputs.items() if k.startswith('count-text-')]
    count_text_values.append(new_data)
    count_text_values.append(f'Total seats: {find_total_seats(title, data, seats)}')
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

@app.callback(
    Output("title", "children"),
    [Output(f'count-text-{seat_type}', 'value', allow_duplicate=True) for seat_type in seat_types],
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
    for seat_type in seat_types:
        output.append(find_seat_count(title, seat_type, data))
    output.append(data[title])
    output.append(f'Total seats: {find_total_seats(title, data, seats)}')
    output.append(f'Seats selected for {title}')
    output.append(next_button)
    output.append(back_button)
    output.append(submit_button)
    return output

@app.callback(
    Output('submission-name-modal', 'is_open'),
    Input('submit-button', 'n_clicks'),
    State('submit-button', 'hidden'),
)
def toggle_modal(submit_clicks, submit_button_hidden):
    if submit_button_hidden == True:
        return False
    else:
        return True

if __name__ == '__main__':
    app.run_server(debug=False)