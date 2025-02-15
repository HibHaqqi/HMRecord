from app import db
from datetime import datetime
from app.models.user import User

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    unit_code = db.Column(db.String(50), nullable=False)
    contractor = db.Column(db.String(100), nullable=False)
    hm_start = db.Column(db.Float, nullable=False)
    hm_stop = db.Column(db.Float, nullable=False)
    hm = db.Column(db.Float, nullable=False)
    opex_capex = db.Column(db.String(50), nullable=False)
    cost_category = db.Column(db.String(100), nullable=False)
    cost_activity = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Automatically set on creation
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Automatically set on update

    def __repr__(self):
        return f'<Equipment {self.unit_code} - {self.date}>'