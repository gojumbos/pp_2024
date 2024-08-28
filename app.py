from flask import Flask, render_template

import logging

app = Flask(__name__, static_url_path='/static')

logger = logging.getLogger('logger')


@app.route('/', methods=['GET'])
def landing_page():

    return render_template('index.html',
                           )


# @app.route('/paper', methods=['GET'])
# def landing_page():
#
#     return render_template('index.html',
#                            )



