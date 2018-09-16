import mlbgame
from baseball.team import TeamFinder
from slack.token import Token
from slack.user import User
from flask import Flask, redirect, url_for, session, request, render_template
from flask_sqlalchemy import SQLAlchemy
import json
import os

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']

# Database setup
if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

from models import UserModel
db.create_all()
db.session.commit()

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
    except KeyError:
        session['error'] = 'Missing required params during authorization!'
        return redirect(url_for('failed'))

    try:
        response = t.generate_token()
        if not response:
            return redirect(url_for('unavailable'))
        print(response)
        db.session.add(UserModel(user_id=response['user_id'], token=response['access_token']))
        db.session.commit()
        session['current_user'] = response['user_id']
        return redirect(url_for('setup'))
    except KeyError:
        if 'error' in response:
            session['error'] = response['error']


@app.route("/setup", methods=['GET', 'POST'])
def setup():
    from form import SetupForm
    setup = SetupForm()
    setup.team.choices = list_team_abbreviations()
    if 'current_user' in session:
        setup.user_id.data = session['current_user']

    if setup.validate_on_submit() and 'current_user' in session:
        u = UserModel.query.filter_by(user_id=session['current_user'])
        u.team = setup.team.data
        db.session.commit()
        return redirect(url_for('current_user'))
    return render_template('setup.html', title='Setup MLB team', form=setup)
    # return "Current user: {}<br/>Status: {}<br/>Emoji: {}".format(user.id, user.status(), user.emoji())


@app.route("/user/<id>")
def current_user(id):
    um = UserModel.query.filter_by(user_id=id)
    return um


@app.route("/failure")
def failed():
    if 'error' in session:
        return "Authorization failed! Error: {}".format(session['error'])
    return "Authorization failed due to unknown error!"


@app.route("/unavailable")
def unavailable():
    return "Service unavailable (is Slack down?)"
    create_req_table()


@app.route("/team/abbreviations")
def list_team_abbreviations():
    # if len(teams) == 0:
    #     populate_teams(divisions)
    return app.response_class(json.dumps(list_team_abbreviations(),
            sort_keys=json_sorted, indent=json_indent), mimetype='application/json')


@app.route("/team/all")
def list_teams():
    # if len(teams) == 0:
    #     populate_teams(divisions)
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


def serialize_division(division):
    type(division)
    return division.name
    # division_names_list = []
    # for div in divisions:
        # division_names_list.append(div.name)
    # return division_names_list


def serialize_team(team):
    return team.__dict__


def populate_teams(divisions):
    for division in divisions:
        for team in division.teams:
            t = TeamFinder(divisions, abbreviation=team.team_abbrev)
            t.find_team()
            teams.append(t.team)
    return teams


if __name__ == "__main__":
    populate_teams(divisions)
    app.run()
