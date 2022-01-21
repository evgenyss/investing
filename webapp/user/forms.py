from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from webapp.user.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"class": "form-control"})
    remember_me = BooleanField('Remember me', default=True, render_kw={"class": "form-check-input"})
    submit = SubmitField('Sign in', render_kw={"class": "btn btn-primary"})


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"class": "form-control"})
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')],
                              render_kw={"class": "form-control"})
    submit = SubmitField('Register', render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        users_count = User.query.filter_by(username=username.data).count()
        if users_count > 0:
            raise ValidationError('User is exist in database')
