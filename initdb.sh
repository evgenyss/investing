#!/bin/sh
export FLASK_APP=webapp
flask db init
flask db migrate -m "Create DB"
flask db upgrade
