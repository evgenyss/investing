from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user

from webapp.assets.forms import AssetSelection, UpdateRates, AssetDelete
from webapp.assets.models import Asset, Portfolio, Currency
from webapp.db import db

from webapp.get_data import get_last_prices_formatted, get_last_prices

blueprint = Blueprint('assets', __name__)


@blueprint.route("/")
def index():
    display_list = []
    title = "Portfolio"
    asset_form = AssetSelection()
    update_rates_form = UpdateRates()

    # Get currency exchange rates from database
    currencies_list = ['usd', 'eur', 'gbp']
    curr_price_list = []
    for curr in currencies_list:
        curr_price = Currency.query.filter(Currency.isoCurrencyName == curr).with_entities(Currency.price).first()[0]
        curr_price_list.append((curr, '{:.2f}'.format(curr_price)))

    # Create options for dropdown form
    responce_data = Asset.query.with_entities(Asset.ticker, Asset.name, Asset.type).order_by(Asset.name).all()
    output = [" : ".join(output[:3]) for output in responce_data]

    # Create data for Portfolio table
    if current_user.is_authenticated:
        jointed_data = db.session.query(Asset, Portfolio).join(
            Portfolio, Asset.id == Portfolio.asset_id
            ).filter(Portfolio.user_id == current_user.id)
        for asset, portfolio in jointed_data:
            delete_form = AssetDelete()
            display_list.append([asset.type, asset.ticker, asset.name, asset.sector,
                                portfolio.number, portfolio.price, asset.currency, portfolio.asset_id, delete_form])

    return render_template("assets/index.html", page_title=title,
                           asset_list=output, portfolio_list=display_list,
                           form=asset_form, update_rates_form=update_rates_form, currencies_list=curr_price_list)


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
            flash(f'Success data updating for {ticker}', 'alert-warning')
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
    currency_list = ['usd', 'eur', 'gbp']

    if update_rates_form.validate_on_submit():

        # Get currency exchange rates
        currency_figi = {}
        for currency_name in currency_list:
            currency_figi[currency_name] = Currency.query.filter(
                Currency.isoCurrencyName == currency_name).with_entities(Currency.figi).first()[0]
        currency_figi_list = list(currency_figi.values())
        currency_figi_price_dictionary = get_last_prices_formatted(currency_figi_list)

        # Update currencies rates in database
        for figi, price in currency_figi_price_dictionary.items():
            curr_price = Currency.query.filter(Currency.figi == figi)
            curr_price.first().price = price
        db.session.commit()
        # flash("Currency Rates Updated", 'alert-success')

        # Join tables for update assets rates
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

        # Get last prices for figi list
        figi_price_dictionary = get_last_prices_formatted(figi_list)

        # Insert data in database
        for asset, portfolio in jointed_data:
            try:
                portfolio.price = figi_price_dictionary[asset.figi]
            except KeyError:
                flash(f"No data for {asset.ticker}", 'alert-warning')
        db.session.commit()
        flash("Rates Updated", 'alert-success')

    return redirect(url_for('assets.index'))


@blueprint.route('/delete/<int:asset_id>', methods=['POST'])
def asset_delete(asset_id):
    asset_delete_form = AssetDelete()
    if asset_delete_form.validate_on_submit():
        delete_data = Portfolio.query.filter(Portfolio.asset_id == asset_id).filter(
            Portfolio.user_id == current_user.id)
        if delete_data.count():
            delete_data.delete()
            db.session.commit()
            flash(f"Asset id {asset_id} has been deleted", 'alert-success')
    return redirect(url_for('assets.index'))
