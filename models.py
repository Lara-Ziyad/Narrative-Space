from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship

# Initialize the SQLAlchemy object (linked later in app.py)
db = SQLAlchemy()


# Conversation table to store AI interactions
class Conversation(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    input_text = db.Column(db.Text, nullable=False)
    output_text = db.Column(db.Text)
    model_used = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = relationship("User", backref="conversations")
