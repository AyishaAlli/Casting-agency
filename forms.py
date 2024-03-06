from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, DateField


class ActorForm(FlaskForm):
    name = StringField("name")
    age = StringField("age")
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])

class MovieForm(FlaskForm):
    title = StringField("title")
    release_date = StringField("release_date")


