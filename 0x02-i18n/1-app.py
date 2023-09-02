#!/usr/bin/env python3
"""Flask app
"""
from flask import Flask, render_template
from flask_babel import Babel


class Config(object):
    """Config for languages
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)


@app.route('/', methods=["GET"], strict_slashes=False)
def index():
    """Return index
    """
    return render_template('1-index.html')


if __name__ == ('__main__'):
    app.run()
