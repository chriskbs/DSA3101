# testing flask for uploads and downloads
import unittest
from flask_testing import TestCase
import app as app

class TestApp(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app.server

    def test_file_upload(self):
        # Simulate a file upload
        with open('data/20230413_clb_taps.csv', 'rb') as file:
            response = self.client.post('http://127.0.0.1:5000/upload', data={'entries.csv': (file, '20230413_clb_taps.csv')})

        # Assertions for upload endpoint
        self.assertEqual(response.status_code, 200)

    def test_file_download(self):
        # Simulate a file download request
        response = self.client.get('http://127.0.0.1:5000/download')

        # Assertions for download endpoint
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
