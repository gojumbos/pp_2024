from flask import Flask, request, jsonify, render_template


import logging

import ai
from ai import ChatManager
from random import randint
import time

app = Flask(__name__, static_url_path='/static')

logger = logging.getLogger('logger')

chatManager = ChatManager()

@app.route('/', methods=['GET'])
def landing_page():

    return render_template('index.html',
                           )

@app.route('/twenty_q', methods=['GET'])
def twenty_q():
    print("CHATS", chatManager.chat_count())
    return render_template('twenty_q.html',
                           )


@app.route('/start_chat', methods=['POST'])
def start_chat():
    chat_id = chatManager.add_chat()
    reply = chatManager.start_chat(global_id=chat_id)
    print("START CHAT", chat_id)
    # reply = ai_object.ai_start_chat()
    for x in chatManager.get_convo(chat_id):
        print(x)
        print("\n")
    return jsonify({'reply': reply,
                    'chat_id': chat_id
                    })



@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    chat_id = int(request.json.get('chat_id'))

    print(f'Chat() Chat id: {chat_id}')
    # reply = ai_object.ai_chat(user_message)
    reply = chatManager.send_chat(global_id=chat_id,
                                  user_message=user_message)
    for x in chatManager.get_convo(chat_id):
        print(f'Chat id: {chat_id}, {x}')
        print("\n")
    return jsonify({'reply': reply})


@app.route('/reset_chats', methods=['GET'])
def reset_chats():
    user_message = request.json.get('message', '')
    chatManager.clear_all_chats()
    ct = chatManager.chat_count()
    return jsonify({'reply': f'Chats reset: counter {ct}'})

