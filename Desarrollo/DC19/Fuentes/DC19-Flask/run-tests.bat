@echo off
title RUN TESTS
set FLASK_APP=dc19.py
set DC19_ADMIN=admin@dc19.org
set FLASK_DEBUG=1
set MAIL_USERNAME=app.supp.20@gmail.com
set MAIL_PASSWORD=jylxdygtzzeqjsyz
pip install -r requeriments/r.txt && start "TESTING SERVER" /MIN python testing-app.py
cls
echo +------------------------------------+
echo ^|              TESTING               ^|
echo ^|          @DifusionCOVID19          ^|
echo +------------------------------------+
color 0a
timeout 3 > NUL
flask test
pause