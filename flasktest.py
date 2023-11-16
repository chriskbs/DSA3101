import pytest
import requests
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_post(requests_mock):
    with patch('requests.post') as mock:
        yield mock

@pytest.fixture
def mock_get(requests_mock):
    # Mock the GET request
    url = 'http://127.0.0.1:5000/download/example.csv'
    requests_mock.get(url, text='Test file content', status_code=200)
    return url

def test_file_upload(mock_post):
    # Specify the API endpoint
    upload_url = 'http://127.0.0.1:5000/upload'

    # Prepare files to upload
    files = {
        'json': ('submission.json', MagicMock(read=lambda: b'json content')),
        'csv': ('entries.csv', MagicMock(read=lambda: b'csv content'))
    }

    # Mock the response from the server
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {'result_csv': 'path/to/result.csv', 'result_json': 'path/to/result.json'}

    # Make the POST request to the API
    response = requests.post(upload_url, params={'exam_period': 'False'}, files=files)

    # Check the response
    assert response.status_code == 200
    result = response.json()
    assert 'result_csv' in result
    assert 'result_json' in result

    # Assert that the mock_post was called with the expected parameters
    mock_post.assert_called_once_with(upload_url, params={'exam_period': 'False'}, files=files)

def test_file_download(requests_mock):
    # Specify the download URL
    download_url = 'http://127.0.0.1:5000/download'

    # Mock the response from the server
    requests_mock.get(f'{download_url}/example.csv', text='Test file content', status_code=200)

    # Make the GET request to the download URL
    response = requests.get(f'{download_url}/example.csv')

    # Check the response
    assert response.status_code == 200
    assert response.text == 'Test file content'

    #test on terminal at the correct directory using
    ## pytest flasktest.py