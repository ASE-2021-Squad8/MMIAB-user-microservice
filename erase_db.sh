#!/bin/bash

rm db.sqlite
rm -rf migrations/
export FLASK_ENV=development
flask db init
flask db migrate
flask db upgrade