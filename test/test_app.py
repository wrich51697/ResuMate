import unittest
from app import app


class BasicTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Resume Upload Form', response.data)

    def test_upload_no_file(self):
        response = self.app.post('/upload', data={})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No file part', response.data)

    def test_upload_file(self):
        data = {
            'resume': (open('tests/test_resume.txt', 'rb'), 'test_resume.txt')
        }
        response = self.app.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'skills', response.data)


if __name__ == "__main__":
    unittest.main()
