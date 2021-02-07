# import os
from flask import Flask, jsonify, render_template

# from player import Player
from scientist import ALL_SCIENTISTS


app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('scientist_scroller.html')


@app.route('/scientists')
def scientists():
    scientists = sorted(ALL_SCIENTISTS, key=lambda s: s.year)
    scientists_json = [scientist.toJSON() for scientist in scientists]
    return jsonify(scientists_json)


# @app.route('/')
# def index():
#     return 'Index Page'


# @app.route('/')
# def index():
#     return 'Index Page'



# def play_game():
#     os.system('clear')
#     player = Player()
#     # TODO: make this some kind of loop
#     won = player.start_battle(heat={}, lifelines={})


# if __name__ == '__main__':
#     play_game()
