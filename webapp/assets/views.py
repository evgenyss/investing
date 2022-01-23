from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user
from webapp.assets.models import Asset
from webapp.assets.forms import AssetSelection

from webapp.assets.models import Portfolio
from webapp.db import db

blueprint = Blueprint('assets', __name__)


@blueprint.route("/")
def index():
    title = "Portfolio"
    asset_form = AssetSelection()
    responce_data = Asset.query.with_entities(Asset.ticker, Asset.name, Asset.type).order_by(Asset.name).all()
    output = [" : ".join(output[:3]) for output in responce_data]
    return render_template("assets/index.html", page_title=title, asset_list=output, form=asset_form)


@blueprint.route('/asset-select', methods=['POST'])
def asset_selection():
    form = AssetSelection()
    if form.validate_on_submit():
        # for ticker and assetid - validation in form.py
        ticker = form.asset.data.split(" : ")[0]
        assetid = Asset.query.filter(Asset.ticker == ticker).with_entities(Asset.id).first()[0]
        # flash(f'{form.asset.data} : {form.number.data } : {current_user.id} : {assetid}', 'alert-success')
        new_portfolio_data = Portfolio(asset_id=assetid,
                                       user_id=current_user.id,
                                       number=int(form.number.data),
                                       price=0)
        db.session.add(new_portfolio_data)
        db.session.commit()
        flash(f'Success data insertion in database for {ticker}', 'alert-success')
        return redirect(url_for('assets.index'))

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Error in "{}": - {}'.format(getattr(form, field).label.text, error), 'alert-danger')
    return redirect(url_for('assets.index'))
