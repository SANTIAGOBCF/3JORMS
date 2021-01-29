#!/bin/bash

export FLASK_APP=dc19.py
export DC19_ADMIN=admin@dc19.org
export FLASK_DEBUG=1
export MAIL_USERNAME=app.supp.20@gmail.com
export MAIL_PASSWORD=appsup20
pip3 install -r requeriments/r.txt && flask run

firefox http://127.0.0.1:5000/