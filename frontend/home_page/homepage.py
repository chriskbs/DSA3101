import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from datetime import datetime

app = dash.Dash(__name__)

image_url = "https://blog.nus.edu.sg/linus/files/2020/02/20200115_083307.jpg"

bahnschrift_style = {
    'font-family': 'Bahnschrift, sans-serif'
}

clickable_style = {
    'cursor': 'pointer',
    'transition': 'background-color 0.3s, color 0.3s',
}

translucent_image_style = {
    'width': '100%',
    'height': 'auto',
    'opacity': 0.7,
}


header_style = {
    'background-color': '#0A2E4B',
    'color': 'white',
    'position': 'fixed',
    'top': '0',
    'left': '0',
    'width': '100%',
    'z-index': '1',
    'padding': '10px',  
}

button_style = {
    'background-color': '#0A2E4B',
    'color': 'white',
    'font-size': '16px',
    'border-radius': '10px',
    'width': '100%',
    'display': 'flex',
    'justify-content': 'center',
    'align-items': 'center',
    **bahnschrift_style,
    **clickable_style
}

app.layout = html.Div([
    html.Div([
        html.H1("Central Library Occupancy Rate Simulator", style={'text-align': 'center', 'margin-bottom': '20px', 'font-size': '30px', **bahnschrift_style}),
        html.H2(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), style={'text-align': 'center', **bahnschrift_style}),
    ],
        style=header_style
    ),
    html.Div([
        html.Img(src=image_url, style=translucent_image_style),
        html.Div([
            html.Div([
                html.Button("Check past simulations", id="check-past-simulations-button", style=button_style),
                html.P("📊", style={'font-size': '24px', 'background-color': 'white', 'border-radius': '50%', 'width': '40px', 'height': '40px', 'text-align': 'center', **clickable_style}),
            ], style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'margin-bottom': '10px'}),
            html.Div([
                html.Button("Add new seat arrangement", id="add-seat-arrangement-button", style=button_style),
                html.P("➕", style={'font-size': '24px', 'background-color': 'white', 'border-radius': '50%', 'width': '40px', 'height': '40px', 'text-align': 'center', **clickable_style}),
            ], style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'margin-bottom': '10px'}),
            html.Div([
                html.Button("Choose seat arrangement & simulated period to run model", id="run-model-button", style=button_style),
                html.P("⚙️", style={'font-size': '24px', 'background-color': 'white', 'border-radius': '50%', 'width': '40px', 'height': '40px', 'text-align': 'center', **clickable_style}),
            ], style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center'}),
        ],
            style={'position': 'absolute', 'top': '60%', 'left': '50%', 'transform': 'translate(-50%, -50%)', 'display': 'flex', 'flex-direction': 'column'}),
    ],
        style={'position': 'relative', 'top': '0', 'height': '100vh', 'overflow': 'hidden', 'background-color': 'black'}),
],
    style={'background-color': 'black', 'height': '100vh'})

if __name__ == '__main__':
    app.run_server(debug=True)
