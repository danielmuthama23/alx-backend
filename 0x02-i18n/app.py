#!/usr/bin/env python3
"""Flask app for i18n practice"""

from datetime import datetime
from flask import Flask, render_template, request, g
from flask_babel import Babel
from flask_babel import gettext as _
from pytz import timezone
from pytz.exceptions import UnknownTimeZoneError


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config(object):
    """Config for languages"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """Get locale selector for babel"""
    if request.args.get('locale'):
        lang = request.args.get('locale')
        if lang in app.config['LANGUAGES']:
            return lang
    elif g.user and g.user['locale'] in app.config['LANGUAGES']:
        lang = g.user['locale']
        return lang
    else:
        return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user():
    """Get user or return None
    args: None
    return: user(str)
    """
    user_id = request.args.get('login_as', None)
    return users.get(int(user_id)) if user_id else None


def fmt_timezone():
    """Return current time with format"""
    timezone = get_timezone()
    loc_dt = timezone.localize(datetime.utcnow())
    return loc_dt.strftime('%b %d, %Y %H:%M:%S')


@app.before_request
def before_request():
    """before request for user"""
    g.user = get_user()
    g.current_time = fmt_timezone()


def checked_timezone(time_zone: str):
    """timezone validator

    args:
        time_zone: str
    """
    try:
        return timezone(time_zone)
    except UnknownTimeZoneError:
        return None


@babel.timezoneselector
def get_timezone():
    """
    Get timezone with regards to:
    1.- timezone parameter in URL parameters
    2.- time zone from user settings
    3.- Default to UTC
    """
    timezone = request.args.get('timezone')
    if timezone:
        zone = checked_timezone(timezone)
    elif g.user and g.user['timezone']:
        zone = checked_timezone(g.user['timezone'])
    else:
        zone = app.config['BABEL_DEFAULT_TIMEZONE']
    return zone if zone else app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/', methods=["GET"], strict_slashes=False)
def index():
    """Return index page"""
    return render_template('index.html')


if __name__ == ('__main__'):
    app.run(debug=True)
