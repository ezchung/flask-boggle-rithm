from unittest import TestCase

from app import app, games

from boggle import BoggleGame


TEST_GAME = BoggleGame() #this is not a global const
TEST_GAME.board = [
    ['K','B','O','F','E'],
    ['S','I','E','K','D'],
    ['A','H','O','B','G'],
    ['E','A','S','S','L'],
    ['E','W','L','L','K']
]

games['d34ad458-eaaa-49fc-9dd1-b7e8999bae1f'] = TEST_GAME

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

TEST_GAME_ID = 'd34ad458-eaaa-49fc-9dd1-b7e8999bae1f'


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            # test that you're getting a template
            self.assertIn('<title>Boggle</title>', html)
            self.assertEqual(response.status_code, 200)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post('/api/new-game')
            data = response.get_json()

            # write a test for this route
            self.assertEqual(type(data["gameId"]), str)
            self.assertEqual(type(data["board"]), list) #this is failing
            self.assertEqual(type(data["board"].pop()), list)
            self.assertNotEqual(data["board"], [])
            self.assertNotEqual(data["board"], [[]])

    def test_score_word(self):
        """Test get word score"""

        with self.client as client:
            response = client.post(
                "/api/score-word",
                json={
                    "word": "FED",
                    "game_id": TEST_GAME_ID
                }
                )

            self.assertEqual(response.status_code, 200)
            response_dict = response.get_json()
            self.assertEqual(response_dict.get('result'), 'ok') #square bracket. more strict!

        with self.client as client:
            response = client.post(
                "/api/score-word",
                json={
                    "word": "STRING",
                    "game_id": TEST_GAME_ID
                }
                )

            self.assertEqual(response.status_code, 200)
            response_dict = response.get_json()
            self.assertEqual(response_dict.get('result'), 'not-on-board')

        with self.client as client:
            response = client.post(
                "/api/score-word",
                json={
                    "word": "ASDF",
                    "game_id": TEST_GAME_ID
                }
                )
            response_dict = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response_dict.get('result'), 'not-word')
