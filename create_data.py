from webapp import create_app
from webapp.get_data import parse_asset, save_asset, parse_currency, save_data_row
from webapp.assets.models import Currency

app = create_app()
with app.app_context():
    save_asset(parse_asset("Etfs"))
    save_asset(parse_asset("Bonds"))
    save_asset(parse_asset("Shares"))
    for data in parse_currency():
        save_data_row(Currency, data)
