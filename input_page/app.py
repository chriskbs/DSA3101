from dash import Dash, dcc, html, callback, Input, Output, dash_table
import dash_daq as daq
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df  = pd.read_csv("prediction_output/demo.csv")

# create figure for utilazation bar plot
x_hour_data = (df[df['Hour'] == '09:00'].iloc[0][1:7] * 100).apply(lambda x: int(x))
y_level = ['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5', 'Level 6']
bar_utilization_fig = px.bar(
    x=x_hour_data,
    y=y_level,
    orientation='h',
    text=x_hour_data,
    range_color=[0, 100],
    color_continuous_scale='portland',
    color=x_hour_data
)

# Add indicator lines
thresholds = [0, 25, 50, 75, 100]
for threshold in thresholds:
    bar_utilization_fig.add_shape(
        dict(
            type='line',
            x0=threshold,
            x1=threshold,
            y0=-0.5,  # Below the first bar
            y1=len(df) - 0.5,  # Above the last bar
            line=dict(color='gray', width=1)
        )
    )

bar_utilization_fig.update_layout(
    xaxis=dict(
        title='Utilization Rate',
        range=[0, 100],  # Fixed y-axis range from 0 to 100%
        showgrid=False,
        tickvals=[0, 25, 50, 75, 100],
        ticktext=["0", "25", "50", "75", "100"]
    ),
    yaxis=dict(
        title='Level', 
        showgrid=False
    ),
    title='Utilization Rate by Level at 09:00',
    barmode='relative',
    height=400,
    showlegend=False
)

hour_map = {
    0: '09:00',
    1: '10:00',
    2: '11:00',
    3: '12:00',
    4: '13:00',
    5: '14:00',
    6: '15:00',
    7: '16:00',
    8: '17:00',
    9: '18:00',
    10: '19:00',
    11: '20:00',
    12: '21:00',
    13: '22:00',
    14: '23:00',
    15: '00:00',
    16: '01:00',
    17: '02:00',
    18: '03:00',
    19: '04:00',
    20: '05:00',
    21: '06:00',
    22: '07:00',
    23: '08:00'
}

bar_utilization = dcc.Graph(
    id='bar_utilization',
    figure=bar_utilization_fig
)

tab_utilization_rate = dbc.Card(
    dbc.CardBody([
        html.Div([
            bar_utilization
        ])
    ])
)

graph_tabs = dbc.Tabs(
    [
        dbc.Tab(tab_utilization_rate, label="Utilization Rate"),
        dbc.Tab("A very nice Population Plot", label="Population Size"),
    ]
)

time_slider = dcc.Slider(
    id='time_slider',
    marks=hour_map,
    value=0,
    step=None
)

simulated_period = dcc.RadioItems(
    ['Normal period', 'Exam period', 'Event day'], 
    'Normal period', 
    id='simulated_period',
    style={'display': 'inline-block'},
    labelStyle={'display': 'inline-block', 'margin-right': '10px'}
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
    labelStyle={'display': 'inline-block', 'padding': '10px'}
)

seats_level = dcc.Dropdown(
    ['Level_1', 'Level_2', 'Level_3', 'Level_4', 'Level_5', 'Level_6'], 
    'Level_1', 
    id='seats_level',
    style={'width': '200px'}
)

tables = daq.NumericInput(
    id='tables',
    min=0,
    max=100,
    value=50
)

seats = daq.NumericInput(
    id='seats',
    min=0,
    max=400,
    value=200
)

check_time_series = dcc.Checklist(
    id='check_time_series',
    options=[
        {'label': 'Time Series', 'value': 'toggled'}
    ],
    value=[],  # Initially unchecked
    style={'border': '1px solid #000', 'display': 'inline-block', 'padding': '20px'}
)

button_calculate = html.Button(
    'Calculate', 
    id='button_calculate', 
    n_clicks=0,
    style={'border': '1px solid #000', 'display': 'inline-block', 'padding': '20px'}
)

button_auto_balance = html.Button(
    'Auto Balance Seats', 
    id='button_auto_balance', 
    n_clicks=0
)

table_balanced_seats_data = {
    'Level': ['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5', 'Level 6'],
    'Number of Tables': [10, 15, 8, 20, 25, 12],
    'Number of Seats': [40, 60, 32, 80, 100, 48]
}
table_balanced_seats_df = pd.DataFrame(table_balanced_seats_data)

