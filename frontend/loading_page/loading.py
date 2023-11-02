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
                            dcc.Interval(
                                id='timer',
                                interval=1000,  
                                n_intervals=0
                            ),
                            html.Div(
                                id='timer-output',
                                children='Timer: 0s',
                                style={**bahnschrift_style, "margin-top": "30px"}  
                            )
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

@app.callback(
    Output('timer-output', 'children'),
    Input('timer', 'n_intervals')
)
def update_timer(n):
    return f'Timer: {n}s'

if __name__ == "__main__":
    app.run_server(debug=True)
