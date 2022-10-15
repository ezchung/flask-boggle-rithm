from urllib import response
from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"


# The boggle games created, keyed by game id
games = {}


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

    return {"game_id": game_id, "board": board}


@app.post('/api/score-word')
def score_word():
    """Handles post request to score word when given game_id and word"""

    data = request.get_json()
    game_id = data["game_id"]
    word = data["word"]

    game_instance = games[game_id]

    is_on_board = game_instance.check_word_on_board(word)
    is_word = game_instance.is_word_in_word_list(word)

    if is_on_board and is_word:
        return {"result": "ok"}
    elif not is_word:
        return {"result": "not-word"}
    else:
        return {"result": "not-on-board"}
