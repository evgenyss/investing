import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

API_TOKEN = ""

API_DATA_URL = "https://invest-public-api.tinkoff.ru/rest/tinkoff.public.invest.api.contract.v1.InstrumentsService/"
API_LASTPRICES_URL = "https://invest-public-api.tinkoff.ru/rest/\
tinkoff.public.invest.api.contract.v1.MarketDataService/GetLastPrices"

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')

SECRET_KEY = ""

SQLALCHEMY_TRACK_MODIFICATIONS = False

REMEMBER_COOKIE_DURATION = timedelta(days=1)
