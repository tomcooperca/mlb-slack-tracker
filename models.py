from app import db

class UserModel(db.Model):
    __tablename__ = 'configured_users'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), unique=True, nullable=False)
    token = db.Column(db.String(10240), nullable=False)
    team = db.Column(db.String(50))

    def __repr__(self):
        if self.team:
            return '<User {}, team {}>'.format(self.user_id, self.team)
        return '<User {}}>'.format(self.user_id)
