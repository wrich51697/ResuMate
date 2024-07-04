import unittest
from app import create_app


class TemplateTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config.TestingConfig')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_index_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Index</title>', response.data)  # Assuming your index.html contains <title>Index</title>


if __name__ == '__main__':
    unittest.main()
