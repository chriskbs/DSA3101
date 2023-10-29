import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_loading_spinners as dls  

app = dash.Dash(__name__)


app.layout = html.Div([
    html.Div(
        [
            dcc.Loading(
                id="loading",
                type="default",
                fullscreen=True,  
                color="navy",  # Text color
                children=[
                    html.Div(
                        "Loading",
                        style={
                            "color": "navy",
                            "font-size": "24px",
                            "display": "inline",
                        },
                    ),
                    dcc.Loading(
                        type="default",
                        children=[
                            dls.Ring(color="navy"),  
                        ],
                    ),
                ],
            ),
        ],
        style={
            "position": "absolute",
            "top": "50%",
            "left": "50%",
            "transform": "translate(-50%, -50%)",
            "text-align": "center",
        },
    ),
])

if __name__ == "__main__":
    app.run_server(debug=True)
