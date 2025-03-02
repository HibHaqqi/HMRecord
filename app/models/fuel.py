from app import db
from app.models.user import User

class Fuel(db.Model):
    __tablename__ = 'fuel'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    unit_ft = db.Column(db.String(100), nullable=False)
    unit_code = db.Column(db.String(100), nullable=False)
    contractor = db.Column(db.String(100), nullable=False)
    fuel_issued = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)