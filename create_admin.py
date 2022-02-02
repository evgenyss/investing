from getpass import getpass
import sys

from webapp import create_app
from webapp.db import db
from webapp.user.models import User

app = create_app()

with app.app_context():
    username = input('Please input username: ')

    if User.query.filter(User.username == username).count():
        print('Username is exists')
        sys.exit(0)

    password = getpass('Please enter password: ')
    password2 = getpass('Please enter the password again: ')
    if not password == password2:
        print("Password mismatch")
        sys.exit(0)

    new_user = User(username=username, role='admin')
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    print('Admin user "{}" added, id = {}'.format(new_user.username, new_user.id))


