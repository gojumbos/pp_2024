from flask import Flask, request, jsonify, render_template


import logging

app = Flask(__name__, static_url_path='/static')

logger = logging.getLogger('logger')


@app.route('/', methods=['GET'])
def landing_page():

    return render_template('index.html',
                           )

@app.route('/twenty_q', methods=['GET'])
def twenty_q():

    return render_template('twenty_q.html',
                           )


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    #trest
    reply = f"You said: {user_message}"

    return jsonify({'reply': reply})


# @app.route('/paper', methods=['GET'])
# def landing_page():
#
#     return render_template('index.html',
#                            )



