import app
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, BooleanField
from wtforms.validators import Required

class SetupForm(FlaskForm):
    user_id = StringField('User ID')
    team = SelectField('Team', choices=app.list_team_abbreviations(), validators = [Required()])
    update_now = BooleanField('Update Status now')
    submit = SubmitField('Sign In')
