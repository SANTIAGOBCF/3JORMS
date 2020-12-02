from . import uploads
from flask import render_template, abort, request
from jinja2 import TemplateNotFound
from werkzeug.utils import secure_filename
import os
from app import app

# @uploads.route('/', defaults={'page': 'index'})
# @uploads.route('/<page>')
# def show(page):
@uploads.route('/', methods = ['POST','GET'])
def upload_files():
    try:
        if(request.method == "POST"):
            uploaded_file = request.files['file']
            filename = secure_filename(uploaded_file.filename)
            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                    abort(400)
                uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        return render_template('index.html')
    #     return '''<html>
    # <head>
    #     <title>My web</title>
    # </head>
    # <body>
    #     <h1>Hello, Whatever you are!</h1>
    # </body>
    # </html>'''
    except TemplateNotFound:
        abort(404)