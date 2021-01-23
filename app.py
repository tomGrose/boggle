from boggle import Boggle
from flask import Flask, request, render_template, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "turtles"

debug = DebugToolbarExtension(app)

boggle_game = Boggle()


@app.route('/')
def build_board():
    """ 
    call the make board method of the boggle class when the root page is loaded. 
    Send the board as a variable to jinja to render on the board html template 
    """
    board = boggle_game.make_board()
    session["game_board"] = board
    high_score = session.get("high_score", 0)
    times_played = session.get("times_played", 0)
    return render_template("board.html", board=board, high_score=high_score, times_played = times_played)



@app.route("/guess")
def check_guess():
    """ 
    Recieve the post request with the users guess, check to see if it is valid
    and on the board by calling the check_valid_word method. Return the result
    """
    guess = request.args["user_guess"]
    board = session["game_board"]
    is_correct = boggle_game.check_valid_word(board, guess)
    answer = {'result': is_correct}
    return jsonify(answer)


@app.route("/stats", methods=["POST"])
def updateStats():
    """
    Recieve the final score once a game has completed. check to see if high score and times 
    played have been initialized in the session yet.If the score from the game is higher than 
    the high score from session update the session to reflect this. Update the times played by 1
    Return times played and the high score.
    """
    post = request.get_json()
    score = int(post.get("high_score"))
    high_score = session.get("high_score", 0)
    times_played = session.get("times_played", 0)

    if score > high_score:
        session["high_score"] = score
        high_score = session["high_score"]
    
    times_played += 1
    session["times_played"] = times_played

    stats = {"high_score": high_score, "times_played": times_played}
    return jsonify(stats)