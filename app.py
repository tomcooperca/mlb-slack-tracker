import mlbgame
from baseball.team import TeamMapper
from slack.token import Token
from slack.user import User
from flask import Flask, redirect, url_for, session, request, render_template
from flask_sqlalchemy import SQLAlchemy
import json
import os
from datetime import datetime

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']

# Database setup
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from models import UserModel
db.create_all()
db.session.commit()

# mlb data
divisions = None
teams = []
team_form_choices = []

# json
json_sorted = False
json_indent = 4
json_sorted_env = os.getenv('JSON_SORTED')
json_indent_env = os.getenv('JSON_INDENT')
if json_sorted_env:
    json_sorted = bool(os.getenv('JSON_SORTED') == 'true')
if json_indent_env:
    json_indent = int(os.getenv('JSON_INDENT'))


@app.route("/")
def add_to_slack():
    return app.send_static_file("slack_button.html")


@app.route("/authorize")
def authorize():
    try:
        t = Token(request.args.get('code'),
            request.args.get('redirect_uri'),
            os.environ['SLACK_CLIENT_ID'],
            os.environ['SLACK_CLIENT_SECRET'])
    except KeyError:
        session['error'] = 'Missing required params during authorization!'
        return redirect(url_for('failed'))

    try:
        response = t.generate_token()
        if not response:
            return redirect(url_for('unavailable'))

        um = UserModel.query.filter_by(user_id=response['user_id']).first()
        if not um:
            db.session.add(UserModel(user_id=response['user_id'], token=response['access_token']))
        else:
            um.token = response['access_token']
        db.session.commit()
        session['current_user'] = response['user_id']
        return redirect(url_for('setup'))
    except KeyError:
        if 'error' in response:
            session['error'] = response['error']


@app.route("/config", methods=['GET', 'POST'])
def setup():
    from form import SetupForm
    setup = SetupForm()
    setup.team.choices = team_form_choices
    if 'current_user' in session:
        setup.user_id.data = session['current_user']

    if setup.validate_on_submit():
        u = UserModel.query.filter_by(user_id=setup.user_id.data).first()
        u.team = setup.team.data
        db.session.commit()
        if setup.update_now.data:
            slackuser = User(token=u.token, id=u.user_id, team=find_by_abbreviation(setup.team.data))
            slackuser.todays_game_score_and_standings()
        return redirect(url_for('current_user', id=u.user_id))
    return render_template('setup.html', title='Setup MLB team', form=setup)


@app.route("/user/<id>")
def current_user(id):
    um = UserModel.query.filter_by(user_id=id).first()
    slackuser = User(id=um.user_id, token=um.token, team=find_by_abbreviation(um.team))
    return render_template('user.html', user=slackuser, status=slackuser.status(), emoji=slackuser.emoji())


@app.route("/failure")
def failed():
    if 'error' in session:
        return "Authorization failed! Error: {}".format(session['error'])
    return "Authorization failed due to unknown error!"


@app.route("/unavailable")
def unavailable():
    return "Service unavailable (is Slack down?)"


@app.before_first_request
def first_things_first():
    populate_data()
    for team in teams:
        team_form_choices.append((team.abbreviation, team.full_name))

@app.route("/team/abbreviations")
def list_team_abbreviations():
    return app.response_class(json.dumps(list_team_abbreviations(),
            sort_keys=json_sorted, indent=json_indent), mimetype='application/json')


@app.route("/team/all")
def list_teams():
    return app.response_class(json.dumps(teams, default=serialize_team, sort_keys=json_sorted, indent=json_indent),
            mimetype='application/json')


@app.route("/division/all")
def list_divisons():
    return app.response_class(json.dumps(divisions, default=serialize_division,
            sort_keys=json_sorted, indent=json_indent), mimetype='application/json')


def list_team_abbreviations():
    abbreviations = []
    for team in teams:
        abbreviations.append(team.abbreviation)
    return abbreviations


def find_by_abbreviation(abbreviation):
    for team in teams:
        if team.abbreviation == abbreviation:
            return team
    return None


def serialize_division(division):
    return division.name


def serialize_team(team):
    return team.__dict__


def populate_data():
    divisions = mlbgame.standings().divisions
    todays_games = mlbgame.day(datetime.now().year, datetime.now().month, datetime.now().day)
    for division in divisions:
        for team in division.teams:
            t = TeamMapper(divisions, todays_games, abbreviation=team.team_abbrev)
            t.find_team()
            teams.append(t.team)
    return teams


if __name__ == "__main__":
    app.run()
