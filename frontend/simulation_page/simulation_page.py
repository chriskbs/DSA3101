import dash
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from datetime import datetime, timedelta
import random
import plotly.graph_objs as go

# Initializing the app
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

data = pd.read_csv("frontend/simulation_page/dummy_data/trial_data_1lvl.csv")
levels = list(data['level'].unique())  # Identifying the levels that users have chosen to simulate

# If the user only inputs data for one level, the graph would occupy the whole screen else just half the screen
if len(levels) == 1:
    x = '100%'
    y = '100%'
else:
    x = "48%"
    y = "48%"

def create_level_layout(level, data):
    indexes_level = [index for index, value in enumerate(data['level']) if value == level]
    df_level = data.iloc[indexes_level].sort_values(by=' seat_type')
    fig_level = px.bar(df_level, x=' seat_type', y=' changeInOccupancy', title=f'Level {level}', color=' changeInOccupancy',
                       color_discrete_sequence=['red' if value < 0 else 'green' for value in df_level[' changeInOccupancy']],
                       text=df_level[' changeInOccupancy'],
                       hover_data={' changeInOccupancy': True})

    fig_level.update_traces(marker=dict(color=['red' if value < 0 else 'green' for value in df_level[' changeInOccupancy']]))  # To ensure that the graph color would be red and green
    fig_level.update_layout(hovermode='closest')

    # Create the layout for the given level
    tab_bp_layout_level = html.Div([
        dcc.Graph(id=f'Graph_{level}', figure=fig_level),
        dbc.Button(f"Full Graph (Level {level})", id=f"button_lvl{level}", n_clicks=0, style={'float': 'right', 'background-color': 'lightblue'}),
        html.Div(id=f"popup-content{level}", children=[
            dbc.Modal([
                dbc.ModalHeader(f"Level {level}", style={'background-color': 'lightblue', 'font-size': '24px', 'font-weight': 'bold'}),
                dbc.ModalBody([
                    dcc.Graph(id=f'Graph_{level}', figure=fig_level, style={'width': '100%', 'height': '100%'}),
                ], style={'background-color': 'white'}),
            ], id=f"popup{level}", fullscreen=True, centered=True)
        ])
    ], style={'width': x, 'height': y, 'display': 'inline-block'})
    return tab_bp_layout_level


level_layouts = {level: create_level_layout(level, data) for level in levels}

# Sample data for four library floors
floors = ["Floor 3", "Floor 4", "Floor 5", "Floor 6"]
time_range = [datetime(2023, 1, 1, 9, 0), datetime(2023, 1, 2, 8, 0)]
time_interval = timedelta(minutes=15)
timestamps = [time_range[0] + i * time_interval for i in range(int((time_range[1] - time_range[0]).total_seconds() / time_interval.total_seconds()))]

data = {
    floor: [random.randint(0, 100) for _ in range(len(timestamps))] for floor in floors
}

button_style = {'backgroundColor': 'black', 'color': 'white', 'borderRadius': '15px', 'margin': '5px'}

# The overall skeleton
app.layout = html.Div([
    html.Button("Home", id="button_home", n_clicks=0, style={'background-color': 'light grey', 'border-radius': '5px'}),
    html.Button(children=[html.Img(src='assets/close.png', style={'width': '17px', 'height': '17px'})], id="button_close", n_clicks=0, style={'border-radius': '5px', 'float': 'right'}),
    html.Div([
        dcc.Tabs(id='tabs', value='tab-1', children=[
            dcc.Tab(label='Overall Change in Occupancy', value='tab-1', style={'padding': '10px', 'background-color': 'lightblue'}),
            dcc.Tab(label='Occupancy overtime', value='tab-2', style={'padding': '10px', 'background-color': 'lightblue'})
        ]),
        html.Div(id='tab-content')
    ])], style={'padding': '10px'})

# Create callback functions for the "Full Graph" buttons for each level
for level in levels:
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

# Time series plot for 'Occupancy Overtime'
traces = []

for floor in floors:
    trace = go.Scatter(
        x=timestamps,
        y=data[floor],
        mode='lines',
        name=floor,
        line_shape='spline',
        opacity=1  
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
    html.Div([
        html.Button("Level 3 only", id="level-3-button", style=button_style),
        html.Button("Level 4 only", id="level-4-button", style=button_style),
        html.Button("Level 5 only", id="level-5-button", style=button_style),
        html.Button("Level 6 only", id="level-6-button", style=button_style),
    ], style={'text-align': 'center'}),
])

# Callback for switching between tabs and displaying the full graphs
@app.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'value')
)
def update_content(tab):
    if tab == 'tab-1':
        return [level_layouts[level] for level in levels]
    else:
        return tab_oo_layout

if __name__ == '__main__':
    app.run_server(debug=True)
