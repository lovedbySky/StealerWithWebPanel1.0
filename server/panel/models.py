from datetime import datetime

from . import db


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    info = db.Column(db.String, nullable = False)
    chrome = db.Column(db.Text)
    brave = db.Column(db.Text)
    chromium = db.Column(db.Text)
    opera = db.Column(db.Text)
    amigo = db.Column(db.Text)
    firefox = db.Column(db.Text)
    edge = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return '<Article %r>' % self.id
