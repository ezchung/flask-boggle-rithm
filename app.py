from urllib import response
from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

TEST_GAME = BoggleGame()
TEST_GAME.board = [
    ['K','B','O','F','E'],
    ['S','I','E','K','D'],
    ['A','H','O','B','G'],
    ['E','A','S','S','L'],
    ['E','W','L','L','K']
]

# The boggle games created, keyed by game id
games = {
    'd34ad458-eaaa-49fc-9dd1-b7e8999bae1f':
        TEST_GAME
}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game
    board = game.board

    return {"gameId": "need-real-id", "board": "need-real-board"}


@app.post('/api/score-word')
def score_word():
    # print("---------HELLO NEW TEST--------")
    # print("request form is", request.form)
    # print("request type is", type(request.form))
    # breakpoint()
    data = request.get_json()
    game_id = data.get("game_id")
    word = data.get("word")

    if not game_id or not word:
        return {"result": "ERROR: bad input"}

    game_instance = games.get(game_id)

    if game_instance == None:
        return {"result": "ERROR: no such game"}

    is_on_board = game_instance.check_word_on_board(word)
    is_word = game_instance.is_word_in_word_list(word)

    if is_on_board and is_word:
        return {"result": "ok"}
    elif not is_word:
        return {"result": "not-word"}
    else:
        return {"result": "not-on-board"}
