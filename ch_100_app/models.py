"""Create database models to represent tables."""
from ch_100_app import db
from flask_login import UserMixin
from sqlalchemy_utils import URLType
from ch_100_app.utils import FormEnum


class ItemCategory(FormEnum):
    """Categories of grocery items."""

    pass
    # PRODUCE = "Produce"
    # DELI = "Deli"
    # BAKERY = "Bakery"
    # PANTRY = "Pantry"
    # FROZEN = "Frozen"
    # OTHER = "Other"


class User(UserMixin, db.Model):
    """User model."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
