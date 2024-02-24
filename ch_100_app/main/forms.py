from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    DateField,
    SelectField,
    SubmitField,
    FloatField,
)

# from wtforms.fields.html5 import URLField
# from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, NumberRange
from ch_100_app.models import User
