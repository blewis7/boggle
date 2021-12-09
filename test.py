from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def test_setup(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
     
    def test_homepage(self):
        response = self.client.get('/')
        self.assertsIn(b'<p>Highscore:', response.data)
        self.assertsIn('board', session)
        self.assertsIn(b'Score:', response.data)
        self.assertsIn(b'Time:', response.data)
        self.assertNotIn(b"<b class='timer'>-1</b>", response.data)
    
    def test_check_words(self):
        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [['L', 'O', 'V', 'E', 'Z'], 
                                    ['L', 'O', 'V', 'E', 'Z'], 
                                    ['L', 'O', 'V', 'E', 'Z'], 
                                    ['L', 'O', 'V', 'E', 'Z'], 
                                    ['L', 'O', 'V', 'E', 'Z']]

        valid = self.client.get('/check-word?word=love')
        self.assertEqual(valid.json['result'], 'ok')

        invalid = self.client.get('/check-word?word=lovez')
        self.assertEqual(invalid.json['result'], 'not-word')

        absent = self.client.get('/check-word?word=crazy')
        self.assertEqual(absent.json['result'], 'not-on-board')
                
