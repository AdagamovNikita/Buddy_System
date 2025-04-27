from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class CompleteProfileForm(FlaskForm):
    student_id = StringField("Student ID", validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired()])
    gender = SelectField("Gender", choices=[("male", "Male"), ("female", "Female"), ("other", "Other")])
    nationality = StringField("Nationality", validators=[DataRequired()])
    major = StringField("Major", validators=[DataRequired()])
    academic_year = StringField("Academic Year", validators=[DataRequired()])
    languages = StringField("Languages", validators=[DataRequired()])
    bio = TextAreaField("Short Bio", validators=[DataRequired()])
    phone = StringField("Phone Number", validators=[DataRequired()])
    submit = SubmitField("Save Profile")