table_balanced_seats = dash_table.DataTable(
    id='table_balanced_seats',
    columns=[
        {'name': 'Level', 'id': 'Level'},
        {'name': 'Number of Tables', 'id': 'Number of Tables'},
        {'name': 'Number of Seats', 'id': 'Number of Seats'}
    ],
    data=table_balanced_seats_df.to_dict('records'),
    style_table={'display': 'inline-block', 'margin-right': '20px'}
    # style_table={'height': '300px', 'overflowY': 'auto'}  # Add vertical scroll if needed
)

app.layout = html.Div([
    html.Div([
        html.Div([
            graph_tabs # dbc.Tabs
        ], style={'overflow': 'auto', 'vertical-align': 'top'}),
        html.Div([
            time_slider # dcc.Slider
        ])
    ], style={'border': '1px solid #000', 'padding': '20px'}),
    html.Br(),
    html.Div([
        html.Div([
            html.Li([
                html.Label('Simulated period'),
                html.Br(),
                simulated_period, # dcc.RadioItems
            ], style={'display': 'inline-block', 'margin-right': '100px'}),
            html.Li([
                    upload_csv # dcc.Upload
            ], style={'display': 'inline-block'})
        ], style={'border': '1px solid #000', 'padding': '20px'}),
        html.Br(),
        html.Div([
            html.Label('Levels Available'),
            available_levels # dcc.Checklist
        ], style={'border': '1px solid #000', 'padding': '20px'}),
        html.Br(),
        html.Div([
            html.Label('Change the Number of Table and Seats'),
            html.Br(),
            html.Li([
                seats_level, # dcc.Dropdown
            ], style={'display': 'inline-block', 'margin-right': '200px', 'vertical-align': 'top'}),
            html.Li([
                html.Div([
                    html.Label('Number of Tables'),
                    tables, # daq.NumericInput
                    html.Label('Number of Seats'),
                    seats # daq.NumericInput
                ])
            ], style={'display': 'inline-block', 'vertical-align': 'top'})
        ], style={'border': '1px solid #000', 'padding': '20px'}),
        html.Br(),
        html.Div([
            html.Li([
                check_time_series, # dcc.Checklist
                html.Br(),
                button_calculate # html.Button
            ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top'}),
            html.Li([
                html.Div([
                    html.Li([
                        button_auto_balance, # html.Button
                        html.Br(),
                        html.H4(id='average_rate_text', children="Average Rate: N/A%", style={'display': 'inline-block'}),
                    ], style={'padding': '20px', 'display': 'inline-block', 'vertical-align': 'top'}),
                    html.Li([
                        table_balanced_seats # dash_table.DataTable
                    ], style={'display': 'inline-block', 'overflow': 'auto', 'vertical-align': 'top'})
                ])
            ], style={'border': '1px solid #000', 'padding': '20px', 'width': '80%', 'display': 'inline-block', 'vertical-align': 'top'})
        ], style={'border': '1px solid #000', 'padding': '20px'})
    ], style={'padding': '20px'})
], style={'padding': '40px'})

@app.callback(
    Output('bar_utilization', 'figure'),
    Input('time_slider', 'value')
)
def update_time_utilization_bar(selected_hour):
    hour = hour_map[selected_hour]
    x_hour_data = (df[df['Hour'] == hour].iloc[0][1:7] * 100).apply(lambda x: int(x))
    updated_fig = px.bar(
        x=x_hour_data,
        y=y_level,
        orientation='h',
        text=x_hour_data,
        range_color=[0, 100],
        color_continuous_scale='portland',
        color=x_hour_data,
    )
    updated_fig.update_layout(
        xaxis=dict(
            title='Utilization Rate',
            range=[0, 100],  # Fixed y-axis range from 0 to 100%
            showgrid=False,
            tickvals=[0, 25, 50, 75, 100],
            ticktext=["0", "25", "50", "75", "100"]
        ),
        yaxis=dict(
            title='Level', 
            showgrid=False
        ),
        title='Utilization Rate by Level at 09:00',
        barmode='relative',
        height=400,
        showlegend=False
    )
    return updated_fig

if __name__ == '__main__':
    app.run_server(debug=True)