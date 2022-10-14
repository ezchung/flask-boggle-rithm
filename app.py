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

    return {"gameId": "need-real-id", "board": "need-real-board"}


@app.post('/api/score-word')
def score_word():
    print("---------HELLO NEW TEST--------")
    print("request form is", request.form)
    print("request type is", type(request.form))

    game_id = request.form.get("game_id")
    word = request.form.get("word")

    return {'game': game_id, 'isThisJSON': "iStHiSjSoN"}
