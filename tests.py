import unittest


from app import app, db

class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_check_status(self):
        reponse = self.app.get('/status')