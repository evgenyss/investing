from flask import Blueprint, render_template, flash, redirect, url_for
from webapp.assets.models import Asset
from webapp.assets.forms import AssetSelection

# from webapp.user.models import User
# from webapp.db import db


blueprint = Blueprint('assets', __name__)


@blueprint.route("/")
def index():
    title = "Portfolio"
    asset_form = AssetSelection()
    responce_data = Asset.query.filter_by(type="Etf").\
        with_entities(Asset.figi, Asset.name).order_by(Asset.name).limit(50).all()
    output = [" : ".join(output[:2]) for output in responce_data]
    return render_template("assets/index.html", page_title=title, asset_list=output, form=asset_form)


@blueprint.route('/asset-select', methods=['POST'])
def asset_selection():
    form = AssetSelection()
    if form.validate_on_submit():
        # print(form.asset.data)
        flash(f'{form.asset.data} : {form.number.data }')
        return redirect(url_for('assets.index'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Error in "{}": - {}'.format(getattr(form, field).label.text, error))
    return redirect(url_for('assets.index'))
