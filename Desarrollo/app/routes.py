from app import app
from flask import render_template, redirect, request, url_for, session, flash
from app.models import User

@app.route('/')
def index():
    user = User(username = 'Hola', email = 'chau')
    return '''<html>
    <head>
        <title>My web</title>
    </head>
    <body>
        <h1>Hello, ''' + user.username + '''!</h1>
    </body>
    </html>'''

@app.route('/testeo')
def testeo():
    return render_template('testeo.html')