from lib_simulation import run_simulation
from flask import Flask, request, jsonify, send_file
import json
import pandas as pd
import os
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'downloads'
ALLOWED_EXTENSIONS = {'json', 'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def compute_avg_score(graph_df, attribute):
    return (graph_df[attribute] * graph_df['capacity']).sum()/graph_df['capacity'].sum()

@app.route('/test', methods=['GET'])
def test():
    print('zuccess')
    return '200'

@app.route('/upload', methods=['POST'], defaults={'exam_period':'False', 'num_runs':1})
def upload_files(exam_period, num_runs):
    # Check if the POST request has the .json file part
    if 'json' not in request.files:
        return jsonify({'error': 'Missing .json file'}), 400
    else:
        json_file = request.files['json']
    
    # TODO: Use num_runs to do number of batch runs
    # Exam period
    exam_period = exam_period == 'False'


    # Check if the files have the allowed extensions
    if json_file and allowed_file(json_file.filename):
        # Save the files to the upload folder
        json_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'input.json')
        csv_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'input.csv')

        # check if the POST request has .csv file, else proceed with default file
        if 'csv' not in request.files:
            if exam_period:
                csv_data = pd.read_csv('data/dummy_exam_period.csv')
            else:
                csv_data = pd.read_csv('data/dummy_normal_period.csv')
        else: 
            csv_file = request.files['csv']
            if not allowed_file(csv_file.filename):
                return jsonify({'error': '.csv file is not in the right format'}), 400
            csv_file.save(csv_filename)
            csv_data = pd.read_csv(csv_filename)

        json_file.save(json_filename)

        # Process the files (example: concatenate the dataframes)
        json_data = json.load(open(json_filename))

        submission_name = json_data['submission_name']

        result_df, sections_df = run_simulation(csv_data, json_data, exam_period=exam_period)
        result_json = {
            'name': json_data['submission_name'],
            'score': compute_avg_score(sections_df, 'overall'),
            'privacy': compute_avg_score(sections_df, 'privacy'),
            'crowd level': compute_avg_score(sections_df, 'crowd_level'),
            'comfort': compute_avg_score(sections_df, 'comfort'),
            'scenery': compute_avg_score(sections_df, 'scenery'),
            'lighting': compute_avg_score(sections_df, 'lighting'),
            'crowd level': compute_avg_score(sections_df, 'crowd_level'),
            'ease of access': compute_avg_score(sections_df, 'ease_find'),
        }

        # Save the result to the output folder
        result_csv_filename = os.path.join(app.config['OUTPUT_FOLDER'], f'{submission_name}.csv')
        result_json_filename = os.path.join(app.config['OUTPUT_FOLDER'], f'{submission_name}.json')

        result_df.to_csv(result_csv_filename, index=False)
        with open(result_json_filename,'w') as fi:
            json.dump(result_json, fi, indent = 4)

        return jsonify({'message': 'Files processed successfully',
                        'result_csv': f'{submission_name}.csv',
                        'result_json': f'{submission_name}.json'}), 200
    else:
        return jsonify({'error': 'Invalid file format'}), 400
    
@app.route('/download/<filename>')
def download_file(filename):
    # Provide the path to the file in the outputs folder
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)

    # Check if the file exists
    if os.path.exists(file_path):
        # Return the file using Flask's send_file function
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)