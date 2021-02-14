from flask import Flask, jsonify, send_file, make_response, send_from_directory

# from player import Player
from scientist import ALL_SCIENTISTS


app = Flask(__name__)


@app.route('/')
def home_page():
    return send_file('./static/scientist_scroller.html')


@app.route('/service_worker.js')
def service_worker():
    """
    Normally this would just be served directly from the static directly where it lives. But we need to add this 
    'Service-Worker-Allowed' header so that the worker can have access to all requests. That way we can cache all pages
    """
    response = make_response(send_from_directory('static',filename='service_worker.js'))
    #change the content header file
    response.headers['Content-Type'] = 'application/javascript'
    response.headers['Service-Worker-Allowed'] = '/'
    return response


@app.route('/scientists')
def scientists():
    scientists = sorted(ALL_SCIENTISTS, key=lambda s: s.year)
    scientists_json = [scientist.toJSON() for scientist in scientists]
    return jsonify(scientists_json)


@app.route('/player')
def player():
    return jsonify()



# def play_game():
#     os.system('clear')
#     player = Player()
#     # TODO: make this some kind of loop
#     won = player.start_battle(heat={}, lifelines={})


# if __name__ == '__main__':
#     play_game()
