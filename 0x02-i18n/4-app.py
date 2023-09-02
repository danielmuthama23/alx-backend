#!/usr/bin/env python3
"""Flask app
babel.init_app(app, locale_selector=get_locale)
"""
from flask import Flask, render_template, request
from flask_babel import Babel
from flask_babel import gettext as _


class Config(object):
    """Config languages
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """Get locale selector for babel
    """
    if request.args.get('locale'):
        lang = request.args.get('locale')
        if lang in app.config['LANGUAGES']:
            return lang
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', methods=["GET"], strict_slashes=False)
def index():
    """Return index
    """
    return render_template('4-index.html')


if __name__ == ('__main__'):
    app.run(debug=True)
