from flask import Flask, request, jsonify, render_template


import logging

import ai

app = Flask(__name__, static_url_path='/static')

logger = logging.getLogger('logger')

ai_object = ai.ai_object()

@app.route('/', methods=['GET'])
def landing_page():

    return render_template('index.html',
                           )

@app.route('/twenty_q', methods=['GET'])
def twenty_q():

    return render_template('twenty_q.html',
                           )


@app.route('/start_chat', methods=['POST'])
def start_chat():

    ai_object.reset()
    reply = ai_object.ai_start_chat()
    for x in ai_object.conversation:
        print(x)
        print("\n")
    return jsonify({'reply': reply})




@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    reply = ai_object.ai_chat(user_message)
    for x in ai_object.conversation:
        print(x)
        print("\n")
    return jsonify({'reply': reply})



