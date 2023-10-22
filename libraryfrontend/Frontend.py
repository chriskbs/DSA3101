import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import base64
from datetime import datetime

app = dash.Dash(__name__)

# Image URLs
image_url = "https://scontent.fsin14-1.fna.fbcdn.net/v/t1.6435-9/124273130_10158705825858540_3544426173736036766_n.jpg?_nc_cat=105&ccb=1-7&_nc_sid=7f8c78&_nc_ohc=7PF7Bw7iamkAX_KVrDp&_nc_ht=scontent.fsin14-1.fna&oh=00_AfDZ4EiHTaB8Kh8p67dGOx1JF7QGat3Pw2AKUTpMlIjE4Q&oe=655C20FB"
past_simulation_image_url = "https://www.shanelynn.ie/wp-content/uploads/2014/01/SOM_heatmaps_all-e1425208462463.jpg"

app.layout = html.Div([
    html.H1("Central Library Occupancy Rate Simulator", style={'text-align': 'center', 'color': 'white', 'margin-bottom': '20px'}),
    
    # Date and time in the middle of the first image
    html.H2(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), style={'text-align': 'center', 'color': 'white'}),
    
    # "New Simulation" button and mini text box in the middle of the first image
    html.Div([
        html.Img(src=image_url, style={'width': '100%', 'opacity': 0.6}),
        html.Div([
            html.Div("No. of pax?", style={'color': 'white', 'text-align': 'center'}),
            dcc.Input(id="mini-text-box", type="text", placeholder="Enter the number", style={'margin-top': '5px', 'text-align': 'center'}),
            html.Button("New Simulation", id="new-simulation-button", style={'background-color': 'black', 'color': 'white'}),
        ], style={'position': 'absolute', 'top': '50%', 'left': '50%', 'transform': 'translate(-50%, -50%)', 'display': 'flex', 'flex-direction': 'column'}),
    ], style={'position': 'relative'}),
    
    # Past simulation data with a centered and smaller image
    html.Div([
        html.H3("Past simulation data", style={'text-align': 'center', 'color': 'white'}),
        html.Img(src=past_simulation_image_url, style={'max-width': '100%', 'display': 'block', 'margin': '0 auto'}),
    ], style={'position': 'relative'}),
    
    # Previous and Next Page buttons on the same row, right-aligned
    html.Div([
        html.Button("Previous Page", id="previous-page-button", style={'background-color': 'black', 'color': 'white'}),
        html.Button("Next Page", id="next-page-button", style={'background-color': 'black', 'color': 'white'}),
    ], style={'display': 'flex', 'justify-content': 'flex-end', 'margin-top': '10px'}),
    
    # Add a component with the ID "simulation-history"
    dcc.Store(id="simulation-history", data=[]),
], style={'background-color': 'black'})

@app.callback(
    Output("simulation-history", "data"),
    Input("new-simulation-button", "n_clicks"),
)
def update_simulation_data(n_clicks):
    if n_clicks is not None:
        # You can update the simulation history data here
        return []
    else:
        return []

if __name__ == '__main__':
    app.run_server(debug=True)
