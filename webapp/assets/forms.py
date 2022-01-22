from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired


class AssetSelection(FlaskForm):
    asset = StringField('Select Share / Bond / ETF', validators=[DataRequired()],
                        render_kw={"class": "form-control", "placeholder": "Select Share / Bond / ETF..."})
    number = IntegerField('Number', validators=[DataRequired()],
                          render_kw={"class": "form-control", "placeholder": "Number..."})
    submit = SubmitField('Add', render_kw={"class": "btn btn-primary btn-block"})

    def validate_number(self, number):
        if number.data <= 0:
            raise ValidationError('Number must be greater than 0')
