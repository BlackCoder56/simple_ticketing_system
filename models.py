from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(50))
    price = db.Column(db.Integer, nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship 
    tickets = db.relationship("Ticket", backref="event", lazy=True)


class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    qr_id = db.Column(db.String(100), unique=True, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    qr_path = db.Column(db.String(200))
    status = db.Column(db.String(10), default="valid")
    purchase_time = db.Column(db.DateTime, default=datetime.utcnow)