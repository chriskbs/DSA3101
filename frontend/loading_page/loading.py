import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import dash_loading_spinners as dls

app = dash.Dash(__name__)

bahnschrift_style = {
    'font-family': 'Bahnschrift, sans-serif'
}

app.layout = html.Div([
    html.Div(
        [
            dcc.Loading(
                id="loading",
                type="default",
                fullscreen=True,
                color="navy",
                children=[
                    html.Div(
                        "Please wait...",
                        style={
                            "color": "navy",
                            "font-size": "24px",
                            "display": "block",
                            "margin-bottom": "20px",
                            **bahnschrift_style,
                        },
                    ),
                    dcc.Loading(
                        type="default",
                        children=[
                            dls.Ring(color="navy"),
                            html.Div(
                                "If undirected in 5 seconds, please click here",
                                style={
                                    "text-align": "center",
                                    "margin-top": "30px",  
                                }
                            ),
                        ],
                    ),
                ],
                style={
                    "position": "absolute",
                    "top": "70%",
                    "left": "50%",
                    "transform": "translate(-50%, -50%)",
                    "text-align": "center",
                },
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
