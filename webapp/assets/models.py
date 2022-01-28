from webapp.db import db


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    figi = db.Column(db.String, unique=True, nullable=False)
    ticker = db.Column(db.String, unique=True, nullable=False)
    isin = db.Column(db.String, unique=True, nullable=False)
    currency = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    sector = db.Column(db.String, nullable=False)
    country_of_risk = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<{} : {} {}>'.format(self.type, self.figi, self.name)


class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    figi = db.Column(db.String, unique=True, nullable=False)
    ticker = db.Column(db.String, unique=True, nullable=False)
    currency = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    isoCurrencyName = db.Column(db.String, unique=True, nullable=False)
    price = db.Column(db.Float, default=0)

    def __repr__(self):
        return '<Currency : {} {}>'.format(self.figi, self.name)


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float)

    def __repr__(self):
        return '<Portfolio instance {} {}>'.format(self.asset_id, self.price)
