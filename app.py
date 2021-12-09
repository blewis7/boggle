from flask import Flask, request, render_template, flash, redirect, session
from flask.json import jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'brockisgood'

boggle_game = Boggle()

@app.route('/')
def homepage():
    '''Open to homepage that contains a button to begin the game'''
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore', 0)

    return render_template('base.html', board=board, highscore=highscore)


@app.route('/check-word')
def check():
    '''check if word is valid and return it to my-script.js'''
    word = request.args['word']
    board = session['board']
    result = boggle_game.check_valid_word(board, word)

    return jsonify({'result': result})


@app.route('/post-score', methods=['POST'])
def post_score():
    '''check if a new highscore was achieved and post if so'''
    score = request.json['score']
    highscore = session.get('highscore', 0)

    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)
