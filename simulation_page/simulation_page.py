import dash
import plotly.express as px 
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State

# Initializing the app 
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

data = pd.read_csv("simulation_page/dummy_data/trial_data_1lvl.csv")
levels = list(data['level'].unique()) # identifying the levels that users have chosen to simulate

# If user only input data for one level, the graph would occupy the whole screen else just half the screen
if len(levels) == 1:
    x = '100%'
    y = '100%'
else:
    x = "48%"
    y = "48%"

for i in levels:
    if i == 3:
        # creating the dataframe for data of level 3
        indexes_level3 = [index for index, value in enumerate(data['level']) if value == 3]
        df_lvl3 = data.iloc[indexes_level3].sort_values(by = ' set')
        fig_lvl3 = px.bar(df_lvl3, x = ' set', y = ' changeInOccupancy', title = 'Level 3', color = ' changeInOccupancy', 
                                  color_discrete_sequence = ['red' if value <0 else 'green' for value in df_lvl3[' changeInOccupancy']],
                                  text = df_lvl3[' changeInOccupancy'],
                                  hover_data = {' changeInOccupancy': True})

        fig_lvl3.update_traces(marker=dict(color=['red' if value <0 else 'green' for value in df_lvl3[' changeInOccupancy']])) # to ensure that the graph color would just be red and green 
        fig_lvl3.update_layout(hovermode = 'closest')

        # the graph layout given the data from level 3
        tab_bp_layout_level3 = html.Div([
            dcc.Graph(id = 'Graph_1', figure = fig_lvl3),
            dbc.Button("Full Graph", id = "button_lvl3", n_clicks = 0, style = {'float':'right', 'background-color':'black'}),
            html.Div(id = "popup-content", children = [
                dbc.Modal([
                    dbc.ModalHeader("Level 3", style = {'background-color':'grey', 'font-size': '24px', 'font-weight': 'bold'}),
                    dbc.ModalBody([
                        dcc.Graph(id = 'Graph_1', figure = fig_lvl3, style = {'width':'100%', 'height':'100%'}),
                        ],
                        style = {'background-color':'white'}),
                        ], id = "popup", fullscreen = True, centered = True)
                        ]),
                        ], style = {'width':x, 'height' :y, 'display': 'inline-block'})

    if i == 4:
        indexes_level4 = [index for index, value in enumerate(data['level']) if value == 4]
        df_lvl4 = data.iloc[indexes_level4].sort_values(by = ' set')
        fig_lvl4 = px.bar(df_lvl4, x = ' set', y = ' changeInOccupancy', title = 'Level 4', color = ' changeInOccupancy', 
                                  color_discrete_sequence = ['red' if value <0 else 'green' for value in df_lvl4[' changeInOccupancy']])

        fig_lvl4.update_traces(marker=dict(color=['red' if value <0 else 'green' for value in df_lvl4[' changeInOccupancy']]))
        tab_bp_layout_level4 = html.Div([
            dcc.Graph(id = 'Graph_2', figure = fig_lvl4),
            dbc.Button("Full Graph", id = "button_lvl4", n_clicks = 0, style = {'float':'right', 'background-color':'black'}),
            html.Div(id = "popup-content2", children = [
                dbc.Modal([
                    dbc.ModalHeader("Level 4", style = {'background-color':'grey'}),
                    dbc.ModalBody([
                        dcc.Graph(id = 'Graph_2', figure = fig_lvl4, style = {'width': '100%', 'height': '100%'}),
                        ],
                        style = {'background-color':'white'}),
                        ], id = "popup2", fullscreen = True, centered = True)
                        ]),
                        ], style = {'width':x, 'height' :y, 'display': 'inline-block'})
    
    if i == 5:
        indexes_level5 = [index for index, value in enumerate(data['level']) if value == 5]
        df_lvl5 = data.iloc[indexes_level5].sort_values(by = ' set')
        fig_lvl5 = px.bar(df_lvl5, x = ' set', y = ' changeInOccupancy', title = 'Level 5', color = ' changeInOccupancy', 
                                  color_discrete_sequence = ['red' if value <0 else 'green' for value in df_lvl5[' changeInOccupancy']])

        fig_lvl5.update_traces(marker=dict(color=['red' if value <0 else 'green' for value in df_lvl5[' changeInOccupancy']]))
        tab_bp_layout_level5 = html.Div([
            dcc.Graph(id = 'Graph_3', figure = fig_lvl5),
            dbc.Button("Full Graph", id = "button_lvl5", n_clicks = 0, style = {'float':'right', 'background-color':'black'}),
            html.Div(id = "popup-content3", children = [
                dbc.Modal([
                    dbc.ModalHeader("Level 5", style = {'background-color':'grey'}),
                    dbc.ModalBody([
                        dcc.Graph(id = 'Graph_3', figure = fig_lvl5, style = {'width': '100%', 'height': '100%'}),
                        ],
                        style = {'background-color':'white'}),
                        ], id = "popup3", fullscreen = True, centered = True)
                        ]),
                        ], style = {'width':x, 'height' :y, 'display': 'inline-block'})
    
    if i == 6:
        indexes_level6 = [index for index, value in enumerate(data['level']) if value == 6]
        df_lvl6 = data.iloc[indexes_level6].sort_values(by = ' set')
        fig_lvl6 = px.bar(df_lvl6, x = ' set', y = ' changeInOccupancy', title = 'Level 6', color = ' changeInOccupancy', 
                                  color_discrete_sequence = ['red' if value <0 else 'green' for value in df_lvl6[' changeInOccupancy']])

        fig_lvl6.update_traces(marker=dict(color=['red' if value <0 else 'green' for value in df_lvl6[' changeInOccupancy']]))
        tab_bp_layout_level6 = html.Div([
            dcc.Graph(id = 'Graph_4', figure = fig_lvl6),
            dbc.Button("Full Graph", id = "button_lvl6", n_clicks = 0, style = {'float':'right', 'background-color':'black'}),
            html.Div(id = "popup-content4", children = [
                dbc.Modal([
                    dbc.ModalHeader("Level 6", style = {'background-color':'grey'}),
                    dbc.ModalBody([
                        dcc.Graph(id = 'Graph_4', figure = fig_lvl6, style = {'width': '100%', 'height': '100%'}),
                        ],
                        style = {'background-color':'white'}),
                        ], id = "popup4", fullscreen = True, centered = True)
                        ]),
                        ], style = {'width':x, 'height' :y, 'display': 'inline-block'})

# # Dummy inputs 
# df = pd.DataFrame({ # dummy results 
#     'Furniture Set': [1, 2, 3, 4, 5],
#     'Change in Occupancy': [-5, 10, 50, -40, 10]
# })

# The overall skeleton 
app.layout = html.Div([
    dcc.Tabs(id = 'tabs', value = 'BarPlot',children = [
        dcc.Tab(label = 'Overall Change in Occupancy', value = 'tab-1'),
        dcc.Tab(label = 'Occupancy overtime', value = 'tab-2')
    ]),
    html.Div(id = 'tab-content')
])

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
    Input('tabs', 'value')
)

def render_content(tab):
    if tab == 'tab-1': # referring to the 'Overall Change in Occupancy' tab
        to_show =[]
        for i in levels:
            if i == 3:
                to_show.append(tab_bp_layout_level3)
            if i == 4:
                to_show.append(tab_bp_layout_level4)
            if i == 5:
                to_show.append(tab_bp_layout_level5)
            if i == 6:
                to_show.append(tab_bp_layout_level6)
        return html.Div(to_show)
    else: # referring to the 'Occupancy Overtime' tab 
        return html.Div([
            html.H3('Working in Progress')
        ])

if __name__ == '__main__':
    app.run_server(debug = True)
