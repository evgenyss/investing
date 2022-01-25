from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user

from webapp.assets.forms import AssetSelection, UpdateRates
from webapp.assets.models import Asset, Portfolio
from webapp.db import db

from webapp.get_data import get_last_prices, format_price

blueprint = Blueprint('assets', __name__)


@blueprint.route("/")
def index():
    display_list = []
    title = "Portfolio"
    asset_form = AssetSelection()
    update_rates_form = UpdateRates()
    responce_data = Asset.query.with_entities(Asset.ticker, Asset.name, Asset.type).order_by(Asset.name).all()
    output = [" : ".join(output[:3]) for output in responce_data]
    if current_user.is_authenticated:
        jointed_data = db.session.query(Asset, Portfolio).join(
            Portfolio, Asset.id == Portfolio.asset_id
            ).filter(Portfolio.user_id == current_user.id)
        for asset, portfolio in jointed_data:
            display_list.append([asset.type, asset.ticker, asset.name, asset.sector,
                                portfolio.number, portfolio.price, asset.currency])
    # print(display_list)
    return render_template("assets/index.html", page_title=title,
                           asset_list=output, portfolio_list=display_list,
                           form=asset_form, update_rates_form=update_rates_form)


@blueprint.route('/asset-select', methods=['POST'])
def asset_selection():
    form = AssetSelection()
    if form.validate_on_submit():
        # for ticker and assetid - validation in form.py
        ticker = form.asset.data.split(" : ")[0]
        assetid = Asset.query.filter(Asset.ticker == ticker).with_entities(Asset.id).first()[0]

        # Update row, if ticker exist for user, else insert data in database
        ticker_for_user = Portfolio.query.filter(
            Portfolio.asset_id == assetid).filter(Portfolio.user_id == current_user.id)
        if ticker_for_user.count():
            ticker_for_user.first().number = int(form.number.data)
            db.session.commit()
            flash(f'Success data updating for {ticker}', 'alert-success')
        else:
            new_portfolio_data = Portfolio(asset_id=assetid,
                                           user_id=current_user.id,
                                           number=int(form.number.data),
                                           price=0)
            db.session.add(new_portfolio_data)
            db.session.commit()
            flash(f'Success data insertion for {ticker}', 'alert-success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Error in "{}": - {}'.format(getattr(form, field).label.text, error), 'alert-danger')
    return redirect(url_for('assets.index'))


@blueprint.route('/update-rates', methods=['POST'])
def update_rates():
    update_rates_form = UpdateRates()
    if update_rates_form.validate_on_submit():

        jointed_data = db.session.query(Asset, Portfolio).join(
            Portfolio, Asset.id == Portfolio.asset_id
            ).filter(Portfolio.user_id == current_user.id)

        # Get figi list
        figi_list = []
        for asset, portfolio in jointed_data:
            figi_list.append(asset.figi)

        if not figi_list:
            flash("No Data in Portfolio", 'alert-warning')
            return redirect(url_for('assets.index'))

        # Get Last Prices for figi list
        figi_price_dictionary = {}
        for last_price_dict in get_last_prices(figi_list)['lastPrices']:
            last_price = format_price(last_price_dict['price'])
            figi_key = last_price_dict['figi']
            figi_price_dictionary[figi_key] = last_price

        # Insert data in database
        for asset, portfolio in jointed_data:
            portfolio.price = figi_price_dictionary[asset.figi]
        db.session.commit()
        flash("Rates Updated", 'alert-success')

    return redirect(url_for('assets.index'))
