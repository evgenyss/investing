import requests
from flask import current_app
from datetime import datetime
from webapp.db import db
from webapp.assets.models import Asset
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


def get_data_by_asset(type_of_asset):
    """
    Get data list in json for asset type
    """
    url = f"{current_app.config['API_DATA_URL']}{type_of_asset}"

    headers = {}
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer { current_app.config['API_TOKEN'] }"
    headers["Content-Type"] = "application/json"

    data = '{"instrumentStatus": "INSTRUMENT_STATUS_UNSPECIFIED"}'
    try:
        result = requests.post(url, headers=headers, data=data)
        result.raise_for_status()
        print(f"--------- {type_of_asset} --------")
        return result.json()
    except(requests.RequestException, ValueError) as err:
        print(f'Network Error : {err}')
        if result.status_code == 401:
            print("Please check TOKEN")
        return False


def get_last_prices(figi_list):
    """
    Get last prices in json for list of figi
    """
    url = current_app.config['API_LASTPRICES_URL']

    headers = {}
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer { current_app.config['API_TOKEN'] }"
    headers["Content-Type"] = "application/json"

    data = f'{{"figi": {figi_list}}}'
    try:
        result = requests.post(url, headers=headers, data=data)
        result.raise_for_status()
        return result.json()['lastPrices']
    except(requests.RequestException, ValueError, KeyError) as err:
        print(f'Network Error : {err}')
        if result.status_code == 401:
            print("Please check TOKEN")
        return {}


def format_nominal(nominal_dict):
    """
    format dictionary like:
    {'units': '98', 'nano': 475000000} -> to float 98,4750
    {'currency': 'rub', 'units': '267', 'nano': 400000000} -> to float 267,4000
    {'currency': 'rub', 'units': '1000'} -> to float 1000,0000
    {'currency': 'usd', 'nano': 195000000} -> to float 0,1950
    """
    if 'units' in nominal_dict and 'nano' in nominal_dict:
        nominal = int(nominal_dict['units']) + float(nominal_dict['nano']/1000000000)
    elif 'nano' in nominal_dict and 'units' not in nominal_dict:
        nominal = float(nominal_dict['nano']/1000000000)
    else:
        nominal = int(nominal_dict['units'])
    return float('{:.4f}'.format(nominal))


def get_last_prices_formatted(figi_list):
    """ Get Last Prices Formatted """
    figi_price_dictionary = {}
    if get_last_prices:
        for last_price_dict in get_last_prices(figi_list):
            if 'price' in last_price_dict:
                last_price = format_nominal(last_price_dict['price'])
                figi_key = last_price_dict['figi']
                figi_price_dictionary[figi_key] = last_price
            else:
                print(f"No data for {last_price_dict['figi']}")
        return figi_price_dictionary
    else:
        return figi_price_dictionary


def format_datetime(datetime_string):
    """
    format time from string like "2022-01-14T19:48:51.981204035Z" to datetime
    """
    try:
        datetime_string = datetime.strptime(datetime_string.split(".")[0], '%Y-%m-%dT%H:%M:%S')
        print("Error")
    except ValueError:
        datetime_string = datetime.now()
    return datetime_string


def save_asset(asset_data):
    """
    Save All Asset (Etf, Bond or Share) instances to database
    Using bulk insertion, if no rows in table for asset
    Else adding data one by one
    """
    if asset_data:
        rows_exists = Asset.query.filter(Asset.type == asset_data[0]["type"]).count()
        if not rows_exists:
            try:
                db.session.bulk_insert_mappings(Asset, asset_data)
            except (IntegrityError, SQLAlchemyError) as e:
                db.session.rollback()
                print(e)
            db.session.commit()
        else:
            for asset_dict in asset_data:
                save_data_row(Asset, asset_dict)
        return True
    else:
        return False


def save_data_row(modelName, rowDataDict):
    """ Save row to database """
    figi_exists = modelName.query.filter(modelName.figi == rowDataDict["figi"]).count()
    if not figi_exists:
        print(rowDataDict["figi"], rowDataDict["name"])
        row_object = modelName(**rowDataDict)
        try:
            db.session.add(row_object)
        except (IntegrityError, SQLAlchemyError) as e:
            db.session.rollback()
            print(e)
        db.session.commit()
    else:
        print(f'figi { rowDataDict["figi"] } exist in database')


def check_in_data(var, data):
    """ Check, if var in data dictionary or not """
    if var not in data:
        # print(f"Info : Key error for { var }")
        data[var] = ""
    return data[var]


def parse_asset(type_of_asset):
    """
    Parse asset for save_data_row and save_asset function
    Input - type of asset: Bonds, Shares or Etfs
    Output - dictionary of vars
    """
    result_list = []
    data_dict = get_data_by_asset(type_of_asset)
    if data_dict:
        if 'instruments' in data_dict:
            for data in data_dict['instruments']:
                result = {}
                result["type"] = type_of_asset[:-1]
                result["figi"] = check_in_data("figi", data)
                result["ticker"] = check_in_data("ticker", data)
                result["isin"] = check_in_data("isin", data)
                result["currency"] = check_in_data("currency", data)
                result["name"] = check_in_data("name", data)
                result["sector"] = check_in_data("sector", data)
                result["country_of_risk"] = check_in_data("countryOfRisk", data)

                if result["type"] == 'Bond':
                    if data["nominal"]:
                        result["nominal"] = format_nominal(data["nominal"])
                else:
                    result["nominal"] = 0

                result_list.append(result)
    return result_list


def parse_currency():
    """
    Parse currency for save_data_row function
    Output - dictionary of vars
    """
    result_list = []
    data_dict = get_data_by_asset("Currencies")
    if data_dict:
        if 'instruments' in data_dict:
            for data in data_dict['instruments']:
                result = {}
                result["figi"] = check_in_data("figi", data)
                result["ticker"] = check_in_data("ticker", data)
                result["currency"] = check_in_data("currency", data)
                result["name"] = check_in_data("name", data)
                result["isoCurrencyName"] = check_in_data("isoCurrencyName", data)
                result_list.append(result)
    return result_list


if __name__ == "__main__":
    # Test 1
    # print(formatted_price({'units': '98', 'nano': 475000000}))

    # Test 2
    # list_of_id = ["BBG00T22WKV5", "BBG004731489", "BBG000B9XRY4", "BBG006L8G4H1", "BBG006G2JVL2"]
    # print(get_last_prices(list_of_id))

    # Test 3 Format Datetime
    # print(format_datetime("2022-01-14T19:48:51.981204035Z"))
    pass
