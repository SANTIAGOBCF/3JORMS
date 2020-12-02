from flask import Blueprint

uploads = Blueprint('uploads', __name__,
                        template_folder='templates')

from . import views