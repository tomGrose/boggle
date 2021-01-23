from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client
        app.config['TESTING'] = True

    def test_board_build(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Play Boggle!</h1>', html)
            self.assertIsNone(session.get('high_score'))
            self.assertIsNone(session.get('times_played'))
            self.assertIn('game_board', session)


    def test_valid_guess(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['game_board'] = [["J", "O","Y", "L", "K"],\
                    ["H", "Z","P", "L", "W"],\
                    ["r", "O","N", "P", "K"],\
                    ["v", "X","Y", "L", "X"],\
                    ["W", "O","Y", "S", "K"]]

            resp = client.get('/guess?user_guess=joy')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('ok', html)

    def test_wrong_guess(self):
        with app.test_client() as client:
            client.get('/')
            resp = client.get('/guess?user_guess=acylamidobenzene')
            self.assertEqual(resp.json['result'], 'not-on-board')

    def test_invalid_guess(self):
        with app.test_client() as client:
            client.get('/')
            resp = client.get('/guess?user_guess=kdjdjfhjfj')
            self.assertEqual(resp.json['result'], 'not-word')

    
    
    def test_data_response(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['high_score'] = 4
            resp = client.post('/stats',
                               data={'high_score': '5'})
            #stats = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json['high_score'], '4')
    