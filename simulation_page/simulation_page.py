import dash
import os
import plotly.express as px 
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State

# Initializing the app 
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Dummy inputs 
df = pd.DataFrame({ # dummy results 
    'Furniture Set': [1, 2, 3, 4, 5],
    'Change in Occupancy': [-5, 10, 50, -40, 10]
})


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
        dcc.Graph(id = 'Graph_1', figure = fig_lvl3),
        dbc.Button("Full Graph", id = "button_lvl3", n_clicks = 0, style = {'float':'right', 'background-color':'black'}),
        html.Div(id = "popup-content", children = [
            dbc.Modal([
                dbc.ModalHeader("Level 3", style = {'background-color':'grey'}),
                dbc.ModalBody([
                    dcc.Graph(id = 'Graph_1', figure = fig_lvl3),
                    ],
                    style = {'background-color':'white'}),
            ], id = "popup", fullscreen = True, centered = True)
        ]),
    ], style = {'width':'50%', 'height' :'50%', 'display':'inline-block'}),

    html.Div([
        dcc.Graph(id = 'Graph_2', figure = fig_lvl4),
        dbc.Button("Full Graph", id = "button_lvl4", n_clicks = 0, style = {'float':'right', 'background-color':'black'}),
        html.Div(id = "popup-content2", children = [
            dbc.Modal([
                dbc.ModalHeader("Level 4", style = {'background-color':'grey'}),
                dbc.ModalBody([
                    dcc.Graph(id = 'Graph_2', figure = fig_lvl4),
                    ],
                    style = {'background-color':'white'}),
            ], id = "popup2", fullscreen = True, centered = True)
        ]),
    ], style = {'width':'50%', 'height' :'50%', 'display':'inline-block'}),

    html.Div([
        dcc.Graph(id = 'Graph_3', figure = fig_lvl5),
        dbc.Button("Full Graph", id = "button_lvl5", n_clicks = 0, style = {'float':'right', 'background-color':'black'}),
        html.Div(id = "popup-content3", children = [
            dbc.Modal([
                dbc.ModalHeader("Level 5", style = {'background-color':'grey'}),
                dbc.ModalBody([
                    dcc.Graph(id = 'Graph_3', figure = fig_lvl5),
                    ],
                    style = {'background-color':'white'}),
            ], id = "popup3", fullscreen = True, centered = True)
        ]),
    ], style = {'width':'50%', 'height' :'50%', 'display':'inline-block'}),

    html.Div([
        dcc.Graph(id = 'Graph_4', figure = fig_lvl6),
        dbc.Button("Full Graph", id = "button_lvl6", n_clicks = 0, style = {'float':'right', 'background-color':'black'}),
        html.Div(id = "popup-content4", children = [
            dbc.Modal([
                dbc.ModalHeader("Level 6", style = {'background-color':'grey'}),
                dbc.ModalBody([
                    dcc.Graph(id = 'Graph_4', figure = fig_lvl6),
                    ],
                    style = {'background-color':'white'}),
            ], id = "popup4", fullscreen = True, centered = True)
        ]),
    ], style = {'width':'50%', 'height' :'50%', 'display':'inline-block'})
])

# The overall skeleton 
app.layout = html.Div([
    dcc.Tabs(id = 'tabs', value = 'BarPlot',children = [
        dcc.Tab(label = 'Overall Change in Occupancy', value = 'tab-1'),
        dcc.Tab(label = 'Occupancy overtime', value = 'tab-2')
    ]),
    html.Div(id = 'tab-content')
])

# Full graph button for the level 3 graph
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

# Full graph button for the level 4 graph 
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

# Full graph button for the level 5 graph
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

# Full graph button for the level 6 graph 
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

# Output for the different tabs 
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
