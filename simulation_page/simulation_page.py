import dash
import plotly.express as px 
import plotly.graph_objs as go
import pandas as pd
from dash import html, dcc, Input, Output 
from datetime import datetime, timedelta
import random

# Initializing the app 
app = dash.Dash(__name__)

# Sample data for four library floors
floors = ["Floor 3", "Floor 4", "Floor 5", "Floor 6"]
time_range = [datetime(2023, 1, 1, 9, 0), datetime(2023, 1, 1, 18, 0)]
time_interval = timedelta(minutes=15)
timestamps = [time_range[0] + i * time_interval for i in range(int((time_range[1] - time_range[0]).total_seconds() / time_interval.total_seconds()))]

data = {
    floor: [random.randint(0, 100) for _ in range(len(timestamps))] for floor in floors
}

# Dummy inputs 
df = pd.DataFrame({ # dummy results 
    'Furniture Set': [1, 2, 3, 4, 5],
    'Change in Occupancy': [-5, 10, 50, -40, 10]
})

# The overall skeleton 
app.layout = html.Div([
    dcc.Tabs(id = 'tabs', value = 'BarPlot',children = [
        dcc.Tab(label = 'Overall Change in Occupancy', value = 'tab-1'),
        dcc.Tab(label = 'Occupancy overtime', value = 'tab-2')
    ]),
    html.Div(id = 'tab-content')
])

# Bar plots for 'Overall Change in Occupancy'
fig_lvl3 = px.bar(df, x = 'Furniture Set', y = 'Change in Occupancy', title = 'Level 3', color = 'Change in Occupancy', 
                                  color_discrete_sequence = ['red' if value <0 else 'green' for value in df['Change in Occupancy']])

fig_lvl3.update_traces(marker=dict(color=['red' if value <0 else 'green' for value in df['Change in Occupancy']])) # to ensure that the graph color would just be red and green 

fig_lvl4 = px.bar(df, x = 'Furniture Set', y = 'Change in Occupancy', title = 'Level 4', color = 'Change in Occupancy', 
                                  color_discrete_sequence = ['red' if value <0 else 'green' for value in df['Change in Occupancy']])

fig_lvl4.update_traces(marker=dict(color=['red' if value <0 else 'green' for value in df['Change in Occupancy']]))

fig_lvl5 = px.bar(df, x = 'Furniture Set', y = 'Change in Occupancy', title = 'Level 5', color = 'Change in Occupancy', 
                                  color_discrete_sequence = ['red' if value <0 else 'green' for value in df['Change in Occupancy']])

fig_lvl5.update_traces(marker=dict(color=['red' if value <0 else 'green' for value in df['Change in Occupancy']]))

fig_lvl6 = px.bar(df, x = 'Furniture Set', y = 'Change in Occupancy', title = 'Level 6', color = 'Change in Occupancy', 
                                  color_discrete_sequence = ['red' if value <0 else 'green' for value in df['Change in Occupancy']])

fig_lvl6.update_traces(marker=dict(color=['red' if value <0 else 'green' for value in df['Change in Occupancy']]))

# Layout for the 'Overall Change in Occupancy' tab
tab_bp_layout = html.Div([
    html.Div([
        dcc.Graph(figure = fig_lvl3), 
    ], style = {'width':'48%', 'height' :'48%', 'display':'inline-block'}),
    html.Div([
        dcc.Graph(figure = fig_lvl4)
    ], style = {'width':'48%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(figure = fig_lvl5),
    ], style = {'width':'48%', 'height' :'48%', 'display':'inline-block'}),
    html.Div([
        dcc.Graph(figure = fig_lvl6),
    ], style = {'width':'48%', 'height' :'48%', 'display':'inline-block'})
])

# Time series plot for 'Occupancy Overtime'
traces = []

for floor in floors:
    trace = go.Scatter(
        x=timestamps,
        y=data[floor],
        mode='lines',
        name=floor,
        line_shape='spline'
    )
    traces.append(trace)

layout = go.Layout(
    title='Central Library TimeSeries Plot by Floor',
    xaxis=dict(
        title='Time',
        range=[time_range[0], time_range[1]],
        rangeselector=dict(
            buttons=list([
                dict(count=1, label='1H', step='hour', stepmode='backward'),
                dict(count=6, label='6H', step='hour', stepmode='backward'),
                dict(count=1, label='1D', step='day', stepmode='backward'),
            ])
        ),
        type='date',
        showline=False,
        hoverformat=''
    ),
    yaxis=dict(
        title='Occupancy Rate'
    ),
    legend=dict(
        orientation='h'
    )
)

layout['xaxis']['tickformat'] = '%H:%M'

tab_oo_layout = dcc.Graph(figure={'data': traces, 'layout': layout})

@app.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'value')
)

def render_content(tab):
    if tab == 'tab-1': # referring to the 'Overall Change in Occupancy' tab
        return tab_bp_layout
    else: # referring to the 'Occupancy Overtime' tab 
        return html.Div([
            html.H3('Working in Progress')
        ])

if __name__ == '__main__':
    app.run_server(debug = True)
