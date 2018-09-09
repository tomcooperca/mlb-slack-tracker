import mlbgame
from baseball import Team
from slack.token import Token
from slack.user import User
from flask import Flask, redirect, url_for, session, request, send_from_directory
from celery import Celery
import sqlite3
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import os

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = '7ce9431ef410e9fb730e140f290abd0b69e2568515b27644'
if os.getenv('DATABASE_CONNECT'):
    conn = sqlite3.connect(os.getenv('DATABASE_CONNECT'))
else:
    conn = sqlite3.connect('test.db')
teams = []
# app.config.update(
#     CELERY_BROKER_URL='redis://localhost:6379',
#     CELERY_RESULT_BACKEND='redis://localhost:6379'
# )
# celery = make_celery(app)

@app.route("/")
def hello():
    return app.send_static_file("slack_button.html")


@app.route("/authorize")
def authorize():
    try:
        t = Token(request.args.get('code'),
            request.args.get('redirect_uri'),
            os.environ['SLACK_CLIENT_ID'],
            os.environ['SLACK_CLIENT_SECRET'])
        response = t.generate_token()
        if not response:
            return redirect(url_for('unavailable'))
        print(response)
        session['token'] = response['access_token']
        session['user_id'] = response['user_id']
        return redirect(url_for('successful'))
    except KeyError:
        if 'error' in raw_token:
            session['error'] = raw_token['error']
        return redirect(url_for('failed'))


@app.route("/success")
def successful():
    print("Token: {}".format(session['token']))
    user = User(token=session['token'], id=session['user_id'])
    return "Current user: {}\nStatus: {}\nEmoji: {}".format(user.id, user.status(), user.emoji())


@app.route("/failure")
def failed():
    if 'error' in session:
        return "Authorization failed! Error: {}".format(sesion['error'])
    return "Authorization failed due to unknown error!"

@app.route("/unavailable")
def unavailable():
    return "Service unavailable (is Slack down?)"


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def populate_teams(d):
    for k, v in d.items():
        if isinstance(v, dict):
            populate_teams(v)
        else:
            for team in v:
                teams.append(Team(v.name))


def populate_db():
    create_req_table()
    conn.commit()


def create_req_table():
    conn.execute('''CREATE TABLE user_db
                    (id PRIMARY KEY ASC, user_id varchar(128) NOT NULL,
                    token varchar(1024) NOT NULL, team varchar(50))
                    IF NOT EXISTS
    ''')

if __name__ == "__main__":
    # populate_db(populate_teams(mlbgame.divisions()))
    app.run()
