import mlbgame
from baseball.team import TeamFinder
from slack.token import Token
from slack.user import User
from flask import Flask, redirect, url_for, session, request
from celery import Celery
import sqlite3
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import json
import os

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = '7ce9431ef410e9fb730e140f290abd0b69e2568515b27644'
if os.getenv('DATABASE_CONNECT'):
    conn = sqlite3.connect(os.getenv('DATABASE_CONNECT'))
else:
    conn = sqlite3.connect('test.db')

# mlb data
divisions = mlbgame.standings().divisions
teams = []

# json
json_sorted = False
json_indent = 4
json_sorted_env = os.getenv('JSON_SORTED')
json_indent_env = os.getenv('JSON_INDENT')
if json_sorted_env:
    json_sorted = bool(os.getenv('JSON_SORTED') == 'true')
if json_indent_env:
    json_indent = int(os.getenv('JSON_INDENT'))

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
    write_user_to_db
    return "Current user: {}<br/>Status: {}<br/>Emoji: {}".format(user.id, user.status(), user.emoji())


@app.route("/failure")
def failed():
    if 'error' in session:
        return "Authorization failed! Error: {}".format(sesion['error'])
    return "Authorization failed due to unknown error!"

@app.route("/unavailable")
def unavailable():
    return "Service unavailable (is Slack down?)"

@app.route("/team/abbreviations")
def list_team_abbreviations():
    if len(teams) == 0:
        populate_teams(divisions)
    return app.response_class(json.dumps(list_team_abbreviations(),
            sort_keys=json_sorted, indent=json_indent), mimetype='application/json')

@app.route("/team/all")
def list_teams():
    if len(teams) == 0:
        populate_teams(divisions)
    return app.response_class(json.dumps(teams, default=serialize_team, sort_keys=json_sorted, indent=json_indent),
            mimetype='application/json')

@app.route("/division/all")
def list_divisons():
    return app.response_class(json.dumps(divisions, default=serialize_division,
            sort_keys=json_sorted, indent=json_indent), mimetype='application/json')

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



def list_team_abbreviations():
    abbreviations = []
    for team in teams:
        abbreviations.append(team.abbreviation)
    return abbreviations


def serialize_division(division):
    type(division)
    return division.name
    # division_names_list = []
    # for div in divisions:
        # division_names_list.append(div.name)
    # return division_names_list


def serialize_team(team):
    return team.__dict__


def create_req_table():
    conn.execute('''CREATE TABLE user_db
                    (id integer PRIMARY KEY AUTOINCREMENT, user_id varchar(128) NOT NULL,
                    email varchar(128) NOT NULL, token varchar(1024) NOT NULL, team varchar(50))
                    IF NOT EXISTS;
    ''')
    conn.commit()

def write_user_to_db(user):
    conn.execute("INSERT INTO user_db VALUES ({}, {}, {})".format(user.id, user.display_email(), user.token))
    conn.commit()

def populate_teams(divisions):
    for division in divisions:
        for team in division.teams:
            t = TeamFinder(divisions, abbreviation=team.team_abbrev)
            t.find_team()
            teams.append(t.team)
    return teams


if __name__ == "__main__":
    populate_teams(divisions)
    create_req_table()
    app.run()
