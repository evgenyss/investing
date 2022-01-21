from flask import Blueprint, render_template
from webapp.assets.models import Asset

blueprint = Blueprint('assets', __name__)


@blueprint.route("/")
def index():
    title = "Portfolio"
    responce_data = Asset.query.filter_by(type="Etf").\
        with_entities(Asset.figi, Asset.name).order_by(Asset.name).limit(10).all()
    output = [" : ".join(output[:2]) for output in responce_data]
    return render_template("assets/index.html", page_title=title, asset_list=output)
