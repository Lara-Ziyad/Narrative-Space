from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from backend.extensions import db

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                          default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password: str):
        """Hash the plain-text password and store it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Return True if password matches the stored hash."""
        return check_password_hash(self.password_hash, password)


# Conversation table to store AI interactions
class Conversation(db.Model):
    __tablename__ = 'conversation'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    style = db.Column(db.String(50))
    model_used = db.Column(db.String(50))
    prompt = db.Column(db.Text, nullable=False)
    augmented_prompt = db.Column(db.Text)
    output_text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    user = relationship("User", backref="conversations")
