from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, InputRequired
from webapp.assets.models import Asset


class AssetSelection(FlaskForm):
    asset = StringField('Select Share / Bond / ETF', validators=[DataRequired()],
                        render_kw={"class": "form-control", "placeholder": "Select Share / Bond / ETF..."})
    number = IntegerField('Number', validators=[InputRequired()],
                          render_kw={"class": "form-control", "placeholder": "Number..."})
    submit = SubmitField('Add', render_kw={"class": "btn btn-primary btn-block"})

    def validate_number(self, number):
        if number.data < 0:
            raise ValidationError('Number must be greater than 0')

    def validate_asset(self, asset):
        try:
            ticker = asset.data.split(" : ")[0]
            asset_count = Asset.query.filter(Asset.ticker == ticker).count()
            if not asset_count:
                raise ValidationError('Select asset from dropdown list')
        except (ValueError, KeyError):
            raise ValidationError('Please select asset from dropdown list')


class UpdateRates(FlaskForm):
    submit = SubmitField('Update Rates', render_kw={"class": "btn btn-primary btn-lg"})
