@echo off
set FLASK_APP=dc19.py
set DC19_ADMIN=admin@dc19.org
set FLASK_DEBUG=1
set MAIL_USERNAME=app.supp.20@gmail.com
set MAIL_PASSWORD=appsup20
pip uninstall -y flask_bootstrap
pip install -r requeriments/r.txt && start "DC19-SERVER" flask run
timeout 3 > NUL
start firefox http://127.0.0.1:5000/