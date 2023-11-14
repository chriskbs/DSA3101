import dash
from dash import dcc, html #, Input, Output
import base64
# import requests
# from io import BytesIO
import os 
external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

image_path = r"data/CSV.png"

with open(image_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

json_files_path = r"data/seat arrangement"
csv_files_path = r"data/period"
def get_json_filenames(directory):
    return [{'label': os.path.splitext(filename)[0], 'value': filename} 
            for filename in os.listdir(directory) 
            if filename.endswith(".json")]

home = html.Div([
        html.A(html.Button("Home", className="home-btn", id="home-button"), href="/"),
    ], style={'position': 'absolute', 'top': '20px', 'left': '20px'})

seat_arrangement_dp = dcc.Dropdown(
    id='submission-dropdown',
    options=get_json_filenames(json_files_path),
    style={'width': '250px', 'margin': 'auto'},
    value='random submission.json'
)

seat_arrangement_div = html.Div([
    html.H3("Choose Submission", style={'color': 'navy', 'font-size': '18px'}),
    seat_arrangement_dp,
    html.I(className="fas fa-caret-down", style={'color': 'navy', 'font-size': '18px', 'margin-top': '10px'})
], className="feature")

period_dp = dcc.Dropdown(
            id='period-dropdown',
            options=[
                {'label': 'Normal Period', 'value': 'normal.csv'},
                {'label': 'Exam Period', 'value': 'exam.csv'},
                {'label': 'Event Period', 'value': 'event.csv'},
            ],
            style={'width': '250px', 'margin': 'auto'},
        )

period_div = html.Div([
        html.H3("Choose Period", style={'color': 'navy', 'font-size': '18px'}),
        period_dp
    ], className="feature")

rs_layout = html.Div([
    home,
    seat_arrangement_div,
    period_div,
    html.Div("OR", style={'color': 'navy', 'font-size': '20px', 'margin-top': '20px'}),

    html.Div([
        html.Div("CSV Sample", style={'color': 'navy', 'font-size': '18px', 'margin-top': '20px'}),
        html.Img(src=f"data:image/png;base64,{encoded_image}", style={'width': '200px', 'height': '200px', 'margin-left': '10px', 'margin-top': '10px'}),
        dcc.Upload(
            id='upload-data',
            children=[
                html.Button("Submit Custom Period", className="btn", id="submit-button", style={'font-size': '18px'}),
            ],
            style={'margin-top': '10px'},
            multiple=False
        ),
    ], className="feature"),
    html.Div([
        html.I(className="fas fa-caret-down", style={'color': 'navy', 'font-size': '18px', 'margin-top': '20px'}),
    ], className="feature"),

    html.Div([
        html.Button("Run Simulation", id="run_sim", className="btn-run", style={'margin-top': '30px', 'font-size': '18px', 'margin-bottom': '30px'})
    ], className="feature"),
    
    html.Div(id='output-data-upload'),
], className="feature-container", style={'text-align': 'center', 'padding-top': '50px'})

app.layout = rs_layout

# @app.callback(
#     Output('submission-dropdown', 'value'),
#     Input('submission-dropdown', 'value')
# )
# def update_selected_submission(selected_submission):
#     global selected_submission_file_path
#     if selected_submission == 'option1':
#         selected_submission_file_path = r"data/seat arrangement/random submission.json"
#     if selected_submission == 'option2':
#         selected_submission_file_path = r"data/seat arrangement/random submission2.json"
#     if selected_submission == 'option3':
#         selected_submission_file_path = r"data/seat arrangement/random submission3.json"
#     # Add similar conditions for other options if needed
#     return selected_submission

# @app.callback(Output('output-data-upload', 'children'),
#               Input('upload-data', 'contents'))
# def update_output(list_of_contents):
#     if list_of_contents is not None:
#         content = list_of_contents[0]
#         return content


# @app.callback(Output('output-data-upload', 'children'),
#               [Input('upload-data', 'contents'),
#                Input('submit-button', 'n_clicks')])
# def update_output(list_of_contents, n_clicks):
#     ctx = dash.callback_context
#     triggered_id = ctx.triggered_id if ctx.triggered_id else 'No trigger'
    
#     if triggered_id == 'upload-data.contents':
#         if list_of_contents is not None:
#             content = list_of_contents[0]
#             return content
#     elif triggered_id == 'submit-button.n_clicks':
#         if n_clicks is None:
#             raise PreventUpdate

#         upload_url = 'http://127.0.0.1:5000/upload'

#         files = {
#             'json': ('submission.json', open('static/lib_sections.json', 'rb')),
#             'csv': ('entries.csv', open('data/20230413_clb_taps.csv', 'rb'))
#         }

#         response = requests.post(upload_url, params={'exam_period': 'False'}, files=files)

#         if response.status_code == 200:
#             result = response.json()
#             message = f'Files processed successfully. Result CSV file: {result["result_csv"]}, Result JSON file: {result["result_json"]}'
#         else:
#             message = f'Error: {response.status_code}\n{response.json()}'

#         return html.Div(message)

#     return None  
    
if __name__ == '__main__':
    app.run_server(debug=True)
