import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css'
    ),
    html.Div([
        html.Div([
            html.H4("Choose Submission", style={'color': 'navy'}),
            dcc.Dropdown(
                options=[
                    {'label': 'Option 1', 'value': 'option1'},
                    {'label': 'Option 2', 'value': 'option2'},
                    {'label': 'Option 3', 'value': 'option3'}
                ],
                style={'width': '150px', 'margin': 'auto'},
            ),
            html.I(className="fas fa-caret-down", style={'color': 'navy', 'margin-top': '20px'})
        ], className="feature"),
        
        html.Div([
            html.H4("Choose Period", style={'color': 'navy'}),
            dcc.Dropdown(
                options=[
                    {'label': '9am ~ 10am', 'value': '9am ~ 10am'},
                    {'label': '10am ~ 11am', 'value': '10am ~ 11am'},
                    {'label': '11am ~ 12pm', 'value': '11am ~ 12pm'},
                    {'label': '12pm ~ 1pm', 'value': '12pm ~ 1pm'},
                    {'label': '1pm ~ 2pm', 'value': '1pm ~ 2pm'},
                    {'label': '2pm ~ 3pm', 'value': '2pm ~ 3pm'},
                    {'label': '3pm ~ 4pm', 'value': '3pm ~ 4pm'},
                    {'label': '4pm ~ 5pm', 'value': '4pm ~ 5pm'},
                    {'label': '5pm ~ 6pm', 'value': '5pm ~ 6pm'},
                    {'label': '6pm ~ 7pm', 'value': '6pm ~ 7pm'},
                    {'label': '7pm ~ 8pm', 'value': '7pm ~ 8pm'},
                    {'label': '8pm ~ 8am', 'value': '8pm ~ 9pm'},
                    {'label': '9am ~ 10am', 'value': '9pm ~ 10pm'},
                    {'label': '10am ~ 11am', 'value': '10pm ~ 11pm'},
                    {'label': '11am ~ 12pm', 'value': '11pm ~ 12am'},
                    {'label': '12pm ~ 1pm', 'value': '12am ~ 1am'},
                    {'label': '1pm ~ 2pm', 'value': '1am ~ 2am'},
                    {'label': '2pm ~ 3pm', 'value': '2am ~ 3am'},
                    {'label': '3pm ~ 4pm', 'value': '3am ~ 4am'},
                    {'label': '4pm ~ 5pm', 'value': '4am ~ 5am'},
                    {'label': '5pm ~ 6pm', 'value': '5am ~ 6am'},
                    {'label': '6pm ~ 7pm', 'value': '6am ~ 7am'},
                    {'label': '7pm ~ 8pm', 'value': '7am ~ 8am'}
                ],
                style={'width': '150px', 'margin': 'auto'},
            ),
        ], className="feature"),
        
        html.Div("OR", style={'color': 'navy', 'font-size': '20px', 'margin-top': '5px'}),  
        
        html.Div([
            html.Button("Submit CSV", className="btn", id="submit-button", style={'margin-top': '10px'}),
        ], className="feature"),
        
        html.Div([
            html.I(className="fas fa-caret-down", style={'color': 'navy', 'margin-top': '20px'}),  
        ], className="feature"),
        
        html.Div([
            html.Button("Run Simulation", className="btn-run", style={'margin-top': '20px'})  
        ], className="feature")
    ], className="feature-container")
], className="page", style={'text-align': 'center', 'padding-top': '50px'})

@app.callback(
    Output('submit-button', 'n_clicks'),
    Input('submit-button', 'n_clicks')
)
def trigger_upload(n_clicks):
    return None

if __name__ == '__main__':
    app.run_server(debug=True)
