import unittest
from app import app

class TestAplikace(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.klient = app.test_client()

    def test_hlavni_stranky(self):
        odpoved = self.klient.get('/')
        self.assertEqual(odpoved.status_code, 200)

if __name__ == "__main__":
    unittest.main()
