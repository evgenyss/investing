from flask import Blueprint, render_template
from webapp.user.decorators import admin_required
from webapp.user.models import User

blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route('/')
@admin_required
def admin_index():
    title = "Admin Console"
    user_data = User.query.with_entities(User.username, User.role).order_by(User.username).all()
    output = [" : ".join(output[:2]) for output in user_data]
    return render_template('admin/index.html', page_title=title, user_list=output)
