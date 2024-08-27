from flask import Flask, render_template

import logging

app = Flask(__name__, static_url_path='/static')

logger = logging.getLogger('logger')


@app.route('/', methods=['GET'])
def landing_page():
    # app_controller.curr_env = os.getenv('CURR_ENV')  # dev/prod
    # app_controller.CURR_ENV_LINK_LIT = constants.HOME_URL_LIT_SEL[app_controller.curr_env]
    # fav_link = app_controller.CURR_ENV_LINK_LIT.replace("api", "") + "static/favicon.ico"
    # home_link = app_controller.CURR_ENV_LINK_LIT + "/home"

    return render_template('index.html',
                           )

if __name__ == '__main__':
    app.run()
